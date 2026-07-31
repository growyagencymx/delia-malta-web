#!/usr/bin/env python3
"""
Genera las versiones web del logo a partir de assets/Logo_Delia.png.

Salidas (proporcion original respetada, sin deformar):
  assets/logo-delia.png        -> fondo transparente, colores originales (headers claros)
  assets/logo-delia-blanco.png -> version clara para fondos oscuros (footer / hero dark)

Tecnica: el original es RGB sobre blanco. Se recupera el alfa con
alpha = 1 - min(r,g,b)/255 y se "desmultiplica" el color, lo que conserva
el antialiasing de los bordes sin halos.
"""
from PIL import Image

SRC = "assets/Logo_Delia.png"
TARGET_H = 132  # alto del asset: cubre 3x un logo mostrado a 44px
NEAR_WHITE = 244
MINT = (125, 227, 209)
OFF_WHITE = (247, 248, 246)


def trim(img: Image.Image) -> Image.Image:
    """Recorta el margen blanco sin tocar la proporcion del contenido."""
    px = img.load()
    w, h = img.size
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if not (r > NEAR_WHITE and g > NEAR_WHITE and b > NEAR_WHITE):
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)
    return img.crop((minx, miny, maxx + 1, maxy + 1))


def to_transparent(img: Image.Image) -> Image.Image:
    out = Image.new("RGBA", img.size)
    src, dst = img.load(), out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            a = 255 - min(r, g, b)
            if a == 0:
                dst[x, y] = (0, 0, 0, 0)
                continue
            k = a / 255
            dst[x, y] = (
                max(0, min(255, round((r - 255 * (1 - k)) / k))),
                max(0, min(255, round((g - 255 * (1 - k)) / k))),
                max(0, min(255, round((b - 255 * (1 - k)) / k))),
                a,
            )
    return out


def to_light(img: Image.Image) -> Image.Image:
    """Version para fondos oscuros: tinta oscura -> blanco roto, teal -> mint."""
    out = Image.new("RGBA", img.size)
    src, dst = img.load(), out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                dst[x, y] = (0, 0, 0, 0)
                continue
            is_teal = (g > r + 30) and (b > r + 20)
            dst[x, y] = (*(MINT if is_teal else OFF_WHITE), a)
    return out


def resize(img: Image.Image) -> Image.Image:
    w, h = img.size
    return img.resize((round(w * TARGET_H / h), TARGET_H), Image.LANCZOS)


def main() -> None:
    base = resize(to_transparent(trim(Image.open(SRC).convert("RGB"))))
    base.save("assets/logo-delia.png", optimize=True)
    to_light(base).save("assets/logo-delia-blanco.png", optimize=True)
    print(f"logo-delia.png        {base.size[0]}x{base.size[1]}")
    print(f"logo-delia-blanco.png {base.size[0]}x{base.size[1]}")
    print(f"proporcion {base.size[0] / base.size[1]:.4f}")


if __name__ == "__main__":
    main()
