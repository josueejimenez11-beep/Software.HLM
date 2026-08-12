/**
 * Verificador de traducciones de Chimborazo Rey.
 * -----------------------------------------------------------------------------
 * Recorre los archivos HTML y JS del proyecto, extrae todas las claves de
 * traducción utilizadas y comprueba que existan en los cuatro idiomas.
 * También informa de las claves declaradas que ya no se usan.
 *
 * Uso:  node assets/verificar-idiomas.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

/* Carga el diccionario evaluando el archivo en un contexto aislado. */
const source = fs.readFileSync(path.join(ROOT, 'js', 'idiomas.js'), 'utf8');
const sandbox = {};
new Function('exports', `${source}\n exports.translations = translations; exports.LANGS = LANGS;`)(sandbox);
const { translations, LANGS } = sandbox;

const LANG_CODES = Object.keys(LANGS);
const used = new Set();

/* --- Claves usadas en los HTML --- */
const htmlFiles = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html'));
const HTML_ATTR = /data-i18n(?:-html|-placeholder|-aria-label|-title|-alt|-content|-value)?="([^"]+)"/g;

htmlFiles.forEach((file) => {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
  for (const match of html.matchAll(HTML_ATTR)) used.add(match[1]);
});

/* --- Claves usadas en los JS (CR.t('...') y campos *Key) --- */
const jsFiles = fs.readdirSync(path.join(ROOT, 'js')).filter((f) => f.endsWith('.js') && f !== 'idiomas.js');
const JS_T = /CR\.t\(\s*'([^']+)'/g;
const JS_KEY = /(?:Key|titleKey|labelKey):\s*'([^']+)'/g;
const JS_ARRAY = /'((?:travel|resto|lodge|home|form|contact|nav|footer|gallery)\.[A-Za-z0-9._]+)'/g;

jsFiles.forEach((file) => {
  const js = fs.readFileSync(path.join(ROOT, 'js', file), 'utf8');
  for (const match of js.matchAll(JS_T)) used.add(match[1]);
  for (const match of js.matchAll(JS_KEY)) used.add(match[1]);
  for (const match of js.matchAll(JS_ARRAY)) used.add(match[1]);
});

/* --- Comprobaciones --- */
let errors = 0;

console.log(`Claves utilizadas en el proyecto: ${used.size}`);

LANG_CODES.forEach((lang) => {
  const missing = [...used].filter((key) => !(key in translations[lang])).sort();
  if (missing.length) {
    errors += missing.length;
    console.log(`\n✗ [${lang}] faltan ${missing.length} claves:`);
    missing.forEach((key) => console.log(`    ${key}`));
  } else {
    console.log(`✓ [${lang}] todas las claves presentes (${Object.keys(translations[lang]).length} declaradas)`);
  }
});

/* Paridad entre idiomas: todas las claves del español deben existir en el resto. */
const base = Object.keys(translations.es);
LANG_CODES.filter((l) => l !== 'es').forEach((lang) => {
  const missing = base.filter((key) => !(key in translations[lang]));
  const extra = Object.keys(translations[lang]).filter((key) => !base.includes(key));
  if (missing.length || extra.length) {
    errors += missing.length + extra.length;
    console.log(`\n✗ [${lang}] paridad con es → faltan: ${missing.join(', ') || '—'} | sobran: ${extra.join(', ') || '—'}`);
  }
});

/* Claves declaradas pero nunca utilizadas (sólo informativo). */
const unused = base.filter((key) => !used.has(key));
if (unused.length) {
  console.log(`\nℹ Claves declaradas sin uso detectado (${unused.length}): ${unused.join(', ')}`);
}

console.log(errors ? `\n${errors} problema(s) detectado(s).` : '\nSin errores de traducción.');
process.exit(errors ? 1 : 0);
