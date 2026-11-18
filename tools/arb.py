"""Mapas de Celceta (lang/en/map/*/*.arb, YS7_ARG): nombres visibles.

El archivo es una secuencia de datos binarios con cadenas etiquetadas:
0x7FFF, u32 largo (con el NUL) y los bytes. Ningún tamaño ni offset depende
del largo de las cadenas: fuera de ellas, el inglés y el japonés son idénticos
byte por byte en 203 de 205 mapas, aunque 756 cadenas cambian de largo (los
otros dos difieren en datos que no son texto). Por eso una cadena se puede
reemplazar en su lugar por otra de distinto largo.

Textos visibles (el resto son ids, rutas y notas internas):
- nombre de PNJ: la cadena justo antes de «NPC» o «NPC_SMALL»
  (… talk script, id, NOMBRE, NPC);
- habilidad de campo: la que sigue a un id «…_pa01» (id, ETIQUETA, mapa:script);
- monstruo de misión: la que sigue a un id «qs_…».
"""
import re

TAG = b"\xff\x7f"


def strings(data):
    """[(inicio, fin, bytes)] de cada cadena etiquetada (fin = tras el NUL)."""
    out = []
    i = 0x14
    while True:
        m = data.find(TAG, i)
        if m < 0:
            break
        n = int.from_bytes(data[m + 2:m + 6], "little")
        if 0 < n < 4096 and m + 6 + n <= len(data) and data[m + 5 + n] == 0 \
                and b"\0" not in data[m + 6:m + 5 + n]:
            out.append((m, m + 6 + n, data[m + 6:m + 5 + n]))
            i = m + 6 + n
        else:
            i = m + 1
    return out


PA = re.compile(rb"^[A-Za-z0-9]+_pa\d+[a-z]?$")
IDENT = re.compile(rb"^[A-Za-z0-9_:]+$")   # ids y referencias a guiones, no texto


def visible(data):
    """[(índice en strings, id, tipo)] de las cadenas visibles."""
    S = strings(data)
    out = []
    for i in range(1, len(S) - 1):
        prev, cur, nxt = S[i - 1][2], S[i][2], S[i + 1][2]
        if not cur or (IDENT.search(cur) and b"_" in cur):
            continue
        if nxt in (b"NPC", b"NPC_SMALL"):
            out.append((i, prev, "nombre de PNJ"))
        elif PA.search(prev):
            out.append((i, prev, "habilidad de campo (aviso)"))
        elif prev.startswith(b"qs_"):
            out.append((i, prev, "monstruo de misión"))
    return S, out


def units(data, C):
    S, vis = visible(data)
    used = {}
    for i, ident, kind in vis:
        base = ident.decode("cp932") or f"s{i}"
        n = used.get(base, 0) + 1
        used[base] = n
        uid = base if n == 1 else f"{base}~{n}"
        yield uid, C.decode(S[i][2]), kind


def build(data, tr, C, prefix):
    S, vis = visible(data)
    repl = {}
    used = {}
    for i, ident, kind in vis:
        base = ident.decode("cp932") or f"s{i}"
        n = used.get(base, 0) + 1
        used[base] = n
        uid = base if n == 1 else f"{base}~{n}"
        es = tr.get(f"{prefix}#{uid}")
        if es is not None and es != C.decode(S[i][2]):
            repl[i] = C.encode(es)
    if not repl:
        return data
    out = bytearray()
    p = 0
    for i in sorted(repl):
        a, b, _ = S[i]
        v = repl[i]
        out += data[p:a] + TAG + (len(v) + 1).to_bytes(4, "little") + v + b"\0"
        p = b
    out += data[p:]
    return bytes(out)
