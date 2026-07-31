"""Extrae una seccion de una pagina a un archivo aislado, para inspeccionarla
en una captura sin tener que recorrer toda la pagina."""
import re
import sys

src, dst, marca = sys.argv[1], sys.argv[2], sys.argv[3]

with open(src, encoding="utf-8") as fh:
    html = fh.read()

head = html[: html.index("</head>") + 7]

i = html.index(marca)
ini = html.rindex("<section", 0, i + len(marca))
fin = html.index("</section>", i) + len("</section>")
seccion = html[ini:fin]

IMP = "!important"
extra = (
    "<style>.reveal{opacity:1" + IMP + ";transform:none" + IMP + "}"
    "body{padding:0}</style>"
)

with open(dst, "w", encoding="utf-8") as fh:
    fh.write(head + extra + "<body>" + seccion + "</body></html>")

print(f"{dst}: seccion de {len(seccion)} chars extraida")
