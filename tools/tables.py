"""Tablas de texto de Celceta (lang/en/text/*.tbb) para el adaptador.

Tres tipos de texto:
- Celdas sueltas (nombres, títulos, lugares): un renglón; el límite de ancho es
  el máximo de esa columna en inglés.
- Descripciones con «\\n» literal (monslib, matlib): se exportan sin saltos y se
  reparten en renglones al importar, sin pasar los que usa el inglés.
- Listas del diario y de las misiones (diary, quest): el juego las lee fila por
  fila (una fila = un renglón; «★» abre un párrafo; la bandera de la columna 0
  se omite en las filas que siguen). Se exporta un párrafo por unidad y al
  importar se reparte en las filas que haga falta, con la sangría y la «★» del
  original.

Las filas de comentario («//») y las celdas en japonés son notas internas de los
desarrolladores y no se exportan.
"""
import re

import tbb

JP = re.compile("[　-ヿ一-鿿＀-￯]")
LETTER = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]")
# en los avisos, las firmas («- Bar Owner, Mucho», alineada con espacios) van solas
SIGNATURE = re.compile(r"\S {3,}\S|^ *-|^ {8,}")
NL = "\\n"   # salto literal (dos caracteres) de las descripciones

# tabla: {columna: etiqueta}
CELLS = {
    "item": {1: "nombre", 2: "efecto", 3: "descripcion"},
    "mapname": {1: "mapa", 2: "region"},
    "memory": {0: "titulo", 3: "descripcion"},
    "manual": {2: "tema"},
    "record": {3: "texto", 5: "valor"},
    "monslib": {1: "nombre", 3: "descripcion"},
    "matlib": {1: "descripcion", 3: "nombre"},
    "status": {1: "nombre"},
    "diary": {2: "item", 3: "titulo"},
    "quest": {3: "cliente", 4: "recompensa", 5: "etiqueta", 6: "titulo"},
}
NOTES = {
    ("item", "nombre"): "nombre de objeto", ("item", "efecto"): "efecto del objeto (menú)",
    ("item", "descripcion"): "descripción de objeto", ("mapname", "mapa"): "nombre de mapa",
    ("mapname", "region"): "nombre de región", ("memory", "titulo"): "título de recuerdo",
    ("memory", "descripcion"): "descripción de recuerdo", ("manual", "tema"): "tema del manual",
    ("record", "texto"): "registro de partida", ("record", "valor"): "valor del registro",
    ("monslib", "nombre"): "nombre de monstruo (bestiario)", ("monslib", "descripcion"): "descripción de monstruo",
    ("matlib", "descripcion"): "descripción de material", ("matlib", "nombre"): "nombre de material",
    ("status", "nombre"): "nombre de personaje o monstruo", ("diary", "item"): "capítulo del diario",
    ("diary", "titulo"): "título del diario", ("quest", "cliente"): "cliente de la misión",
    ("quest", "recompensa"): "recompensa de la misión", ("quest", "etiqueta"): "nombre corto de la misión",
    ("quest", "titulo"): "título de la misión",
}
LISTS = {"diary": [1], "quest": [0, 1]}
FILES = sorted(set(CELLS) | set(LISTS))
HEADER_ROWS = {"item": 1}
# columna con el id de la fila, para claves estables (si no hay, el número de fila)
ID_COL = {"item": 0, "mapname": 0, "status": 0, "monslib": 0, "matlib": 0, "manual": 0,
          "record": 1, "memory": 2}


def dec(b):
    import celceta  # import tardío: celceta importa este módulo
    return celceta.decode(b)


def visible_cell(row, c, r, name):
    if r < HEADER_ROWS.get(name, 0):
        return False
    v = dec(row[c])
    c0 = dec(row[0])
    return bool(v) and not v.startswith("//") and not c0.startswith("//") \
        and not JP.search(v) and LETTER.search(v) is not None


def column_limits(t, name, font):
    """{columna: (ancho máximo, renglones máximos)} del inglés."""
    lim = {}
    rows = t.row_list()
    for c in set(CELLS.get(name, {})) | set(LISTS.get(name, [])):
        w, n = 0, 1
        for r, row in enumerate(rows):
            if visible_cell(row, c, r, name):
                parts = dec(row[c]).split(NL)
                n = max(n, len(parts))
                w = max(w, max(font.width(p) for p in parts))
        lim[c] = (w, n)
    return lim


