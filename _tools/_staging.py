#!/usr/bin/env python3
"""
Activa/desactiva el modo STAGING en todas las páginas.

Modo staging  -> inyecta <meta name="robots" content="noindex,nofollow">
                 para que Google NO indexe la web de revision y no compita
                 con el WordPress que sigue en produccion.
Modo produccion -> elimina esas etiquetas.

Uso:
    python3 _staging.py on     # antes de publicar el preview
    python3 _staging.py off    # justo antes de subir al dominio oficial
"""
import glob
import re
import sys

MARKER = '<!--STAGING-NOINDEX--><meta name="robots" content="noindex,nofollow">'
ANCHOR = '<meta name="viewport" content="width=device-width,initial-scale=1">'
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='8' fill='%23102A33'/%3E"
    "%3Ctext x='16' y='22' font-family='Helvetica,Arial' font-size='16' "
    "font-weight='bold' fill='%2300AFA5' text-anchor='middle'%3ED%3C/text%3E"
    '%3C/svg%3E">'
)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
        print(__doc__)
        return 1

    enable = sys.argv[1] == "on"
    changed = []

    for path in sorted(glob.glob("*.html")):
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        html = re.sub(re.escape(MARKER), "", original)

        if enable:
            if ANCHOR not in html:
                print(f"  !  {path}: no se encontro el meta viewport, se omite")
                continue
            html = html.replace(ANCHOR, ANCHOR + MARKER, 1)

        if FAVICON not in html and ANCHOR in html:
            html = html.replace(ANCHOR, ANCHOR + FAVICON, 1)

        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            changed.append(path)

    print(f"Modo {'STAGING (noindex)' if enable else 'PRODUCCION (indexable)'}")
    print(f"Paginas actualizadas: {len(changed)}")
    for path in changed:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
