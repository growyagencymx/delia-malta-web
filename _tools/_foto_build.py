#!/usr/bin/env python3
"""
Genera las versiones web de la foto de Delia Malta.

Origen: assets/hf_20260731_002323_...png  (1856x2304, 5.5 MB)

Medidas detectadas del sujeto (px del original):
  cabeza  y 168 -> 870   x 644 -> 1220   (centro aprox 932, 520)
  hombros arrancan sobre y 900

Salidas:
  delia-portrait.webp/.jpg  800x1000  -> tarjeta .portrait de sobre-delia (4/5)
  delia-avatar.webp/.jpg    144x144   -> avatar del mock de LinkedIn en la home
"""
from PIL import Image

SRC = "_source/hf_20260731_002323_d0ce6640-2373-4172-8307-bf083574b2bd.png"

# Recorte cuadrado centrado en la cabeza: la cara ocupa ~72% del ancho.
CARA_CENTRO = (932, 520)
AVATAR_LADO = 800


def guardar(img: Image.Image, base: str) -> None:
    img.save(f"assets/{base}.webp", quality=86, method=6)
    img.save(f"assets/{base}.jpg", quality=86, optimize=True, progressive=True)
    for ext in ("webp", "jpg"):
        import os

        kb = os.path.getsize(f"assets/{base}.{ext}") // 1024
        print(f"  {base}.{ext:<4} {img.size[0]}x{img.size[1]}  {kb} KB")


def main() -> None:
    src = Image.open(SRC).convert("RGB")
    W, H = src.size

    # --- Retrato 4/5: se recorta solo a lo ancho, no se pierde nada del cuerpo.
    ancho = round(H * 4 / 5)
    x0 = (W - ancho) // 2
    retrato = src.crop((x0, 0, x0 + ancho, H)).resize((800, 1000), Image.LANCZOS)
    print("Retrato 4/5 (recorte horizontal de %d px):" % (W - ancho))
    guardar(retrato, "delia-portrait")

    # --- Avatar cuadrado centrado en la cara.
    cx, cy = CARA_CENTRO
    mitad = AVATAR_LADO // 2
    ax0 = max(0, min(cx - mitad, W - AVATAR_LADO))
    ay0 = max(0, min(cy - mitad, H - AVATAR_LADO))
    avatar = src.crop((ax0, ay0, ax0 + AVATAR_LADO, ay0 + AVATAR_LADO)).resize(
        (144, 144), Image.LANCZOS
    )
    print(f"Avatar cuadrado (origen {ax0},{ay0} lado {AVATAR_LADO}):")
    guardar(avatar, "delia-avatar")


if __name__ == "__main__":
    main()
