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
| Sol-Galva | Sol-Galba | Decidido (G-2), DECISIONS 2026-11-17 | Inconsistencia del original (`map/`): se unifica con «Sol-Galba», la forma del resto del juego. |
| Governor General Griselda | gobernadora general Griselda | Decidido (G-2), DECISIONS 2026-11-18 | Título de Griselda; con artículo en la frase: «la gobernadora general Griselda». |
| Governor General | gobernador general | Decidido (G-2), DECISIONS 2026-11-18 | El cargo sin nombre; «gobernadora general» cuando se refiere a Griselda. |
| Governor General's office | despacho de la gobernadora general | Decidido (G-2), DECISIONS 2026-11-18 | Lugar de las misiones de mapeo. |
| General Government Building | Edificio de la Gobernación General | Decidido (G-2), DECISIONS 2026-11-18 | Nombre de mapa. |
| King Lefance | rey Lefance | Decidido (G-2), DECISIONS 2026-11-18 | Con artículo en la frase: «el rey Lefance». |
| Magician Bami | maga Bami | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo y título (mujer). |
| Beast Tamer Gadis | domador de bestias Gadis | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo y título (hombre). «Tamer Gadis» → «domador Gadis». |
| Shaman Pippi | chamán Pippi | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo y título; si la ficha dice que es mujer, «chamana Pippi». |
| Artisan Saisen | artesano Saisen | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo y título (hombre). |
| Head Miner Wagner | capataz Wagner | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo y título (hombre). «Miner Wagner» → «minero Wagner». |
| Mayor Aaron | alcalde Aaron | Decidido (G-2), DECISIONS 2026-11-18 | «the mayor» → «el alcalde». |
| Agent | agente | Decidido (G-2), DECISIONS 2026-11-18 | Título ante nombre: «Agent Theresa» → «agente Theresa», «Agent Bertha» → «agente Bertha». |
| Gazock the Strong | Gazock el Fuerte | Decidido (G-2), DECISIONS 2026-11-18 | Sobrenombre. |
| Explorer | explorador | Decidido (G-2), DECISIONS 2026-11-18 | Título de los exploradores; el alias queda en inglés: «Explorer Rabbit» → «exploradora Rabbit». Género según la ficha. «Prospector Owl» → «buscador Owl», «Guide Jackal» → «guía Jackal». |
| Information Dealer | informante | Decidido (G-2), DECISIONS 2026-11-18 | Oficio y rótulo: «Information Dealer Mouse» → «informante Mouse». |
| Apostle | apóstol | Decidido (G-2), DECISIONS 2026-11-18 | Rango de Highland; plural «apóstoles». «Apprentice Apostle» → «aprendiz de apóstol». |
| Grand Roo | Gran Roo | Decidido (G-2), DECISIONS 2026-11-18 | Un roo con título propio (mayúscula). |
| Young Sparda | sparda joven | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo de PNJ. |
| Masked Soldier | soldado enmascarado | Decidido (G-2), DECISIONS 2026-11-18 | Igual «Masked Warrior» → «guerrero enmascarado», «Masked Man» → «hombre enmascarado». |
| Phantom Gruda | Gruda Fantasma | Decidido (G-2), DECISIONS 2026-11-18 | Nombre de enemigo. «Shadow Gruda» → «Gruda Sombra»; «Gruda's Shadow» → «Sombra de Gruda». |
| Galbalan | Galbalan | Decidido (G-2), DECISIONS 2026-11-18 | Criatura de la serie, invariable: «Sol-Galba, the White Galbalan» → «Sol-Galba, el Galbalan Blanco». |
| Carna | Karna | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia de `text/status`: se usa el nombre de los diálogos [DECISIONS 2026-11-17]. |
| Canlilica | Calilica | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia de `text/status`: se usa el nombre de los diálogos [DECISIONS 2026-11-17]. |
| frida | Frieda | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia de `text/status`: se usa el nombre de los diálogos [DECISIONS 2026-11-17]. |
| Riesa | Leeza | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia de `text/status`: se usa el nombre de los diálogos [DECISIONS 2026-11-17]. |
| Romun | romuno | Decidido (G-2), DECISIONS 2026-11-18 | Imperio; adjetivo y gentilicio, concuerda: «Romun Army» → «Ejército Romuno», «Romun Empire» → «Imperio Romuno», «a Romun soldier» → «un soldado romuno». No hay forma oficial: *Ys IX* no salió en español. |
| Romuns | romunos | Decidido (G-2), DECISIONS 2026-11-18 | El pueblo: «the Romuns» → «los romunos». |
| Celcetan Army | Ejército Celcetano | Decidido (G-2), DECISIONS 2026-11-18 | Facción, con el adjetivo oficial «celcetano». «Celcetan Army Soldier» → «soldado celcetano». |
| Kingdom of Celceta | Reino de Celceta | Decidido (G-2), DECISIONS 2026-11-18 | Reino antiguo. «the Celcetan Kingdom» → «el Reino de Celceta». |
| Masked Division | División Enmascarada | Decidido (G-2), DECISIONS 2026-11-18 | Unidad militar. |
| Sparda | sparda | Decidido (G-2), DECISIONS 2026-11-18 | Animal acuático sagrado, en minúscula como especie (como «roo»); plural «spardas». |
| sacred beasts | bestias sagradas | Decidido (G-2), DECISIONS 2026-11-18 | Así llama el juego a los spardas y otros animales. «Sacred Beast Collar» → «Collar de bestia sagrada»; «Sacred Beasts' Lair» → «Guarida de las Bestias Sagradas». |
| Fabros | fabros | Decidido (G-2), DECISIONS 2026-11-18 | Animal de granja y enemigo, en minúscula e invariable: «un fabros», «los fabros». «Fabros Milk» → «leche de fabros». |
| Great Forest | Gran Bosque | Decidido (G-2), DECISIONS 2026-11-18 | Lugar principal. «Great Forest of Celceta» → «Gran Bosque de Celceta». |
| Primeval Lands | Tierras Primigenias | Decidido (G-2), DECISIONS 2026-11-18 | Región. |
| Ashen Forest | Bosque de Ceniza | Decidido (G-2), DECISIONS 2026-11-18 | Región. «Forest of Ash» es la misma: se unifica [DECISIONS 2026-11-17]. |
| Forest of Ash | Bosque de Ceniza | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia del original: misma región que «Ashen Forest». |
| Forest of Dawn | Bosque del Alba | Decidido (G-2), DECISIONS 2026-11-18 | Región. |
| Temple of the Sun | Templo del Sol | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Sanctuary of Storms | Santuario de las Tormentas | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. «Sanctuary Approach» → «Acceso al Santuario». |
| Underground Ruins | Ruinas Subterráneas | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Subterranean Forest | Bosque Subterráneo | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| World of Records | Mundo de los Registros | Decidido (G-2), DECISIONS 2026-11-18 | «Iris, the World of Records» → «Iris, el Mundo de los Registros». |
| Akashic Records | Registros Akáshicos | Decidido (G-2), DECISIONS 2026-11-18 | Concepto central. |
| Mt. Vesuvio | monte Vesuvio | Decidido (G-2), DECISIONS 2026-11-18 | En rótulos de mapa, con mayúscula: «Monte Vesuvio: Cima nevada». |
| Ancient Burrow | Madriguera Antigua | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Lake Tolmes | lago Tolmes | Decidido (G-2), DECISIONS 2026-11-18 | «Lake Tolmes Ruins» → «Ruinas del Lago Tolmes». |
| Central Area | Área Central | Decidido (G-2), DECISIONS 2026-11-18 | Zonas de Iris: «Bronze/Silver/Gold Area» → «Área de Bronce/de Plata/de Oro». |
| Colonia Battlefield | Campo de Batalla de Colonia | Decidido (G-2), DECISIONS 2026-11-18 | «Colonia Artifact Laboratory» (y «Lab») → «Laboratorio de Artefactos de Colonia». |
| Roos' Nest | Nido de los Roos | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Forest Labyrinth | Laberinto del Bosque | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Tower of Providence | Torre de la Providencia | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Casnia Mine | mina de Casnia | Decidido (G-2), DECISIONS 2026-11-18 | En rótulos, «Mina de Casnia». |
| Misty Peak | Pico Brumoso | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Forest of Spores | Bosque de las Esporas | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Table Mountain | Montaña Mesa | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Gidona Crater | Cráter de Gidona | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Plateau Path | Sendero de la Meseta | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Algon River Basin | Cuenca del Río Algon | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Beast Plains | Llanuras de las Bestias | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Jade Cave | Cueva de Jade | Decidido (G-2), DECISIONS 2026-11-18 | Igual «Waterfall Cave» → «Cueva de la Cascada», «Quartz Cave» → «Cueva de Cuarzo». |
| Frogs' Inn | Posada de las Ranas | Decidido (G-2), DECISIONS 2026-11-18 | Lugar. |
| Elduke, the Ruined Capital | Elduke, la Capital en Ruinas | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo. «Ruined City of Elduke» → «Ciudad en Ruinas de Elduke»; «Elduke Outskirts» → «Afueras de Elduke». |
| Frontier City of Casnan | Casnan, Ciudad Fronteriza | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo. «Casnan City» → «Ciudad de Casnan». |
| Comodo Village | Aldea de Comodo | Decidido (G-2), DECISIONS 2026-11-18 | Igual «Selray Village» → «Aldea de Selray», «Danan Village» → «Aldea de Danan». |
| Highland Town | Pueblo de Highland | Decidido (G-2), DECISIONS 2026-11-18 | Highland no se traduce. |
| Miasmic Road | Camino del Miasma | Decidido (G-2), DECISIONS 2026-11-18 | Parte del Bosque de Ceniza; «Outskirts» → «Afueras», «Marshland» → «Pantano», «Wetlands» → «Humedal». |
| Mask of the Sun | Máscara del Sol | Decidido (G-2), DECISIONS 2026-11-18 | Objeto clave. |
| Mask of the Moon | Máscara de la Luna | Decidido (G-2), DECISIONS 2026-11-18 | Objeto clave. «Left/Right Mask Fragment» → «Fragmento izquierdo/derecho de máscara». |
| Replica Mask | Máscara réplica | Decidido (G-2), DECISIONS 2026-11-18 | Rótulo de `map/`. |
| Artifact Sword Emeraude | Espada Artefacto Emeraude | Decidido (G-2), DECISIONS 2026-11-18 | Objeto clave. «the Artifact Sword» → «la Espada Artefacto». |
| Roda Leaf | hoja de Roda | Decidido (G-2), DECISIONS 2026-11-18 | Material. «Roda Droplet» → «gota de Roda». |
| Celcetan Flower | flor celcetana | Decidido (G-2), DECISIONS 2026-11-18 | Material. «Celcetan Wreath» → «guirnalda celcetana». |
| Yupel Flower | flor de yupel | Decidido (G-2), DECISIONS 2026-11-18 | Igual «Libra Flower» → «flor de libra», «Marl Flower» → «flor de marl»; «Wreath» → «guirnalda de yupel/libra/marl». |
| Raparo Fruit | fruta de raparo | Decidido (G-2), DECISIONS 2026-11-18 | Igual «Arieda Fruit» → «fruta de arieda», «Chito Nut» → «nuez de chito». |
| Fresh Leaf | hoja fresca | Decidido (G-2), DECISIONS 2026-11-18 | Igual «Rotting Leaf» → «hoja podrida», «Wilted Flower» → «flor marchita», «Rotting Fruit» → «fruta podrida». |
| Iron Ore | mena de hierro | Decidido (G-2), DECISIONS 2026-11-18 | «Silver Ore», «Gold Ore» → «mena de plata/de oro»; «Iron/Silver/Gold Ingot» → «lingote de hierro/plata/oro». |
| Sun Stone | piedra solar | Decidido (G-2), DECISIONS 2026-11-18 | Material de misión. |
| Wind Crest | cimera del viento | Decidido (G-2), DECISIONS 2026-11-18 | Objeto clave. «Rain Crest» → «cimera de la lluvia», «Sun Crest» → «cimera del sol». |
| Fabros Milk | leche de fabros | Decidido (G-2), DECISIONS 2026-11-18 | Objeto de misión. |
| Silver Wing | Ala de plata | Decidido (G-2), DECISIONS 2026-11-18 | Objeto clave para transportarse. «Golden Wing» → «Ala dorada». |
| Honey Potion | poción de miel | Decidido (G-2), DECISIONS 2026-11-18 | Consumible. «Bitter Potion» → «poción amarga», «Kaiser Potion» → «poción káiser». |
| Silver Axe | hacha de plata | Decidido (G-2), DECISIONS 2026-11-18 | Objeto de misión. «Golden Axe» → «hacha de oro». |
| Titanic Bone | hueso titánico | Decidido (G-2), DECISIONS 2026-11-18 | Materiales de misión: «Bizarre Hide» → «piel extraña», «Clear Liquid» → «líquido transparente», «Acidic Liquid» → «líquido ácido», «Filthy Liquid» → «líquido inmundo», «Slime Mold» → «moho viscoso», «Poisonous Organ» → «órgano venenoso», «Indestructible Shell» → «caparazón indestructible», «Frog Extract» → «extracto de rana». |
| Silver Dragon Charm | amuleto de dragón plateado | Decidido (G-2), DECISIONS 2026-11-18 | «Gold Dragon Charm» → «amuleto de dragón dorado». |
| Dwarf Bracelet | brazalete enano | Decidido (G-2), DECISIONS 2026-11-18 | Objeto clave: encoge al grupo. |
| Holy Knight's Magatama | magatama del caballero sagrado | Decidido (G-2), DECISIONS 2026-11-18 | Accesorio de misión. |
| Ruby | rubí | Decidido (G-2), DECISIONS 2026-11-18 | Gemas: «Sapphire» → «zafiro», «Amethyst» → «amatista», «Onyx» → «ónice», «Diamond» → «diamante». |
| Beast Material | material animal | Decidido (G-2), DECISIONS 2026-11-18 | Categoría. «Plant Material» → «material vegetal», «Mineral» → «mineral», «Crafting Materials» → «materiales de fabricación». |
| EXTRA Skill | habilidad EXTRA | Decidido (G-2), DECISIONS 2026-11-18 | Mecánica. La barra y sus objetos «1 EX», «5 EX» quedan como «EX». |
| EXP | EXP | Decidido (G-2), DECISIONS 2026-11-18 | Experiencia. «Skill EXP Gain» → «EXP de habilidad». |
| Max HP | PV máx. | Decidido (G-2), DECISIONS 2026-11-18 | Con «PV» oficial. |
| AGL | AGI | Decidido (G-2), DECISIONS 2026-11-18 | Bono de las tablillas. «DEX» → «DES». |
| BURN | QUEM | Decidido (G-2), DECISIONS 2026-11-18 | Etiquetas de la ficha de equipo: «FRZN» → «CONG», «PARA» → «PAR», «POIS» → «VEN», «ABSB» → «ABS», «CRIT» → «CRÍT», «HEAL» → «CURA», «EVA» → «EVA», «SPD» → «VEL». Columna estrecha: revisar el ancho. |
| Poison | Veneno | Decidido (G-2), DECISIONS 2026-11-18 | Estados alterados: «Paralysis» → «Parálisis», «Burn» → «Quemadura», «Freezing» → «Congelación», «Curse» → «Maldición», «Misfortune» → «Infortunio», «Heavy» → «Pesadez», «Critical» → «Crítico»; «stun» → «aturdir». |
| status ailments | estados alterados | Decidido (G-2), DECISIONS 2026-11-18 | «Status Effects» → «Estados alterados». |
| Slash type | tipo corte | Decidido (G-2), DECISIONS 2026-11-18 | Tipos de ataque: «Strike type» → «tipo golpe», «Pierce type» → «tipo perforación»; «Weak» → «Débil», «No Weakness» → «Sin debilidad». |
| Flash Guard | Guardia relámpago | Decidido (G-2), DECISIONS 2026-11-18 | Mecánica de combate. «Flash Move» → «Esquiva relámpago»; «Simulflash» → «Doble relámpago». |
| Skill Finish | Remate de habilidad | Decidido (G-2), DECISIONS 2026-11-18 | «Finishing Blow» → «Golpe de gracia», «Excellent Kills» → «Eliminaciones excelentes», «Aerial Combos» → «Combos aéreos». |
| Skill Trigger | Activador de habilidades | Decidido (G-2), DECISIONS 2026-11-18 | Botón que se mantiene para usar habilidades. |
| Attack Focus | Prioridad: ataque | Decidido (G-2), DECISIONS 2026-11-18 | Órdenes al grupo: «Evasion Focus» → «Prioridad: evasión»; «Party Orders» → «Órdenes al grupo»; «Party Abilities» → «Habilidades de grupo» (party → grupo). |
| Personal Action | Acción personal | Decidido (G-2), DECISIONS 2026-11-18 | «Unique Actions» es lo mismo: se unifica en «Acciones personales» [DECISIONS 2026-11-17]. |
| Unique Actions | Acciones personales | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia del original: lo mismo que «Personal Action». |
| Memory Sphere | Esfera de recuerdo | Decidido (G-2), DECISIONS 2026-11-18 | Mecánica de recuerdos: «Memory» → «recuerdo», «Memories Menu» → «Menú de recuerdos», «Memory Point» → «Punto de recuerdo», «Unrecalled Memory» → «Recuerdo sin recuperar». |
| Monolith | monolito | Decidido (G-2), DECISIONS 2026-11-18 | Piedras de transporte. «monument» es lo mismo: se unifica en «monolito» [DECISIONS 2026-11-17]. |
| monument | monolito | Decidido (G-2), DECISIONS 2026-11-18 | Inconsistencia del original: lo mismo que «Monolith». |
| Warp Stone | Piedra de transporte | Decidido (G-2), DECISIONS 2026-11-18 | Leyenda del mapa. «Warping» → «Transporte». |
| Harvest Points | Puntos de recolección | Decidido (G-2), DECISIONS 2026-11-18 | «Harvested %d items» → «Recolectaste %d objetos». |
| Reinforcing | Reforzar | Decidido (G-2), DECISIONS 2026-11-18 | Mecánica de tiendas, como *Ys Origin*. |
| Synthesizing | Sintetizar | Decidido (G-2), DECISIONS 2026-11-18 | Mecánica de tiendas: «Refining Ore» → «Refinar menas», «Crafting Accessories» → «Fabricar accesorios», «Exchanging Materials» → «Intercambiar materiales». |
| Quest | misión | Decidido (G-2), DECISIONS 2026-11-18 | Encargos secundarios, como *Ys Origin*. |
| Journal | Diario | Decidido (G-2), DECISIONS 2026-11-18 | Menú y objeto. |
| Key Item | Objeto clave | Decidido (G-2), DECISIONS 2026-11-18 | Categoría de objetos. |
| Treasure Chest | cofre del tesoro | Decidido (G-2), DECISIONS 2026-11-18 | «Chest» → «cofre». |
| Camp | campamento | Decidido (G-2), DECISIONS 2026-11-18 | «Camping and Memories» → «Campamentos y recuerdos»; «Resting» → «Descansar». |
| Monster Compendium | Compendio de monstruos | Decidido (G-2), DECISIONS 2026-11-18 | «Material Compendium» → «Compendio de materiales». |
| krimelye | krimelye | Decidido (G-2), DECISIONS 2026-11-18 | Unidad de distancia de la serie: se deja igual. |
| Time Attack | Contrarreloj | Decidido (G-2), DECISIONS 2026-11-18 | Modo de juego. «Boss Rush» → «Desafío de jefes». |
| Nightmare | Pesadilla | Decidido (G-2), DECISIONS 2026-11-18 | Dificultades: «Easy» → «Fácil», «Normal» → «Normal», «Hard» → «Difícil». «Difficult: %s» → «Dificultad: %s». |
| Mapped | Cartografiado | Decidido (G-2), DECISIONS 2026-11-18 | «Map Completion» → «Mapa completado». |
| Touch Puzzles | Acertijos táctiles | Decidido (G-2), DECISIONS 2026-11-18 | «Touch» → «Tocar». |
