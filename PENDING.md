# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla.

## De los lotes

- [x] `text/item#12/nombre` (delicadas, broma): «Spectacular Heat Sword» → «Espada ardiente fabulosa». La misión 304 (`script/mp3202#QS304_*`, `text/quest#GF_QUEST_304`) explica la broma: es el nombre exagerado que le pone una herrera aficionada que presume de su «amazing naming sense», y contrasta con el nombre sobrio de la versión mejorada, «Flame Sword» → «Espada de fuego» (`text/item#13/nombre`). Por eso no sirve un nombre neutro como «Espada de calor extremo». «Fabulosa» presume igual que «spectacular», y el nombre mide 531, el ancho de los nombres. Alternativa: «Espada ígnea espectacular», más pomposa y con «espectacular», que repite la pregunta `script/mp3202#QS304_Start2/72` («A spectacular sword, or a superb gauntlet?»), pero mide 566 y hay que verla en el menú. Para mantener la coherencia: el diálogo 72, el diario `GF_QS304_MEMO04~2` y la pareja del nombre, «Superb Toxic Gauntlet» (`text/item#32/nombre`), deben usar la misma fórmula (por ejemplo, «¿Una espada fabulosa o un guantelete soberbio?»).
- [ ] `text/item#6/descripcion` (delicadas, posible juego de palabras): «Shark-like. Can take down even the largest fish.» → «Como un tiburón. Ni el pez más grande se le resiste.». No es un juego de palabras sino una frase de propaganda: la serie «Bronze Edge» es de combate en el agua (`text/item#4/descripcion`: «reduced water resistance»). «Como un tiburón» deja abierto, igual que «Shark-like», si se trata de la forma o de la manera de cazar, y «ni… se le resiste» conserva la exageración con una frase hecha (la versión anterior, «Puede abatir hasta al pez más grande», era muy literal). Mide 1129 de 1325. Alternativa: «Parecida a un tiburón. Puede incluso con el pez más grande.» (1296). Aparte, en `text/item#4/descripcion` «menor resistencia al agua» se puede entender como «menos impermeable», cuando el sentido es que corta el agua (por ejemplo, «Espada de una mano que corta el agua con facilidad»). Esa línea no se cambió: queda señalada para que la decidas.
- [ ] `text/item#822/descripcion` (delicadas, humor): «Proof that the monkey king eats bananas in Valhalla now.» → «Prueba de que el rey mono ya come bananas en el Valhalla.». La broma es un eufemismo de la muerte: el rey mono, un guerrero que pelea con espada (`text/monslib#E0160/descripcion`), ahora está en el paraíso de los guerreros comiendo bananas. Funciona igual en español porque el Valhalla se conoce, y «ya» recoge el «now» con el sentido de «ya pasó al otro lado». Se cambió «plátanos» por «bananas» (E-10): en el Caribe, Colombia, Venezuela y Centroamérica «plátano» es el que se cocina, mientras que «banana» se entiende en toda América y es la palabra del original. Mide menos que el ancho de 1325 y la revisión técnica no da avisos. Alternativa: «Prueba de que el rey mono ya está en el Valhalla comiendo bananas.», que deja la imagen graciosa al final, como remate, pero mueve el foco del original, que pone primero lo de las bananas. Si prefieres la forma de México y España, basta con volver a «plátanos».

## Términos por decidir (glosario)

Propuestas del terminólogo (2026-11-17). Lo decidido pasa a GLOSSARY.md y DECISIONS.md.
### Personajes con título

- [ ] `map/mp6210#maru` (delicadas, juego de palabras): «Maroolyn» y los demás nombres de roos con juego de palabras sobre «roo» (Oroocle, Roomeo, Aroostotle, Roocifer, Froogal, Arroogant, Embarroosed, Rooinous, Roopture, Adoroo, Proose, Droowsy, Scrooup, Roopeat). Los resuelve el agente de delicadas (E-23), con la base de *Ys Origin* para los roos [DECISIONS 2026-11-17].

### Lote objetos-materiales-y-habilidades-003 (2026-11-18)

- [x] `text/item#725/descripcion` (reviewer, sin regla): «los PV de quien lo usa» → «los PV máx. de quien lo usa». La línea de efecto de este mismo objeto (item#725/efecto) dice «PV máx. +100» y el aumento es permanente, pero el original de esta descripción dice solo «HP»; sigue la duda de si «PV» o «PV máx.» (serie de anillos de vida: «Raises max HP» → «PV máx.»). **Resuelto (orquestador, por delegación, 2026-11-18): se sigue el original, que dice «HP» → «PV» (E-1).**
- [x] `text/item#712/efecto` (reviewer, sin regla): «PV +200» → «PV máx. +200». El original dice «HP +200» (sin «Max»), pero es un bono fijo de equipo igual que «PV máx. +100…» de los anillos de vida; duda de si el juego lo trata como máximo, y ninguna regla lo decide. **Resuelto (orquestador, por delegación, 2026-11-18): se sigue el original, que dice «HP» → «PV» (E-1).**
