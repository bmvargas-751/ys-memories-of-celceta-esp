# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla.

- [ ] Títulos más largos que el original (T-3, lote diario-misiones-y-recuerdos-003): `text/quest#GF_QUEST_103`, `109`, `204`, `207` y `208/etiqueta` (ancho 462), `text/quest#GF_QUEST_301/recompensa` (699 de 602; cabría «Surtido de productos sugeridos», 589) y `text/memory#memory:MESUB_20/titulo` (590 de 512); del lote 004, `text/quest#GF_QUEST_404/etiqueta` «Coleccionista de firmas» (495 de 462). No se acortan sin perder sentido; ver si se salen de la lista de misiones o de recuerdos.

- [ ] `text/memory#memory:MEMAIN_10/titulo`: «Atacante de alas negras» mide 517 y el original 512 (T-3). Mantiene el epíteto de la descripción y del diario. Si se sale de la lista de recuerdos: «Atacante alado oscuro» (479).

- [ ] Textos rúnicos de los roos (`#2r`, lote guiones-045; en inglés, 190 renglones con `#2r` en `script/mp6210`, `mp6210m` y `sd3110`). `system/runefont.itp` solo tiene ASCII: letras, los dígitos (que se ven como números normales) y `! ' , - . ?`. No tiene á é í ó ú ñ ¡ ¿. En japonés, las líneas rúnicas cierran las runas antes de un carácter de dos bytes y las vuelven a abrir después (`script/mp6210#talk_dhue/11`: `UGLY#0r――#2r!#0r`), señal de que el modo rúnico no dibuja esos caracteres. Además, el inglés corta los renglones rúnicos a mano en unas 730 unidades (28 caracteres como mucho), aunque el cuadro centrado admite 1500, y el adaptador reparte estas líneas a 1500. Hay que ver en el juego: (1) cómo salen las letras con tilde, la ñ y los signos de apertura dentro de las runas; (2) si un renglón rúnico de 1500 cabe. Si algo falla, hay que decidir cómo se escriben estas líneas (sin tildes ni ¡¿, o cerrando las runas alrededor de esas letras) y ajustar el ancho en el adaptador. Con 730, la única delicada que pasaría de 3 renglones es `script/mp6210#talk_kire/9`; cabría «¡VUELVE CON TUS HAMBURGUESAS!» en lugar de «¡VUELVE A TUS HAMBURGUESAS CON QUESO!».

- [ ] Rótulos de menú sin texto en el juego con qué cotejar (lote guiones-006, `script/mp1201m` y `mp1211`): «[Sistema]», «[Opciones]», «[Opciones adicionales]» y «Menú de reintento». «System» es una imagen (`menu_mt1`): alinear con lo que se ponga en las imágenes de menú.

- [ ] `script/mp6365#EV07_04_Battle_Gadis/476` (reviewer, lote guiones-049): duda de atribución. El export pone a Gadis como hablante, pero el japonés va en femenino («特製の仮面よ») y lleva el prefijo `#833c#2M`, el mismo de la voz de Bammy sin cuerpo en mp6342/346–350. Probablemente habla Bammy a través de la máscara. El español no marca género, así que no cambia nada; ver en el juego quién habla.

## De los lotes

(Nada pendiente: lo de los lotes 001 a 052 se decidió el 2026-11-20; ver DECISIONS.md.)

## Términos por decidir (glosario)

(Nada pendiente.)
