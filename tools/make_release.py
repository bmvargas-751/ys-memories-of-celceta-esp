#!/usr/bin/env python3
"""Arma los paquetes de una versión: uno para Windows y otro para Linux (Steam Deck incluida).

    python3 tools/make_release.py v0.9.0   -> dist/release/Celceta-ESP-v0.9.0-windows.zip y -linux.tar.gz

Cada paquete se descomprime dentro de la carpeta del juego (o en cualquier otra) y trae lo
necesario: el instalador, la traducción, las herramientas que arman los archivos y los
lanzadores de instalar y desinstalar. Usa el Python del sistema (3.8 o superior): en
Linux y Steam Deck ya viene; en Windows se pide instalarlo desde python.org.

No incluye archivos del juego. Lleva dos datos derivados, armados aquí con la copia local:
  data/originales.json  ruta → sha256 de cada original que la traducción cambia (para
                        reconocer la versión del juego y no respaldar un archivo ya traducido)
  data/fuente_es.json   los 16 glifos españoles (á é í ó ú ü ñ ¿ ¡ y mayúsculas), que el
                        instalador mete en la fuente del jugador sin necesitar PIL
Antes de empaquetar comprueba que el instalador arma lo mismo que `celceta.py import`.
Necesita PIL (solo aquí, para dibujar los glifos).
"""
import hashlib
import io
import json
import re
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import celceta as C  # noqa: E402

ROOT = HERE.parent
OUT = ROOT / "dist" / "release"
TOP = "Celceta-ESP"
REPO = "https://github.com/bmvargas-751/ys-memories-of-celceta-esp"

# Módulos que necesita el instalador (los demás de tools/ son del trabajo de traducción)
TOOLS = ["installer.py", "celceta.py", "arb.py", "dbin.py", "falcom.py", "itf.py", "records.py",
         "tables.py", "tbb.py", "ys7scp.py", "LICENSE"]
DOCS = ["LICENSE.md"]


def sha(data):
    return hashlib.sha256(data).hexdigest()



# ---------- datos derivados y comprobación ----------

