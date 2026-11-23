# Reglas técnicas

Lo que el juego necesita para que el texto no se rompa. Cada regla tiene un número para citarla, y la mayoría la controla `loc.py check` (el chequeo va entre paréntesis). Salen de cómo está hecho el juego, del adaptador y de la sección 8 del encargo: una traducción nunca puede romper el archivo.

Plantilla del kit: los números quedan; lo de cada regla se completa con lo que muestre la prueba técnica de este juego (PLAN, fase 1). Lo que no aplique se borra.

## Códigos y saltos

- **T-1** Los códigos (variables, etiquetas, colores, nombres insertados) quedan intactos y en el mismo orden que en el original. Los reconoce la lista `codes` de `loc.json`. (`codigos`)
  - En Celceta son `#` + número + letra (`#4C`, `#00407F`, `#2M`, `#0B`), de ancho cero. Los del inicio del cuadro (cara `F`, centrado `C`, gesto `M`, voz `V`, tamaño `S`, pausa `W`) no se exportan: el adaptador los quita del texto y los vuelve a poner. Los que quedan en medio (por ejemplo `#0B`, el icono de un botón) van en la traducción tal cual. En la interfaz también hay `#%dA` (el icono del botón cuyo número llega por `%d`) y los `%s`, `%d` de `printf`; todos van intactos y en el mismo orden. Los textos sin letras («???», «...») no se exportan.
- **T-2** Saltos de línea: los fijos (`fixed_break` en `loc.json`) van exactamente donde están en el original, ni más ni menos. Los demás, si el adaptador parte los renglones, los pone el adaptador. (`saltos`)
  - En Celceta no hay saltos fijos: los cuadros de diálogo y los mensajes se exportan sin saltos y el adaptador los reparte en renglones según el ancho de la fuente. La traducción no lleva saltos. [DECISIONS 2026-11-17]
  - Excepción: los textos de la interfaz (`text/strSystem`, 28 líneas) no se reparten; sus `\n` son saltos fijos (`fixed_break` = `\n`) y van los mismos que en el original. El ancho de la nota es el de todo el texto, y el chequeo de caja cuenta cada `\n` como renglón. [set de oro, 2026-11-18]

## Archivos del juego

El adaptador es `tools/celceta.py` (`export`, `import`, `roundtrip`, `pseudo`). Cubre:

| Clave | Archivo | Formato (módulo) | Qué se traduce |
|---|---|---|---|
| `script/` | `lang/en/script/*.bin` | guiones YS7_SCP (`ys7scp.py`) | diálogos, hablantes, opciones, mensajes |
| `text/` | `lang/en/text/*.tbb` | tablas planas (`tbb.py`, `tables.py`) | objetos, materiales, bestiario, diario, misiones, recuerdos, mapas, manual |
| `text/skill`, `text/warpdata` | `lang/en/text/*.tbb` | registros fijos comprimidos con FALCOM3 (`records.py`, `falcom.py`) | habilidades y destinos |
| `text/strSystem` | `lang/en/text/strSystem.dbin` | pares ID / texto (`dbin.py`) | interfaz |
| `map/` | `lang/en/map/*/*.arb` | mapas YS7_ARG (`arb.py`) | nombres de PNJ, habilidades de campo, monstruos de misión |
| — | `lang/en/system/font.itf` | fuente (`itf.py`, `font_es.py`) | letras españolas |

Exportar e importar sin cambios da los mismos archivos, byte por byte (`roundtrip`).

### Imágenes con texto

Se editan a mano [DECISIONS 2026-11-17]. `tools/images.py export` deja los originales en PNG en `../local/ys-memories-of-celceta/imagenes/en/`; los editados van en `imagenes/es/` con el mismo nombre y tamaño, y `tools/celceta.py import` (o `images.py import`) los convierte a ITP en `build/`. Formato ITP según Cradle (`tools/itp.py`): 32 bits sin compresión, o 256 colores con FALCOM3 y mosaicos de 32×32; si los colores nuevos no están en la paleta, se usa el más cercano o una paleta nueva, lo que se aleje menos.

