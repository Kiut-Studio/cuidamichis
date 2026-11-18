# Guía para los dibujos de Sofía

## Cómo entregar
1. Dibujar cada pose en fondo transparente (PNG), **cuadrado o apaisado**, mismo tamaño y mismo trazo negro grueso que el estilo actual.
2. Guardar en `arte/entrada/` con el nombre exacto de la lista (ej. `feliz.png`).
3. Correr `python3 tools/procesar_arte.py` → convierte a `.webp`, crea la versión del gato negro (`_n`) y actualiza `assets/arte.json`.
4. Correr `python3 tools/construir.py` y `python3 pruebas/juego.py`.

## Poses del gato (obligatorias, 12)
`feliz`, `contento`, `triste`, `hambre`, `comiendo`, `jugando`, `banio`, `miedo`, `enfermo`, `bostezo`, `dormido1`, `dormido2`
(el gato mira a la izquierda en las poses sentadas; las dormidas son más bajas que anchas).

## Opcionales (si no están, el juego usa su dibujo de código)
`tazon`, `cama`, `pelota`, `lana`, `pescado`, `gota`, `caca`, `corazon`, `final_vejez`, `final_descuido`, `final_porton`, `ropa_<nombre>`.

## Para tener en cuenta
- Los dibujos de los avatares y la frutilla ya son de Sofía.
- Nombres sin tildes ni espacios, en minúsculas.
