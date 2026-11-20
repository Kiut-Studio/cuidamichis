# Guía para los dibujos de Sofía

## Cómo entregar
1. Dibujar cada pose en fondo transparente (PNG), **cuadrado o apaisado**, mismo tamaño y mismo trazo negro grueso que el estilo actual.
2. Guardar en `arte/entrada/` con el nombre exacto de la lista (ej. `feliz.png`).
3. Correr `python3 tools/procesar_arte.py` → convierte a `.webp`, crea la versión del gato negro (`_n`) y actualiza `assets/arte.json`.
4. Correr `python3 tools/construir.py` y `python3 pruebas/juego.py`.

## Poses del gato (obligatorias, 12)
`feliz`, `contento`, `triste`, `hambre`, `comiendo`, `jugando`, `banio`, `miedo`, `enfermo`, `bostezo`, `dormido1`, `dormido2`
(el gato mira a la izquierda en las poses sentadas; las dormidas son más bajas que anchas).

## Retratos por edad (4) y caritas (6)
`edad_bebe`, `edad_joven`, `edad_adulto`, `edad_abuelo` y `cara_feliz`, `cara_amor`, `cara_enojo`, `cara_sorpresa`, `cara_triste`, `cara_sueno`. Se procesan igual que las poses.

(Hay una hoja para imprimir con todo: `docs/hoja_sofi.pdf`.)

## Opcionales (si no están, el juego usa su dibujo de código)
`tazon`, `cama`, `pelota`, `lana`, `pescado`, `gota`, `caca`, `corazon`, `final_vejez`, `final_descuido`, `final_porton`, `ropa_<nombre>`.
Ropa que hay hoy en la tienda: `ropa_mono`, `ropa_flor`, `ropa_galera`, `ropa_corona` y las de trabajo `ropa_gorra`, `ropa_auris`, `ropa_paja`, `ropa_vaquero`, `ropa_birrete`.

## Para tener en cuenta
- Los dibujos de los avatares y la frutilla ya son de Sofía.
- Nombres sin tildes ni espacios, en minúsculas.
