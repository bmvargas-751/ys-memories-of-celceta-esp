# Decisiones

Lo que el usuario decidió, con fecha, para no volver a discutirlo. Una regla de STYLE.md, TECH.md o GLOSSARY.md que sale de aquí lo cita: [DECISIONS fecha].

- **2026-11-17** Proyecto creado con el kit de traducción de juegos.
- **2026-11-17** Original: inglés oficial (Steam, `lang/en`); apoyo: japonés (`lang/ja`), solo para género, sujeto omitido y trato.
- **2026-11-17** Terminología oficial: la traducción oficial al español de *Ys Origin*.
- **2026-11-17** Pruebas en Steam (Windows) y Steam Deck / Linux, con instalador multiplataforma.
- **2026-11-17** STYLE.md: se deja toda la base del kit.
- **2026-11-17** Reglas del repositorio iguales a las de The Hundred Line: `main` solo por pull request con revisión del dueño (CODEOWNERS), etiquetas `v*` protegidas, solo squash, licencia doble (MIT para `tools/`, CC BY-NC-SA 4.0 para la traducción) y commits sin firma de Claude.
- **2026-11-17** Cuadros de diálogo (`TalkMes`, hasta 3 renglones): se exporta cada cuadro como un solo texto, sin saltos, y el adaptador lo reparte en renglones al importarlo, según el ancho real de la fuente (reflujo). Si no cabe en 3 renglones, el chequeo avisa y se acorta la frase; no se agregan cuadros.
- **2026-11-17** Imágenes con texto: se editan a mano (PNG en la carpeta local, fuera del repo). `tools/images.py` exporta los originales a PNG y convierte los editados a ITP. Cómo llegan al jugador se decide con el instalador (fase 8).
- **2026-11-17** Los tutoriales (`lang/en/visual/topic_*`, 58 páginas) se hacen al final, después del resto de las imágenes; hasta entonces quedan en inglés.
- **2026-11-17** *Ys Origin* en español es también la referencia de tono (formalidad, épica, trato a diosas y nobles, títulos, estilo de sistema), no solo de términos. Se toma el tono, no la variante: su español de España (*vosotros*, *vale*) pasa a neutro. Regla E-24 de STYLE.md.
- **2026-11-17** Moneda: como *Ys Origin*, «monedas» y la abreviatura «M» («500 M»), aunque Celceta diga «gold».
- **2026-11-17** «Romun» queda invariable: «los de Romun», «Ejército de Romun», «Imperio de Romun», «soldado de Romun».
- **2026-11-17** Los nombres de habilidad de combate se traducen, como en *Ys Origin* (con el límite de 31 bytes del campo).
- **2026-11-17** «SP» → «PH» (puntos de habilidad). «Lv» → «Nv» (más claro que la «N» de *Ys Origin*).
- **2026-11-17** Los alias de los exploradores quedan en inglés (Rabbit, Pigeon, Beaver, Swan, Slash, Owl, Jackal); el título se traduce según el género de cada uno (ver fichas).
- **2026-11-17** Las inconsistencias del original se unifican en una sola forma: «Sol-Galba» (no «Sol-Galva»), una para «Ashen Forest» / «Forest of Ash», una para «monolith» / «monument», una para «Personal Action» / «Unique Actions», «Difficult: %s» como «Dificultad: %s», y en `text/status` los nombres de los diálogos (Karna, Calilica, Frieda, Leeza).
- **2026-11-17** Los nombres de los roos con juego de palabras van al agente de líneas delicadas; base: cómo trata *Ys Origin* a los roos (especie en minúscula, «la costumbre de los roos»).
