# Glosario

Términos fijos de la traducción. La guía de estilo está en [STYLE.md](STYLE.md).

## Reglas

- **G-1** Si la serie tiene una traducción oficial al español (otro juego, el anime, un manual), los términos que comparte con este juego llevan el nombre oficial. Se toma solo el término; el registro es siempre el de esta traducción (el tono del mundo, según E-24 de STYLE.md). Completar en el PLAN cuál es la fuente oficial, o borrar esta regla si no hay. [IVA]
- **G-2** Lo propio de este juego se decide aquí. Hasta que esté decidido, el término va a [PENDING.md](PENDING.md) con una propuesta. [IVA]
- **G-3** Un término de esta tabla se usa igual en todo el juego. `loc.py check` avisa cuando el original lo tiene y la traducción no (`glosario`). [Encargo §6]

## Cómo se arma

1. El terminólogo revisa los candidatos (los de la fuente oficial, si hay, y los términos de sistema del juego) y propone las filas: *oficial* si es el mismo término, o *por decidir* si significa otra cosa en este juego.
2. Las filas *oficial* entran a la tabla. Las *por decidir* van a [PENDING.md](PENDING.md) para que las decida el usuario.

## Términos

Por sección. *Oficial* (G-1) o *decidido* por el usuario (G-2), con fecha. `loc.py` lee toda tabla cuya cabecera empiece por `| Inglés |`.

