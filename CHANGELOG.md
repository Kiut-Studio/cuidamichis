# Cambios

## 1.2.0 — Trabajo, vóley y ropa nueva
- **Trabajar** (pestaña "Vos"): salís a trabajar, jugás un turno de minijuego (**El kiosco** o **Reparto**) y ganás 🍓 (más que jugando con el gatito).
  - Cuesta: −18 comida, −12 higiene, −12 ánimo, y el gatito te extraña (−6 felicidad). El ánimo solo se recupera jugando con él.
  - No se puede salir con el portón abierto, de noche, con poco hambre/higiene/ánimo ni si el gatito está enfermo.
  - **Al volver, el portón queda abierto** y hay que cerrarlo: así el portón tiene un motivo y el riesgo de siempre se mantiene. Si se cierra la app en pleno turno, no queda nada abierto.
- **Vóley juntos** (en "Jugar"): una actividad con el gatito. Tocás cuando la pelota llega a vos (3 vidas); da felicidad al gatito y más ánimo que los otros juegos.
- **Ropa nueva** para ahorrar con el trabajo: gorra (90 🍓), auriculares (130), sombrero de paja (160), sombrero vaquero (200) y birrete (260). Sofía puede dibujarlas como `ropa_gorra`, `ropa_auris`, `ropa_paja`, `ropa_vaquero`, `ropa_birrete`.
- Pruebas nuevas (trabajo y vóley) y tienda actualizada.

## 1.1.2
- Hoja imprimible para Sofía (docs/hoja_sofi.pdf) y el procesador de dibujos ahora también acepta retratos por edad y caritas.

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
