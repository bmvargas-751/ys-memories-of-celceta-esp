"""Chequeos propios de Celceta para loc.py (ver checks.py del kit).

- encode: bytes como los escribe el adaptador (Shift-JIS + letras españolas).
- missing_chars: lo que la fuente no puede mostrar (T-5).
- check: cuadros que no caben en sus renglones (T-3).

Usa la fuente ya modificada (build/lang/en/system/font.itf) si existe; si no,
la original del juego.
"""
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import celceta as C  # noqa: E402


@functools.cache
def font():
    built = C.BUILD / "lang/en/system/font.itf"
    return C.Font(built if built.exists() else C.GAME / "lang/en/system/font.itf")


def encode(key, es):
    return C.encode(es)


def missing_chars(key, es):
    f = font()
    out = []
    for ch in sorted(set(C.CODE.sub("", es))):
        try:
            b = C.encode(ch)
        except UnicodeEncodeError:
            out.append(ch)
            continue
        i = f.index(b)
        if i >= len(f.empty) or f.empty[i]:
            out.append(ch)
    return out


PRINTF = re.compile(r"%[-+ 0#]*\d*(?:\.\d+)?[sdiuxXfc]")  # el ancho de la nota se midió sin ellos
NOTE = re.compile(r"\((\d+|renglones libres)(?: renglón| renglones)?, ancho (\d+)\)")


def check(key, item, es):
    """T-3: el texto repartido en renglones cabe en los que tiene ese lugar."""
    m = NOTE.search(item.get("note") or "")
    if not m:
        return []
    width = int(m.group(2))
    try:
        # Un «\n» es un salto de renglón: cada tramo se reparte por su cuenta.
        lines = [ln for part in es.split("\n") for ln in C.reflow(font(), PRINTF.sub("", part), width)]
    except UnicodeEncodeError:
        return []  # ya lo informa missing_chars
    if m.group(1) == "renglones libres":
        return []
    # Los saltos del original cuentan como renglones disponibles.
    maxl = max(int(m.group(1)), (item.get("en") or "").count("\n") + 1)
    if len(lines) > maxl:
        return [("caja", "T-3", f"{len(lines)} renglones, caben {maxl} (ancho {width})")]
    return []
