# Íconos dibujados para Cuidamichis (reemplazo de emojis)

Hoy el juego usa ~95 emojis distintos. Esta guía lista los que conviene dibujar (63 íconos, en 7 hojas de 9) y trae los prompts listos para pegar en Meta AI (o cualquier generador de imágenes).

## Reglas para todas las hojas
- **Formato:** cuadrada, 1024×1024 mínimo (2048 mejor), **fondo blanco liso**, 3 columnas × 3 filas = 9 íconos separados, cada uno centrado en su casilla con bastante aire alrededor.
- **Sin** texto, marcos, sombras, degradados ni líneas de cuadrícula.
- **Orden de lectura:** izquierda → derecha, arriba → abajo. Ese orden es el que se usa para cortar y nombrar cada ícono, así que no hay que reordenar nada.
- **Nombre del archivo:** `hoja1_estado.png`, `hoja2_objetos.png`, etc. (ver cada hoja) y dejarlas en `arte/iconos/`.
- **Consistencia:** una vez que una hoja salga bien, pasarla como imagen de referencia a las siguientes ("same exact style, line thickness and palette as the attached image"). También sirve adjuntar un dibujo del gato de Sofi como referencia de estilo.
- Si el generador se equivoca con la cantidad, repetir pidiendo "exactly 9 icons"; si falla un solo ícono, regenerarlo solo (ver "Un ícono suelto" abajo).

## Prompt base (se pega al principio de cada hoja)

```
Cute kawaii hand-drawn icon sticker sheet. Thick, slightly wobbly black marker outlines (same thickness on every icon), flat bright colors with at most one slightly darker tone for shading, a small white highlight spot on each shiny object, no gradients, no realistic textures, no drop shadows, no text, no letters, no frames, no grid lines. Chunky rounded simple shapes, like a child's drawing made with a thick pen. Palette: warm orange, strawberry pink, sky blue, leaf green, butter yellow, cream and black outlines. Plain pure white background.
Layout: square image with a 3 columns by 3 rows grid of exactly 9 completely separate icons, each centered in its own cell with generous white space around it (at least 15% margin), nothing touching, overlapping or cut by the image edges. Each icon is one single object seen from the front.
Icons, left to right, top to bottom:
```

Después del prompt base se pega la lista de la hoja (abajo).

## Un ícono suelto (para rehacer uno que salió mal)
```
Cute kawaii hand-drawn icon, thick slightly wobbly black marker outline, flat bright colors, small white highlight, no gradients, no shadow, no text, plain pure white background, one single object centered with generous margin, same style as the attached image: <DESCRIPCIÓN>
```

---

## Hoja 1 — Barras y estado (`hoja1_estado.png`) · prioridad 1
Se ven todo el tiempo en las barras del gatito y del avatar.
```
1) a cooked chicken drumstick with a bone (food)
2) a happy orange cat face with closed smiling eyes and pink blush (happiness)
3) a plump red heart with a small white highlight (health)
4) three light-blue soap bubbles of different sizes (cleanliness)
5) three blue letters "Z z z" stacked and getting bigger, sleeping (energy)
6) two pink hearts touching, one big and one small (affinity)
7) a pink bar of soap with white foam bubbles on top (hygiene)
8) a small rainbow over two white clouds (mood)
9) a sick orange cat face with a thermometer in its mouth and a slightly green tint (sick)
```
Ids: `comida, felicidad, salud, limpieza, energia, afinidad, higiene, animo, enfermo`

## Hoja 2 — Objetos del patio y juguetes (`hoja2_objetos.png`) · prioridad 1
Sirven como ícono de la tienda **y** como dibujo dentro del patio (ya existen como "extras" opcionales: `tazon, cama, pelota, lana, pescado, gota, caca, corazon`).
```
1) a pink cat food bowl filled with brown kibble (seen slightly from above)
2) a round soft pink cat bed with a fluffy cushion
3) a small yellow-green cat toy ball with curved stitch lines
4) a pink ball of yarn with a loose thread curling out
5) a cute small blue fish, side view, with a smiling little face-less body (tuna)
6) a little grey toy mouse with big pink ears and a long curly tail
7) a swirly brown pile of poop, cute and simple, no face
8) a light-blue sweat drop with a white highlight
9) a pink heart with two tiny sparkles
```
Ids: `tazon, cama, pelota, lana, pescado, raton, caca, gota, corazon`
(`pescado` es también el ícono del atún de la tienda.)

