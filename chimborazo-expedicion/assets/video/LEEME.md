# Video teaser de portada

La portada (`index.html`, sección `.hero`) está preparada para reproducir un video de
fondo en bucle: el teaser promocional con tomas de dron y acción de la ruta hacia la cumbre.

## Cómo activarlo

Coloque el archivo en esta carpeta con **exactamente** estos nombres:

```
assets/video/chimborazo-teaser.mp4    (obligatorio — H.264 / AAC)
assets/video/chimborazo-teaser.webm   (opcional — VP9, mejor compresión)
```

No hace falta tocar el HTML: las etiquetas `<source>` ya apuntan a esas rutas.

## Especificaciones recomendadas

| Parámetro   | Valor sugerido                                              |
|-------------|-------------------------------------------------------------|
| Resolución  | 1920 × 1080 (o 2560 × 1440 si el peso lo permite)            |
| Duración    | 12 – 25 s en bucle limpio (el primer y último fotograma deben empatar) |
| Peso        | ≤ 6 MB — es un fondo, no una pieza de cine                   |
| Audio       | **Sin audio.** Se reproduce en silencio; elimine la pista    |
| Códec       | H.264 (`libx264`), perfil `high`, `-movflags +faststart`     |
| Encuadre    | Acción en el tercio superior/izquierdo: el texto ocupa la parte inferior |

Ejemplo de conversión con `ffmpeg`:

```bash
ffmpeg -i original.mov -an -vf "scale=1920:-2" \
       -c:v libx264 -profile:v high -crf 26 -preset slow \
       -movflags +faststart chimborazo-teaser.mp4

ffmpeg -i original.mov -an -vf "scale=1920:-2" \
       -c:v libvpx-vp9 -crf 34 -b:v 0 chimborazo-teaser.webm
```

## Qué ocurre si no hay video

Nada se rompe. `js/app.js` detecta la ausencia del archivo (o el bloqueo de
autorreproducción del navegador) y activa automáticamente un **teaser de respaldo**:
una secuencia cinematográfica de cinco fotografías reales de la ruta con efecto
Ken Burns y fundido cruzado. Ese es el estado actual del sitio.

El comportamiento también respeta `prefers-reduced-motion`: si el usuario pidió
menos animación en su sistema, se muestra una sola imagen fija.
