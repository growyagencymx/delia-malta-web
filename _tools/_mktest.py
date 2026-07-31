"""Genera una copia de una pagina con las animaciones de entrada desactivadas,
para poder medir el render final en capturas headless."""
import sys

IMP = "!important"
EXTRA = (
    ".reveal{opacity:1" + IMP + ";transform:none" + IMP + "}"
    ".hero-r,.hero-sub,.hero-claims,.hero-actions,.hero-trust,.portrait{"
    "opacity:1" + IMP + ";animation:none" + IMP + ";transition:none" + IMP + "}"
)

src = sys.argv[1]
dst = sys.argv[2]

with open(src, encoding="utf-8") as fh:
    html = fh.read()

html = html.replace("</style>", EXTRA + "</style>", 1)

with open(dst, "w", encoding="utf-8") as fh:
    fh.write(html)

print(f"{dst} generado (magenta presente: {'magenta' in html})")
