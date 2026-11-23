# Ys: Memories of Celceta en español

Traducción fan al español neutro de *Ys: Memories of Celceta*, basada en la versión oficial en inglés, para Steam (Windows, Linux y Steam Deck), con la terminología de la traducción oficial de *Ys Origin*.
Las imágenes con texto (nombres de zonas y jefes, etiquetas de los menús y tutoriales) permanecen, por ahora, en inglés.

> Proyecto de fans, sin relación con Nihon Falcom ni con XSEED Games. **No incluye el juego**: el instalador arma la traducción a partir de tu propia copia.

## Instalar

<!-- loc:install -->
Necesitas tu propia copia del juego en Steam, con el idioma en inglés, y Python 3.8 o superior (en Windows, descárgalo de [python.org](https://www.python.org/downloads/) y, al instalarlo, marca **Add python.exe to PATH**; en Linux y Steam Deck ya viene instalado).

**Windows:**

1. Descarga **Celceta-ESP-…-windows.zip** de la [última versión](https://github.com/bmvargas-751/ys-memories-of-celceta-esp/releases/latest).
2. Descomprímelo dentro de la carpeta del juego (junto a `lang` y `Ysc_dx11.exe`). Para abrirla: en Steam, clic derecho en el juego > **Administrar** > **Explorar archivos locales**. Si lo descomprimes en otro lugar, el instalador busca el juego en tus bibliotecas de Steam.
3. En la carpeta **Celceta-ESP**, haz doble clic en **install.bat**.
4. Abre el juego con el idioma en inglés: el texto aparece en español.

<details>
<summary>Linux y Steam Deck</summary>

1. Descarga **Celceta-ESP-…-linux.tar.gz** de la [última versión](https://github.com/bmvargas-751/ys-memories-of-celceta-esp/releases/latest) y descomprímelo dentro de la carpeta del juego (en Steam, clic derecho en el juego > **Administrar** > **Explorar archivos locales**).
2. En la carpeta **Celceta-ESP**, ejecuta **install.sh**. En Steam Deck, en modo escritorio: clic derecho en install.sh > **Ejecutar en terminal**.
3. Abre el juego con el idioma en inglés: el texto aparece en español.

</details>

<details>
<summary>Desinstalar, o si el juego se actualiza</summary>

1. El instalador guarda los archivos originales en `Celceta-ESP/backup/`: no borres esa carpeta antes de desinstalar.
2. Para desinstalar, ejecuta **uninstall.bat** (Windows) o **uninstall.sh** (Linux): devuelve los archivos originales. Si algo quedó mal, en Steam: **Propiedades** > **Archivos instalados** > **Verificar integridad de los archivos del juego**.
3. Si Steam actualiza el juego, la traducción se pierde: vuelve a ejecutar el instalador. Si los archivos del juego cambiaron, te avisa antes de seguir.

</details>
<!-- /loc:install -->

## Avance

<!-- loc:progress -->
Versión 0.9.0, publicada el 20 nov 2026 · [Cambios](CHANGELOG.md)\
Etapa: Prueba en el juego · actualizado el 23 nov 2026

| Sección | Líneas | Traducidas | Avance |
|---|---:|---:|---:|
| Interfaz | 757 | 757 | 100,0 % |
| Objetos y equipo | 1.381 | 1.381 | 100,0 % |
| Criaturas | 338 | 338 | 100,0 % |
| Lugares | 237 | 237 | 100,0 % |
| Historia | 14.602 | 14.602 | 100,0 % |
| Secundarias | 779 | 779 | 100,0 % |

**Propio de este juego**

| Sección | Líneas | Traducidas | Avance |
|---|---:|---:|---:|
| Personajes y PNJ | 929 | 929 | 100,0 % |

**Total: 19.023 de 19.023 líneas (100,0 %)**
<!-- /loc:progress -->

## Documentación

<!-- loc:docs -->
Localización: [Glosario](GLOSSARY.md) · [Personajes](characters/) · [Estilo](STYLE.md) · [Decisiones](DECISIONS.md)\
Desarrollo: [Plan](PLAN.md) · [Técnica](TECH.md) · [Herramientas](tools/README.md) · [Pendientes](PENDING.md)
<!-- /loc:docs -->

## Problemas frecuentes

- **«No encuentro el juego»**: indica la ruta a mano desde una terminal en la carpeta `Celceta-ESP`: `install.bat --game "RUTA"` (Windows) o `./install.sh --game "RUTA"` (Linux).
- **«Hace falta Python»**: instálalo como dice arriba y vuelve a ejecutar el instalador.
- **Windows muestra un aviso de seguridad** al ejecutar el `.bat`: es normal con archivos descargados; el código está en este repositorio.
- **Un texto raro, cortado o con un error**: dinos dónde pasó, sin spoilers, en [Issues](https://github.com/bmvargas-751/ys-memories-of-celceta-esp/issues).

Licencias: [LICENSE.md](LICENSE.md).
