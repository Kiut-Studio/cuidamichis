#!/usr/bin/env python3
"""Procesa los dibujos de Sofía: arte/entrada/*.png -> assets/ (webp) y actualiza assets/arte.json.
Uso:  python3 tools/procesar_arte.py [--sin-negro]
Requiere: pip install pillow"""
import json, sys, pathlib
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ENT = RAIZ / 'arte' / 'entrada'
POSES = ['feliz','contento','triste','hambre','comiendo','jugando','banio','miedo','enfermo','bostezo','dormido1','dormido2']
EDADES = ['edad_bebe','edad_joven','edad_adulto','edad_abuelo']
CARAS = ['cara_feliz','cara_amor','cara_enojo','cara_sorpresa','cara_triste','cara_sueno']
EXTRAS = ['tazon','cama','pelota','lana','pescado','gota','caca','corazon','final_vejez','final_descuido','final_porton','final_abandono']

def negro(im):
    """Versión del gato negro: pasa el naranja/crema a grises oscuros, conserva el trazo."""
    im = im.convert('RGBA'); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0: continue
            l = int(.299*r + .587*g + .114*b)
            if l < 60: continue
            v = int(38 + l*.18)
            px[x, y] = (v, v, v+8, a)
    return im

def main():
    hacer_negro = '--sin-negro' not in sys.argv
    ent = sorted(ENT.glob('*.png')) + sorted(ENT.glob('*.webp'))
    if not ent: print('No hay dibujos en arte/entrada/'); return
    arte = json.loads((RAIZ/'assets'/'arte.json').read_text())
    (RAIZ/'assets'/'extra').mkdir(exist_ok=True)
    poses = []; extras = set(arte.get('opcionales', []))
    for f in ent:
        n = f.stem.lower(); im = Image.open(f).convert('RGBA')
        if n in POSES or n in EDADES or n in CARAS:
            im.save(RAIZ/'assets'/'gato'/f'{n}.webp', 'WEBP', quality=90, method=6)
            if hacer_negro: negro(im).save(RAIZ/'assets'/'gato'/f'{n}_n.webp', 'WEBP', quality=90, method=6)
            poses.append(n); print('gato   ✔', n)
        elif n in EXTRAS or n.startswith('ropa_'):
            im.save(RAIZ/'assets'/'extra'/f'{n}.webp', 'WEBP', quality=90, method=6); extras.add(n); print('extra  ✔', n)
        else: print('?? nombre no reconocido (se ignora):', f.name)
    hechas = {p.stem for p in (RAIZ/'assets'/'gato').glob('*.webp')}
    if set(POSES) <= {n for n in poses} | set(arte.get('poses', [])): arte['gato'] = 'sofia'
    arte['poses'] = sorted(set(arte.get('poses', [])) | set(poses))
    arte['opcionales'] = sorted(extras)
    (RAIZ/'assets'/'arte.json').write_text(json.dumps(arte, indent=2, ensure_ascii=False) + '\n')
    print('\nListo. Ahora: python3 tools/construir.py y python3 pruebas/juego.py')
main()