| Grupo | Archivos | Texto |
|---|---|---|
| `lang/en/visual/mapname/` | 39 | nombres de zona (los mismos de `text/mapname`) |
| `lang/en/visual/bossname/` | 20 | título del jefe; el nombre propio queda |
| `system/ti_icon.itp` | 1 | menú de título |
| `system/system01.itp`, `system/emotion.itp` | 2 | combate (Guard, Miss…) y globos (TALK, SHOP, QUEST) |
| `lang/en/system/menu_mt1-4.itp`, `menucom.itp` | 5 | etiquetas y cabeceras de los menús |
| `lang/en/visual/topic_*.itp` | 58 | tutoriales (al final) [DECISIONS 2026-11-17] |

`system/` no está dentro de `lang/en`: lo comparten los dos idiomas del juego.

## Espacio

Anchos máximos medidos en el inglés, en unidades de la fuente (`tools/celceta.py`, `WIDTH`): cuadro con retrato 960, sin retrato 1100, narración centrada 1500, mensaje del sistema 1300. Cuadros de diálogo: hasta 3 renglones. En el juego (2026-11-17): los cuadros sin retrato caben con un 10–14 % de margen y los con retrato admiten unas 1000 unidades. Los textos de interfaz llevan como límite el ancho del original: el aviso no obliga a recortar (T-3), pero los que van anclados a la derecha (avisos de acción) o junto a otro elemento (cabeceras, columnas de «Records») se salen si son mucho más largos.

- **T-3** La caja: ningún renglón puede pasar del ancho que permite el juego. Si el límite medido es el del original y no el de la pantalla, el aviso no obliga a recortar: se permiten abreviaturas reconocibles, pero nunca se quitan palabras ni se acorta de forma que se pierda el sentido. Si la forma completa no cabe, va completa y con su aviso, y se revisa en el juego. [IVA] (chequeo del proyecto, en `hooks`)
- **T-4** Los textos con largo máximo en bytes (`max` en el lote) no pueden pasarlo: es un límite duro. (`bytes`)
  - En Celceta, cada letra ASCII ocupa 1 byte y cada letra española 2 (Shift-JIS). Solo `skill` y `warpdata` tienen límite de bytes (campos de largo fijo): nombre de habilidad 31, descripción 63, destino 63. Lo demás puede crecer.

## Caracteres

- **T-5** Solo se usan caracteres que tiene la fuente del juego. (`caracteres`)
  - El juego usa Shift-JIS, que no tiene letras españolas. `tools/font_es.py` las agrega a `lang/en/system/font.itf` (á é í ó ú ü ñ, sus mayúsculas, ¿ ¡), armadas con los glifos del juego, en la fila 9 de JIS (`0x8540`–`0x854F`), y el adaptador las escribe con esos códigos. Comillas y apóstrofo: los rectos de ASCII (`"` y `'`), como el inglés.

## Qué se traduce

- **T-6** Lo que no se traduce ni cuenta (restos sin localizar, textos de prueba) va en `excluded` de `loc.json`.
  - En Celceta: el menú de depuración (`script/test`).
- **T-7** Solo se traducen los textos que ve el jugador. Los nombres internos (archivos, etiquetas) no se exportan y no se tocan.
  - En los guiones se exportan: cuadros de diálogo (`TalkMes`), nombre del hablante (`SetName`), opciones (`MenuAdd`), mensajes (`Message`, `Message2`) y el texto antes del objeto obtenido (`GetItemMessageExPlus`). El id interno del hablante (`DUREN`, `Man_A`) no se toca.
- **T-8** Toda línea del lote se traduce completa: ninguna queda vacía, igual al original ni con frases del original mezcladas. (`vacia`, `sin_traducir`, `ingles_mezclado`)
