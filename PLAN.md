# Plan

## Decisiones

Se cierran en la fase 0, porque son caras de cambiar después.

- **Variante:** español neutro (*tú*/*ustedes*, sin regionalismos de ningún país).
- **Original:** inglés oficial de la versión de Steam (`lang/en`), para que los subtítulos coincidan con las voces en inglés. [DECISIONS 2026-11-17]
- **Otra versión de apoyo:** el japonés del mismo juego (`lang/ja`), solo para género, sujeto omitido y trato (E-1). [DECISIONS 2026-11-17]
- **Terminología oficial:** la traducción oficial al español de *Ys Origin* (G-1). [DECISIONS 2026-11-17]
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
- [ ] Adaptador: exportar el texto al formato común (`source` de `loc.json`) e importarlo de vuelta. (Hecho para todo el texto, 19 745 líneas, 2026-11-17; faltan las imágenes con texto.)
- [x] Ida y vuelta idéntica: exportar e importar sin cambios da los mismos archivos. (`tools/celceta.py roundtrip`, 2026-11-17.)
- [x] Caracteres: si la fuente tiene las letras españolas, o cómo se agregan (T-5). (No las tiene; `tools/font_es.py` las agrega. Probado en el juego, 2026-11-17.)
- [ ] Límites: bytes, ancho y renglones de cada tipo de texto (T-3, T-4), y sus chequeos en `hooks`. Los cuadros de diálogo van con reflujo automático, hasta 3 renglones. [DECISIONS 2026-11-17]
- [ ] Pseudolocalización: todo el texto más largo y con letras españolas, en el juego, para ver cortes y glifos que faltan.
  - 2026-11-17, guiones: las letras españolas se ven bien (sin cortes arriba) y los cuadros sin retrato caben con un 10–14 % de margen. Falta ver cuadros con retrato, narración centrada y opciones, y todo lo que no son guiones.
- [ ] Completar TECH.md y `loc.json` (`codes`, `fixed_break`, `excluded`, `sections`).

### Fase 2. Inventario y presupuesto

- [ ] Volumen por sección (`loc.py progress`).
- [ ] Costo estimado por sección, antes de empezarla.

### Fase 3. Documentos

- [ ] Glosario: el terminólogo propone las filas.
- [ ] Fichas de personajes: el perfilador, antes de cada sección.
- [ ] DECISIONS.md y PENDING.md al día.

### Fase 4. Set de oro

Obligatorio: sin él, `loc.py prepare` no arma lotes.

- [ ] Elegir con el usuario los casos reales (al menos uno de cada tipo; mejor dos o tres).
- [ ] Aprobarlo (`loc.py golden approve`).
- [ ] Probar a los agentes (`loc.py golden prepare`, traductor, revisor y corrector, `loc.py golden score`) hasta que pase.

### Fase 5. Piloto

- [ ] Un primer lote de cada tipo de texto con el equipo completo.
- [ ] Ajustar documentos y roles con lo que salga (y volver a pasar el set de oro si cambia un prompt).

### Fase 6. Traducción

- [ ] (una casilla por sección de `loc.json`)

### Fase 7. Prueba en el juego

- [ ] Jugar con la traducción completa y anotar cortes, cajas que se pasan, glifos que faltan y texto que quedó sin traducir.

### Fase 8. Entrega

- [ ] Instalador, registro de cambios y publicación.
