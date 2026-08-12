# Chimborazo Rey — Sitio web

Sitio turístico de **Chimborazo Rey**, en el sector Cruz del Arenal (vía Guaranda – Ambato),
cantón Guaranda, provincia de Bolívar, Ecuador, a una altitud aproximada de 4.250 m s. n. m.

Desarrollado con **HTML5, CSS3 y JavaScript Vanilla (ES6+)**. Sin frameworks, sin dependencias
y sin proceso de compilación: se abre directamente con Live Server o cualquier servidor estático.

---

## 1. Cómo abrirlo

```
# Con Live Server (VS Code): clic derecho sobre index.html → "Open with Live Server"

# O con cualquier servidor estático:
npx serve chimborazo-rey
python3 -m http.server 8000
```

También funciona abriendo `index.html` directamente en el navegador.

---

## 2. Estructura

```
chimborazo-rey/
├── index.html            Inicio / presentación
├── restaurante.html      Restaurante de Aventura
├── lodge.html            Lodge Hotel
├── travel.html           Travel Explore
│
├── css/
│   ├── global.css        Sistema de diseño: tokens, navbar, footer, botones,
│   │                     formularios, galería, modales y animaciones
│   ├── inicio.css        Identidad: nieve, piedra, beige y café suave
│   ├── restaurante.css   Identidad: fuego, naranja, madera
│   ├── lodge.css         Identidad: café, beige, dorado suave
│   └── travel.css        Identidad: azul montaña, celeste glaciar, verde
│
├── js/
│   ├── main.js           Núcleo compartido (espacio de nombres `CR`)
│   ├── idiomas.js        Diccionario de traducciones (ES · EN · FR · DE)
│   ├── restaurante.js    Menú filtrable y reserva de mesa
│   ├── lodge.js          Habitaciones, cálculo de noches y solicitud de hospedaje
│   └── travel.js         Actividades, modal de detalle y consultas
│
├── images/               Fotografías por sección (actualmente placeholders)
│   ├── inicio/  restaurante/  lodge/  travel/
│
└── assets/
    ├── generar-placeholders.js   Genera las imágenes temporales
    └── verificar-idiomas.js      Comprueba la paridad de los cuatro idiomas
```

Orden de carga en cada página: `idiomas.js` → `main.js` → script de la página, todos con `defer`.

---

## 3. Sistema multiidioma

Cuatro idiomas: **Español (por defecto)**, English, Français y Deutsch.
No existen copias del HTML por idioma: todos los textos se traducen desde `js/idiomas.js`.

**Atributos disponibles en el HTML**

| Atributo                   | Efecto                                    |
|----------------------------|-------------------------------------------|
| `data-i18n`                | Reemplaza el `textContent`                |
| `data-i18n-html`           | Reemplaza el `innerHTML` (texto con marcado) |
| `data-i18n-placeholder`    | Atributo `placeholder`                    |
| `data-i18n-aria-label`     | Atributo `aria-label`                     |
| `data-i18n-alt`            | Atributo `alt`                            |
| `data-i18n-title`          | Atributo `title`                          |
| `data-i18n-content`        | Atributo `content` (metaetiquetas SEO)    |

El `<title>` de cada página se toma de `data-title-key` en la etiqueta `<html>`.

El idioma elegido se guarda en `localStorage` (`chimborazo-rey-lang`), de modo que se mantiene
al navegar entre las cuatro páginas. Los nombres propios (Chimborazo Rey, Cruz del Arenal,
Guaranda, Bolívar, Carihuairazo) no se traducen.

**Añadir o cambiar un texto**

1. Añade la clave en los cuatro idiomas dentro de `js/idiomas.js`.
2. Referencia la clave desde el HTML con `data-i18n="tu.clave"`.
3. Comprueba que no falte ninguna traducción:

```
node assets/verificar-idiomas.js
```

El verificador recorre los HTML y los JS, extrae todas las claves en uso y comprueba que existan
en los cuatro idiomas. Actualmente: **485 claves × 4 idiomas, sin errores**.

---

## 4. Color

El fondo general del sitio sigue siendo blanco. El color entra por cuatro vías:

- **La marca.** «Chimborazo» va en el color del soporte y **«Rey» siempre en dorado**
  (`--color-gold` sobre fotografías, `--color-gold-deep` sobre blanco), en el navbar,
  el hero y el footer de las cuatro páginas. La clase es `.brand-accent`.
- **Las secciones alternas** (`.section--surface`) toman un tinte muy suave del color de
  su página: crema en Restaurante, beige dorado en Lodge y celeste en Travel Explore.
- **Las tarjetas de valores** de la portada tienen cada una su propio color —verde páramo,
  azul cielo, fuego, dorado y terracota— en el icono y en un degradado de fondo que se
  desvanece hacia el blanco.
- **La banda final de llamada a la acción** se tiñe con el color secundario de cada página.

Tres tokens gradúan la intensidad y evitan que dos superficies se confundan:

| Token                   | Uso                                                              |
|-------------------------|------------------------------------------------------------------|
| `--color-primary-soft`  | Fondo de las secciones alternas y de los iconos                   |
| `--color-primary-mid`   | Bloques que se apoyan **sobre** una sección ya teñida             |
| `--color-primary`       | Botones, enlaces, antetítulos y bordes activos                    |

Todos los colores de texto se eligieron para superar la relación de contraste 4,5:1 de
WCAG AA sobre el fondo donde realmente se muestran, tintes incluidos.

