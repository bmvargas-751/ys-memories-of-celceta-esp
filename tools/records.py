"""Tablas comprimidas de registros fijos (lang/en/text/skill.tbb, warpdata.tbb).

Formato: u32 número de registros y un bloque FALCOM3 (falcom.py) con los
registros, todos del mismo tamaño. El texto va en campos de largo fijo
terminados en NUL: el límite en bytes es duro (T-4).

    skill.tbb     registros de 188 bytes: nombre [0, 32), descripción [124, 188)
    warpdata.tbb  registros de 148 bytes: destino [8, 72)
"""
import falcom

TABLES = {
    "skill": {"start": 4, "size": 188,
              "fields": {"nombre": (0, 32, "nombre de habilidad"),
                         "descripcion": (124, 64, "descripción de habilidad")}},
    "warpdata": {"start": 4, "size": 148,
                 "fields": {"destino": (8, 64, "destino de teletransporte")}},
}


def _records(name, data):
    t = TABLES[name]
    out, _ = falcom.decompress_falcom3(data[t["start"]:])
    size = t["size"]
    return [bytearray(out[i:i + size]) for i in range(0, len(out), size)]


def units(name, data, font, C):
    """(id, texto, nota, máximo en bytes)."""
    recs = _records(name, data)
    widths = {}
    for label, (off, ln, _) in TABLES[name]["fields"].items():
        widths[label] = max(font.width(C.decode(bytes(r[off:off + ln]).split(b"\0", 1)[0])) for r in recs)
    for i, r in enumerate(recs):
        for label, (off, ln, note) in TABLES[name]["fields"].items():
            raw = bytes(r[off:off + ln]).split(b"\0", 1)[0]
            if raw:
                yield f"{i}/{label}", C.decode(raw), f"{note} (1 renglón, ancho {widths[label]})", ln - 1


def build(name, data, tr, C, prefix):
    t = TABLES[name]
    recs = _records(name, data)
    changed = False
    for i, r in enumerate(recs):
        for label, (off, ln, _) in t["fields"].items():
            raw = bytes(r[off:off + ln]).split(b"\0", 1)[0]
            es = tr.get(f"{prefix}#{i}/{label}")
            if not raw or es is None or es == C.decode(raw):
                continue
            b = C.encode(es)
            if len(b) > ln - 1:
                raise ValueError(f"{prefix}#{i}/{label}: {len(b)} bytes, el máximo es {ln - 1}")
            r[off:off + ln] = b + b"\0" * (ln - len(b))
            changed = True
    if not changed:
        return data
    return data[:t["start"]] + falcom.compress_falcom3(b"".join(bytes(r) for r in recs))
