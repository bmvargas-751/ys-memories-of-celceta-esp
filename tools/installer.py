#!/usr/bin/env python3
"""Instalador de la traducción al español de Ys: Memories of Celceta (Steam).
Funciona igual en Windows y en Linux (Steam Deck incluida).

  python3 tools/installer.py install     arma la traducción con tu copia del juego y la instala
  python3 tools/installer.py uninstall   quita la traducción y devuelve los archivos originales
  python3 tools/installer.py status      muestra qué hay instalado

Opciones: --game RUTA  carpeta del juego (si no se indica, se busca sola: primero la carpeta
                       donde está este paquete y luego las bibliotecas de Steam)
          --force      sigue aunque los archivos del juego no sean los que se tradujeron
          --pause      espera un Enter al terminar (para cuando se abre con doble clic)

Solo usa la biblioteca estándar de Python. No trae archivos del juego: los textos se
arman sobre tu copia, y los originales se guardan antes en la carpeta backup/ del paquete.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import celceta as C  # noqa: E402
import itf  # noqa: E402

ROOT = HERE.parent  # raíz del paquete (o del repositorio)
GAME_NAME = "Ys Memories of Celceta"
BACKUP = ROOT / "backup"
INSTALLED = BACKUP / "installed.sha256"   # hashes de los archivos que instalamos nosotros
ORIGINALS = ROOT / "data" / "originales.json"   # ruta → sha256 de los originales traducidos
GLYPHS = ROOT / "data" / "fuente_es.json"       # las letras españolas de la fuente
FONT = "lang/en/system/font.itf"
READS = ("lang/en/script", "lang/en/text", "lang/en/map")  # carpetas que lee el armado


class Fail(Exception):
    pass


def say(msg=""):
    print(msg, flush=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- dónde está el juego ----------

def steam_roots():
    """Carpetas de Steam conocidas, según el sistema."""
    home = Path.home()
    roots = []
    if sys.platform == "win32":
        try:
            import winreg
            for hive, key, value in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                                     (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath")):
                try:
                    with winreg.OpenKey(hive, key) as k:
                        roots.append(Path(winreg.QueryValueEx(k, value)[0]))
                except OSError:
                    pass
        except ImportError:
            pass
        for env in ("ProgramFiles(x86)", "ProgramFiles"):
            if os.environ.get(env):
                roots.append(Path(os.environ[env]) / "Steam")
    else:
        roots += [home / ".local/share/Steam", home / ".steam/steam", home / ".steam/root",
                  home / ".var/app/com.valvesoftware.Steam/.local/share/Steam"]
        for drive in ("c", "d"):  # WSL
            roots += [Path(f"/mnt/{drive}/Steam"), Path(f"/mnt/{drive}/Program Files (x86)/Steam")]
    return roots


def libraries(root):
    """La carpeta de Steam más las bibliotecas extra que lista libraryfolders.vdf."""
    libs = [root]
    for vdf in (root / "steamapps/libraryfolders.vdf", root / "config/libraryfolders.vdf"):
        if vdf.exists():
            text = vdf.read_text(encoding="utf-8", errors="replace")
            libs += [Path(p.replace("\\\\", "\\")) for p in re.findall(r'"path"\s+"([^"]+)"', text)]
    return libs


def is_game(path):
    p = Path(path)
    return (p / FONT).is_file() and (p / "lang/en/script").is_dir()


def find_game(arg):
    if arg:  # una ruta dada a mano se usa o se rechaza, sin buscar otra
        if is_game(arg):
            return Path(arg)
        raise Fail(f"En «{arg}» no está el juego (falta {FONT}). Indica la carpeta que tiene lang, system y Ysc_dx11.exe.")
    candidates = []
    if os.environ.get("CELCETA_GAME_DIR"):
        candidates.append(Path(os.environ["CELCETA_GAME_DIR"]))
    candidates += [ROOT, ROOT.parent, ROOT.parent.parent]  # paquete dentro de la carpeta del juego
    for root in steam_roots():
        for lib in libraries(root):
            candidates.append(lib / "steamapps" / "common" / GAME_NAME)
    for c in candidates:
        if is_game(c):
            return c
    raise Fail("No encuentro el juego. Descomprime esta carpeta dentro de la carpeta del juego, "
               "o indica la ruta con:  --game \"RUTA\"\n"
               "(En Steam: clic derecho en el juego > Administrar > Explorar archivos locales.)")


# ---------- respaldo ----------

def backup_dirs(game):
    """Respaldos donde buscar originales: el de este paquete y los de otros paquetes junto al juego
    (si se descomprime una versión nueva en otra carpeta, el respaldo de la anterior sigue sirviendo)."""
    dirs = [BACKUP]
    for base in (game, ROOT.parent):
        try:
            dirs += sorted(p / "backup" for p in Path(base).iterdir() if (p / "backup" / "installed.sha256").is_file())
        except OSError:
            pass
    seen, out = set(), []
    for d in dirs:
        if d.resolve() not in seen:
            seen.add(d.resolve())
            out.append(d)
    return out


def read_installed(game):
    found = set()
    for d in backup_dirs(game):
        f = d / "installed.sha256"
        if f.exists():
            found |= set(f.read_text().split())
    return found


def find_original(game, rel, want, installed):
    """Original de un archivo: solo uno que sea el original conocido, o uno guardado que no sea nuestro."""
    for d in backup_dirs(game):
        f = d / rel
        if f.exists() and sha256(f) == want:
            return f
    f = BACKUP / rel  # un original distinto, guardado con --force
    if f.exists() and sha256(f) not in installed:
        return f
    return None


# ---------- armado ----------

def load_originals():
    if not ORIGINALS.exists():
        raise Fail(f"Falta {ORIGINALS.relative_to(ROOT)}: el paquete está incompleto.")
    return json.loads(ORIGINALS.read_text(encoding="utf-8"))


def build_font(src, dst):
    f = itf.ITF(src.read_bytes())
    for ch, g in json.loads(GLYPHS.read_text(encoding="utf-8")).items():
        i = itf.index(C.ES_MAP[ch])
        if f.raw[i]:
            raise Fail(f"La fuente de tu juego ya tiene algo en la casilla de «{ch}»: no es la que se tradujo.")
        f.set_glyph(i, itf.Glyph(g["w"], g["h"], g["yoff"], g["xoff"], g["adv"], g["px"]))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(f.build())


def build(orig_dir, out_dir):
    """Arma en out_dir los archivos traducidos a partir de los originales de orig_dir."""
    C.GAME = orig_dir
    C.TRANSLATION = ROOT / "translation"
    C._VOCAB = None
    build_font(orig_dir / FONT, out_dir / FONT)
    font = C.Font(out_dir / FONT)
    tr = C.load_translation()
    C.build_scripts(tr, font, out_dir)
    C.build_tables(tr, font, out_dir)
    C.build_system(tr, out_dir)
    C.build_records(tr, out_dir)
    C.build_maps(tr, out_dir)


def cmd_install(args):
    game = find_game(args.game)
    say(f"Juego: {game}")
    originals = load_originals()
    installed = read_installed(game)
    sources, bad = {}, []
    say("1/3 Revisando los archivos del juego...")
    for rel, want in originals.items():
        cur = game / rel
        if not cur.is_file():
            raise Fail(f"Falta en el juego: {rel}. En Steam: Propiedades > Archivos instalados > Verificar integridad.")
        h = sha256(cur)
        if h in installed:  # ya tiene la traducción: el inglés sale del respaldo
            orig = find_original(game, rel, want, installed)
            if orig is None:
                raise Fail(f"Falta el respaldo del original de {rel}. En Steam: Propiedades > Archivos instalados > "
                           "Verificar integridad, y vuelve a instalar.")
            sources[rel] = orig
            h = sha256(orig)
        else:
            sources[rel] = cur
        if h != want:
            bad.append(rel)
    if bad:
        say(f"AVISO: {len(bad)} archivos no son los originales que se tradujeron (p. ej. {bad[0]}). Puede ser por:")
        say("       - una actualización del juego en Steam, o")
        say("       - una traducción instalada desde otra carpeta, cuyo respaldo no encuentro.")
        say("       Lo más seguro: en Steam, Propiedades > Archivos instalados > Verificar integridad, y reintenta.")
        if not args.force:
            if not sys.stdin.isatty() or input("¿Continuar de todos modos? [s/N] ").strip().lower() not in ("s", "si", "sí", "y"):
                raise Fail("Cancelado. Con --force sigue sin preguntar.")
    work = Path(tempfile.mkdtemp(prefix="celceta-es-"))
    try:
        say("2/3 Armando la traducción con tus archivos (tarda un poco)...")
        orig_dir, out_dir = work / "orig", work / "es"
        for sub in READS:  # lo que el armado lee aunque no cambie (p. ej. nombres del grupo)
            if (game / sub).is_dir():
                shutil.copytree(game / sub, orig_dir / sub, dirs_exist_ok=True)
        for rel, src in sources.items():  # y encima, los originales de lo que se traduce
            dst = orig_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        build(orig_dir, out_dir)
        say("3/3 Instalando...")
        BACKUP.mkdir(exist_ok=True)
        n = 0
        for rel in originals:
            cur, new = game / rel, out_dir / rel
            if not new.exists() or sha256(new) == originals[rel]:
                continue
            if sha256(cur) not in installed:  # lo que hay es el original: se respalda antes de pisarlo
                bak = BACKUP / rel
                if sha256(cur) == originals[rel] or not bak.exists():
                    bak.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(cur, bak)
            shutil.copyfile(new, cur)
            installed.add(sha256(new))
            n += 1
        INSTALLED.write_text("\n".join(sorted(installed)) + "\n")
        say(f"  {n} archivos instalados (originales en {BACKUP}).")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    say("\nListo. Abre el juego con el idioma en inglés (English) y verás el texto en español.")
    say("Para quitarla: ejecuta el desinstalador. No borres esta carpeta: ahí está el respaldo.")


def cmd_uninstall(args):
    game = find_game(args.game)
    say(f"Juego: {game}")
    originals = load_originals()
    installed = read_installed(game)
    restored = kept = 0
    for rel, want in originals.items():
        cur = game / rel
        if cur.is_file() and sha256(cur) in installed:
            orig = find_original(game, rel, want, installed)
            if orig is None:
                say(f"  sin respaldo: {rel}")
                kept += 1
                continue
            shutil.copyfile(orig, cur)
            restored += 1
    say(f"{restored} archivos restaurados.")
    if kept:
        say(f"{kept} archivos no tenían respaldo: en Steam, Propiedades > Archivos instalados > Verificar integridad.")
    else:
        say("Si algo quedó mal, en Steam: Propiedades > Archivos instalados > Verificar integridad.")


def cmd_status(args):
    game = find_game(args.game)
    say(f"Juego: {game}")
    originals = load_originals()
    installed = read_installed(game)
    count = {"traducción instalada": 0, "original": 0, "distinto (¿actualización?)": 0, "falta": 0}
    for rel, want in originals.items():
        cur = game / rel
        if not cur.is_file():
            count["falta"] += 1
            continue
        h = sha256(cur)
        if h in installed:
            count["traducción instalada"] += 1
        elif h == want:
            count["original"] += 1
        else:
            count["distinto (¿actualización?)"] += 1
    for k, v in count.items():
        if v:
            say(f"  {k}: {v} archivos")


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["install", "uninstall", "status"])
    ap.add_argument("--game")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pause", action="store_true")
    args = ap.parse_args()
    code = 0
    try:
        {"install": cmd_install, "uninstall": cmd_uninstall, "status": cmd_status}[args.cmd](args)
    except Fail as e:
        say(f"\nError: {e}")
        code = 1
    except KeyboardInterrupt:
        say("\nCancelado.")
        code = 1
    if args.pause:
        try:
            input("\nPulsa Enter para cerrar...")
        except EOFError:
            pass
    sys.exit(code)


if __name__ == "__main__":
    main()
