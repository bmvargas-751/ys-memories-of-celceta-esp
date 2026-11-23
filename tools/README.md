# Herramientas

Las herramientas propias de Ys: Memories of Celceta. Las del kit (lotes, validador, avance) están en `~/.claude/loc-kit/tools/loc.py`. Licencia: [MIT](LICENSE).

## Armar los paquetes

`python3 tools/make_release.py vX.Y.Z` deja en `dist/release/` los dos paquetes (Windows y Linux). Necesita la copia local del juego y PIL (solo para dibujar las letras españolas de la fuente), y comprueba antes que el instalador arma lo mismo que `tools/celceta.py import`.

## Los scripts

| Script | Qué hace |
|---|---|
| `celceta.py` | Adaptador del juego para el kit: exporta el texto e importa la traducción a `build/` |
| `installer.py` | El instalador que va en los paquetes (`install.bat`, `install.sh` y la desinstalación) |
| `make_release.py` | Arma los paquetes de una versión |
| `gametest.py` | Prueba en el juego: copia `build/` a la instalación de Steam y la deshace |
| `font_es.py`, `itf.py` | Las letras españolas de la fuente (`font.itf`) |
| `images.py`, `itp.py` | Imágenes con texto: ITP a PNG para editar, y de vuelta |
| `ys7scp.py` | Guiones (`script/*.bin`) |
| `dbin.py`, `tbb.py`, `records.py`, `tables.py` | Interfaz (`strSystem.dbin`) y tablas de texto (`text/*.tbb`) |
| `arb.py` | Nombres visibles de los mapas (`map/*/*.arb`) |
| `falcom.py` | Compresión de Falcom (FALCOM2 / FALCOM3) |
| `hooks.py` | Chequeos propios para `loc.py` |
