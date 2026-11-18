#!/usr/bin/env python3
"""Agrega las letras españolas a la fuente de Celceta, armadas con sus glifos.

    python3 tools/font_es.py                 # escribe build/lang/en/system/font.itf
    python3 tools/font_es.py --preview X.png # y una imagen de muestra

Cada letra sale de la fuente del juego, para que tenga su mismo trazo:
vocal + acento agudo dibujado con el grosor del palo de la «i»; «ü» con dos
puntos de la «i»; «ñ» con la virgulilla de «~»; «¿» y «¡» son «?» y «!»
girados. Van en las casillas de ES_MAP (fila 9 de JIS, vacía en el juego).
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import celceta as C  # noqa: E402
import itf  # noqa: E402

M = 12          # margen del lienzo, para lo que sobresale a la izquierda
H = 64          # alto de la línea
SS = 4          # sobremuestreo para dibujar el acento


def to_img(g):
    im = Image.new("L", (g.w, g.h))
    im.putdata([v * 17 for row in g.px for v in row])
    return im


def ascii_glyph(f, ch):
    return f.glyph(ord(ch) - 0x20)


def canvas(g):
    """Lienzo de toda la línea con el glifo base en su lugar."""
    c = Image.new("L", (g.adv + 2 * M, H))
    c.paste(to_img(g), (g.xoff + M, g.yoff))
    return c


def acute(c, cx, ytop, ybot, thick):
    """Acento agudo: un trazo inclinado hacia la derecha, de ytop a ybot."""
    big = Image.new("L", (c.width * SS, c.height * SS))
    d = ImageDraw.Draw(big)
    slant = (ybot - ytop) * 0.55
    x0, x1 = cx - slant / 2, cx + slant / 2
    t = thick / 2
    poly = [(x0 - t, ybot), (x0 + t, ybot), (x1 + t, ytop), (x1 - t, ytop)]
    d.polygon([(x * SS, y * SS) for x, y in poly], fill=255)
    small = big.resize(c.size, Image.LANCZOS)
    return _max(c, small)


def _max(a, b):
    out = Image.new("L", a.size)
    out.putdata([max(x, y) for x, y in zip(a.getdata(), b.getdata())])
    return out


def paste_max(c, im, x, y):
    layer = Image.new("L", c.size)
    layer.paste(im, (x, y))
    return _max(c, layer)


def finish(c, adv):
    """Recorta al contenido y vuelve a un glifo de 16 niveles."""
    q = c.point(lambda v: round(v / 17) * 17)
    box = q.getbbox()
    crop = q.crop(box)
    x0, y0, x1, y1 = box
    px = [[v // 17 for v in list(crop.getdata())[r * crop.width:(r + 1) * crop.width]]
          for r in range(crop.height)]
    xoff = x0 - M
    if xoff < 0:  # que no empiece antes del cursor
        adv += -xoff
        xoff = 0
    adv = max(adv, xoff + crop.width)
    return itf.Glyph(crop.width, crop.height, y0, xoff, adv, px)


def i_dot(f):
    g = ascii_glyph(f, "i")
    rows = []
    for row in g.px:
        if not any(row):
            break
        rows.append(row)
    dot = itf.Glyph(g.w, len(rows), 0, 0, 0, rows)
    return to_img(dot), g


def stem_thickness(f):
    g = ascii_glyph(f, "i")
    return max(sum(1 for v in row if v >= 8) for row in g.px)


def make(f):
    thick = stem_thickness(f)
    dot, ig = i_dot(f)
    tilde = to_img(ascii_glyph(f, "~"))
    lower_top = ig.yoff                      # arriba del punto de la «i»
    lower_bot = ig.yoff + dot.height         # abajo del punto
    cap_top = ascii_glyph(f, "A").yoff
    upper_bot = cap_top - 2
    upper_top = max(0, upper_bot - (lower_bot - lower_top) - 1)
    out = {}

    def center(g):
        return M + g.xoff + g.w / 2

    for ch, base in zip("áéóú", "aeou"):
        g = ascii_glyph(f, base)
        c = canvas(g)
        out[ch] = finish(acute(c, center(g) + 1, lower_top - 1, lower_bot, thick), g.adv)
    for ch, base in zip("ÁÉÓÚ", "AEOU"):
        g = ascii_glyph(f, base)
        c = canvas(g)
        out[ch] = finish(acute(c, center(g) + 1, upper_top, upper_bot, thick), g.adv)

    # í / Í: palo de la «i» sin punto, o la «I», con su acento
    stem_rows = [row for row in ig.px[dot.height:]]
    while stem_rows and not any(stem_rows[0]):
        stem_rows.pop(0)
    stem = itf.Glyph(ig.w, len(stem_rows), ig.yoff + ig.h - len(stem_rows), ig.xoff, ig.adv, stem_rows)
    c = canvas(stem)
    out["í"] = finish(acute(c, center(stem) + 2, lower_top - 1, lower_bot, thick), stem.adv + 2)
    g = ascii_glyph(f, "I")
    out["Í"] = finish(acute(canvas(g), center(g) + 2, upper_top, upper_bot, thick), g.adv + 2)

    # ü / Ü: dos puntos de la «i»
    for ch, base, top in (("ü", "u", lower_top), ("Ü", "U", upper_bot - dot.height + 1)):
        g = ascii_glyph(f, base)
        c = canvas(g)
        cx = center(g)
        gap = max(2, thick // 2)
        c = paste_max(c, dot, round(cx - gap / 2 - dot.width + 1), top)
        c = paste_max(c, dot, round(cx + gap / 2 - 1), top)
        out[ch] = finish(c, g.adv)

    # ñ / Ñ: virgulilla de «~», al ancho de la letra
    for ch, base, top, bot in (("ñ", "n", lower_top, lower_bot), ("Ñ", "N", upper_top, upper_bot)):
        g = ascii_glyph(f, base)
        c = canvas(g)
        tw = max(10, g.w - 2)
        th = max(6, bot - top - 1)
        t = tilde.resize((tw, th), Image.LANCZOS)
        c = paste_max(c, t, M + g.xoff + (g.w - tw) // 2, top)
        out[ch] = finish(c, g.adv)

    # ¿ / ¡: girados, colgando hasta la línea de las descendentes
    desc = ascii_glyph(f, "g")
    bottom = desc.yoff + desc.h
    for ch, base in (("¿", "?"), ("¡", "!")):
        g = ascii_glyph(f, base)
        im = to_img(g).rotate(180)
        c = Image.new("L", (g.adv + 2 * M, H))
        c.paste(im, (M + g.adv - g.xoff - g.w, bottom - g.h))
        out[ch] = finish(c, g.adv)
    return out


def build(src=None):
    src = src or C.GAME / "lang/en/system/font.itf"
    f = itf.ITF(src.read_bytes())
    glyphs = make(f)
    for ch, g in glyphs.items():
        i = itf.index(C.ES_MAP[ch])
        if f.raw[i]:
            raise SystemExit(f"La casilla de «{ch}» ({C.ES_MAP[ch].hex()}) no está vacía")
        f.set_glyph(i, g)
    return f


def preview(f, text, path, scale=1):
    lines = text.split("\n")
    W = 40 + max(sum(_adv(f, ch) for ch in ln) for ln in lines)
    im = Image.new("L", (W, 20 + H * len(lines)), 0)
    for li, ln in enumerate(lines):
        x = 20
        for ch in ln:
            g = f.glyph(itf.index(C.encode(ch)))
            if g:
                im.paste(_max(im.crop((x + g.xoff, 10 + li * H + g.yoff, x + g.xoff + g.w, 10 + li * H + g.yoff + g.h)),
                              to_img(g)), (x + g.xoff, 10 + li * H + g.yoff))
                x += g.adv
            else:
                x += 16
    if scale != 1:
        im = im.resize((im.width // scale, im.height // scale), Image.LANCZOS)
    im.save(path)


def _adv(f, ch):
    g = f.glyph(itf.index(C.encode(ch)))
    return g.adv if g else 16


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview")
    a = ap.parse_args()
    f = build()
    dst = C.BUILD / "lang/en/system/font.itf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(f.build())
    print(f"Fuente con {len(C.ES_MAP)} letras españolas en {dst}")
    if a.preview:
        preview(f, "¿Qué pasó, Adol? ¡Ñandú, pingüino!\náéíóú ÁÉÍÓÚ üÜ ñÑ ¿¡\nÍñigo usó el óleo: \"Úrsula\", AÉREO ÜBER\nIt's not possible to warp right now.",
                a.preview)
        print(f"Muestra en {a.preview}")


if __name__ == "__main__":
    main()
