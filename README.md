# Ys: Memories of Celceta: traducción al español

Traducción fan al español neutro de *Ys: Memories of Celceta* (versión de Steam), hecha desde el inglés oficial, con la terminología de la traducción oficial de *Ys Origin*. El repo tiene solo la traducción, los documentos y las herramientas propias: ningún archivo del juego.

> Es un proyecto de fans, sin relación con los dueños del juego. **No incluye el juego ni sus archivos**: necesitas tu propia copia en Steam.

- Método y decisiones: [PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md)
- Estilo y términos: [STYLE.md](STYLE.md), [GLOSSARY.md](GLOSSARY.md), [characters/](characters)
- Técnica: [TECH.md](TECH.md)
- Pendientes: [PENDING.md](PENDING.md)
- Licencias: [LICENSE.md](LICENSE.md)

## Instalar

La traducción reemplaza el texto en **inglés** del juego. Se arma con *tus* archivos del juego, y se puede quitar cuando quieras. Funciona en **Windows** y en **Linux / Steam Deck**.

1. Hace falta **Python 3.8 o superior**:
   - Windows: descárgalo de [python.org](https://www.python.org/downloads/) y, al instalarlo, marca *Add python.exe to PATH*.
   - Linux y Steam Deck: ya viene instalado.
2. Descarga el paquete de tu sistema desde la [última versión](https://github.com/bmvargas-751/ys-memories-of-celceta-esp/releases/latest):
   - Windows: `Celceta-ESP-…-windows.zip`
   - Linux y Steam Deck: `Celceta-ESP-…-linux.tar.gz`
3. Descomprímelo, mejor **dentro de la carpeta del juego** (junto a `lang` y `Ysc_dx11.exe`). Te queda una carpeta `Celceta-ESP`.
   Para abrir la carpeta del juego: en Steam, clic derecho en el juego > *Administrar* > *Explorar archivos locales*.
   Si lo descomprimes en otro lugar, el instalador busca el juego en tus bibliotecas de Steam.
4. Ejecuta el instalador de esa carpeta:
   - Windows: doble clic en **`install.bat`**.
   - Linux: **`install.sh`**. En Steam Deck, en modo escritorio: clic derecho en `install.sh` > *Ejecutar en terminal* (o `./install.sh` desde una terminal).
5. Abre el juego con el idioma en inglés: el texto aparece en español.

El instalador guarda antes los archivos originales en `Celceta-ESP/backup/`. Si descomprimes una versión nueva en otra carpeta junto al juego, reutiliza ese respaldo.

### Desinstalar

Ejecuta **`uninstall.bat`** (Windows) o **`uninstall.sh`** (Linux): devuelve los archivos originales. No borres la carpeta `Celceta-ESP` antes de desinstalar, porque ahí está el respaldo.
Si algo quedó mal, en Steam: *Propiedades > Archivos instalados > Verificar integridad de los archivos del juego*.

### Si el juego se actualiza

Steam reemplaza los archivos y la traducción se pierde: vuelve a ejecutar el instalador. Si los archivos del juego cambiaron, el instalador te avisa antes de seguir.

### Problemas frecuentes

- **"No encuentro el juego"**: indica la ruta a mano desde una terminal en la carpeta `Celceta-ESP`: `install.bat --game "RUTA"` (Windows) o `./install.sh --game "RUTA"` (Linux).
- **"Hace falta Python"**: instálalo como en el paso 1 y vuelve a ejecutar el instalador.
- **Windows muestra un aviso de seguridad** al ejecutar el `.bat`: es normal con archivos descargados; el código está en este repositorio.
- **Un texto raro, cortado o con un error**: dinos dónde pasó, sin spoilers, en [Issues](https://github.com/bmvargas-751/ys-memories-of-celceta-esp/issues).

### Armar los paquetes

`python3 tools/make_release.py vX.Y.Z` deja en `dist/release/` los dos paquetes. Necesita la copia local del juego y PIL (solo para dibujar las letras españolas de la fuente), y comprueba antes que el instalador arma lo mismo que `tools/celceta.py import`.

## Avance

Actualizado: 2026-11-20.

### Fases

| Fase | Estado |
|---|---|
| 0. Decisiones | ✅ inglés oficial de Steam; terminología de *Ys Origin* |
| 1. Prueba técnica | ✅ adaptador, fuente con tildes y ñ, ida y vuelta idéntica y prueba en el juego |
| 2. Inventario y costo | ✅ 19 039 líneas por traducir en 63 lotes, ~11 M tokens estimados |
| 3. Glosario y fichas | ✅ 159 términos y 7 personajes |
| 4. Set de oro | ✅ 17 de 17 (oro-007) |
| 5. Piloto | ✅ 5 lotes de 40 líneas, uno por sección |
| 6. Traducción | ✅ 19 023 líneas en todas las secciones; delicadas y pendientes decididos |
| 7. Prueba en el juego | ⬜ |
| 8. Entrega (instalador para Windows y Steam Deck) | ⏳ instalador listo; versión de prueba v0.9.0 |

### Secciones

<!-- loc:progress -->
**Etapa actual:** Fase 6. Traducción: Guiones

| Sección | Líneas | Traducidas | Avance |
|---|---:|---:|---:|
| Interfaz | 994 | 994 | 100,0 % |
| Objetos, materiales y habilidades | 1.381 | 1.381 | 100,0 % |
| Bestiario, nombres y PNJ | 1.267 | 1.267 | 100,0 % |
| Diario, misiones y recuerdos | 779 | 779 | 100,0 % |
| Guiones | 14.602 | 14.602 | 100,0 % |
| **Total** | **19.023** | **19.023** | **100,0 %** |
<!-- /loc:progress -->
