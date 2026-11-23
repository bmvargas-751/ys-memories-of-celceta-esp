#!/usr/bin/env python3
"""Prueba en el juego: copia build/ a la instalación de Steam y la deshace.

    python3 tools/gametest.py install   # respalda los originales y copia build/
    python3 tools/gametest.py restore   # devuelve los originales

El respaldo va en ../local/ys-memories-of-celceta/respaldo-juego/, con la
misma estructura que el juego. Solo se respalda un archivo la primera vez (así
el respaldo siempre es el original, aunque se instale varias veces).
"""
import argparse
import filecmp
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import celceta as C  # noqa: E402

STEAM = Path("/mnt/c/Steam/steamapps/common/Ys Memories of Celceta")
BACKUP = C.LOCAL / "respaldo-juego"


def files():
    return sorted(p.relative_to(C.BUILD) for p in C.BUILD.rglob("*") if p.is_file())


def install(game):
    rels = files()
    if not rels:
        sys.exit(f"No hay nada en {C.BUILD}")
    for rel in rels:
        dst, bak = game / rel, BACKUP / rel
        if not dst.exists():
            sys.exit(f"No existe en el juego: {rel}")
        if not bak.exists():
            bak.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, bak)
            if not filecmp.cmp(dst, bak, shallow=False):
                sys.exit(f"El respaldo de {rel} no quedó igual")
    for rel in rels:
        shutil.copyfile(C.BUILD / rel, game / rel)
    bad = [r for r in rels if not filecmp.cmp(C.BUILD / r, game / r, shallow=False)]
    if bad:
        sys.exit(f"{len(bad)} archivos no quedaron iguales, p. ej. {bad[0]}")
    print(f"Instalados {len(rels)} archivos (respaldo en {BACKUP}).")


def restore(game):
    rels = sorted(p.relative_to(BACKUP) for p in BACKUP.rglob("*") if p.is_file())
    for rel in rels:
        shutil.copyfile(BACKUP / rel, game / rel)
    bad = [r for r in rels if not filecmp.cmp(BACKUP / r, game / r, shallow=False)]
    if bad:
        sys.exit(f"{len(bad)} archivos no quedaron iguales, p. ej. {bad[0]}")
    print(f"Restaurados {len(rels)} archivos originales.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["install", "restore"])
    ap.add_argument("--game", type=Path, default=STEAM, help="carpeta del juego")
    a = ap.parse_args()
    install(a.game) if a.cmd == "install" else restore(a.game)


if __name__ == "__main__":
    main()