## Hoja 3 — Ropa (`hoja3_ropa.png`) · prioridad 1
Hay que dibujarlas **de frente y con la base plana o apenas curva**, para que apoyen sobre la cabeza del gatito. Los mismos dibujos se usan como ropa puesta (`ropa_*`) y como ícono de la tienda.
```
1) a pink ribbon bow with two loops and a small knot (hair bow)
2) a pink flower with five round petals and a yellow center
3) a black top hat with a pink band
4) a golden crown with three points and tiny colored jewels
5) a red baseball cap, front view, short visor
6) light-blue headphones, front view, the band arching over the top
7) a straw hat with a wide brim and a red ribbon
8) a brown cowboy hat with a curved brim
9) a black graduation cap with a yellow tassel
```
Ids: `mono, flor, galera, corona, gorra, auris, paja, vaquero, birrete`

## Hoja 4 — Tienda, acciones y lugares (`hoja4_acciones.png`) · prioridad 1
```
1) a small glass bottle of milk with a pink heart label
2) a small bottle of medicine with a pink cross on the label
3) a pump bottle of cat shampoo, light blue, with a few bubbles
4) a bathtub full of white foam with a rubber duck
5) a shower head with water drops falling
6) a brown briefcase with a golden clasp (work)
7) a pink cupcake with a strawberry on top (shop)
8) a cute pink backpack (bag)
9) a wooden garden gate with two doors, orange wood, small round knobs
```
Ids: `leche, remedio, jabon, banar, ducha, trabajar, tienda, mochila, porton`

## Hoja 5 — Minijuegos y trabajo (`hoja5_juegos.png`) · prioridad 2
```
1) a pink wrapped candy with twisted ends
2) a soda cup with a lid and a straw
3) a golden bread roll
4) a brown cardboard box with tape
5) an orange traffic cone with a white stripe
6) a volleyball with blue and yellow panels
7) a tiny kiosk stand with a striped red and white awning
8) a simple bicycle, side view, with a small basket
9) a golden trophy cup with a star
```
Ids: `caramelo, bebida, pan, paquete, cono, pelota_voley, kiosco, bici, trofeo`

## Hoja 6 — Avisos, clima y burbujas (`hoja6_avisos.png`) · prioridad 2
```
1) a red heart broken in two pieces
2) an angry orange cat face with grumpy eyebrows
3) a sad orange cat face with a single blue tear
4) a yellow crescent moon with a tiny star
5) a smiling sun with short rays
6) a red and orange flame (streak)
7) a pink cat paw print with four toe beans and one big pad
8) a yellow warning triangle with an exclamation mark
9) a yellow light bulb with small shine lines
```
Ids: `corazon_roto, gato_enojado, gato_triste, luna, sol, llama, huella, advertencia, luz`

## Hoja 7 — Interfaz (`hoja7_interfaz.png`) · prioridad 3
```
1) two beamed musical notes
2) a blue circle with a white lowercase letter "i" (info)
3) a grey gear (settings)
4) a speaker with three sound waves
5) a speaker with a red X (muted)
6) a cute running rabbit, side view (fast)
7) a cute walking turtle, side view (slow / real time)
8) a calendar page with a small pink heart
9) a small pink house with a red roof and a round window
```
Ids: `musica, info, ajustes, sonido, silencio, rapido, lento, calendario, casa`

---

## Qué NO hace falta dibujar
- `🍓` y el pancito: ya existen dibujados por Sofía (`assets/frutilla.webp`, `assets/pancito.webp`).
- `✕ ↺ ✔ 👆`: se pueden dejar como símbolos.
- Los emojis de los **créditos** y de textos sueltos pueden quedar como están.

## Cómo se van a usar (plan técnico)
1. `tools/cortar_iconos.py` (todavía no existe): corta cada hoja en 3×3, saca el fondo blanco, recorta y guarda cada ícono en `assets/iconos/<id>.webp`.
2. El juego usa el ícono dibujado si existe y **si no, el emoji de siempre**, así se puede ir agregando hoja por hoja sin romper nada.
3. Opción en Ajustes (como la de los dibujos de Sofía) para elegir "Íconos dibujados" o "Emojis".
