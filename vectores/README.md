# SOFTWARE DE VECTORES — Álgebra

Página web del tema **Vectores** (Habilidades Lógico Matemáticas · PUCE).
Paleta: **rojo / negro / celeste**.

## Archivos

| Archivo | Qué contiene | Dónde pegarlo en VS Code |
|---|---|---|
| `index.html` | Estructura de la página (encabezado, formularios, secciones, tablas) | Archivo nuevo llamado `index.html` |
| `estilos.css` | Todo el diseño: colores, tarjetas, botones, tabla, responsive | Archivo nuevo llamado `estilos.css` |
| `script.js` | Toda la lógica: cálculos, procedimiento paso a paso y la gráfica | Archivo nuevo llamado `script.js` |

## Cómo usarlo en VS Code

1. Crea una carpeta, por ejemplo `vectores`.
2. Dentro crea los tres archivos con **exactamente esos nombres**:
   `index.html`, `estilos.css` y `script.js`.
3. Copia y pega el contenido de cada archivo en el que le corresponde.
4. Abre `index.html` en el navegador (o usa la extensión **Live Server**).

> Los tres archivos deben quedar en la **misma carpeta**. El `index.html`
> ya los llama así:
>
> ```html
> <link rel="stylesheet" href="estilos.css">   <!-- línea 7 -->
> <script src="script.js"></script>            <!-- al final del body -->
> ```
>
> Si les cambias el nombre, cambia también esas dos líneas.

## Si la página se ve bien pero la gráfica y el procedimiento salen vacíos

Significa que **`script.js` no se cargó**. La página te lo avisa sola con un
recuadro rojo al final. Causas más comunes:

1. El archivo no se llama exactamente `script.js` (revisa `script.js.txt`,
   `Script.js`, `scrip.js`). En VS Code: clic derecho → *Rename*.
2. Está en otra carpeta. Los tres archivos van **juntos**.
3. El pegado quedó incompleto. `script.js` debe empezar con
   `const $ = id => document.getElementById(id);` y terminar con `resolver();`
4. Presiona **F12** → pestaña **Console** para ver el error exacto.

## Qué hace la página

- **Ingreso de datos:** componentes x, y del vector A⃗ y del vector B⃗, más un escalar k.
- **9 operaciones:** suma, resta, k·A⃗, producto punto, ángulo entre vectores,
  magnitud y dirección, vector unitario, proyección y producto cruz (área).
- **Gráfica interactiva:** plano cartesiano, flechas, método del paralelogramo,
  componentes rectangulares, arco del ángulo, proyección, zoom y centrar.
- **Procedimiento paso a paso:** fórmula → sustitución → operación → resultado final.
- **Tabla resumen** con las 12 operaciones y **6 ejemplos resueltos** que se cargan
  con un clic.
- **Fundamento teórico** con todas las fórmulas del tema.
- **Logo institucional:** clic en el recuadro del encabezado para cargar la imagen.

## Nota

En la raíz del repositorio está también `software-vectores-puce.html`, que es
la **misma página en un solo archivo** (HTML + CSS + JS juntos), por si se
necesita enviarla o abrirla sin carpetas.
