# Cambios

## 1.3.2
- Arreglo: si el guardado quedó con números rotos (energía o afinidad vacías, escena en blanco por la versión anterior), se reparan solos al abrir.
- Arreglo: pantalla en blanco al abrir una partida guardada con una versión anterior (faltaba la afinidad). Ahora las partidas viejas reciben los valores nuevos por defecto.

## 1.3.1 — Dibujos de Sofía opcionales y detalles
- **Ajustes → Dibujos del gatito:** se puede elegir entre los dibujos de Sofía (activados por defecto) y los provisorios. La elección se guarda y no cambia al empezar con otro gatito. Los dibujos de Sofía se usan pose por pose: las que todavía no dibujó siguen con el provisorio.
- Los dibujos de Sofía ahora viven en `assets/gato_sofia/` y los provisorios quedaron intactos en `assets/gato/`. `tools/procesar_arte.py` escribe en `assets/gato_sofia/`.
- **Cuenta regresiva de los minijuegos:** el 3, 2, 1 y "¡Ya!" aparecen siempre centrados (la animación los movía de lugar).
- **Burbuja de pensamiento** (sueño, hambre, enfermo, sucio…): ahora queda arriba de la cabeza del gatito y ya no le tapa la cara.
- Pruebas nuevas para los tres puntos.

## 1.3.0 — Afinidad
- Barra nueva **💞 Afinidad** (0 a 100, **de cada gatito**; arranca en 40): cuánto te quiere.
- **Sube** con mimos (cada 45 s), jugar (más con el vóley), atenderlo cuando lo necesita y los días bien cuidados.
- **Baja** si lo descuidás (necesidades en rojo), si hace más de 8 horas que no le das cariño (darle de comer o bañarlo solo no alcanza; de noche no cuenta), si lo despertás de noche y con cada turno de trabajo (−4). Mientras no estás pierde como máximo 25 puntos.
- **Consecuencias de la afinidad baja:** por debajo de 50 los mimos valen la mitad; por debajo de 25 a veces los rechaza (😾), se queda más lejos, los juegos le suben menos la felicidad y **el portón le tienta el doble**. Avisa cuando está solo y cuando piensa en irse.
- **Final nuevo "se fue de casa"**: si la afinidad queda en 0 durante 2 días del gatito, sale por el portón y no vuelve (no se activa mientras no estás).
- **Con afinidad alta (70+):** carita de amor, juegos que rinden 20 % más y el portón le tienta menos.
- Dibujo opcional `final_abandono` para Sofía. Pruebas nuevas de afinidad.

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
