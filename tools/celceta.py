#!/usr/bin/env python3
"""Adaptador de Ys: Memories of Celceta (Steam) para el kit de traducción.

    python3 tools/celceta.py export      # juego → source.jsonl (formato común)
    python3 tools/celceta.py import      # translation/ → archivos del juego en build/
    python3 tools/celceta.py roundtrip   # exportar e importar sin cambios = mismos bytes
    python3 tools/celceta.py pseudo      # pseudolocalización en build/ (prueba en el juego)

Rutas (relativas a la raíz del proyecto):
    ../ys-memories-of-celceta-esp-local/celceta/   copia del juego (lang/, text/, system/)
    ../ys-memories-of-celceta-esp-local/build/     archivos del juego ya traducidos

Cubre los guiones (lang/en/script/*.bin, ys7scp.py) y las tablas de texto
(lang/en/text/*.tbb, tables.py). Los demás formatos se agregan aquí mismo.

Cuadros de diálogo: cada cuadro (TalkMes, hasta 3 renglones) se exporta como un
solo texto y al importar se reparte en renglones según el ancho de la fuente
(reflujo). [DECISIONS 2026-11-17]
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arb  # noqa: E402
import dbin  # noqa: E402
import records  # noqa: E402
import tables  # noqa: E402
import ys7scp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT.parent / "ys-memories-of-celceta-esp-local"
GAME = LOCAL / "celceta"
BUILD = LOCAL / "build"
SOURCE = LOCAL / "source.jsonl"
TRANSLATION = ROOT / "translation"

# Códigos de control del texto: #4C, #00407F, #2M, #0B... (ancho cero)
CODE = re.compile(r"#-?(?:\d+|%d)[A-Za-z]")
LEAD = re.compile(r"^(?:#-?(?:\d+|%d)[A-Za-z])+")

# ---------------------------------------------------------------- codificación

# Las letras españolas no existen en Shift-JIS: van a la fila 9 de JIS X 0208,
# que está vacía (lead 0x85), y la fuente lleva sus glifos en esas casillas.
SPANISH = "áéíóúüñÁÉÍÓÚÜÑ¿¡"
ES_MAP = {ch: bytes([0x85, 0x40 + i]) for i, ch in enumerate(SPANISH)}
ES_BASE = dict(zip(SPANISH, "aeiouunAEIOUUN?!"))  # para medir antes de tener la fuente


def encode(text):
    out = bytearray()
    for ch in text:
        if ch in ES_MAP:
            out += ES_MAP[ch]
        else:
            out += ch.encode("cp932")
    return bytes(out)


ES_UNMAP = {v: k for k, v in ES_MAP.items()}


def decode(data):
    if b"\x85" not in data:
        return data.decode("cp932")
    out, i = [], 0
    while i < len(data):
        b = data[i]
        if (0x81 <= b <= 0x9F or 0xE0 <= b <= 0xFC) and i + 1 < len(data):
            pair = data[i:i + 2]
            out.append(ES_UNMAP.get(pair) or pair.decode("cp932"))
            i += 2
        else:
            out.append(bytes([b]).decode("cp932"))
            i += 1
    return "".join(out)


# ---------------------------------------------------------------- fuente

class Font:
    """Avances de lang/en/system/font.itf (glifos indexados como Shift-JIS)."""

    def __init__(self, path):
        d = path.read_bytes()
        n = struct.unpack_from("<H", d, 2)[0]
        offs = struct.unpack_from(f"<{n}I", d, 16)
        self.adv = [d[o + 4] if o < len(d) else 0 for o in offs]
        self.empty = [b - a == 0 for a, b in zip(offs, list(offs[1:]) + [len(d)])]

    @staticmethod
    def index(b):
        if len(b) == 1:
            return b[0] - 0x20 if b[0] < 0x80 else 95 + b[0] - 0xA1
        s1, s2 = b
        row = (s1 - 0x81) * 2 + 1 if s1 < 0xA0 else (s1 - 0xC1) * 2 + 1
        if s2 >= 0x9F:
            row += 1
            col = s2 - 0x9E
        else:
            col = s2 - 0x3F - (1 if s2 >= 0x80 else 0)
        return 158 + (row - 1) * 94 + (col - 1)

    def char_width(self, ch):
        b = encode(ch)
        i = self.index(b)
        if ch in ES_MAP and self.empty[i]:
            i = self.index(ES_BASE[ch].encode("cp932"))
        return self.adv[i]

    def width(self, text):
        return sum(self.char_width(c) for c in CODE.sub("", text))


# Anchos máximos medidos en el inglés (unidades de la fuente), por tipo de cuadro.
WIDTH = {"cara": 960, "normal": 1100, "centrado": 1500, "mensaje": 1300}
LINES = {"talk": 3, "mensaje": 3}
KIND_NOTE = {"cara": "con retrato", "normal": "sin retrato", "centrado": "centrado (narración)"}


def box_kind(first_line):
    lead = "".join(CODE.findall(LEAD.match(first_line).group() if LEAD.match(first_line) else ""))
    letters = set(re.findall(r"[A-Za-z]", lead))
    if "F" in letters:
        return "cara"
    if "C" in letters:
        return "centrado"
    return "normal"


def reflow(font, text, maxw):
    """Reparte text en renglones de ancho ≤ maxw, cortando en espacios."""
    lines, cur = [], ""
    for word in text.split(" "):
        cand = word if not cur else cur + " " + word
        if not cur or font.width(cand) <= maxw:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def join_lines(lines):
    """Une renglones: con espacio, o sin él si el anterior termina en guion."""
    out = ""
    for ln in lines:
        if not ln:
            continue
        if not out:
            out = ln
        elif out.endswith("-") and not out.endswith("--"):
            out += ln
        else:
            out += " " + ln
    return out


# ---------------------------------------------------------------- guiones

TALK, SETNAME, MESSAGE, MESSAGE2, MENU, GETITEM = 0x8040, 0x803F, 0x8007, 0x8041, 0x8036, 0x80C9


def _s(ins, i):
    a = ins.args
    return a[i][1] if i < len(a) and a[i][0] == ys7scp.STR else None


def party_names():
    """{id interno: nombre visible} de los personajes del grupo (lang/en/text/pc.tbb).

    pc.tbb: rutas de modelos y, desde 0x89, un bloque FALCOM3 con registros de
    145 bytes (id[32], nombre[32], ...).
    """
    import falcom
    d = (GAME / "lang/en/text/pc.tbb").read_bytes()
    out, _ = falcom.decompress_falcom3(d[0x89:])
    names = {}
    for p in range(0, len(out) - 63, 145):
        cid = out[p:p + 32].split(b"\0", 1)[0].decode("ascii")
        name = out[p + 32:p + 64].split(b"\0", 1)[0].decode("cp932")
        if cid:
            names[cid] = name
    return names


_PARTY = None


def talk_speaker(ins):
    global _PARTY
    if _PARTY is None:
        _PARTY = party_names()
    cid = decode(_s(ins, 0) or b"")
    if not cid or cid == "UNDEF":
        return None
    return _PARTY.get(cid.upper(), cid)


def script_units(script):
    """Unidades traducibles: (id, texto, hablante, nota, aplicar) en orden del juego.

    aplicar(script, texto_es, font) escribe la traducción en el guion.
    El hablante es el nombre de SetName si hay uno activo; si no, el del grupo
    (pc.tbb) o el id interno de TalkMes.
    """
    for si, seg in enumerate(script.segments):
        sname = script.seg_name(si)
        speaker = None
        for ii, ins in enumerate(seg):
            uid = f"{sname}/{ii}"
            if ins.op == SETNAME and _s(ins, 0) is not None:
                speaker = decode(_s(ins, 0)) or None
                if speaker:
                    yield uid, speaker, None, "nombre del hablante", _apply_simple(si, ii, 0)
            elif ins.op == TALK:
                lines = [decode(_s(ins, i) or b"") for i in (1, 2, 3)]
                if not any(lines):
                    continue
                lead = LEAD.match(lines[0])
                lead = lead.group() if lead else ""
                text = join_lines([lines[0][len(lead):]] + lines[1:])
                kind = box_kind(lines[0])
                note = f"cuadro de diálogo {KIND_NOTE[kind]} ({LINES['talk']} renglones, ancho {WIDTH[kind]})"
                yield uid, text, speaker or talk_speaker(ins), note, _apply_talk(si, ii, lead, kind)
            elif ins.op == MESSAGE and _s(ins, 0):
                raw = decode(_s(ins, 0))
                lead = LEAD.match(raw)
                lead = lead.group() if lead else ""
                text = join_lines(raw[len(lead):].split("\\n"))
                note = f"mensaje del sistema ({LINES['mensaje']} renglones, ancho {WIDTH['mensaje']})"
                yield uid, text, None, note, _apply_message(si, ii, lead)
            elif ins.op == MESSAGE2:
                idx = [i for i in range(3, len(ins.args)) if _s(ins, i)]
                if not idx:
                    continue
                lines = [decode(_s(ins, i)) for i in range(3, len(ins.args)) if _s(ins, i) is not None]
                lead = LEAD.match(lines[0])
                lead = lead.group() if lead else ""
                text = join_lines([lines[0][len(lead):]] + lines[1:])
                nslots = len(ins.args) - 3
                note = f"mensaje en pantalla ({nslots} renglones, ancho {WIDTH['normal']})"
                yield uid, text, speaker, note, _apply_message2(si, ii, lead)
            elif ins.op == MENU and _s(ins, 1):
                yield uid, decode(_s(ins, 1)), None, "opción de menú", _apply_simple(si, ii, 1)
            elif ins.op == GETITEM and _s(ins, 3):
                yield uid, decode(_s(ins, 3)), None, "antes del nombre del objeto obtenido", _apply_simple(si, ii, 3)


def _apply_simple(si, ii, ai):
    def apply(script, es, font):
        script.set_string(si, ii, ai, encode(es))
    return apply


def _apply_talk(si, ii, lead, kind):
    def apply(script, es, font):
        lines = reflow(font, es, WIDTH[kind])
        lines += [""] * (3 - len(lines))
        if len(lines) > 3:  # el chequeo ya avisa; aquí se junta el resto en el último renglón
            lines = lines[:2] + [" ".join(lines[2:])]
        for k, ln in enumerate(lines):
            script.set_string(si, ii, k + 1, encode((lead if k == 0 else "") + ln))
    return apply


def _apply_message(si, ii, lead):
    def apply(script, es, font):
        lines = reflow(font, es, WIDTH["mensaje"])
        script.set_string(si, ii, 0, encode(lead + "\\n".join(lines)))
    return apply


def _apply_message2(si, ii, lead):
    def apply(script, es, font):
        ins = script.segments[si][ii]
        slots = [i for i in range(3, len(ins.args)) if ins.args[i][0] == ys7scp.STR]
        lines = reflow(font, es, WIDTH["normal"])
        if len(lines) > len(slots):
            lines = lines[:len(slots) - 1] + [" ".join(lines[len(slots) - 1:])]
        lines += [""] * (len(slots) - len(lines))
        for k, (ai, ln) in enumerate(zip(slots, lines)):
            script.set_string(si, ii, ai, encode((lead if k == 0 else "") + ln))
    return apply


def script_files():
    return sorted((GAME / "lang/en/script").glob("*.bin"))


# ---------------------------------------------------------------- comandos

PRINTF = re.compile(r"%[-+0-9.]*[sdifxXu]")


def has_letters(text):
    return re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", PRINTF.sub("", CODE.sub("", text))) is not None


def table_files():
    return [GAME / "lang/en/text" / f"{n}.tbb" for n in tables.FILES]


def export():
    n = 0
    font = Font(GAME / "lang/en/system/font.itf")
    with open(SOURCE, "w", encoding="utf-8") as out:
        for path in table_files():
            for u in tables.units(path.stem, path.read_bytes(), font, sys.modules[__name__]):
                row = {"key": f"text/{path.stem}#{u.uid}", "en": u.text, "note": u.note}
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                n += 1
        for name in records.TABLES:
            path = GAME / "lang/en/text" / f"{name}.tbb"
            for uid, text, note, mx in records.units(name, path.read_bytes(), font, sys.modules[__name__]):
                out.write(json.dumps({"key": f"text/{name}#{uid}", "en": text, "max": mx, "note": note},
                                     ensure_ascii=False) + "\n")
                n += 1
        for path in map_files():
            for uid, text, kind in arb.units(path.read_bytes(), sys.modules[__name__]):
                if not has_letters(text):
                    continue
                out.write(json.dumps({"key": f"map/{path.stem}#{uid}", "en": text, "note": kind},
                                     ensure_ascii=False) + "\n")
                n += 1
        for uid, text, note in system_units(font):
            out.write(json.dumps({"key": f"text/strSystem#{uid}", "en": text, "note": note},
                                 ensure_ascii=False) + "\n")
            n += 1
        for path in script_files():
            script = ys7scp.Script(path.read_bytes())
            for uid, text, speaker, note, _ in script_units(script):
                if not has_letters(text):
                    continue  # «???», «...»: no se traduce
                row = {"key": f"script/{path.stem}#{uid}", "en": text}
                if speaker:
                    row["speaker"] = speaker
                if note:
                    row["note"] = note
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                n += 1
    print(f"{n} textos en {SOURCE}")


def load_translation():
    tr = {}
    for p in sorted(TRANSLATION.rglob("*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                tr[r["key"]] = r["es"]
    return tr


def build_scripts(tr, font, outdir):
    """Escribe en outdir los guiones con la traducción. Devuelve los archivos escritos."""
    written = []
    for path in script_files():
        data = path.read_bytes()
        script = ys7scp.Script(data)
        units = list(script_units(script))
        changed = False
        for uid, text, _, _, apply in units:
            es = tr.get(f"script/{path.stem}#{uid}")
            if es is None or es == text:
                continue  # sin traducir o idéntico: se deja el original tal cual
            apply(script, es, font)
            changed = True
        out = script.build() if changed else data
        dst = outdir / "lang/en/script" / path.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(out)
        written.append((path, dst))
    return written


def build_tables(tr, font, outdir):
    written = []
    me = sys.modules[__name__]
    for path in table_files():
        data = path.read_bytes()
        out = tables.build(path.stem, data, tr, font, me, f"text/{path.stem}")
        dst = outdir / "lang/en/text" / path.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(out)
        written.append((path, dst))
    return written


SYSTEM = "lang/en/text/strSystem.dbin"


def system_units(font, data=None):
    """(id, texto, nota) de strSystem.dbin: los textos con letras."""
    d = dbin.DBIN(data or (GAME / SYSTEM).read_bytes())
    for i, (sid, txt) in enumerate(d.pairs()):
        text = decode(txt)
        if not re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", CODE.sub("", re.sub(r"%[-+0-9.]*[sdifxXu]", "", text))):
            continue
        w = font.width(re.sub(r"%[-+0-9.]*[sdifxXu]", "", text))
        yield sid.decode("ascii"), text, f"texto de la interfaz (1 renglón, ancho {w})"


def build_system(tr, outdir):
    src = GAME / SYSTEM
    d = dbin.DBIN(src.read_bytes())
    for i, (sid, txt) in enumerate(d.pairs()):
        es = tr.get(f"text/strSystem#{sid.decode('ascii')}")
        if es is not None and es != decode(txt):
            d.set_text(i, encode(es))
    dst = outdir / SYSTEM
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(d.build())
    return [(src, dst)]


def map_files():
    return sorted((GAME / "lang/en/map").glob("*/*.arb"))


def build_maps(tr, outdir):
    written = []
    me = sys.modules[__name__]
    for src in map_files():
        dst = outdir / "lang/en/map" / src.parent.name / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(arb.build(src.read_bytes(), tr, me, f"map/{src.stem}"))
        written.append((src, dst))
    return written


def build_records(tr, outdir):
    written = []
    me = sys.modules[__name__]
    for name in records.TABLES:
        src = GAME / "lang/en/text" / f"{name}.tbb"
        dst = outdir / "lang/en/text" / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(records.build(name, src.read_bytes(), tr, me, f"text/{name}"))
        written.append((src, dst))
    return written


def built_font():
    f = BUILD / "lang/en/system/font.itf"
    return Font(f if f.exists() else GAME / "lang/en/system/font.itf")


def do_import():
    import font_es
    f = font_es.build()
    dst = BUILD / "lang/en/system/font.itf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(f.build())
    font = Font(dst)
    tr = load_translation()
    ws = build_scripts(tr, font, BUILD)
    wt = build_tables(tr, font, BUILD) + build_system(tr, BUILD) + build_records(tr, BUILD) + build_maps(tr, BUILD)
    import images
    wi = images.build_images(BUILD)
    print(f"{len(wi)} imágenes editadas")
    print(f"{len(ws)} guiones, {len(wt)} tablas y mapas, y la fuente en {BUILD / 'lang/en'}")


def roundtrip():
    """Exporta, toma el inglés como traducción e importa: debe dar los mismos bytes."""
    tr = {}
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        tr[r["key"]] = r["en"]
    font = Font(GAME / "lang/en/system/font.itf")
    tmp = LOCAL / "roundtrip"
    bad = 0
    for src, dst in build_scripts(tr, font, tmp) + build_tables(tr, font, tmp) + build_system(tr, tmp) \
            + build_records(tr, tmp) + build_maps(tr, tmp):
        if src.read_bytes() != dst.read_bytes():
            bad += 1
            print(f"DISTINTO: {src.name}")
    # Además, cada guion reconstruido entero (sin atajos) da los mismos bytes.
    for path in script_files():
        data = path.read_bytes()
        if ys7scp.Script(data).build() != data:
            bad += 1
            print(f"RECONSTRUCCIÓN DISTINTA: {path.name}")
    print("Ida y vuelta idéntica." if bad == 0 else f"{bad} archivos distintos.")
    return bad == 0


PSEUDO = str.maketrans("aeiounAEIOUN", "áéíóúñÁÉÍÓÚÑ")


def pseudo_text(text):
    """Un 25 % más largo y con letras españolas; los códigos quedan intactos."""
    parts = CODE.split(text)
    codes = CODE.findall(text)
    parts = [p.translate(PSEUDO) for p in parts]
    out = parts[0]
    for c, p in zip(codes, parts[1:]):
        out += c + p
    extra = [w for w in out.split(" ")[::4] if w and not CODE.search(w)]
    return "¿" + out + (" " + " ".join(extra) if extra else "")


def pseudo():
    import font_es
    tr = {}
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        es = pseudo_text(r["en"])
        while r.get("max") is not None and len(encode(es)) > r["max"]:
            es = es[:-1]  # los campos de largo fijo no pueden pasarse
        tr[r["key"]] = es
    f = font_es.build()
    dst = BUILD / "lang/en/system/font.itf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(f.build())
    font = Font(dst)
    ws = build_scripts(tr, font, BUILD)
    wt = build_tables(tr, font, BUILD) + build_system(tr, BUILD) + build_records(tr, BUILD) + build_maps(tr, BUILD)
    print(f"Pseudolocalización: {len(ws)} guiones, {len(wt)} tablas y mapas, y la fuente en {BUILD / 'lang/en'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["export", "import", "roundtrip", "pseudo"])
    a = ap.parse_args()
    if a.cmd == "export":
        export()
    elif a.cmd == "import":
        do_import()
    elif a.cmd == "pseudo":
        pseudo()
    else:
        sys.exit(0 if roundtrip() else 1)


if __name__ == "__main__":
    main()