# ------------------------------------------------------------ recorrido

class Unit:
    def __init__(self, uid, text, note, render):
        self.uid, self.text, self.note, self.render = uid, text, note, render


def walk(name, t, font, C):
    """Divide la tabla en filas fijas (listas de bytes) y unidades de texto.

    Devuelve una lista de elementos: ("rows", [filas]) o ("unit", Unit, [filas
    originales]). Unit.render(es) devuelve las filas nuevas.
    """
    rows = t.row_list()
    lim = column_limits(t, name, font)
    lists = LISTS.get(name, [])
    out = []
    used = set()

    def uid_for(base):
        k, n = base, 2
        while k in used:
            k = f"{base}~{n}"
            n += 1
        used.add(k)
        return k

    # banderas de contexto para claves estables
    flag = quest = None
    section = None
    r = 0
    while r < len(rows):
        row = rows[r]
        c0 = dec(row[0])
        if c0.startswith("[") and c0.endswith("]"):
            section = c0
        if name == "quest" and c0 == "[QUEST]":
            quest = dec(row[1]) or quest
        if c0 and not c0.startswith("//") and not c0.startswith("[") \
                and not (name == "quest" and section != "[QUESTSTATE]"):
            flag = c0

        # listas: párrafos de varias filas
        lc = _list_col(name, section, row, lists)
        if lc is not None and _para_start(rows, r, lc, name):
            end = _para_end(rows, r, lc, name)
            block = rows[r:end]
            ctx = quest if name == "quest" else flag
            part = "aviso" if (name == "quest" and lc == 0) else (flag if name == "quest" else None)
            base = "/".join(x for x in (ctx, part) if x) or f"r{r}"
            uid = uid_for(base)
            text, render = _para_unit(block, lc, lim[lc][0], font, C)
            if is_signature(block, lc):
                note = f"firma del aviso, alineada a la derecha (1 renglón, ancho {lim[lc][0]})"
            else:
                kind = ("aviso de misión" if (name == "quest" and lc == 0) else
                        "diario de misión" if name == "quest" else "diario de la historia")
                note = f"{kind} (renglones libres, ancho {lim[lc][0]})"
            out.append(("unit", Unit(uid, text, note, render), block))
            r = end
            continue

        # celdas sueltas
        cells = CELLS.get(name, {})
        units = []
        for c, label in cells.items():
            if name == "quest" and c0 != "[QUEST]":
                continue
            if visible_cell(row, c, r, name):
                idv = dec(row[ID_COL[name]]) if name in ID_COL else ""
                ident = quest if name == "quest" else (idv if re.fullmatch(r"[A-Za-z0-9_:]+", idv) else f"r{r}")
                units.append((c, label, ident))
        if units:
            for c, label, ident in units:
                text = dec(row[c])
                w, n = lim[c]
                uid = uid_for(f"{ident}/{label}")
                plain = " ".join(p.strip() for p in text.split(NL)) if NL in text or n > 1 else text
                note = f"{NOTES[(name, label)]} ({n} renglón{'es' if n > 1 else ''}, ancho {w})"
                out.append(("unit", Unit(uid, plain, note, _cell_render(c, n, w, font, C)), [row]))
            # varias unidades en la misma fila: se aplican sobre la misma fila
            r += 1
            continue
        out.append(("rows", [row]))
        r += 1
    return _merge_same_row(out)


def _merge_same_row(items):
    """Junta las unidades que comparten fila para que se apliquen en cadena."""
    out = []
    for it in items:
        if it[0] == "unit" and out and out[-1][0] == "cell-group" and out[-1][2] is it[2][0] \
                and len(it[2]) == 1:
            out[-1][1].append(it[1])
        elif it[0] == "unit" and len(it[2]) == 1 and getattr(it[1].render, "cell", False):
            out.append(["cell-group", [it[1]], it[2][0]])
        else:
            out.append(it)
    return out


