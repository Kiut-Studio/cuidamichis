#!/usr/bin/env python3
"""Deja el juego listo para subir: arma la lista de archivos de la copia sin conexión (sw.js),
sube la versión de la caché y revisa que no falte ningún dibujo.

Uso:  python3 tools/construir.py            # actualiza sw.js (y sube la versión si cambió algo)
      python3 tools/construir.py --revisar  # solo revisa, no escribe nada
Correrlo cada vez que cambien los dibujos, el código o las fuentes, antes de subir a GitHub.
"""
import os, re, sys, json, hashlib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLO_REVISAR = '--revisar' in sys.argv
RAIZ_ARCHIVOS = ['index.html', 'manifest.json', 'icon-192.png', 'icon-512.png', 'favicon-32.png']
EXT = {'.webp', '.png', '.woff2', '.json', '.jpg', '.svg'}

def archivos():
    lista = ['./'] + [f for f in RAIZ_ARCHIVOS if os.path.exists(os.path.join(RAIZ, f))]
    for d, _, fs in os.walk(os.path.join(RAIZ, 'assets')):
        for f in sorted(fs):
            if os.path.splitext(f)[1].lower() in EXT:
                lista.append(os.path.relpath(os.path.join(d, f), RAIZ).replace(os.sep, '/'))
    return lista

def huella(lista):
    h = hashlib.sha1()
    for f in lista:
        p = os.path.join(RAIZ, f)
        if os.path.isfile(p):
            h.update(f.encode()); h.update(open(p, 'rb').read())
    return h.hexdigest()[:10]

def referencias():
    """Dibujos que el código pide: assets/... escritos en index.html."""
    html = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
    ref = set(re.findall(r"assets/[\w./-]+\.(?:webp|png|woff2)", html))
    out = set()
    for r in ref:
        if os.path.exists(os.path.join(RAIZ, r)): continue
        out.add(r)
    return out

def main():
    lista = archivos()
    # poses del gatito (el código arma los nombres: assets/gato/<pose>[_n].webp)
    html = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
    poses = re.search(r"const CAT_KEYS=\[(.*?)\]", html).group(1).replace("'", '').split(',')
    falta = []
    for k in poses + ['edad_bebe', 'edad_joven', 'edad_adulto', 'edad_abuelo'] + ['cara_' + c for c in ['feliz', 'amor', 'enojo', 'sorpresa', 'sueno', 'triste']]:
        for suf in ['', '_n']:
            f = f'assets/gato/{k.strip()}{suf}.webp'
            if not os.path.exists(os.path.join(RAIZ, f)): falta.append(f)
    for r in sorted(referencias()):
        if '${' in r or r.endswith('/'): continue
        falta.append(r)
    falta = sorted(set(falta))
    if falta:
        print('❌ Faltan dibujos que el juego usa:'); [print('   ', f) for f in falta]
    else:
        print(f'✅ Están todos los dibujos que el juego usa ({len(lista)} archivos en la copia sin conexión)')
    if SOLO_REVISAR: sys.exit(1 if falta else 0)
    sw = open(os.path.join(RAIZ, 'sw.js'), encoding='utf-8').read()
    ver = int(re.search(r"const C=PRE\+'v(\d+)'", sw).group(1))
    marca = re.search(r"// huella:(\w+)", sw)
    nueva = huella(lista)
    if not marca or marca.group(1) != nueva:
        ver += 1
        print(f'↑ Cambió algo: la caché pasa a cuidamichis-v{ver}')
    else:
        print(f'= Sin cambios desde la última vez (v{ver})')
    sw = re.sub(r"const C=PRE\+'v\d+';", f"const C=PRE+'v{ver}';", sw)
    sw = re.sub(r"const FILES=\[.*?\];(\n// huella:\w+)?", "const FILES=" + json.dumps(lista, ensure_ascii=False) + f";\n// huella:{nueva}", sw, flags=re.S)
    open(os.path.join(RAIZ, 'sw.js'), 'w', encoding='utf-8').write(sw)
    sys.exit(1 if falta else 0)
main()
