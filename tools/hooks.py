"""Chequeos propios de Celceta para loc.py (ver checks.py del kit).

- encode: bytes como los escribe el adaptador (Shift-JIS + letras españolas).
- missing_chars: lo que la fuente no puede mostrar (T-5).
- check: cuadros que no caben en sus renglones (T-3) y términos del glosario
  escritos en minúscula a media frase, que el chequeo del kit no ve (G-3).

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
    return box(item, es) + glossary_lower(item, es)


@functools.cache
def _glossary():
    """(rx del término en minúscula, rx de la traducción) de las filas del glosario
    con mayúscula inicial: «Ore» también es «ore» a media frase."""
    from lockit import checks  # el kit ya está en sys.path cuando loc.py carga los hooks
    rows = checks.glossary_rx()
    have = {t_en for t_en, *_ in rows}
    out = []
    for t_en, t_es, rx_en, rx_es in rows:
        low = t_en[:1].lower() + t_en[1:]
        # solo términos comunes («mena», «objeto»): una etiqueta («Quemadura») en minúscula suele ser otra cosa («burning sun»)
        if t_en[:1].isupper() and low not in have and t_es[:1].islower():
            out.append((t_en, t_es, re.compile(rf"(?<![A-Za-z]){re.escape(low)}(?![A-Za-z])"), rx_es))
    return out


def glossary_lower(item, es):
    """G-3 para términos en minúscula («rare ore»), si el glosario solo trae la forma con mayúscula."""
    from lockit import checks
    en, ves = item.get("en") or "", checks.plain(checks.visible(es))
    out = []
    for t_en, t_es, rx_low, rx_es in _glossary():
        if rx_low.search(en) and not rx_es.search(ves):
            out.append(("glosario", "G-3", f"{t_en} (en minúscula) → {t_es}"))
    return out


def box(item, es):
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
