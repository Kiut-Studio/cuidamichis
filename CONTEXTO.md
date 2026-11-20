# Contexto para quien siga el proyecto

- **Qué es**: juego de cuidar un gato, un solo `index.html` con canvas, sin dependencias.
- **Idea**: surgió de un sueño de la hija de Leandro; desde 1.1 es de Kiut Studio y los dibujos los hace Sofía.
- **Reglas del simulador**: 5 barras del gato (hambre, felicidad, salud, limpieza, energía) + 3 del avatar. Finales: portón (se escapa), descuido (muere), vejez (14 días).
- **Tiempo**: modo `real` por defecto; `prueba` va 1 día de gato = 12 min. Al volver a abrir, `catchUp` simula lo que pasó (máx. 3 días).
- **Dibujos**: el gato son 12 poses `.webp` (+ `_n` para el gato negro "callejero"). Todo lo demás (patio, objetos) se dibuja con código; si Sofía agrega un dibujo en `assets/extra/` y figura en `assets/arte.json`, el juego lo usa en lugar del de código.
- **Trabajo (1.2)**: el avatar sale a trabajar (kiosco/reparto), paga 🍓 pero gasta comida/higiene/ánimo y baja la felicidad del gato; al volver el portón queda abierto y hay que cerrarlo. El vóley es una actividad juntos dentro de "Jugar". La ropa cara (gorra…birrete) es la meta de ahorro.
- **Convenciones del estudio**: un repo por juego, SW con prefijo propio, pruebas en `pruebas/`.
