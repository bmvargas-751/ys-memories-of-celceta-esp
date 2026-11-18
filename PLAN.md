# Plan

## Decisiones

Se cierran en la fase 0, porque son caras de cambiar después.

- **Variante:** español neutro (*tú*/*ustedes*, sin regionalismos de ningún país).
- **Original:** inglés oficial de la versión de Steam (`lang/en`), para que los subtítulos coincidan con las voces en inglés. [DECISIONS 2026-11-17]
- **Otra versión de apoyo:** el japonés del mismo juego (`lang/ja`), solo para género, sujeto omitido y trato (E-1). [DECISIONS 2026-11-17]
- **Terminología oficial:** la traducción oficial al español de *Ys Origin* (G-1). [DECISIONS 2026-11-17]
- **Tono:** el de *Ys Origin* en español, adaptado a español neutro (E-24). [DECISIONS 2026-11-17]
- **Pruebas:** la versión de Steam en Windows y en Steam Deck / Linux, con un instalador multiplataforma que arma la traducción con la copia de cada persona. [DECISIONS 2026-11-17]
- **Sin spoilers:** los documentos, los commits y el chat nombran zonas o archivos, nunca hechos de la historia.
- **Contenido del repo:** solo la traducción y las herramientas propias; nunca archivos del juego.

## Fases

### Fase 0. Antes de empezar

- [x] Cerrar las decisiones de arriba con el usuario.
- [x] Revisar con el usuario la base de STYLE.md: lo que no aplique se borra. (Se dejan todas, 2026-11-17.)

### Fase 1. Prueba técnica

Antes de esto no se decide nada más.

- [x] Extraer los archivos del juego, a una carpeta fuera del repo. (`../ys-memories-of-celceta-esp-local/celceta/`, 2026-11-17.)
- [x] Adaptador: exportar el texto al formato común (`source` de `loc.json`) e importarlo de vuelta. (`tools/celceta.py`, 19 374 textos; imágenes con `tools/images.py`, 2026-11-17.)
- [x] Ida y vuelta idéntica: exportar e importar sin cambios da los mismos archivos. (`tools/celceta.py roundtrip`, 2026-11-17.)
- [x] Caracteres: si la fuente tiene las letras españolas, o cómo se agregan (T-5). (No las tiene; `tools/font_es.py` las agrega. Probado en el juego, 2026-11-17.)
- [x] Límites: bytes, ancho y renglones de cada tipo de texto (T-3, T-4), y sus chequeos en `hooks`. Los cuadros de diálogo van con reflujo automático, hasta 3 renglones. [DECISIONS 2026-11-17] (`tools/hooks.py`; ver TECH.md.)
- [x] Pseudolocalización: todo el texto más largo y con letras españolas, en el juego, para ver cortes y glifos que faltan. (`tools/gametest.py`.)
  - 2026-11-17, guiones: las letras españolas se ven bien (sin cortes arriba) y los cuadros sin retrato caben con un 10–14 % de margen.
  - 2026-11-17, todo el texto: funcionan tablas (con filas extra en el diario), habilidades comprimidas, interfaz, nombres de PNJ y la fuente del mapa. Los cuadros con retrato admiten unas 1000 unidades (límite 960). Se corrigieron el pie `STRL` de `strSystem.dbin` y el código `#%dA`. Lo que se sale (cabeceras, avisos a la derecha, valores de «Records») es por el largo de la pseudo y lo marca el chequeo.
- [x] Completar TECH.md y `loc.json` (`codes`, `fixed_break`, `excluded`, `sections`).

### Fase 2. Inventario y presupuesto

- [x] Volumen por sección (`loc.py progress`).
- [x] Costo estimado por sección, antes de empezarla. (2026-11-17; referencia de METHOD.md: 25 000 + 18 000 tokens por agente cada 250 líneas, 4 agentes Sonnet por lote. Las líneas repetidas se traducen una vez.)

| Sección | Líneas | Distintas | Palabras | Lotes | Tokens aprox. |
|---|---:|---:|---:|---:|---:|
| Interfaz | 994 | 747 | 2209 | 3 | 0,5 M |
| Objetos, materiales y habilidades | 1381 | 1015 | 5696 | 5 | 0,9 M |
| Bestiario, nombres y PNJ | 1267 | 633 | 4112 | 3 | 0,5 M |
| Diario, misiones y recuerdos | 795 | 696 | 11 335 | 3 | 0,5 M (líneas largas: hasta ×1,5) |
| Guiones | 14 602 | 12 021 | 124 887 | 49 | 8,4 M |
| **Total** | **19 039** | **15 112** | **148 239** | **63** | **≈ 11 M** |

Aparte: terminólogo, perfilador (Opus), delicadas y las pruebas del set de oro.

### Fase 3. Documentos

- [x] Glosario: el terminólogo propone las filas. (2026-11-18: 158 términos en GLOSSARY.md, 32 oficiales de *Ys Origin* y el resto decididos con el usuario; en PENDING.md solo quedan los nombres de los roos, para delicadas.)
- [x] Fichas de personajes: el perfilador, antes de cada sección. (2026-11-18: el grupo principal y Griselda — Duren, Karna, Ozma, Calilica, Frieda, Leeza, Griselda — con muestras de 300 líneas; género y trato aprobados. Los demás, antes de cada sección.)
- [x] DECISIONS.md y PENDING.md al día.

### Fase 4. Set de oro

Obligatorio: sin él, `loc.py prepare` no arma lotes.

- [x] Elegir con el usuario los casos reales (al menos uno de cada tipo; mejor dos o tres). (2026-11-18: 17 casos en `golden.jsonl`, dos o tres de cada tipo.)
- [x] Aprobarlo (`loc.py golden approve`).
- [x] Probar a los agentes (`loc.py golden prepare`, traductor, revisor y corrector, `loc.py golden score`) hasta que pase. (2026-11-18: pasó `oro-007`, 17 de 17, tras corregir casos, el chequeo de caja, los saltos fijos de `strSystem` y una línea del prompt del traductor (género).)

### Fase 5. Piloto

- [x] Un primer lote de cada tipo de texto con el equipo completo. (2026-11-18: 5 lotes de 40 líneas, uno por sección; 200 líneas y 62 copias idénticas, 0 avisos.)
- [x] Ajustar documentos y roles con lo que salga (y volver a pasar el set de oro si cambia un prompt). (2026-11-18: G-4 para nombres de monstruos, 13 filas nuevas del glosario, marcadores `DIARY_*` excluidos; en el kit, dos falsos positivos del validador. Ningún prompt cambió.)

### Fase 6. Traducción

- [x] Interfaz (994 líneas; 2026-11-18, lotes interfaz-001 a 004).
- [x] Objetos, materiales y habilidades (1381 líneas; 2026-11-18, lotes objetos-…-002 a 005).
- [ ] Bestiario, nombres y PNJ
- [ ] Diario, misiones y recuerdos
- [ ] Guiones

### Fase 7. Prueba en el juego

- [ ] Jugar con la traducción completa y anotar cortes, cajas que se pasan, glifos que faltan y texto que quedó sin traducir.

### Fase 8. Entrega

- [ ] Instalador, registro de cambios y publicación.
