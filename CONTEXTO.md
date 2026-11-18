# Contexto para quien siga el proyecto

- **Qué es**: juego de cuidar un gato, un solo `index.html` con canvas, sin dependencias.
- **Idea**: surgió de un sueño de la hija de Leandro; desde 1.1 es de Kiut Studio y los dibujos los hace Sofía.
- **Reglas del simulador**: 5 barras del gato (hambre, felicidad, salud, limpieza, energía) + 3 del avatar. Finales: portón (se escapa), descuido (muere), vejez (14 días).
- **Tiempo**: modo `real` por defecto; `prueba` va 1 día de gato = 12 min. Al volver a abrir, `catchUp` simula lo que pasó (máx. 3 días).
- **Dibujos**: el gato son 12 poses `.webp` (+ `_n` para el gato negro "callejero"). Todo lo demás (patio, objetos) se dibuja con código; si Sofía agrega un dibujo en `assets/extra/` y figura en `assets/arte.json`, el juego lo usa en lugar del de código.
- **Convenciones del estudio**: un repo por juego, SW con prefijo propio, pruebas en `pruebas/`.
