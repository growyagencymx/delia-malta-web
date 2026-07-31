#!/usr/bin/env python3
"""
Sustituye la marca en texto por el logo de Delia Malta en el header y el
footer de todas las paginas, e inyecta el CSS necesario.

Se incluyen las dos versiones del logo (oscura y clara) y se alterna por CSS:
  - header sobre fondo claro   -> logo-delia.png
  - header sobre hero oscuro   -> logo-delia-blanco.png
  - menu movil abierto         -> logo-delia-blanco.png
  - footer (fondo onix)        -> logo-delia-blanco.png
"""
import glob
import re

BRAND_RE = re.compile(r'<a href="index\.html" class="brand">.*?</a>', re.S)

LOGO = (
    '<a href="index.html" class="brand" '
    'aria-label="Delia Malta, inicio">'
    '<img class="logo logo-dark" src="assets/logo-delia.png" '
    'alt="Delia Malta - LinkedIn B2B &amp; Social Selling" '
    'width="489" height="132" decoding="async">'
    '<img class="logo logo-light" src="assets/logo-delia-blanco.png" '
    'alt="" aria-hidden="true" width="489" height="132" decoding="async">'
    "</a>"
)

CSS = """
/* ===== Logo de marca ===== */
.brand{gap:0}
.brand .logo{display:block;width:auto;height:44px;transition:height .45s var(--ease)}
.brand .logo-light{display:none}
.nav.scrolled .brand .logo{height:38px}
.nav.dark-top:not(.scrolled) .brand .logo-dark{display:none}
.nav.dark-top:not(.scrolled) .brand .logo-light{display:block}
body:has(.mobile.open) .nav .brand .logo-dark{display:none}
body:has(.mobile.open) .nav .brand .logo-light{display:block}
body:has(.mobile.open) .nav .burger span{background:#fff}
.footer .brand{margin-bottom:.2rem}
.footer .brand .logo-dark{display:none}
.footer .brand .logo-light{display:block;height:54px}
@media(max-width:640px){
  .brand .logo,.nav.scrolled .brand .logo{height:34px}
  .footer .brand .logo-light{height:44px}
}
"""

MARK = "/* ===== Logo de marca ===== */"


def main() -> None:
    for path in sorted(glob.glob("*.html")):
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html

        html, n = BRAND_RE.subn(LOGO, html)

        if MARK not in html and "</style>" in html:
            html = html.replace("</style>", CSS + "</style>", 1)

        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
        print(f"{path:22} marcas reemplazadas: {n}")


if __name__ == "__main__":
    main()
