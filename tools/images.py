#!/usr/bin/env python3
"""Imágenes con texto de Celceta: ITP → PNG para editar, y PNG editado → ITP.

    python3 tools/images.py export   # originales a ../local/ys-memories-of-celceta/imagenes/en/
    python3 tools/images.py import   # imagenes/es/*.png → build/ (mismo camino que en el juego)

Los PNG editados van en imagenes/es/ con el mismo nombre que el original
(p. ej. imagenes/es/lang/en/visual/mapname/mnmp1101.itp.png) y el mismo tamaño.
Solo se convierten las que existen: lo demás queda como en el juego.

Las imágenes del juego nunca van al repositorio.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import celceta as C  # noqa: E402
import itp  # noqa: E402

IMAGES = C.LOCAL / "imagenes"

# Imágenes con texto visible (ruta relativa a la carpeta del juego).
TEXT_IMAGES = (
    ["lang/en/system/menu_mt1.itp", "lang/en/system/menu_mt2.itp", "lang/en/system/menu_mt3.itp",
     "lang/en/system/menu_mt4.itp", "lang/en/system/menucom.itp",
     "system/ti_icon.itp", "system/system01.itp", "system/emotion.itp"]
    + sorted(str(p.relative_to(C.GAME)) for p in (C.GAME / "lang/en/visual/mapname").glob("*.itp"))
    + sorted(str(p.relative_to(C.GAME)) for p in (C.GAME / "lang/en/visual/bossname").glob("*.itp"))
    + sorted(str(p.relative_to(C.GAME)) for p in (C.GAME / "lang/en/visual").glob("topic_*.itp"))
)


def export():
    n = 0
    for rel in TEXT_IMAGES:
        im = itp.ITP((C.GAME / rel).read_bytes())
        dst = IMAGES / "en" / f"{rel}.png"
        dst.parent.mkdir(parents=True, exist_ok=True)
        Image.frombytes("RGBA", (im.w, im.h), im.to_rgba()).save(dst)
        n += 1
    print(f"{n} imágenes en {IMAGES / 'en'}")


def build_images(outdir):
    written = []
    for rel in TEXT_IMAGES:
        png = IMAGES / "es" / f"{rel}.png"
        if not png.exists():
            continue
        src = C.GAME / rel
        im = itp.ITP(src.read_bytes())
        new = Image.open(png).convert("RGBA")
        if new.size != (im.w, im.h):
            raise SystemExit(f"{png}: mide {new.size}, el original {im.w}×{im.h}")
        im.from_rgba(new.tobytes())
        dst = outdir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(im.build())
        written.append((src, dst))
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["export", "import"])
    a = ap.parse_args()
    if a.cmd == "export":
        export()
    else:
        w = build_images(C.BUILD)
        print(f"{len(w)} imágenes en {C.BUILD}")


if __name__ == "__main__":
    main()
