#!/usr/bin/env python3
"""
Coloca la foto de Delia Malta en los dos huecos que el diseno ya reservaba
con el monograma "DM":

  sobre-delia.html -> tarjeta .portrait del hero (4/5)
  index.html       -> avatar del mock de publicacion de LinkedIn

Sustituye el degradado radial teal del .portrait por un scrim inferior para
que el nombre y el badge sigan legibles encima de la foto.
"""

ALT = "Delia Malta, consultora en LinkedIn B2B y Social Selling"

RETRATO = (
    '<picture class="pphoto">'
    '<source srcset="assets/delia-portrait.webp" type="image/webp">'
    '<img src="assets/delia-portrait.jpg" alt="' + ALT + '" '
    'width="800" height="1000" decoding="async">'
    "</picture>"
)

AVATAR = (
    '<div class="av has-photo"><picture>'
    '<source srcset="assets/delia-avatar.webp" type="image/webp">'
    '<img src="assets/delia-avatar.jpg" alt="Delia Malta" '
    'width="144" height="144" decoding="async">'
    "</picture></div>"
)

CSS_RETRATO = """
/* ===== Foto de Delia (tarjeta retrato) ===== */
.portrait .pphoto{position:absolute;inset:0;z-index:1}
.portrait .pphoto img{width:100%;height:100%;object-fit:cover;object-position:center top}
.portrait::before{background:linear-gradient(to top,rgba(11,32,39,.9) 0%,rgba(11,32,39,.55) 17%,rgba(11,32,39,0) 44%);z-index:2}
.portrait .tvb{z-index:4}
.portrait .pinfo{z-index:4}
.pchips{z-index:5}
"""

CSS_AVATAR = """
/* ===== Foto de Delia (avatar) ===== */
.post-h .av.has-photo{padding:0;overflow:hidden;background:var(--onix)}
.post-h .av.has-photo img{width:100%;height:100%;object-fit:cover}
"""


def aplicar(path: str, viejo: str, nuevo: str, css: str) -> None:
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    if viejo not in html:
        print(f"{path:20} AVISO: no se encontro {viejo[:40]!r}")
        return

    html = html.replace(viejo, nuevo, 1)
    marca = css.strip().splitlines()[0]
    if marca not in html:
        html = html.replace("</style>", css + "</style>", 1)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"{path:20} foto aplicada")


def main() -> None:
    aplicar("sobre-delia.html", '<span class="mono">DM</span>', RETRATO, CSS_RETRATO)
    aplicar("index.html", '<div class="av">DM</div>', AVATAR, CSS_AVATAR)


if __name__ == "__main__":
    main()
