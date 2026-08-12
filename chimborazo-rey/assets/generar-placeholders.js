/**
 * Generador de imágenes placeholder (SVG) para Chimborazo Rey.
 * -----------------------------------------------------------------------------
 * Estas imágenes son TEMPORALES. Se deben reemplazar por las fotografías reales
 * de Chimborazo Rey conservando el mismo nombre de archivo (o actualizando la
 * ruta en el HTML correspondiente).
 *
 * Uso:  node assets/generar-placeholders.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', 'images');

/* Paletas por sección: [cielo alto, cielo bajo, montaña lejana, montaña cerca, base] */
const PALETTES = {
  inicio: ['#eef1f4', '#dcd7cd', '#b9b2a6', '#8a8177', '#5d564e'],
  restaurante: ['#fdf3e9', '#f6e0c8', '#e0a86a', '#b4703a', '#7b4b2a'],
  lodge: ['#fbf6ee', '#f0e4d1', '#d9bd93', '#ab8557', '#6a4b32'],
  travel: ['#eef6fb', '#d5e9f5', '#9dc6e0', '#5б8fb3', '#2c5470']
};
PALETTES.travel[3] = '#5b8fb3';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/**
 * Construye un SVG con silueta de montaña nevada y una etiqueta discreta.
 */
function buildSvg({ w, h, palette, label, snow = true, seed = 1 }) {
  const [skyTop, skyBottom, far, near, base] = palette;
  const r = (n) => Math.abs(Math.sin(seed * n) * 10000) % 1;

  const peak = w * (0.36 + r(1) * 0.22);
  const peakY = h * (0.24 + r(2) * 0.14);
  const peak2 = w * (0.74 + r(3) * 0.16);
  const peak2Y = h * (0.42 + r(4) * 0.12);
  const horizon = h * 0.78;

  const farPath =
    `M0 ${h} L0 ${h * 0.62} ` +
    `L${w * 0.18} ${h * 0.5} L${w * 0.3} ${h * 0.58} ` +
    `L${peak2.toFixed(1)} ${peak2Y.toFixed(1)} L${w} ${h * 0.6} L${w} ${h} Z`;

  const nearPath =
    `M0 ${h} L0 ${horizon.toFixed(1)} ` +
    `L${(peak * 0.42).toFixed(1)} ${(h * 0.6).toFixed(1)} ` +
    `L${peak.toFixed(1)} ${peakY.toFixed(1)} ` +
    `L${(peak * 1.55).toFixed(1)} ${(h * 0.66).toFixed(1)} ` +
    `L${w} ${(h * 0.72).toFixed(1)} L${w} ${h} Z`;

  const snowPath = snow
    ? `<path d="M${(peak - w * 0.09).toFixed(1)} ${(peakY + h * 0.13).toFixed(1)} ` +
      `L${peak.toFixed(1)} ${peakY.toFixed(1)} ` +
      `L${(peak + w * 0.11).toFixed(1)} ${(peakY + h * 0.15).toFixed(1)} ` +
      `L${(peak + w * 0.045).toFixed(1)} ${(peakY + h * 0.1).toFixed(1)} ` +
      `L${(peak + w * 0.015).toFixed(1)} ${(peakY + h * 0.15).toFixed(1)} ` +
      `L${(peak - w * 0.03).toFixed(1)} ${(peakY + h * 0.09).toFixed(1)} Z" fill="#ffffff" opacity=".92"/>`
    : '';

  /* Etiqueta discreta en una esquina: identifica el placeholder sin competir
     con el contenido superpuesto (títulos del hero, indicador de scroll…). */
  const fontSize = Math.min(20, Math.max(12, Math.round(w * 0.02)));
  const padX = fontSize * 0.9;
  const tagW = label.length * fontSize * 0.54 + padX * 2;
  const tagH = fontSize * 2.1;
  /* Centrada horizontalmente: es la zona que `object-fit: cover` nunca recorta. */
  const tagX = (w - tagW) / 2;
  const tagY = h * 0.08;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${esc(label)}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${skyTop}"/>
      <stop offset="1" stop-color="${skyBottom}"/>
    </linearGradient>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${near}"/>
      <stop offset="1" stop-color="${base}"/>
    </linearGradient>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#sky)"/>
  <circle cx="${(w * 0.8).toFixed(0)}" cy="${(h * 0.2).toFixed(0)}" r="${(h * 0.075).toFixed(0)}" fill="#ffffff" opacity=".55"/>
  <path d="${farPath}" fill="${far}" opacity=".75"/>
  <path d="${nearPath}" fill="url(#ground)"/>
  ${snowPath}
  <rect x="${tagX}" y="${tagY}" width="${tagW.toFixed(0)}" height="${tagH.toFixed(0)}" rx="${(tagH / 2).toFixed(0)}"
        fill="#000000" opacity=".38"/>
  <text x="${(w / 2).toFixed(0)}" y="${(tagY + tagH * 0.68).toFixed(0)}" text-anchor="middle"
        font-family="Georgia, serif" font-size="${fontSize}" fill="#ffffff" opacity=".9"
        letter-spacing="1">${esc(label)}</text>
</svg>`;
}

/* Definición de todas las imágenes del sitio. */
const IMAGES = {
  inicio: [
    /* hero-chimborazo: ya es una fotografía real (images/inicio/hero-chimborazo.jpg),
       por eso no se genera ningún placeholder para la portada. */
    ['destino-paramo.svg', 900, 700, 'FOTO PENDIENTE · Páramo andino'],
    ['destino-cultura.svg', 900, 700, 'FOTO PENDIENTE · Cultura andina'],
    ['destino-hospitalidad.svg', 900, 700, 'FOTO PENDIENTE · Hospitalidad'],
    ['card-restaurante.svg', 900, 1100, 'FOTO PENDIENTE · Restaurante'],
    ['card-lodge.svg', 900, 1100, 'FOTO PENDIENTE · Lodge Hotel'],
    ['card-travel.svg', 900, 1100, 'FOTO PENDIENTE · Travel Explore'],
    ['sobre-chimborazo-rey.svg', 1100, 800, 'FOTO PENDIENTE · Chimborazo Rey'],
    ['mision-vision.svg', 1100, 800, 'FOTO PENDIENTE · Cruz del Arenal'],
    ['ubicacion-mapa.svg', 1200, 800, 'MAPA PENDIENTE · Cruz del Arenal']
  ],
  restaurante: [
    ['hero-restaurante.svg', 1920, 1080, 'FOTO PENDIENTE · Restaurante de Aventura'],
    ['sobre-cocina.svg', 1000, 800, 'FOTO PENDIENTE · Cocina andina'],
    ['sobre-salon.svg', 1000, 800, 'FOTO PENDIENTE · Salón del restaurante'],
    ['plato-generico.svg', 800, 600, 'FOTO PENDIENTE · Plato'],
    ['galeria-1.svg', 900, 1200, 'FOTO PENDIENTE · Preparación'],
    ['galeria-2.svg', 900, 700, 'FOTO PENDIENTE · Fuego y parrilla'],
    ['galeria-3.svg', 900, 900, 'FOTO PENDIENTE · Plato de la casa'],
    ['galeria-4.svg', 900, 1100, 'FOTO PENDIENTE · Coffee shop'],
    ['galeria-5.svg', 900, 700, 'FOTO PENDIENTE · Cerveza artesanal'],
    ['galeria-6.svg', 900, 950, 'FOTO PENDIENTE · Salón principal'],
    ['galeria-7.svg', 900, 700, 'FOTO PENDIENTE · Visitantes'],
    ['galeria-8.svg', 900, 1150, 'FOTO PENDIENTE · Entorno del restaurante']
  ],
  lodge: [
    ['hero-lodge.svg', 1920, 1080, 'FOTO PENDIENTE · Lodge Hotel'],
    ['habitacion-familiar.svg', 1000, 750, 'FOTO PENDIENTE · Habitación familiar'],
    ['habitacion-grupal.svg', 1000, 750, 'FOTO PENDIENTE · Habitación grupal'],
    ['habitacion-matrimonial.svg', 1000, 750, 'FOTO PENDIENTE · Habitación matrimonial'],
    ['experiencia-calefaccion.svg', 900, 700, 'FOTO PENDIENTE · Calefacción'],
    ['experiencia-sala.svg', 900, 700, 'FOTO PENDIENTE · Sala de estar'],
    ['experiencia-amanecer.svg', 900, 700, 'FOTO PENDIENTE · Amanecer'],
    ['experiencia-arquitectura.svg', 900, 700, 'FOTO PENDIENTE · Arquitectura'],
    ['galeria-1.svg', 900, 1150, 'FOTO PENDIENTE · Habitación'],
    ['galeria-2.svg', 900, 700, 'FOTO PENDIENTE · Vista al nevado'],
    ['galeria-3.svg', 900, 900, 'FOTO PENDIENTE · Sala de estar'],
    ['galeria-4.svg', 900, 1100, 'FOTO PENDIENTE · Cocina'],
    ['galeria-5.svg', 900, 700, 'FOTO PENDIENTE · Exteriores'],
    ['galeria-6.svg', 900, 950, 'FOTO PENDIENTE · Atardecer'],
    ['galeria-7.svg', 900, 700, 'FOTO PENDIENTE · Descanso'],
    ['galeria-8.svg', 900, 1150, 'FOTO PENDIENTE · Entorno del Lodge']
  ],
  travel: [
    ['hero-travel.svg', 1920, 1080, 'FOTO PENDIENTE · Nevado Chimborazo'],
    ['actividad-cumbre-chimborazo.svg', 1000, 750, 'FOTO PENDIENTE · Cumbre Chimborazo'],
    ['actividad-carihuairazo.svg', 1000, 750, 'FOTO PENDIENTE · Carihuairazo'],
    ['actividad-cabalgatas.svg', 1000, 750, 'FOTO PENDIENTE · Cabalgatas'],
    ['actividad-ciclismo.svg', 1000, 750, 'FOTO PENDIENTE · Descenso en bicicleta'],
    ['actividad-trekking-nocturno.svg', 1000, 750, 'FOTO PENDIENTE · Trekking nocturno'],
    ['seguridad-equipo.svg', 1100, 800, 'FOTO PENDIENTE · Equipamiento de montaña']
  ]
};

let count = 0;
for (const [section, list] of Object.entries(IMAGES)) {
  const dir = path.join(ROOT, section);
  fs.mkdirSync(dir, { recursive: true });
  list.forEach(([file, w, h, label], i) => {
    const svg = buildSvg({
      w, h,
      palette: PALETTES[section],
      label,
      snow: section !== 'restaurante',
      seed: i + 1 + section.length
    });
    fs.writeFileSync(path.join(dir, file), svg, 'utf8');
    count++;
  });
}
console.log(`${count} placeholders generados en images/`);
