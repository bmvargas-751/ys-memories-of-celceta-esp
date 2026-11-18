# Decisiones

Lo que el usuario decidió, con fecha, para no volver a discutirlo. Una regla de STYLE.md, TECH.md o GLOSSARY.md que sale de aquí lo cita: [DECISIONS fecha].

- **2026-11-17** Proyecto creado con el kit de traducción de juegos.
- **2026-11-17** Original: inglés oficial (Steam, `lang/en`); apoyo: japonés (`lang/ja`), solo para género, sujeto omitido y trato.
- **2026-11-17** Terminología oficial: la traducción oficial al español de *Ys Origin*.
- **2026-11-17** Pruebas en Steam (Windows) y Steam Deck / Linux, con instalador multiplataforma.
- **2026-11-17** STYLE.md: se deja toda la base del kit.
- **2026-11-17** Reglas del repositorio iguales a las de The Hundred Line: `main` solo por pull request con revisión del dueño (CODEOWNERS), etiquetas `v*` protegidas, solo squash, licencia doble (MIT para `tools/`, CC BY-NC-SA 4.0 para la traducción) y commits sin firma de Claude.
- **2026-11-17** Cuadros de diálogo (`TalkMes`, hasta 3 renglones): se exporta cada cuadro como un solo texto, sin saltos, y el adaptador lo reparte en renglones al importarlo, según el ancho real de la fuente (reflujo). Si no cabe en 3 renglones, el chequeo avisa y se acorta la frase; no se agregan cuadros.