---

## 5. Contenido pendiente de cargar

El sitio está completo y funcional, pero hay datos que **no se han inventado** porque no constan
en la documentación disponible. Cada uno está marcado en el código y es fácil de reemplazar.

| Qué falta | Dónde se edita |
|-----------|----------------|
| **Platos y precios del menú** | `js/restaurante.js` → arreglo `MENU_ITEMS`. Hoy genera 2 tarjetas de marcador por categoría. El comentario del archivo incluye un ejemplo listo para copiar. Al cargar la carta real, elimina también la nota temporal `.menu-note` de `restaurante.html`. |
| **Fotografías** | `images/inicio/`, `images/restaurante/`, `images/lodge/`, `images/travel/`. Sustituye cada SVG por la foto real conservando el nombre de archivo (o actualiza la ruta en el HTML). La portada (`images/inicio/hero-chimborazo.jpg`) ya es una fotografía real; el resto siguen siendo placeholders. |
| **Mapa de Google Maps** | `index.html`, sección `#ubicacion`: sustituye el bloque `.map-frame` por el iframe oficial del negocio. No se incluyeron coordenadas porque no constan en la documentación. |
| **Redes sociales** | Los cuatro `footer`: los enlaces `href="#"` de Facebook, Instagram y TikTok esperan las URL oficiales. No se inventaron nombres de usuario. |
| **Tarifas de habitaciones** | `lodge.html`: las tarjetas muestran «Tarifa disponible bajo consulta» porque la documentación no especifica precios. |
| **Duración, altitud, punto de encuentro, terreno e itinerario de cada actividad** | `js/travel.js` → arreglo `ACTIVITIES`. Los campos con valor `null` se muestran como pendientes en el modal. Las listas `itinerary` y `bring` están vacías: al añadirles claves, sus secciones aparecen automáticamente. |
| **Niveles de dificultad** | `js/travel.js`. Los niveles mostrados son referenciales y deben confirmarse con la documentación oficial; el sitio lo advierte bajo la leyenda de niveles. |

> **Nota sobre la portada.** La fotografía del hero mide 1290 × 727 px. En pantallas de 1920 px se
> amplía alrededor de 1,6×, por lo que puede verse ligeramente menos nítida. Si dispones del archivo
> original de la cámara, sustitúyelo por una versión de ~2400 px de ancho y actualiza los atributos
> `width` y `height` de la etiqueta `<img>` del hero en `index.html`.

### Datos reales ya incorporados

- Contacto: Guido Castro · 0968596592 · gustavocc1982@hotmail.com
- Ubicación: Cruz del Arenal, vía Guaranda – Ambato, Guaranda, Bolívar, Ecuador · ~4.250 m s. n. m.
- Restaurante: cocina nacional e internacional, opciones veganas y vegetarianas, coffee shop,
  cerveza artesanal Chimborazo Rey, amplios salones; pagos con tarjeta, efectivo y transferencia.
- Lodge: habitaciones familiares, grupales y matrimoniales; calefacción, seguridad 24 h, cámaras,
  internet, TV por cable, área de cocina, sala de estar, paquetes turísticos y vista al nevado.
- Travel Explore: Cumbre Chimborazo ($300), Cumbre Central Carihuairazo ($140), cabalgatas
  ($35 – $60), descenso en bicicleta ($50) y trekking nocturno (sin precio publicado).

Los datos de contacto se centralizan en la constante `CONTACT` de `js/main.js`: al cambiarlos ahí
se actualizan todos los enlaces de llamada, WhatsApp, correo e indicaciones de las cuatro páginas.

---

## 6. Formularios

El sitio es estático y **no tiene backend**. Los tres formularios (reserva de mesa, solicitud de
hospedaje y consulta de actividades):

1. Validan los datos en el navegador, con mensajes de error traducidos a los cuatro idiomas.
2. Al enviarlos, abren WhatsApp con un mensaje prellenado que resume la solicitud.
3. No almacenan ni envían información por su cuenta. Así se indica al usuario en cada formulario.

Si más adelante se añade un servidor, basta con sustituir la llamada a `openWhatsApp()` dentro de
`initForm()` en `js/main.js` por el `fetch` correspondiente.

---

## 7. Accesibilidad y rendimiento

- HTML semántico, un único `<h1>` por página y jerarquía de encabezados sin saltos.
- Contraste WCAG AA verificado en los 445 textos del sitio, sobre fondos blancos y teñidos.
- `alt` descriptivo y traducido en todas las imágenes; `label` en todos los campos de formulario.
- Navegación completa por teclado: menú, selector de idioma, galería y modales; foco visible,
  cierre con `Escape`, foco atrapado dentro de las superposiciones y enlace «saltar al contenido».
- `aria-expanded`, `aria-current`, `aria-pressed`, `aria-selected` y `aria-live` donde corresponde.
- `@media (prefers-reduced-motion: reduce)` desactiva animaciones y desplazamiento suave.
- `loading="lazy"`, `width`/`height` y `decoding="async"` en las imágenes fuera del hero.
- Animaciones con `IntersectionObserver`, limitadas a `transform` y `opacity`.
- Sin scroll horizontal de 320 px a 1920 px.

---

## 8. Utilidades

```
node assets/verificar-idiomas.js     # paridad de traducciones en los 4 idiomas
node assets/generar-placeholders.js  # regenera las imágenes temporales
```
