# Expedición Cumbre Chimborazo — Propuesta comercial y operativa

Sitio de una sola página con la propuesta comercial y operativa completa de la
expedición al volcán Chimborazo (6.268 m) de **Chimborazo Rey · Travel Explore**.

Construido en HTML, CSS y JavaScript puros, sin dependencias ni proceso de compilación.

## Estructura

```
chimborazo-expedicion/
├── index.html            Marcado completo de la propuesta
├── css/estilos.css       Hoja de estilos (paleta, componentes, responsive, impresión)
├── js/app.js             Comportamiento (portada, galería, cotizador, formulario…)
└── assets/
    ├── img/              Fotografías del archivo del cliente, optimizadas
    └── video/            Teaser de portada (ver LEEME.md de esa carpeta)
```

## Cómo verlo

Abrir `index.html` directamente en el navegador, o servirlo:

```bash
cd chimborazo-expedicion
python3 -m http.server 8000
# http://localhost:8000
```

## Secciones

| # | Sección        | Contenido |
|---|----------------|-----------|
| — | Portada        | Video de fondo (con teaser de respaldo), título, eslogan y cifras clave |
| 01| La montaña     | El punto más cercano al sol, campo base a 4.250 m, exigencia real |
| 02| Galería        | Las 10 imágenes estratégicas del paquete, con filtros y visor |
| 03| Alimentación   | Desayuno pre-ascenso, box lunch de marcha y cena de recuperación |
| 04| Itinerario     | Cronograma hora por hora, de El Arenal a la cumbre y el retorno |
| 05| Equipo y seguridad | Equipo incluido, qué traer, ratios de guía y políticas |
| 06| Inversión      | Tarifario y cotizador interactivo |
| 07| Preguntas frecuentes | Objeciones habituales de venta |
| 08| Reserva        | Formulario validado con salida a correo y a WhatsApp |

## Funcionalidad del JavaScript

- **Portada**: reproduce `assets/video/chimborazo-teaser.mp4|webm` si existe. Si el
  archivo falta o el navegador bloquea la autorreproducción, activa un teaser de
  respaldo: cinco fotografías reales con efecto Ken Burns y fundido cruzado.
- **Navegación**: barra de progreso de lectura, fondo sólido al desplazar,
  resaltado de la sección activa y menú móvil.
- **Galería**: filtros por categoría y visor con teclado (`←`, `→`, `Esc`),
  bloqueo de scroll y devolución del foco al cerrar.
- **Cotizador**: calcula el estimado según número de montañistas y complementos,
  y traslada el número de personas al formulario de reserva.
- **Formulario**: validación en vivo campo por campo; genera el mensaje de
  solicitud y lo envía por `mailto:` o por WhatsApp (`wa.me`).
- **Accesibilidad**: pestañas y acordeón operables por teclado, `aria-*`
  coherentes, enlace de salto al contenido y respeto por `prefers-reduced-motion`.

## Puntos de edición frecuentes

| Qué cambiar | Dónde |
|---|---|
| Teléfono, correo, empresa | `js/app.js` → objeto `CONTACTO` (y enlaces en el HTML) |
| Precio base de la expedición | `js/app.js` → constante `BASE`, y la tabla en `index.html` |
| Complementos del cotizador | `index.html` → `.cot-extra` (`data-precio`, `data-nombre`) |
| Paleta de color | `css/estilos.css` → bloque `:root` |
| Video de portada | `assets/video/` → ver `LEEME.md` |

## Notas sobre el contenido

Todos los datos operativos —altitudes, duraciones, terreno, equipo incluido,
lista de qué llevar, itinerario, tarifas y datos de contacto— provienen de la
documentación entregada por el cliente.

Los siguientes puntos son **propuestas** que conviene confirmar antes de publicar:

- Ratios de guía (1:2 estándar, 1:1 opcional, máximo 6 por salida).
- Política de reserva (50 % de anticipo) y de reprogramación.
- Ventanas climáticas recomendadas (diciembre–enero, junio–septiembre).
- Horas concretas del itinerario del día 1 (encuentro, prueba de equipo, cena):
  la documentación fija las horas del ascenso (22:00, 23:00) pero no las previas.
- Las imágenes 08 (placa geodésica IGM 1955) y 09 (monolito de El Arenal) se
  muestran como ilustración vectorial porque no había fotografía disponible en
  el archivo entregado. Basta sustituir el bloque `<div class="arte">` por un
  `<img>` cuando se disponga de la foto.
