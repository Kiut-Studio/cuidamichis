# Cambios

## 1.1.1
- En compu y tablet el juego entra entero en la pantalla, sin scroll vertical (se achica el alto del juego y, en pantallas bajitas, se oculta el cartelito).

## 1.1.0 — pasa a Kiut Studio y se llama Cuidamichis
**Juego**
- Nuevo patio: casa con chimenea y ventana que se prende de noche, cerca, farol, calle con autos, sol/luna/estrellas/nubes, mariposas de día y luciérnagas de noche.
- Noche con luz real (farol y ventana iluminan); efectos de zzz, chispas y gota de susto.
- Celular acostado: patio a la izquierda, cuidados a la derecha.
- Minijuegos con fondo y objetos dibujados con código; pantalla final nueva.
- Variantes de color hechas por píxel: ya no depende de `ctx.filter` (Safari).
- Créditos dinámicos (cambian solos cuando lleguen los dibujos de Sofía).

**Errores corregidos**
- Premios de frutillas después de morir el gato.
- Minijuego que seguía abierto al terminar la partida.
- Cartel de "creció" tapado por otra ventana.
- Reloj del celular adelantado congelaba el tiempo.
- Gato "dormido" al esconder la app; gato sin nombre al arrancar.
- Botón del portón tapaba al gatito en pantallas chicas.
- Tipografías ya no dependen de Google Fonts.

**Estructura**: manifest con `id`/`scope`, service worker por prefijo, `tools/construir.py`, 125 pruebas automáticas, documentación.

## 1.0.0
Primera versión (dibujos provisorios con Meta AI).