| Inglés | Español | Fuente | Nota |
|---|---|---|---|
| Short Sword | Espada corta | Oficial (G-1), Ys Origin `invinfo` sw_05, 2026-11-17 | Arma de entrenamiento (`text/item#1/nombre`). |
| Spirit Cape | Capa espectral | Oficial (G-1), Ys Origin `invinfo` ac_04, 2026-11-17 | Accesorio: restaura PV mientras el grupo está quieto, igual que en Ys Origin (`text/item#742/nombre`). «Spirit Cape+» → «Capa espectral+». |
| Spirit Necklace | Collar espectral | Oficial (G-1), Ys Origin `invinfo` ac_08, 2026-11-17 | Accesorio: revive una vez a quien lo lleva (`text/item#194/nombre`). |
| Water Dragon's Scales | Escamas de dragón acuátil | Oficial (G-1), Ys Origin `invinfo` tl_31, 2026-11-17 | Objeto para bucear y respirar bajo el agua (`text/item#738/nombre`). «Water Dragon's Scales+» → «Escamas de dragón acuátil+». |
| Celcetan Panacea | Panacea celcetana | Oficial (G-1), Ys Origin `invinfo` tl_23, 2026-11-17 | Consumible de curación (`text/item#679/nombre`). |
| Roda Fruit | fruta de Roda | Oficial (G-1), Ys Origin `invinfo` tl_21 y guiones («Obtienes fruta de Roda x 1»), 2026-11-17 | Fruto del árbol Roda; material (`text/item#868/nombre`). Mayúscula inicial solo en etiquetas de menú (E-59): «Fruta de Roda». |
| Roda Tree | árbol Roda | Oficial (G-1), Ys Origin guiones («the Roda Tree» → «el árbol Roda»; «Elder Roda Tree» → «Árbol Roda viejo»), 2026-11-17 | Árbol sagrado del bosque (`text/item#678/descripcion`). |
| Roo | roo | Oficial (G-1), Ys Origin guiones («The Roo appears to be hungry» → «El roo parece hambriento»), 2026-11-17 | Animal sagrado; en minúscula como especie (`script/` y `text/diary`). |
| Roos | roos | Oficial (G-1), Ys Origin guiones («us Roos» → «los roos»), 2026-11-17 | Plural de «roo». |
| pikkard | pikkard | Oficial (G-1), Ys Origin guiones («piel de pikkard»), 2026-11-17 | Animal de la serie; en minúscula como especie (`text/monslib#E0950/descripcion`). |
| Celcetan | celcetano, celcetana | Oficial (G-1), Ys Origin `invinfo` tl_23 («Panacea celcetana»), 2026-11-17 | Adjetivo de Celceta; concuerda con el sustantivo. El nombre «Celceta» se queda igual. |
| Emerald | esmeralda | Oficial (G-1), Ys Origin guiones («Acquired Emerald.» → «Obtienes esmeralda.»), 2026-11-17 | Gema; material (`text/item#763/nombre`). |
| Topaz | topacio | Oficial (G-1), Ys Origin guiones («Acquired Topaz.» → «Obtienes topacio.»), 2026-11-17 | Gema; material (`text/item#764/nombre`). |
| Commander | comandante | Oficial (G-1), Ys Origin guiones («Commander Saul Tovah» → «el comandante Saúl Tovah»), 2026-11-17 | Título militar, en minúscula ante el nombre: «Commander Leo» → «el comandante Leo». |
| Lord | señor | Oficial (G-1), Ys Origin guiones («Lord Dalles» → «el señor Dalles»), 2026-11-17 | Título de respeto ante un nombre, en minúscula: «Lord Eldeel» → «el señor Eldeel». |
| Lady | señora | Oficial (G-1), Ys Origin guiones («Lady Feena» → «la señora Feena»), 2026-11-17 | Título de respeto ante un nombre: «Lady Rabbit» → «señora Rabbit». |
| artifact | artefacto | Oficial (G-1), Ys Origin guiones («The artifacts of Ys» → «Los artefactos de Ys»), 2026-11-17 | Objeto antiguo con poder (`text/manual#topic_40/tema`). Los nombres que lo llevan («Artifact Sword», «Artifact Laboratory») están en PENDING. |
| Ore | mena | Oficial (G-1), Ys Origin guiones («Cleria Ore» → «mena de cleria»), 2026-11-17 | Mineral sin refinar: «Iron Ore» → «mena de hierro» (`text/item#746/nombre`). |
| Crest | cimera | Oficial (G-1), Ys Origin `invinfo` tl_26 y guiones («Red Moon Crest» → «cimera de Luna roja»), 2026-11-17 | Emblema con poder que se usa en altares o paneles (`text/item#698/descripcion`). Los nombres completos están en PENDING. |
| Skill | habilidad | Oficial (G-1), Ys Origin guiones («Hasten Skill recovery» → «Acelerar recup. habilidad»), 2026-11-17 | Técnica especial de combate (`text/manual#topic_13/tema`). |
| Boss | jefe | Oficial (G-1), Ys Origin guiones («Area Boss» → «Jefe de área»; «Last Boss» → «Jefe final»), 2026-11-17 | Enemigo principal (`text/record#RD_BOSSRUSHTIME/texto`). |
| Item | objeto | Oficial (G-1), Ys Origin guiones («Unknown Item» → «objeto desconocido»), 2026-11-17 | Objeto del inventario: «Item Menu» → «Menú de objetos». |
| warp | transportarse | Oficial (G-1), Ys Origin guiones («warp back to base» → «me voy a transportar a la base»), 2026-11-17 | Viajar al instante entre monolitos (`text/strSystem#STR_WARP_CONFIRM`): «Warp to [%s]?» → «¿Transportarse a [%s]?». |
| Save | Guardar | Oficial (G-1), Ys Origin menú («Save» → «Guardar»), 2026-11-17 | Guardar la partida (`text/strSystem#STR_SAVEUI_SAVE`). |
| Load | Cargar | Oficial (G-1), Ys Origin («Loading backup data» → «Cargando respaldo de datos»), 2026-11-17 | Cargar la partida (`text/strSystem#STR_SAVEUI_LOAD`). |
| HP | PV | Oficial (G-1), Ys Origin `invinfo` tl_00 («Recovers HP by 10.» → «Restaura 10 PV.»), 2026-11-17 | Puntos de vida (`text/item#670/efecto`). |
| STR | FUE | Oficial (G-1), Ys Origin `invinfo` ac_05 («STR +5, DEF +5» → «FUE +5, DEF +5»), 2026-11-17 | Fuerza; en Celceta es el poder de las armas (`text/item#1/efecto`). |
| DEF | DEF | Oficial (G-1), Ys Origin `invinfo` ac_05, 2026-11-17 | Defensa (`text/item#121/efecto`). |
| ATK | ATA | Oficial (G-1), Ys Origin `invinfo` tl_06 («Temporary ATK+.» → «ATA+ temporal.»), 2026-11-17 | Ataque; etiqueta de la ficha de armas (`text/strSystem#STR_ITEMINFO_WEPON_ZOKU_ATK`). |
| Lv | Nv | Decidido (G-2), DECISIONS 2026-11-17 | Nivel (de habilidad) (`text/strSystem#STR_ANNOUNCE_SKILL_LEVELUP`). *Ys Origin* abrevia «N»; se usa «Nv», más claro: «Lv1» → «Nv1». |
| Man's Voice | Voz de hombre | Oficial (G-1), Ys Origin guiones, 2026-11-17 | Rótulo de quien habla. Patrón oficial: «X's Voice» → «Voz de X» («Leo's Voice» → «Voz de Leo»). |
| Woman's Voice | Voz de mujer | Oficial (G-1), Ys Origin guiones, 2026-11-17 | Rótulo de quien habla (`script/mp4203#EV04_35_Come_Griselda/483`). |
| Girl's Voice | Voz de chica | Oficial (G-1), Ys Origin guiones, 2026-11-17 | Rótulo de quien habla (`script/mp3202m#MESUB_10ev/103`). |
| SP | PH | Decidido (G-2), DECISIONS 2026-11-17 | Puntos de habilidad: la barra que gastan las habilidades (`text/strSystem#STR_MENU_COST_SP`). En *Ys Origin* «SP» era otra cosa («PE»). «Req. SP» → «PH nec.». |
| gold | monedas | Decidido (G-2), DECISIONS 2026-11-17 | Moneda, como *Ys Origin*: «You don't have enough gold» → «No tienes suficientes monedas». En nombres («Gold Ore», «Gold Colossus») es el metal: «oro». |
| %d G | %d M | Decidido (G-2), DECISIONS 2026-11-17 | Abreviatura de la moneda, como *Ys Origin*: «500 G» → «500 M». |
| Romun | Romun | Decidido (G-2), DECISIONS 2026-11-17 | Imperio; invariable: «the Romuns» → «los de Romun», «Romun Army» → «Ejército de Romun», «Romun Empire» → «Imperio de Romun», «Romun Soldier» → «soldado de Romun». |
| Sol-Galva | Sol-Galba | Decidido (G-2), DECISIONS 2026-11-17 | Inconsistencia del original (`map/`): se unifica con «Sol-Galba», la forma del resto del juego. |
