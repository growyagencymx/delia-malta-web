"""Comprobacion visual: mide la columna central de la tarjeta .portrait."""
from PIL import Image


def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


im = Image.open("/tmp/final.png").convert("RGB")
px = im.load()

print("columna central de la tarjeta (x=1080):")
for y in range(350, 790, 30):
    p = px[1080, y]
    print(f"  y{y:>4} ({p[0]:>3},{p[1]:>3},{p[2]:>3}) lum {lum(p):>5.0f}")

im.crop((880, 330, 1280, 800)).save("/tmp/tarjeta-final.png")
print("recorte guardado")
