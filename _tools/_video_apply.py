#!/usr/bin/env python3
"""
Añade el reproductor de YouTube del podcast Inside B2B Business en
podcast.html, como seccion de episodio destacado justo antes del bloque
"Episodios destacados".

Cambios respecto al embed original de YouTube:
  - Sin width/height fijos (560x315 rompia en movil). Se usa aspect-ratio 16/9.
  - Sin frameborder (atributo obsoleto), el borde se quita por CSS.
  - loading="lazy": YouTube no se carga hasta que el usuario llega al bloque.
  - Dominio youtube-nocookie.com: no deja cookies de seguimiento hasta que se
    da play. Si se prefiere el dominio normal, cambiar VIDEO_HOST.
"""

VIDEO_ID = "7HTQeLUvcKE"
VIDEO_HOST = "https://www.youtube-nocookie.com"

ANCLA = '<section class="sec sand-bg">'

SECCION = (
    '<section class="sec dark" id="episodio-destacado">'
    '<div class="wrap">'
    '<div class="sec-head center reveal">'
    '<span class="eyebrow light center">Episodio destacado</span>'
    '<h2 class="h-xl">Escucha Inside B2B Business</h2>'
    "<p>Una conversación completa sobre cómo se construyen, se lideran y "
    "crecen las empresas B2B desde adentro.</p>"
    "</div>"
    '<div class="video reveal d2">'
    f'<iframe src="{VIDEO_HOST}/embed/{VIDEO_ID}" '
    'title="Inside B2B Business, episodio en YouTube" '
    'loading="lazy" '
    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
    'gyroscope; picture-in-picture; web-share" '
    'referrerpolicy="strict-origin-when-cross-origin" '
    "allowfullscreen></iframe>"
    "</div>"
    "</div>"
    "</section>"
)

CSS = """
/* ===== Reproductor de video (podcast) ===== */
.video{position:relative;aspect-ratio:16/9;max-width:940px;margin:0 auto;border-radius:var(--r-lg);overflow:hidden;background:#000;box-shadow:var(--sh-2)}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
.sec.dark .video{box-shadow:0 40px 90px -40px rgba(0,0,0,.7)}
@media(max-width:640px){.video{border-radius:var(--r-md)}}
"""

MARCA = "/* ===== Reproductor de video (podcast) ===== */"


def main() -> None:
    path = "podcast.html"
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    if "youtube" in html and MARCA in html:
        print("El reproductor ya estaba puesto, no se toca nada.")
        return

    if ANCLA not in html:
        raise SystemExit("No se encontro el bloque de Episodios destacados.")

    html = html.replace(ANCLA, SECCION + ANCLA, 1)
    html = html.replace("</style>", CSS + "</style>", 1)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("podcast.html: seccion de episodio destacado añadida")


if __name__ == "__main__":
    main()
