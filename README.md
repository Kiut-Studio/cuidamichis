# 🐱 Con Cuidado

Un juego de **Kiut Studio** para cuidar un gatito: darle de comer, jugar, bañarlo y quererlo. Si no lo cuidás bien, puede morir.

- Un solo archivo (`index.html`), sin servidor ni cuenta: se juega en el navegador y se puede instalar como app (PWA).
- Funciona sin conexión. La partida se guarda en el dispositivo (`localStorage`, clave `conCuidado.v1`).
- Tiempo real: las barras bajan en horas, el gato crece en días (bebé → joven → adulto → abuelo → final a los 14 días). Hay modo `prueba` (acelerado) para probar.

## Cómo probarlo

```bash
python3 -m http.server 8000     # y abrir http://localhost:8000
```

Atajo de pruebas: `http://localhost:8000/#prueba` expone `window.CC` en la consola.

## Estructura

| Carpeta / archivo | Para qué |
|---|---|
| `index.html` | El juego completo |
| `manifest.json`, `sw.js` | App instalable y modo sin conexión (`sw.js` lo regenera `tools/construir.py`) |
| `assets/` | Dibujos, fuentes e íconos |
| `assets/arte.json` | Lista de los dibujos de Sofía que ya están (lo escribe `tools/procesar_arte.py`) |
| `arte/` | **Acá se dejan los dibujos nuevos de Sofía** (ver `docs/ARTE_SOFIA.md`) |
| `pruebas/` | Pruebas automáticas (Playwright, Python) |
| `docs/` | Hoja de ruta, guía de arte, capturas |

## Pruebas

```bash
pip install playwright && playwright install chromium
python3 pruebas/juego.py                 # todas (125 comprobaciones)
python3 pruebas/juego.py -k pantallas --capturas
```

## Antes de subir cambios

```bash
python3 tools/construir.py     # regenera la lista de archivos y sube la versión de la caché
python3 pruebas/juego.py
```

## Licencia

Código: MIT. Dibujos: © Sofía — todos los derechos reservados (ver `LICENSE`).