def _list_col(name, section, row, lists):
    if name == "diary" and 1 in lists:
        return 1 if dec(row[1]).strip() and not dec(row[0]).startswith("//") and not JP.search(dec(row[1])) else None
    if name == "quest":
        if section == "[QUEST]" and dec(row[0]).strip() and not dec(row[0]).startswith(("//", "[")) \
                and not JP.search(dec(row[0])):
            return 0
        if section == "[QUESTSTATE]" and dec(row[1]).strip() and not dec(row[0]).startswith("//") \
                and not JP.search(dec(row[1])):
            return 1
    return None


def _starts(text):
    return text.lstrip(" ").startswith("★")


def _para_start(rows, r, c, name):
    return True  # el recorrido solo llega aquí al comienzo de un párrafo


def _para_end(rows, r, c, name):
    e = r + 1
    while e < len(rows):
        row = rows[e]
        v = dec(row[c])
        c0 = dec(row[0])
        if not v.strip() or JP.search(v) or c0.startswith("//"):
            break
        if c == 0:   # aviso: termina en fila vacía, marcador o firma
            if c0.startswith("[") or SIGNATURE.search(v) or SIGNATURE.search(dec(rows[r][c])):
                break
        else:
            if c0 or _starts(v):
                break
        if any(row[k] for k in range(len(row)) if k != c and not (c == 1 and k == 0)):
            break
        e += 1
    return e


def _indent(s):
    return s[:len(s) - len(s.lstrip(" "))]


def is_signature(block, c):
    return c == 0 and len(block) == 1 and SIGNATURE.search(dec(block[0][c])) is not None


def _signature_unit(block, c, font, C):
    """Firma de un aviso: una sola fila, alineada a la derecha como el original."""
    line = dec(block[0][c])
    right = font.width(line)
    text = line.strip(" ")

    def render(es):
        if es is None:
            return block
        es = es.strip()
        pad = max(8, round((right - font.width(es)) / font.char_width(" ")))  # 8+: se sigue viendo como firma
        row = list(block[0])
        row[c] = C.encode(" " * pad + es)
        return [row]
    return text, render


def _para_unit(block, c, width, font, C):
    if is_signature(block, c):
        return _signature_unit(block, c, font, C)
    lines = [dec(r[c]) for r in block]
    first_ind = _indent(lines[0])
    star = lines[0].lstrip(" ").startswith("★")
    cont_ind = _indent(lines[1]) if len(lines) > 1 else first_ind + ("  " if star else "")
    body = [lines[0].lstrip(" ")[1 if star else 0:]] + [ln.lstrip(" ") for ln in lines[1:]]
    text = C.join_lines([b.rstrip(" ") for b in body])
    first = block[0]

    def render(es):
        if es is None:
            return block
        avail = width - max(font.width(first_ind + ("★" if star else "")), font.width(cont_ind))
        parts = C.reflow(font, es.strip(), avail)
        rows = []
        for i, p in enumerate(parts):
            s = (first_ind + ("★" if star else "") + p) if i == 0 else cont_ind + p
            if i == 0:
                row = list(first)
            else:
                row = [b""] * len(first)
            row[c] = C.encode(s)
            rows.append(row)
        return rows
    return text, render


def _cell_render(c, n, w, font, C):
    def render(es, row):
        row = list(row)
        if n > 1:
            row[c] = C.encode(NL.join(C.reflow(font, es, w)))
        else:
            row[c] = C.encode(es)
        return row
    render.cell = True
    return render


# ------------------------------------------------------------ export / import

def units(name, data, font, C):
    t = tbb.TBB(data)
    for it in walk(name, t, font, C):
        if it[0] == "unit":
            yield it[1]
        elif it[0] == "cell-group":
            yield from it[1]


def build(name, data, tr, font, C, prefix):
    """Bytes de la tabla con la traducción (tr: {clave: es})."""
    t = tbb.TBB(data)
    rows = []
    changed = False
    for it in walk(name, t, font, C):
        if it[0] == "rows":
            rows += it[1]
        elif it[0] == "cell-group":
            row = it[2]
            for u in it[1]:
                es = tr.get(f"{prefix}#{u.uid}")
                if es is not None and es != u.text:
                    row = u.render(es, row)
                    changed = True
            rows.append(row)
        else:
            u, block = it[1], it[2]
            es = tr.get(f"{prefix}#{u.uid}")
            if es is not None and es != u.text:
                rows += u.render(es)
                changed = True
            else:
                rows += block
    if not changed:
        return data
    t.set_rows(rows)
    return t.build()