def make_data(stage):
    """Escribe stage/data/ y comprueba que el instalador arma lo mismo que celceta.py import."""
    import font_es
    import itf
    import installer as I
    data = stage / "data"
    data.mkdir(parents=True)
    f = itf.ITF((C.GAME / I.FONT).read_bytes())
    glyphs = {ch: {"w": g.w, "h": g.h, "yoff": g.yoff, "xoff": g.xoff, "adv": g.adv, "px": g.px}
              for ch, g in font_es.make(f).items()}
    (data / "fuente_es.json").write_text(json.dumps(glyphs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # 1) armado de referencia, el del adaptador
    print("armando con celceta.py import...")
    ref = Path(tempfile.mkdtemp(prefix="celceta-ref-"))
    out = Path(tempfile.mkdtemp(prefix="celceta-inst-"))
    try:
        C.BUILD = ref
        C.do_import()
        # 2) armado del instalador, con los datos recién escritos
        print("armando con el instalador...")
        I.GLYPHS = data / "fuente_es.json"
        I.build(C.GAME, out)
        orig_game = C.LOCAL / "celceta"
        refs = {p.relative_to(ref).as_posix(): p for p in ref.rglob("*") if p.is_file()}
        outs = {p.relative_to(out).as_posix(): p for p in out.rglob("*") if p.is_file()}
        extra = set(refs) - set(outs)
        if extra:
            raise SystemExit(f"El instalador no arma {len(extra)} archivos del adaptador, p. ej. {sorted(extra)[0]}")
        diff = [r for r in refs if refs[r].read_bytes() != outs[r].read_bytes()]
        if diff:
            raise SystemExit(f"{len(diff)} archivos salen distintos del adaptador, p. ej. {diff[0]}")
        changed = {r: sha((orig_game / r).read_bytes()) for r in sorted(outs)
                   if outs[r].read_bytes() != (orig_game / r).read_bytes()}
    finally:
        shutil.rmtree(ref, ignore_errors=True)
        shutil.rmtree(out, ignore_errors=True)
    (data / "originales.json").write_text(json.dumps(changed, indent=0, sort_keys=True), encoding="utf-8")
    print(f"comprobado: el instalador arma lo mismo que el adaptador; {len(changed)} archivos cambian")
    return changed


# ---------- paquetes ----------

def readme(version, windows):
    launch = "install.bat" if windows else "install.sh"
    remove = "uninstall.bat" if windows else "uninstall.sh"
    other = ('   install.bat --game "RUTA DEL JUEGO"' if windows else
             '   ./install.sh --game "RUTA DEL JUEGO"')
    need = ("  0. Hace falta Python 3.8 o superior. Si no lo tienes, descárgalo de\n"
            "     https://www.python.org/downloads/ y, al instalarlo, marca \"Add python.exe to PATH\".\n"
            if windows else
            "  0. Hace falta python3 (3.8 o superior). En Steam Deck y casi todas las distros ya viene.\n")
    deck = "" if windows else (
        "     En Steam Deck: en modo escritorio, abre esta carpeta, clic derecho en install.sh >\n"
        "     Ejecutar en terminal (o desde una terminal: ./install.sh).\n")
    return f"""YS: MEMORIES OF CELCETA — TRADUCCIÓN AL ESPAÑOL {version}
Traducción no oficial, hecha por fans. No incluye el juego: se arma con TU copia de Steam.

INSTALAR
{need}  1. Lo más fácil: deja esta carpeta ({TOP}) DENTRO de la carpeta del juego, junto a
     "lang" y "Ysc_dx11.exe". En Steam: clic derecho en el juego > Administrar >
     Explorar archivos locales.
     Si la dejas en otro lugar, el instalador busca el juego en tus bibliotecas de Steam.
  2. Ejecuta {launch}.
{deck}  3. Abre el juego con el idioma en inglés (English): el texto aparece en español.

  Si no encuentra el juego, indica la ruta a mano desde una terminal en esta carpeta:
{other}

DESINSTALAR
  Ejecuta {remove}. Devuelve los archivos originales del juego.
  No borres esta carpeta antes de desinstalar: en backup/ están los originales.
  Si algo quedó mal: en Steam, Propiedades > Archivos instalados > Verificar integridad.

Si el juego se actualiza, Steam pisa la traducción: vuelve a ejecutar {launch}.
Errores y comentarios (sin spoilers): {REPO}/issues
Licencias: ver LICENSE.md y tools/LICENSE.
"""


BAT = """@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PY="
py -3 -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1 && set "PY=python"
if not defined PY goto nopython
%PY% "%~dp0tools\\installer.py" {cmd} --pause %*
exit /b
:nopython
echo Hace falta Python 3.8 o superior y no lo encuentro.
echo Descargalo de https://www.python.org/downloads/
echo Al instalarlo, marca la casilla "Add python.exe to PATH" y vuelve a ejecutar este archivo.
pause
exit /b 1
"""
SH = """#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
if ! python3 -c "import sys; sys.exit(sys.version_info < (3, 8))" 2>/dev/null; then
  echo "Hace falta python3 (3.8 o superior). En Steam Deck ya viene; en otras distros, instálalo con tu gestor de paquetes."
  read -r -p "Pulsa Enter para cerrar..." _
  exit 1
fi
python3 tools/installer.py {cmd} --pause "$@"
"""


def common_files(version, windows, stage):
    """(ruta dentro del paquete, bytes, ejecutable)."""
    files = [(f"tools/{t}", (HERE / t).read_bytes(), False) for t in TOOLS]
    for p in sorted((ROOT / "translation").rglob("*")):
        if p.is_file():
            files.append((p.relative_to(ROOT).as_posix(), p.read_bytes(), False))
    for p in sorted((stage / "data").iterdir()):
        files.append((f"data/{p.name}", p.read_bytes(), False))
    for d in DOCS:
        files.append((d, (ROOT / d).read_bytes(), False))
    text = readme(version, windows)
    files.append(("LEEME.txt", (text.replace("\n", "\r\n") if windows else text).encode("utf-8"), False))
    return files



def build_windows(version, stage):
    out = OUT / f"{TOP}-{version}-windows.zip"
    files = common_files(version, True, stage)
    files.append(("install.bat", BAT.format(cmd="install").replace("\n", "\r\n").encode(), False))
    files.append(("uninstall.bat", BAT.format(cmd="uninstall").replace("\n", "\r\n").encode(), False))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data, _ in files:
            z.writestr(f"{TOP}/{name}", data)
    return out, len(files)


def build_linux(version, stage):
    out = OUT / f"{TOP}-{version}-linux.tar.gz"
    files = common_files(version, False, stage)
    files.append(("install.sh", SH.format(cmd="install").encode(), True))
    files.append(("uninstall.sh", SH.format(cmd="uninstall").encode(), True))
    with tarfile.open(out, "w:gz", compresslevel=9) as t:
        for name, data, exe in files:
            info = tarfile.TarInfo(f"{TOP}/{name}")
            info.size, info.mode, info.mtime = len(data), 0o755 if exe else 0o644, 0
            t.addfile(info, io.BytesIO(data))
    return out, len(files)


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"v\d+\.\d+\.\d+", sys.argv[1]):
        raise SystemExit("Uso: python3 tools/make_release.py vX.Y.Z")
    version = sys.argv[1]
    OUT.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="celceta-release-"))
    try:
        make_data(stage)
        for build in (build_windows, build_linux):
            path, n = build(version, stage)
            print(f"{path.name}: {n} archivos, {path.stat().st_size / 1e6:.1f} MB\n  sha256 {sha(path.read_bytes())}")
    finally:
        shutil.rmtree(stage, ignore_errors=True)


if __name__ == "__main__":
    main()
