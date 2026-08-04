/* ============================================================================
   SOFTWARE DE VECTORES — Álgebra Lineal (vectores en el plano)
   ----------------------------------------------------------------------------
   Todo el cálculo se realiza dinámicamente con los valores que escribe el
   usuario. No hay resultados fijos ni precalculados.
   Organización del archivo:
     1) Utilidades numéricas y de formato
     2) Operaciones vectoriales básicas (álgebra pura)
     3) Lectura y validación de las entradas
     4) Catálogo de operaciones (procedimiento paso a paso)
     5) Renderizado del procedimiento y del resultado
     6) Gráfica interactiva en Canvas
     7) Ejemplos rápidos
     8) Eventos e inicialización
   ========================================================================== */

'use strict';

/* ============================================================================
   1) UTILIDADES NUMÉRICAS Y DE FORMATO
   ========================================================================== */

/** Tolerancia para considerar que un valor es cero. */
const EPS = 1e-10;

/**
 * Redondea a un número máximo de decimales (por defecto 3) evitando
 * resultados como 0.30000000000000004.
 */
function redondear(valor, decimales = 3) {
  const f = Math.pow(10, decimales);
  return Math.round((valor + Number.EPSILON) * f) / f;
}

/**
 * Formatea un número para mostrarlo: máximo 3 decimales y sin ceros
 * innecesarios al final (5.000 -> "5", 1.5000 -> "1.5").
 */
function fmt(valor, decimales = 3) {
  if (!isFinite(valor)) return '—';
  let n = redondear(valor, decimales);
  if (Object.is(n, -0)) n = 0;            // evita mostrar "-0"
  return String(n);
}

/** Envuelve entre paréntesis los números negativos: -2 -> "(-2)". */
function termino(valor, decimales = 3) {
  const texto = fmt(valor, decimales);
  return valor < 0 ? `(${texto})` : texto;
}

/** Representación de un vector: "(x, y)". */
function vecTexto(v, decimales = 3) {
  return `(${fmt(v.x, decimales)}, ${fmt(v.y, decimales)})`;
}

/** Forma canónica (combinación lineal de i y j): "7i + 1j". */
function formaCanonica(v, decimales = 3) {
  const x = redondear(v.x, decimales);
  const y = redondear(v.y, decimales);
  const signo = y < 0 ? '−' : '+';
  return `${fmt(x, decimales)}i ${signo} ${fmt(Math.abs(y), decimales)}j`;
}

/** ¿El vector es el vector cero? */
function esCero(v) {
  return Math.abs(v.x) < EPS && Math.abs(v.y) < EPS;
}

/**
 * Dirección del vector en grados usando atan2, normalizada al rango [0, 360).
 * Devuelve null si el vector es el vector cero (dirección indefinida).
 */
function direccionGrados(v) {
  if (esCero(v)) return null;
  let grados = Math.atan2(v.y, v.x) * 180 / Math.PI;
  if (grados < 0) grados += 360;
  return grados;
}

/** Cuadrante o eje en el que se ubica el extremo del vector. */
function cuadrante(v) {
  const x = Math.abs(v.x) < EPS ? 0 : v.x;
  const y = Math.abs(v.y) < EPS ? 0 : v.y;

  if (x === 0 && y === 0) return 'Origen (vector cero)';
  if (y === 0) return x > 0 ? 'Sobre el eje X positivo' : 'Sobre el eje X negativo';
  if (x === 0) return y > 0 ? 'Sobre el eje Y positivo' : 'Sobre el eje Y negativo';
  if (x > 0 && y > 0) return 'Cuadrante I  (+x, +y)';
  if (x < 0 && y > 0) return 'Cuadrante II  (−x, +y)';
  if (x < 0 && y < 0) return 'Cuadrante III  (−x, −y)';
  return 'Cuadrante IV  (+x, −y)';
}

/* ============================================================================
   2) OPERACIONES VECTORIALES BÁSICAS
   ========================================================================== */

const sumar      = (a, b) => ({ x: a.x + b.x, y: a.y + b.y });
const restar     = (a, b) => ({ x: a.x - b.x, y: a.y - b.y });
const porEscalar = (k, a) => ({ x: k * a.x,   y: k * a.y   });
const magnitud   = (a)    => Math.sqrt(a.x * a.x + a.y * a.y);
const productoPunto = (a, b) => a.x * b.x + a.y * b.y;
const productoCruz  = (a, b) => a.x * b.y - a.y * b.x;   // componente z en 2D
const distancia  = (a, b) => magnitud(restar(b, a));

/** Vector unitario (requiere |a| ≠ 0). */
function vectorUnitario(a) {
  const m = magnitud(a);
  return { x: a.x / m, y: a.y / m };
}

/** Proyección vectorial de a sobre b (requiere |b| ≠ 0). */
function proyeccion(a, b) {
  const factor = productoPunto(a, b) / productoPunto(b, b);
  return { vector: porEscalar(factor, b), factor: factor };
}

/** Ángulo entre dos vectores, en radianes (requiere ambos ≠ 0). */
function anguloEntre(a, b) {
  let coseno = productoPunto(a, b) / (magnitud(a) * magnitud(b));
  coseno = Math.min(1, Math.max(-1, coseno));   // protege contra error numérico
  return { radianes: Math.acos(coseno), coseno: coseno };
}

/* ============================================================================
   3) LECTURA Y VALIDACIÓN DE ENTRADAS
   ========================================================================== */

/** Referencias a los elementos del DOM. */
const dom = {
  ax: document.getElementById('ax'),
  ay: document.getElementById('ay'),
  bx: document.getElementById('bx'),
  by: document.getElementById('by'),
  k:  document.getElementById('k'),
  operacion: document.getElementById('operacion'),
  campoK: document.getElementById('campoK'),
  campoParalelogramo: document.getElementById('campoParalelogramo'),
  verParalelogramo: document.getElementById('verParalelogramo'),
  bloqueA: document.getElementById('bloqueA'),
  bloqueB: document.getElementById('bloqueB'),
  previewA: document.getElementById('previewA'),
  previewB: document.getElementById('previewB'),
  btnResolver: document.getElementById('btnResolver'),
  btnLimpiar: document.getElementById('btnLimpiar'),
  alerta: document.getElementById('alerta'),
  procedimiento: document.getElementById('procedimiento'),
  resultado: document.getElementById('resultado'),
  nombreOperacion: document.getElementById('nombreOperacion'),
  ejemplos: document.getElementById('ejemplos'),
  lienzo: document.getElementById('lienzo'),
  btnZoomIn: document.getElementById('btnZoomIn'),
  btnZoomOut: document.getElementById('btnZoomOut'),
  btnCentrar: document.getElementById('btnCentrar'),
  logoSlot: document.getElementById('logoSlot'),
  logoVacio: document.getElementById('logoVacio'),
  logoImg: document.getElementById('logoImg'),
  logoQuitar: document.getElementById('logoQuitar'),
  logoArchivo: document.getElementById('logoArchivo')
};

/**
 * Convierte el texto de un campo a número.
 * Acepta enteros, decimales (con punto o coma) y valores negativos.
 * Devuelve { ok, valor, motivo }.
 */
function leerNumero(input, etiqueta) {
  const bruto = (input.value || '').trim();

  if (bruto === '') {
    return { ok: false, motivo: `El campo <strong>${etiqueta}</strong> está vacío.` };
  }

  // Se admite la coma como separador decimal (5,25 -> 5.25)
  const normalizado = bruto.replace(',', '.');

  // Patrón: signo opcional + dígitos + parte decimal opcional (también .5)
  if (!/^[+-]?(\d+(\.\d*)?|\.\d+)$/.test(normalizado)) {
    return { ok: false, motivo: `El campo <strong>${etiqueta}</strong> no contiene un número válido: “${bruto}”.` };
  }

  const valor = parseFloat(normalizado);
  if (!isFinite(valor)) {
    return { ok: false, motivo: `El campo <strong>${etiqueta}</strong> no contiene un número finito.` };
  }

  return { ok: true, valor: valor };
}

/** Marca o desmarca visualmente un campo con error. */
function marcarError(input, hayError) {
  input.classList.toggle('error', hayError);
}

/** Limpia todas las marcas de error. */
function limpiarErrores() {
  [dom.ax, dom.ay, dom.bx, dom.by, dom.k].forEach(i => marcarError(i, false));
  dom.alerta.classList.add('oculto');
  dom.alerta.innerHTML = '';
}

/** Muestra la lista de errores de validación. */
function mostrarErrores(errores) {
  dom.alerta.innerHTML =
    '<strong>Revisa los datos ingresados:</strong>' +
    '<ul>' + errores.map(e => `<li>${e}</li>`).join('') + '</ul>';
  dom.alerta.classList.remove('oculto');
}

/* ============================================================================
   4) CATÁLOGO DE OPERACIONES
   ----------------------------------------------------------------------------
   Cada operación declara:
     nombre     -> título legible
     usaA/usaB  -> qué vectores necesita (para validar y atenuar campos)
     usaK       -> si necesita el escalar K
     validar    -> comprobaciones extra (vector cero, división entre cero…)
     resolver   -> construye el procedimiento completo y el resultado
   ========================================================================== */

const OPERACIONES = {

  /* ---------- 1. Suma A + B ---------- */
  suma: {
    nombre: 'Suma de vectores  A + B',
    usaA: true, usaB: true, usaK: false,
    resolver: ({ A, B }) => {
      const R = sumar(A, B);
      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'A + B = (a₁ + b₁, a₂ + b₂)',
        sustitucion: `A + B = (${termino(A.x)} + ${termino(B.x)}, ${termino(A.y)} + ${termino(B.y)})`,
        desarrollo: `A + B = (${fmt(A.x + B.x)}, ${fmt(A.y + B.y)})`,
        resultadoTexto: `R = ${vecTexto(R)}`,
        explicacion: 'La suma de vectores se hace componente a componente. ' +
                     'Gráficamente, R es la diagonal del paralelogramo formado por A y B ' +
                     '(o el resultado de colocar B a continuación de A).',
        salida: { tipo: 'vector', vector: R, etiqueta: 'R = A + B' },
        grafica: { modo: 'suma', mostrarA: true, mostrarB: true, R: R, etiquetaR: 'R' }
      };
    }
  },

  /* ---------- 2. Resta A − B ---------- */
  resta: {
    nombre: 'Resta de vectores  A − B',
    usaA: true, usaB: true, usaK: false,
    resolver: ({ A, B }) => {
      const R = restar(A, B);
      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'A − B = (a₁ − b₁, a₂ − b₂)',
        sustitucion: `A − B = (${termino(A.x)} − ${termino(B.x)}, ${termino(A.y)} − ${termino(B.y)})`,
        desarrollo: `A − B = (${fmt(A.x - B.x)}, ${fmt(A.y - B.y)})`,
        resultadoTexto: `R = ${vecTexto(R)}`,
        explicacion: 'Restar B a A equivale a sumar el opuesto de B: A + (−B). ' +
                     'Gráficamente, el vector resultante va desde el extremo de B hasta el extremo de A.',
        salida: { tipo: 'vector', vector: R, etiqueta: 'R = A − B' },
        grafica: { modo: 'resta', mostrarA: true, mostrarB: true, R: R, etiquetaR: 'R' }
      };
    }
  },

  /* ---------- 3. Multiplicación por escalar K·A ---------- */
  escalar: {
    nombre: 'Multiplicación por escalar  K·A',
    usaA: true, usaB: false, usaK: true,
    resolver: ({ A, K }) => {
      const R = porEscalar(K, A);
      let efecto;
      if (Math.abs(K) < EPS)      efecto = 'Al multiplicar por 0 se obtiene el vector cero.';
      else if (Math.abs(K) === 1) efecto = K > 0 ? 'Con K = 1 el vector no cambia.' : 'Con K = −1 el vector conserva su magnitud pero invierte su sentido.';
      else if (Math.abs(K) > 1)   efecto = `El vector se alarga ${fmt(Math.abs(K))} veces` + (K < 0 ? ' y cambia de sentido.' : '.');
      else                        efecto = `El vector se acorta (queda al ${fmt(Math.abs(K) * 100)} % de su tamaño)` + (K < 0 ? ' y cambia de sentido.' : '.');

      return {
        datos: [`A = ${vecTexto(A)}`, `K = ${fmt(K)}`],
        formula: 'K·A = (K·a₁, K·a₂)',
        sustitucion: `K·A = (${termino(K)}·${termino(A.x)}, ${termino(K)}·${termino(A.y)})`,
        desarrollo: `K·A = (${fmt(K * A.x)}, ${fmt(K * A.y)})`,
        resultadoTexto: `R = ${vecTexto(R)}`,
        explicacion: 'La multiplicación por un escalar afecta cada componente del vector. ' +
                     efecto + ' La dirección de la recta soporte no cambia.',
        salida: { tipo: 'vector', vector: R, etiqueta: `R = ${fmt(K)}·A` },
        grafica: { modo: 'escalar', mostrarA: true, mostrarB: false, R: R, etiquetaR: 'R' }
      };
    }
  },

  /* ---------- 4. Magnitud de A ---------- */
  magnitudA: {
    nombre: 'Magnitud del vector A  |A|',
    usaA: true, usaB: false, usaK: false,
    resolver: ({ A }) => construirMagnitud(A, 'A', 'a₁', 'a₂')
  },

  /* ---------- 5. Magnitud de B ---------- */
  magnitudB: {
    nombre: 'Magnitud del vector B  |B|',
    usaA: false, usaB: true, usaK: false,
    resolver: ({ B }) => construirMagnitud(B, 'B', 'b₁', 'b₂')
  },

  /* ---------- 6. Producto punto A · B ---------- */
  punto: {
    nombre: 'Producto punto  A · B',
    usaA: true, usaB: true, usaK: false,
    resolver: ({ A, B }) => {
      const p = productoPunto(A, B);
      let interpretacion;
      if (Math.abs(p) < EPS)  interpretacion = 'El producto punto es 0: los vectores son perpendiculares (forman 90°).';
      else if (p > 0)         interpretacion = 'El producto punto es positivo: el ángulo entre los vectores es agudo (menor a 90°).';
      else                    interpretacion = 'El producto punto es negativo: el ángulo entre los vectores es obtuso (mayor a 90°).';

      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'A · B = a₁·b₁ + a₂·b₂',
        sustitucion: `A · B = ${termino(A.x)}·${termino(B.x)} + ${termino(A.y)}·${termino(B.y)}`,
        desarrollo: `A · B = ${fmt(A.x * B.x)} + ${fmt(A.y * B.y)}`,
        resultadoTexto: `A · B = ${fmt(p)}`,
        explicacion: 'El producto punto es un número (escalar), no un vector. ' + interpretacion,
        salida: { tipo: 'escalar', valor: p, unidad: 'unidades²', interpretacion: interpretacion },
        grafica: { modo: 'basico', mostrarA: true, mostrarB: true, R: null }
      };
    }
  },

  /* ---------- 7. Ángulo entre A y B ---------- */
  angulo: {
    nombre: 'Ángulo entre A y B',
    usaA: true, usaB: true, usaK: false,
    validar: ({ A, B }) => {
      const errores = [];
      if (esCero(A)) errores.push('No se puede calcular el ángulo: el <strong>vector A es el vector cero</strong> y su dirección no está definida (se dividiría entre cero).');
      if (esCero(B)) errores.push('No se puede calcular el ángulo: el <strong>vector B es el vector cero</strong> y su dirección no está definida (se dividiría entre cero).');
      return errores;
    },
    resolver: ({ A, B }) => {
      const p  = productoPunto(A, B);
      const mA = magnitud(A);
      const mB = magnitud(B);
      const ang = anguloEntre(A, B);
      const grados = ang.radianes * 180 / Math.PI;

      let interpretacion;
      if (Math.abs(grados - 90) < 1e-6)  interpretacion = 'Los vectores son perpendiculares (ortogonales).';
      else if (grados < 90)              interpretacion = 'El ángulo es agudo: los vectores apuntan hacia el mismo semiplano.';
      else if (Math.abs(grados - 180) < 1e-6) interpretacion = 'Los vectores son opuestos (antiparalelos).';
      else if (Math.abs(grados) < 1e-6)  interpretacion = 'Los vectores son paralelos y del mismo sentido.';
      else                               interpretacion = 'El ángulo es obtuso: los vectores apuntan en sentidos mayormente contrarios.';

      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'θ = arccos( (A · B) / (|A| · |B|) )',
        sustitucion:
          `A · B = ${termino(A.x)}·${termino(B.x)} + ${termino(A.y)}·${termino(B.y)} = ${fmt(p)}\n` +
          `|A| = √(${termino(A.x)}² + ${termino(A.y)}²) = ${fmt(mA)}\n` +
          `|B| = √(${termino(B.x)}² + ${termino(B.y)}²) = ${fmt(mB)}\n` +
          `θ = arccos( ${fmt(p)} / (${fmt(mA)} · ${fmt(mB)}) )`,
        desarrollo:
          `cos θ = ${fmt(p)} / ${fmt(mA * mB)} = ${fmt(ang.coseno, 4)}\n` +
          `θ = arccos(${fmt(ang.coseno, 4)}) = ${fmt(ang.radianes, 4)} rad`,
        resultadoTexto: `θ ≈ ${fmt(grados)}°`,
        explicacion: 'El ángulo se obtiene despejando el coseno de la definición geométrica del producto punto. ' +
                     interpretacion,
        salida: {
          tipo: 'escalar',
          valor: grados,
          unidad: 'grados (°)',
          interpretacion: `${interpretacion} Equivale a ${fmt(ang.radianes, 4)} radianes.`
        },
        grafica: { modo: 'angulo', mostrarA: true, mostrarB: true, R: null }
      };
    }
  },

  /* ---------- 8. Producto cruz en 2D ---------- */
  cruz: {
    nombre: 'Producto cruz en 2D  (A × B)z',
    usaA: true, usaB: true, usaK: false,
    resolver: ({ A, B }) => {
      const c = productoCruz(A, B);
      let interpretacion;
      if (Math.abs(c) < EPS) interpretacion = 'El producto cruz es 0: los vectores son paralelos (colineales) y no generan área.';
      else if (c > 0)        interpretacion = 'El valor es positivo: el giro de A hacia B es en sentido antihorario (el vector resultante apunta hacia +z).';
      else                   interpretacion = 'El valor es negativo: el giro de A hacia B es en sentido horario (el vector resultante apunta hacia −z).';

      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'A × B = a₁·b₂ − a₂·b₁     (componente z, perpendicular al plano)',
        sustitucion: `A × B = ${termino(A.x)}·${termino(B.y)} − ${termino(A.y)}·${termino(B.x)}`,
        desarrollo: `A × B = ${fmt(A.x * B.y)} − ${fmt(A.y * B.x)}`,
        resultadoTexto: `(A × B)z = ${fmt(c)}`,
        explicacion: 'En el plano, el producto cruz da un solo número: la componente z del vector perpendicular. ' +
                     interpretacion,
        salida: { tipo: 'escalar', valor: c, unidad: 'unidades² (componente z)', interpretacion: interpretacion },
        grafica: { modo: 'area', mostrarA: true, mostrarB: true, R: null }
      };
    }
  },

  /* ---------- 9. Área del paralelogramo ---------- */
  area: {
    nombre: 'Área del paralelogramo formado por A y B',
    usaA: true, usaB: true, usaK: false,
    resolver: ({ A, B }) => {
      const c = productoCruz(A, B);
      const area = Math.abs(c);
      const interpretacion = area < EPS
        ? 'El área es 0: los vectores son paralelos, por lo que no encierran ninguna superficie.'
        : `El paralelogramo generado por A y B cubre ${fmt(area)} unidades cuadradas. ` +
          `El triángulo formado por A y B tendría la mitad: ${fmt(area / 2)} u².`;

      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'Área = |A × B| = |a₁·b₂ − a₂·b₁|',
        sustitucion: `Área = |${termino(A.x)}·${termino(B.y)} − ${termino(A.y)}·${termino(B.x)}|`,
        desarrollo: `Área = |${fmt(A.x * B.y)} − ${fmt(A.y * B.x)}| = |${fmt(c)}|`,
        resultadoTexto: `Área = ${fmt(area)} u²`,
        explicacion: 'El valor absoluto del producto cruz mide el área del paralelogramo cuyos lados son A y B. ' +
                     interpretacion,
        salida: { tipo: 'escalar', valor: area, unidad: 'unidades cuadradas (u²)', interpretacion: interpretacion },
        grafica: { modo: 'area', mostrarA: true, mostrarB: true, R: null }
      };
    }
  },

  /* ---------- 10. Proyección de A sobre B ---------- */
  proyeccion: {
    nombre: 'Proyección de A sobre B',
    usaA: true, usaB: true, usaK: false,
    validar: ({ B }) => {
      if (esCero(B)) {
        return ['No se puede proyectar sobre el <strong>vector cero</strong>: la fórmula dividiría entre |B|² = 0.'];
      }
      return [];
    },
    resolver: ({ A, B }) => {
      const p    = productoPunto(A, B);
      const mB   = magnitud(B);
      const mB2  = productoPunto(B, B);
      const proy = proyeccion(A, B);
      const R    = proy.vector;
      const compEscalar = p / mB;                 // componente escalar de A sobre B
      const perpendicular = restar(A, R);          // componente ortogonal

      return {
        datos: [`A = ${vecTexto(A)}`, `B = ${vecTexto(B)}`],
        formula: 'proy_B A = ( (A · B) / |B|² ) · B',
        sustitucion:
          `A · B = ${termino(A.x)}·${termino(B.x)} + ${termino(A.y)}·${termino(B.y)} = ${fmt(p)}\n` +
          `|B|² = ${termino(B.x)}² + ${termino(B.y)}² = ${fmt(mB2)}\n` +
          `proy_B A = ( ${fmt(p)} / ${fmt(mB2)} ) · ${vecTexto(B)}`,
        desarrollo:
          `factor = ${fmt(p)} / ${fmt(mB2)} = ${fmt(proy.factor, 4)}\n` +
          `proy_B A = ${fmt(proy.factor, 4)} · ${vecTexto(B)} = (${fmt(R.x)}, ${fmt(R.y)})`,
        resultadoTexto: `proy_B A = ${vecTexto(R)}`,
        explicacion: 'La proyección es la “sombra” de A sobre la recta que contiene a B. ' +
                     `Su componente escalar es (A·B)/|B| = ${fmt(compEscalar)}. ` +
                     `La parte de A que sobra, A − proy_B A = ${vecTexto(perpendicular)}, es perpendicular a B.`,
        salida: { tipo: 'vector', vector: R, etiqueta: 'proy_B A' },
        grafica: {
          modo: 'proyeccion',
          mostrarA: true, mostrarB: true,
          R: R, etiquetaR: 'proy',
          extra: { pieProyeccion: R }
        }
      };
    }
  },

  /* ---------- 11. Vector unitario de A ---------- */
  unitario: {
    nombre: 'Vector unitario de A',
    usaA: true, usaB: false, usaK: false,
    validar: ({ A }) => {
      if (esCero(A)) {
        return ['No existe el vector unitario del <strong>vector cero</strong>: la fórmula dividiría entre |A| = 0.'];
      }
      return [];
    },
    resolver: ({ A }) => {
      const m = magnitud(A);
      const R = vectorUnitario(A);

      return {
        datos: [`A = ${vecTexto(A)}`],
        formula: 'û = A / |A| = (a₁/|A| , a₂/|A|)',
        sustitucion:
          `|A| = √(${termino(A.x)}² + ${termino(A.y)}²) = √${fmt(A.x * A.x + A.y * A.y)} = ${fmt(m)}\n` +
          `û = ( ${fmt(A.x)} / ${fmt(m)} , ${fmt(A.y)} / ${fmt(m)} )`,
        desarrollo: `û = (${fmt(R.x, 4)}, ${fmt(R.y, 4)})   →   |û| = ${fmt(magnitud(R))}`,
        resultadoTexto: `û = ${vecTexto(R)}`,
        explicacion: 'El vector unitario conserva exactamente la misma dirección y sentido que A, ' +
                     'pero su magnitud siempre vale 1. Sirve para indicar solo la orientación.',
        salida: { tipo: 'vector', vector: R, etiqueta: 'û (unitario de A)' },
        grafica: { modo: 'unitario', mostrarA: true, mostrarB: false, R: R, etiquetaR: 'û' }
      };
    }
  },

  /* ---------- 12. Distancia entre los extremos de A y B ---------- */
  distancia: {
    nombre: 'Distancia entre los extremos de A y B',
    usaA: true, usaB: true, usaK: false,
    resolver: ({ A, B }) => {
      const dx = B.x - A.x;
      const dy = B.y - A.y;
      const d  = Math.sqrt(dx * dx + dy * dy);
      const interpretacion = d < EPS
        ? 'La distancia es 0: los extremos de A y B coinciden en el mismo punto.'
        : `Los puntos extremos ${vecTexto(A)} y ${vecTexto(B)} están separados ${fmt(d)} unidades. ` +
          'Equivale a la magnitud del vector B − A.';

      return {
        datos: [`A = ${vecTexto(A)}   (punto extremo)`, `B = ${vecTexto(B)}   (punto extremo)`],
        formula: 'd(A, B) = √( (b₁ − a₁)² + (b₂ − a₂)² )',
        sustitucion: `d(A, B) = √( (${termino(B.x)} − ${termino(A.x)})² + (${termino(B.y)} − ${termino(A.y)})² )`,
        desarrollo:
          `d(A, B) = √( (${fmt(dx)})² + (${fmt(dy)})² )\n` +
          `d(A, B) = √( ${fmt(dx * dx)} + ${fmt(dy * dy)} ) = √${fmt(dx * dx + dy * dy)}`,
        resultadoTexto: `d(A, B) = ${fmt(d)} u`,
        explicacion: 'Es la fórmula de la distancia entre dos puntos del plano, aplicada a los extremos ' +
                     'de los vectores A y B. ' + interpretacion,
        salida: { tipo: 'escalar', valor: d, unidad: 'unidades (u)', interpretacion: interpretacion },
        grafica: { modo: 'distancia', mostrarA: true, mostrarB: true, R: null }
      };
    }
  }
};

/**
 * Constructor reutilizable para las operaciones 4 y 5 (magnitud de A o de B),
 * ya que el procedimiento es idéntico cambiando solo el nombre del vector.
 */
function construirMagnitud(V, nombre, s1, s2) {
  const cuadrados = V.x * V.x + V.y * V.y;
  const m = Math.sqrt(cuadrados);
  const interpretacion = m < EPS
    ? 'La magnitud es 0: se trata del vector cero, que no tiene longitud ni dirección definida.'
    : `El vector ${nombre} mide ${fmt(m)} unidades de longitud.`;

  return {
    datos: [`${nombre} = ${vecTexto(V)}`],
    formula: `|${nombre}| = √(${s1}² + ${s2}²)`,
    sustitucion: `|${nombre}| = √( ${termino(V.x)}² + ${termino(V.y)}² )`,
    desarrollo: `|${nombre}| = √( ${fmt(V.x * V.x)} + ${fmt(V.y * V.y)} ) = √${fmt(cuadrados)}`,
    resultadoTexto: `|${nombre}| = ${fmt(m)} u`,
    explicacion: 'La magnitud (o norma) es la longitud del vector y se obtiene con el teorema de Pitágoras ' +
                 'aplicado a sus componentes. Siempre es un número mayor o igual a cero. ' + interpretacion,
    salida: { tipo: 'escalar', valor: m, unidad: 'unidades (u)', interpretacion: interpretacion },
    grafica: {
      modo: 'magnitud',
      mostrarA: nombre === 'A',
      mostrarB: nombre === 'B',
      R: null
    }
  };
}

/* ============================================================================
   5) RENDERIZADO DEL PROCEDIMIENTO Y DEL RESULTADO
   ========================================================================== */

/** Escapa caracteres HTML para insertar texto de forma segura. */
function esc(texto) {
  return String(texto)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/** Crea el bloque HTML de un paso del procedimiento. */
function paso(titulo, contenido, final = false) {
  return `
    <div class="paso${final ? ' paso-final' : ''}">
      <h3>${esc(titulo)}</h3>
      <pre>${esc(contenido)}</pre>
    </div>`;
}

/** Dibuja el procedimiento completo de la operación resuelta. */
function renderProcedimiento(res) {
  dom.procedimiento.innerHTML =
    paso('Datos del problema', res.datos.join('\n')) +
    paso('Fórmula general', res.formula) +
    paso('Sustitución de valores', res.sustitucion) +
    paso('Operación desarrollada', res.desarrollo) +
    paso('Resultado final', res.resultadoTexto, true) +
    `<div class="paso"><h3>Explicación</h3><p>${esc(res.explicacion)}</p></div>`;
}

/** Crea una tarjeta de característica (término / valor). */
function caracteristica(titulo, valor) {
  return `<div class="caracteristica"><dt>${esc(titulo)}</dt><dd>${esc(valor)}</dd></div>`;
}

/**
 * Dibuja el resultado final:
 *  - Si es vector: vector, magnitud, dirección (atan2), cuadrante y forma canónica.
 *  - Si es escalar: solo el valor con su unidad o interpretación.
 */
function renderResultado(res) {
  const s = res.salida;
  let html = '';

  if (s.tipo === 'vector') {
    const v = s.vector;
    const m = magnitud(v);
    const dir = direccionGrados(v);

    html += `
      <div class="resultado-principal">
        <span class="rp-etiqueta">${esc(s.etiqueta)}</span>
        <span class="rp-valor">${esc(vecTexto(v))}</span>
      </div>
      <dl class="rejilla-caracteristicas">
        ${caracteristica('Vector resultante', vecTexto(v))}
        ${caracteristica('Magnitud |R|', `${fmt(m)} u`)}
        ${caracteristica('Dirección (atan2)', dir === null ? 'No definida' : `${fmt(dir)}°`)}
        ${caracteristica('Ubicación', cuadrante(v))}
        ${caracteristica('Forma canónica', formaCanonica(v))}
        ${caracteristica('Componentes', `x = ${fmt(v.x)} · y = ${fmt(v.y)}`)}
      </dl>`;

    if (dir === null) {
      html += `<p class="nota-interpretacion">El resultado es el <strong>vector cero</strong>: tiene magnitud 0 y su dirección no está definida.</p>`;
    }

  } else {
    // Resultado escalar: únicamente el valor con su unidad o interpretación.
    html += `
      <div class="resultado-principal">
        <span class="rp-etiqueta">Valor escalar</span>
        <span class="rp-valor">${esc(fmt(s.valor))}</span>
        <span class="rp-etiqueta">${esc(s.unidad || '')}</span>
      </div>
      <p class="nota-interpretacion">${esc(s.interpretacion || '')}</p>`;
  }

  dom.resultado.innerHTML = html;
}

/* ============================================================================
   6) GRÁFICA INTERACTIVA (CANVAS)
   ========================================================================== */

const ctx = dom.lienzo.getContext('2d');

/** Colores usados en la gráfica. */
const COLOR = {
  fondo:      '#050a14',
  rejilla:    'rgba(56, 189, 248, 0.10)',
  eje:        'rgba(125, 211, 252, 0.75)',
  texto:      '#9db3d4',
  A:          '#38bdf8',   // celeste
  B:          '#ef4444',   // rojo
  R:          '#fde68a',   // amarillo claro
  auxiliar:   'rgba(255, 255, 255, 0.45)',
  relleno:    'rgba(253, 230, 138, 0.10)'
};

/** Estado de la gráfica. */
const grafica = {
  A: null,
  B: null,
  R: null,
  etiquetaR: 'R',
  modo: 'basico',
  mostrarA: true,
  mostrarB: true,
  extra: null,
  escalaBase: 40,     // píxeles por unidad (ajuste automático)
  zoom: 1,            // factor de acercamiento del usuario
  centro: { x: 0, y: 0 },  // punto del mundo que queda en el centro del lienzo
  ancho: 0,
  alto: 0
};

/** Escala efectiva en píxeles por unidad. */
function escala() {
  return grafica.escalaBase * grafica.zoom;
}

/** Convierte coordenadas del mundo a píxeles del lienzo. */
function aPantalla(p) {
  const e = escala();
  return {
    x: grafica.ancho / 2 + (p.x - grafica.centro.x) * e,
    y: grafica.alto  / 2 - (p.y - grafica.centro.y) * e
  };
}

/** Convierte píxeles del lienzo a coordenadas del mundo. */
function aMundo(px, py) {
  const e = escala();
  return {
    x: grafica.centro.x + (px - grafica.ancho / 2) / e,
    y: grafica.centro.y - (py - grafica.alto  / 2) / e
  };
}

/** Ajusta el tamaño real del lienzo a su tamaño en pantalla (nitidez en HiDPI). */
function redimensionarLienzo() {
  const caja = dom.lienzo.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;

  grafica.ancho = Math.max(1, Math.round(caja.width));
  grafica.alto  = Math.max(1, Math.round(caja.height));

  dom.lienzo.width  = Math.round(grafica.ancho * dpr);
  dom.lienzo.height = Math.round(grafica.alto  * dpr);

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

/**
 * Calcula un paso de cuadrícula "bonito" (1, 2, 5, 10, 20, 50, …)
 * en función de cuántas unidades son visibles.
 */
function pasoBonito(unidadesVisibles, divisionesObjetivo = 10) {
  // Sin este resguardo, un ancho de 0 daría paso = 0 y el bucle de la
  // cuadrícula no terminaría nunca (la pestaña se congelaría).
  if (!isFinite(unidadesVisibles) || unidadesVisibles <= 0) return 1;

  const bruto = unidadesVisibles / divisionesObjetivo;
  const exponente = Math.floor(Math.log10(bruto));
  const base = Math.pow(10, exponente);
  const f = bruto / base;
  let mult;
  if (f <= 1)      mult = 1;
  else if (f <= 2) mult = 2;
  else if (f <= 5) mult = 5;
  else             mult = 10;

  const paso = mult * base;
  return (isFinite(paso) && paso > 0) ? paso : 1;
}

/** Reúne todos los puntos relevantes para el ajuste automático de escala. */
function puntosRelevantes() {
  const puntos = [{ x: 0, y: 0 }];
  if (grafica.mostrarA && grafica.A) puntos.push(grafica.A);
  if (grafica.mostrarB && grafica.B) puntos.push(grafica.B);
  if (grafica.R) puntos.push(grafica.R);
  // En la suma y en el área se dibuja el paralelogramo, cuyo vértice es A + B
  if ((grafica.modo === 'suma' || grafica.modo === 'area') && grafica.A && grafica.B) {
    puntos.push(sumar(grafica.A, grafica.B));
  }
  return puntos;
}

/** Escala automática según los valores ingresados: todo debe caber en pantalla. */
function ajustarEscalaAutomatica() {
  const puntos = puntosRelevantes();
  let maxX = 0, maxY = 0;
  puntos.forEach(p => {
    maxX = Math.max(maxX, Math.abs(p.x));
    maxY = Math.max(maxY, Math.abs(p.y));
  });

  // Extensión mínima para que el plano nunca quede vacío
  const extX = Math.max(maxX * 1.20, 4);
  const extY = Math.max(maxY * 1.20, 4);

  const margen = 34;
  const dispX = Math.max(40, grafica.ancho / 2 - margen);
  const dispY = Math.max(40, grafica.alto  / 2 - margen);

  grafica.escalaBase = Math.min(dispX / extX, dispY / extY);
  grafica.zoom = 1;
  grafica.centro = { x: 0, y: 0 };
}

/** Dibuja una línea entre dos puntos del mundo. */
function linea(p1, p2, color, ancho = 1, discontinua = null) {
  const a = aPantalla(p1);
  const b = aPantalla(p2);
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = ancho;
  if (discontinua) ctx.setLineDash(discontinua);
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);
  ctx.stroke();
  ctx.restore();
}

/** Dibuja un vector (flecha) desde un punto del mundo hasta otro. */
function flecha(desde, hasta, color, ancho = 3) {
  const a = aPantalla(desde);
  const b = aPantalla(hasta);
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const largo = Math.hypot(dx, dy);

  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = ancho;
  ctx.lineCap = 'round';
  ctx.shadowColor = color;
  ctx.shadowBlur = 8;

  if (largo < 1) {
    // Vector prácticamente nulo: se marca solo un punto
    ctx.beginPath();
    ctx.arc(a.x, a.y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    return;
  }

  const cabeza = Math.min(14, largo * 0.32);
  const ang = Math.atan2(dy, dx);

  // Cuerpo de la flecha (se recorta para que no sobresalga de la punta)
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x - Math.cos(ang) * cabeza * 0.75, b.y - Math.sin(ang) * cabeza * 0.75);
  ctx.stroke();

  // Punta de la flecha
  ctx.beginPath();
  ctx.moveTo(b.x, b.y);
  ctx.lineTo(b.x - Math.cos(ang - 0.40) * cabeza, b.y - Math.sin(ang - 0.40) * cabeza);
  ctx.lineTo(b.x - Math.cos(ang + 0.40) * cabeza, b.y - Math.sin(ang + 0.40) * cabeza);
  ctx.closePath();
  ctx.fill();

  ctx.restore();
}

/** Escribe una etiqueta con fondo semitransparente cerca de un punto del mundo. */
function etiqueta(texto, punto, color, desplazamiento = { x: 10, y: -10 }) {
  const p = aPantalla(punto);
  ctx.save();
  ctx.font = '600 12px "Segoe UI", Arial, sans-serif';
  const ancho = ctx.measureText(texto).width;

  let x = p.x + desplazamiento.x;
  let y = p.y + desplazamiento.y;

  // Mantiene la etiqueta dentro del lienzo
  x = Math.min(Math.max(4, x), grafica.ancho - ancho - 10);
  y = Math.min(Math.max(14, y), grafica.alto - 8);

  ctx.fillStyle = 'rgba(4, 8, 18, 0.78)';
  ctx.fillRect(x - 5, y - 13, ancho + 10, 18);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.strokeRect(x - 5, y - 13, ancho + 10, 18);
  ctx.fillStyle = color;
  ctx.fillText(texto, x, y);
  ctx.restore();
}

/** Dibuja la cuadrícula, los ejes y los números. */
function dibujarPlano() {
  const e = escala();
  const min = aMundo(0, grafica.alto);
  const max = aMundo(grafica.ancho, 0);
  const unidadesX = max.x - min.x;
  const paso = pasoBonito(unidadesX, 12);

  // El origen y la escala se calculan una sola vez y las posiciones se obtienen
  // con una multiplicación, en lugar de llamar a aPantalla() por cada línea.
  const origen = aPantalla({ x: 0, y: 0 });
  const medioPaso = paso / 2;

  ctx.save();
  ctx.font = '11px "Segoe UI", Arial, sans-serif';
  ctx.textBaseline = 'top';
  ctx.lineWidth = 1;

  // --- Cuadrícula completa en un solo trazo ---
  // Todas las líneas comparten color, así que se acumulan en un único path y se
  // pintan con un solo stroke() en vez de uno por línea.
  // Se recorren con un contador entero (iniX + i·paso) para que los valores no
  // se desvíen al acumular sumas de decimales.
  const iniX = Math.ceil(min.x / paso) * paso;
  const lineasX = Math.floor((max.x - iniX) / paso);
  const iniY = Math.ceil(min.y / paso) * paso;
  const lineasY = Math.floor((max.y - iniY) / paso);

  ctx.strokeStyle = COLOR.rejilla;
  ctx.beginPath();

  for (let i = 0; i <= lineasX; i++) {
    const px = origen.x + (iniX + i * paso) * e;
    ctx.moveTo(px, 0);
    ctx.lineTo(px, grafica.alto);
  }
  for (let i = 0; i <= lineasY; i++) {
    const py = origen.y - (iniY + i * paso) * e;
    ctx.moveTo(0, py);
    ctx.lineTo(grafica.ancho, py);
  }

  ctx.stroke();

  // --- Ejes ---
  const ejeY = Math.min(Math.max(origen.y, 0), grafica.alto);
  const ejeX = Math.min(Math.max(origen.x, 0), grafica.ancho);

  ctx.strokeStyle = COLOR.eje;
  ctx.lineWidth = 1.6;
  ctx.beginPath();  // eje X
  ctx.moveTo(0, ejeY);
  ctx.lineTo(grafica.ancho, ejeY);
  ctx.stroke();
  ctx.beginPath();  // eje Y
  ctx.moveTo(ejeX, 0);
  ctx.lineTo(ejeX, grafica.alto);
  ctx.stroke();

  // --- Números sobre los ejes ---
  ctx.fillStyle = COLOR.texto;
  ctx.textAlign = 'center';
  const saltar = e * paso < 30 ? 2 : 1;   // evita amontonar los números
  for (let i = 0; i <= lineasX; i++) {
    if (i % saltar !== 0) continue;
    const x = iniX + i * paso;
    if (Math.abs(x) < medioPaso) continue;
    ctx.fillText(fmt(x), origen.x + x * e, ejeY + 5);
  }

  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  for (let i = 0; i <= lineasY; i++) {
    if (i % saltar !== 0) continue;
    const y = iniY + i * paso;
    if (Math.abs(y) < medioPaso) continue;
    ctx.fillText(fmt(y), ejeX - 6, origen.y - y * e);
  }

  // --- Nombres de los ejes y origen ---
  ctx.fillStyle = COLOR.eje;
  ctx.textAlign = 'right';
  ctx.textBaseline = 'top';
  ctx.fillText('X', grafica.ancho - 6, ejeY + 5);
  ctx.textAlign = 'left';
  ctx.fillText('Y', ejeX + 6, 6);
  ctx.fillStyle = COLOR.texto;
  ctx.textAlign = 'right';
  ctx.fillText('0', ejeX - 6, ejeY + 5);

  ctx.restore();
}

/** Dibuja los elementos auxiliares según el tipo de operación. */
function dibujarAuxiliares() {
  const A = grafica.A;
  const B = grafica.B;
  const O = { x: 0, y: 0 };

  // Método del paralelogramo en la suma (líneas punteadas)
  if (grafica.modo === 'suma' && A && B && dom.verParalelogramo.checked) {
    const S = sumar(A, B);
    linea(A, S, COLOR.auxiliar, 1.4, [6, 5]);
    linea(B, S, COLOR.auxiliar, 1.4, [6, 5]);
  }

  // Resta: el vector A − B trasladado desde el extremo de B hasta el de A
  if (grafica.modo === 'resta' && A && B) {
    linea(B, A, COLOR.auxiliar, 1.4, [6, 5]);
    etiqueta('A − B (trasladado)', { x: (A.x + B.x) / 2, y: (A.y + B.y) / 2 }, COLOR.auxiliar, { x: 8, y: -6 });
  }

  // Distancia entre los extremos
  if (grafica.modo === 'distancia' && A && B) {
    linea(A, B, COLOR.R, 2, [7, 5]);
    etiqueta(`d = ${fmt(distancia(A, B))}`, { x: (A.x + B.x) / 2, y: (A.y + B.y) / 2 }, COLOR.R, { x: 8, y: -6 });
  }

  // Paralelogramo sombreado para área y producto cruz
  if ((grafica.modo === 'area') && A && B) {
    const S = sumar(A, B);
    const pO = aPantalla(O), pA = aPantalla(A), pS = aPantalla(S), pB = aPantalla(B);
    ctx.save();
    ctx.fillStyle = COLOR.relleno;
    ctx.beginPath();
    ctx.moveTo(pO.x, pO.y);
    ctx.lineTo(pA.x, pA.y);
    ctx.lineTo(pS.x, pS.y);
    ctx.lineTo(pB.x, pB.y);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
    linea(A, S, COLOR.auxiliar, 1.2, [5, 4]);
    linea(B, S, COLOR.auxiliar, 1.2, [5, 4]);
  }

  // Arco del ángulo entre A y B
  if (grafica.modo === 'angulo' && A && B && !esCero(A) && !esCero(B)) {
    const o = aPantalla(O);
    const radio = Math.min(46, Math.min(magnitud(A), magnitud(B)) * escala() * 0.55);
    const a1 = Math.atan2(-A.y, A.x);   // el eje Y del lienzo está invertido
    const a2 = Math.atan2(-B.y, B.x);
    ctx.save();
    ctx.strokeStyle = COLOR.R;
    ctx.lineWidth = 2;
    ctx.beginPath();
    // Se dibuja siempre el arco menor entre los dos vectores
    let delta = a2 - a1;
    while (delta >  Math.PI) delta -= 2 * Math.PI;
    while (delta < -Math.PI) delta += 2 * Math.PI;
    ctx.arc(o.x, o.y, radio, a1, a1 + delta, delta < 0);
    ctx.stroke();
    ctx.restore();

    const grados = anguloEntre(A, B).radianes * 180 / Math.PI;
    const medio = a1 + delta / 2;
    etiqueta(
      `θ = ${fmt(grados)}°`,
      aMundo(o.x + Math.cos(medio) * (radio + 22), o.y + Math.sin(medio) * (radio + 22)),
      COLOR.R,
      { x: -18, y: 0 }
    );
  }

  // Proyección: línea perpendicular auxiliar desde el extremo de A
  if (grafica.modo === 'proyeccion' && A && B && !esCero(B) && grafica.R) {
    const P = grafica.R;
    linea(A, P, COLOR.auxiliar, 1.5, [5, 4]);          // segmento perpendicular

    // Recta soporte de B (prolongada hacia ambos lados)
    const uB = vectorUnitario(B);
    const largo = Math.max(magnitud(A), magnitud(B), magnitud(P)) * 1.6;
    linea(porEscalar(-largo, uB), porEscalar(largo, uB), 'rgba(239, 68, 68, 0.30)', 1, [4, 5]);

    // Pequeño símbolo de ángulo recto en el pie de la proyección
    if (magnitud(restar(A, P)) > EPS) {
      const u1 = vectorUnitario(restar(A, P));
      const u2 = vectorUnitario(B);
      const lado = 12 / escala();
      const q1 = sumar(P, porEscalar(lado, u1));
      const q2 = sumar(P, porEscalar(lado, u2));
      const q3 = sumar(q1, porEscalar(lado, u2));
      linea(q1, q3, COLOR.auxiliar, 1.2);
      linea(q2, q3, COLOR.auxiliar, 1.2);
    }
  }
}

/** Dibuja la gráfica completa. */
function dibujar() {
  if (grafica.ancho === 0) redimensionarLienzo();

  // Fondo
  ctx.save();
  ctx.fillStyle = COLOR.fondo;
  ctx.fillRect(0, 0, grafica.ancho, grafica.alto);
  ctx.restore();

  dibujarPlano();
  dibujarAuxiliares();

  const O = { x: 0, y: 0 };

  // Vector A (celeste)
  if (grafica.mostrarA && grafica.A) {
    flecha(O, grafica.A, COLOR.A, 3);
    etiqueta(`A ${vecTexto(grafica.A)}`, grafica.A, COLOR.A, { x: 12, y: -10 });
  }

  // Vector B (rojo)
  if (grafica.mostrarB && grafica.B) {
    flecha(O, grafica.B, COLOR.B, 3);
    etiqueta(`B ${vecTexto(grafica.B)}`, grafica.B, COLOR.B, { x: 12, y: 16 });
  }

  // Vector resultante (amarillo claro)
  if (grafica.R) {
    flecha(O, grafica.R, COLOR.R, 3.5);
    etiqueta(`${grafica.etiquetaR} ${vecTexto(grafica.R)}`, grafica.R, COLOR.R, { x: 12, y: 30 });
  }
}

/* ---------- Redibujado sincronizado con la pantalla ---------- */

/**
 * Los eventos de arrastre y de rueda se disparan muchas más veces por segundo
 * que los fotogramas que el monitor puede mostrar. En lugar de repintar en cada
 * evento, se agenda un único repintado por fotograma con requestAnimationFrame.
 */
let cuadroPendiente = 0;

function solicitarDibujo() {
  if (cuadroPendiente) return;             // ya hay un repintado agendado
  cuadroPendiente = requestAnimationFrame(() => {
    cuadroPendiente = 0;
    dibujar();
  });
}

/* ---------- Controles de la gráfica ---------- */

function aplicarZoom(factor, centroPantalla) {
  const antes = centroPantalla
    ? aMundo(centroPantalla.x, centroPantalla.y)
    : { x: grafica.centro.x, y: grafica.centro.y };

  grafica.zoom = Math.min(40, Math.max(0.05, grafica.zoom * factor));

  if (centroPantalla) {
    // Mantiene fijo el punto del mundo que está bajo el cursor
    const e = escala();
    grafica.centro.x = antes.x - (centroPantalla.x - grafica.ancho / 2) / e;
    grafica.centro.y = antes.y + (centroPantalla.y - grafica.alto  / 2) / e;
  }
  solicitarDibujo();
}

dom.btnZoomIn.addEventListener('click',  () => aplicarZoom(1.25));
dom.btnZoomOut.addEventListener('click', () => aplicarZoom(1 / 1.25));
dom.btnCentrar.addEventListener('click', () => { ajustarEscalaAutomatica(); dibujar(); });

// Zoom con la rueda del ratón (centrado en el cursor)
dom.lienzo.addEventListener('wheel', (ev) => {
  ev.preventDefault();
  const caja = dom.lienzo.getBoundingClientRect();
  const punto = { x: ev.clientX - caja.left, y: ev.clientY - caja.top };
  aplicarZoom(ev.deltaY < 0 ? 1.12 : 1 / 1.12, punto);
}, { passive: false });

// Arrastre para desplazar el plano
let arrastrando = false;
let ultimoPunto = null;

dom.lienzo.addEventListener('pointerdown', (ev) => {
  arrastrando = true;
  ultimoPunto = { x: ev.clientX, y: ev.clientY };
  dom.lienzo.setPointerCapture(ev.pointerId);
});

dom.lienzo.addEventListener('pointermove', (ev) => {
  if (!arrastrando) return;
  const e = escala();
  grafica.centro.x -= (ev.clientX - ultimoPunto.x) / e;
  grafica.centro.y += (ev.clientY - ultimoPunto.y) / e;
  ultimoPunto.x = ev.clientX;      // se reutiliza el objeto en vez de crear otro
  ultimoPunto.y = ev.clientY;
  solicitarDibujo();
});

['pointerup', 'pointercancel'].forEach(evento => {
  dom.lienzo.addEventListener(evento, (ev) => {
    arrastrando = false;
    if (dom.lienzo.hasPointerCapture(ev.pointerId)) {
      dom.lienzo.releasePointerCapture(ev.pointerId);
    }
  });
});

// Redibuja al cambiar el tamaño de la ventana (también agrupado por fotograma:
// evita medir el lienzo decenas de veces mientras se arrastra el borde)
let cuadroTamano = 0;
window.addEventListener('resize', () => {
  if (cuadroTamano) return;
  cuadroTamano = requestAnimationFrame(() => {
    cuadroTamano = 0;
    redimensionarLienzo();
    dibujar();
  });
});

/* ============================================================================
   7) EJEMPLOS RÁPIDOS
   ========================================================================== */

const EJEMPLOS = [
  { titulo: 'Suma',            op: 'suma',       A: [4, 3],  B: [-2, 5], detalle: 'A=(4,3)  B=(−2,5)' },
  { titulo: 'Resta',           op: 'resta',      A: [6, 2],  B: [1, 4],  detalle: 'A=(6,2)  B=(1,4)' },
  { titulo: 'Escalar',         op: 'escalar',    A: [2, -1], B: [1, 1], K: 3, detalle: 'K=3  A=(2,−1)' },
  { titulo: 'Magnitud',        op: 'magnitudA',  A: [3, 4],  B: [1, 1],  detalle: 'A=(3,4)' },
  { titulo: 'Producto punto',  op: 'punto',      A: [2, 3],  B: [4, -1], detalle: 'A=(2,3)  B=(4,−1)' },
  { titulo: 'Ángulo',          op: 'angulo',     A: [1, 0],  B: [1, 1],  detalle: 'A=(1,0)  B=(1,1)' },
  { titulo: 'Proyección',      op: 'proyeccion', A: [4, 2],  B: [3, 0],  detalle: 'A=(4,2)  B=(3,0)' },
  { titulo: 'Área',            op: 'area',       A: [5, 0],  B: [0, 4],  detalle: 'A=(5,0)  B=(0,4)' },
  { titulo: 'Producto cruz',   op: 'cruz',       A: [3, 1],  B: [-2, 4], detalle: 'A=(3,1)  B=(−2,4)' },
  { titulo: 'Vector unitario', op: 'unitario',   A: [6, -8], B: [1, 1],  detalle: 'A=(6,−8)' },
  { titulo: 'Distancia',       op: 'distancia',  A: [-3, 2], B: [4, -1], detalle: 'A=(−3,2)  B=(4,−1)' },
  { titulo: 'Magnitud de B',   op: 'magnitudB',  A: [1, 1],  B: [-5, 12], detalle: 'B=(−5,12)' }
];

/** Crea los botones de ejemplos rápidos. */
function construirEjemplos() {
  dom.ejemplos.innerHTML = '';
  EJEMPLOS.forEach(ej => {
    const boton = document.createElement('button');
    boton.type = 'button';
    boton.className = 'ejemplo';
    boton.innerHTML = `<b>${esc(ej.titulo)}</b><span>${esc(ej.detalle)}</span>`;
    boton.addEventListener('click', () => cargarEjemplo(ej));
    dom.ejemplos.appendChild(boton);
  });
}

/** Carga los valores del ejemplo, selecciona la operación y resuelve. */
function cargarEjemplo(ej) {
  dom.ax.value = ej.A[0];
  dom.ay.value = ej.A[1];
  dom.bx.value = ej.B[0];
  dom.by.value = ej.B[1];
  if (ej.K !== undefined) dom.k.value = ej.K;
  dom.operacion.value = ej.op;
  actualizarInterfaz();
  resolver();
  dom.procedimiento.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ============================================================================
   8) LÓGICA PRINCIPAL, EVENTOS E INICIALIZACIÓN
   ========================================================================== */

/**
 * Ajusta la interfaz según la operación elegida:
 *  - muestra el campo K solo en la multiplicación escalar
 *  - muestra la opción del paralelogramo solo en la suma
 *  - atenúa los bloques de vectores que no participan
 */
function actualizarInterfaz() {
  const clave = dom.operacion.value;
  const op = OPERACIONES[clave];
  if (!op) return;

  dom.campoK.classList.toggle('oculto', !op.usaK);
  dom.campoParalelogramo.classList.toggle('oculto', clave !== 'suma');
  dom.bloqueA.classList.toggle('inactivo', !op.usaA);
  dom.bloqueB.classList.toggle('inactivo', !op.usaB);
  dom.nombreOperacion.textContent = op.nombre;

  actualizarVistaPrevia();
}

/** Muestra junto a cada bloque el vector tal como está escrito. */
function actualizarVistaPrevia() {
  const a1 = leerNumero(dom.ax, 'Aₓ'), a2 = leerNumero(dom.ay, 'A_y');
  const b1 = leerNumero(dom.bx, 'Bₓ'), b2 = leerNumero(dom.by, 'B_y');

  dom.previewA.textContent = (a1.ok && a2.ok) ? `A = (${fmt(a1.valor)}, ${fmt(a2.valor)})` : 'A = ( ? , ? )';
  dom.previewB.textContent = (b1.ok && b2.ok) ? `B = (${fmt(b1.valor)}, ${fmt(b2.valor)})` : 'B = ( ? , ? )';
}

/**
 * Lee y valida únicamente los campos que la operación necesita.
 * Devuelve { ok, datos, errores }.
 */
function obtenerEntradas(op) {
  const errores = [];
  const datos = {};

  if (op.usaA) {
    const x = leerNumero(dom.ax, 'componente X de A');
    const y = leerNumero(dom.ay, 'componente Y de A');
    marcarError(dom.ax, !x.ok);
    marcarError(dom.ay, !y.ok);
    if (!x.ok) errores.push(x.motivo);
    if (!y.ok) errores.push(y.motivo);
    if (x.ok && y.ok) datos.A = { x: x.valor, y: y.valor };
  }

  if (op.usaB) {
    const x = leerNumero(dom.bx, 'componente X de B');
    const y = leerNumero(dom.by, 'componente Y de B');
    marcarError(dom.bx, !x.ok);
    marcarError(dom.by, !y.ok);
    if (!x.ok) errores.push(x.motivo);
    if (!y.ok) errores.push(y.motivo);
    if (x.ok && y.ok) datos.B = { x: x.valor, y: y.valor };
  }

  if (op.usaK) {
    const k = leerNumero(dom.k, 'escalar K');
    marcarError(dom.k, !k.ok);
    if (!k.ok) errores.push(k.motivo);
    else datos.K = k.valor;
  }

  return { ok: errores.length === 0, datos: datos, errores: errores };
}

/** Prepara el estado de la gráfica con los datos disponibles. */
function prepararGrafica(config, datos) {
  grafica.A = datos.A || null;
  grafica.B = datos.B || null;
  grafica.R = config.R || null;
  grafica.etiquetaR = config.etiquetaR || 'R';
  grafica.modo = config.modo || 'basico';
  grafica.mostrarA = config.mostrarA !== false && !!grafica.A;
  grafica.mostrarB = config.mostrarB !== false && !!grafica.B;
  grafica.extra = config.extra || null;

  ajustarEscalaAutomatica();
  dibujar();
}

/** Proceso completo: validar, calcular, mostrar procedimiento, resultado y gráfica. */
function resolver() {
  limpiarErrores();

  const clave = dom.operacion.value;
  const op = OPERACIONES[clave];
  if (!op) return;

  // --- Validación de campos vacíos y valores no numéricos ---
  const entrada = obtenerEntradas(op);
  if (!entrada.ok) {
    mostrarErrores(entrada.errores);
    return;
  }

  // --- Validaciones propias de la operación (vector cero, división entre cero) ---
  if (typeof op.validar === 'function') {
    const errores = op.validar(entrada.datos);
    if (errores.length > 0) {
      mostrarErrores(errores);
      return;
    }
  }

  // --- Cálculo dinámico y presentación ---
  const res = op.resolver(entrada.datos);
  dom.nombreOperacion.textContent = op.nombre;
  renderProcedimiento(res);
  renderResultado(res);
  prepararGrafica(res.grafica || {}, entrada.datos);
}

/** Restablece la aplicación a su estado inicial. */
function limpiar() {
  dom.ax.value = '';
  dom.ay.value = '';
  dom.bx.value = '';
  dom.by.value = '';
  dom.k.value  = '';
  dom.operacion.value = 'suma';
  dom.verParalelogramo.checked = true;

  limpiarErrores();
  actualizarInterfaz();

  dom.procedimiento.innerHTML =
    '<p class="vacio">Ingresa los datos y presiona <strong>Resolver</strong> para ver el desarrollo paso a paso.</p>';
  dom.resultado.innerHTML =
    '<p class="vacio">Aquí aparecerán el resultado final y sus características.</p>';

  grafica.A = grafica.B = grafica.R = null;
  grafica.modo = 'basico';
  ajustarEscalaAutomatica();
  dibujar();

  dom.ax.focus();
}

/* ---------- Registro de eventos ---------- */

dom.btnResolver.addEventListener('click', resolver);
dom.btnLimpiar.addEventListener('click', limpiar);
dom.operacion.addEventListener('change', actualizarInterfaz);
dom.verParalelogramo.addEventListener('change', dibujar);

// Actualiza la vista previa mientras se escribe
[dom.ax, dom.ay, dom.bx, dom.by].forEach(campo => {
  campo.addEventListener('input', () => {
    marcarError(campo, false);
    actualizarVistaPrevia();
  });
});
dom.k.addEventListener('input', () => marcarError(dom.k, false));

// Resolver con la tecla Enter desde cualquier campo
[dom.ax, dom.ay, dom.bx, dom.by, dom.k].forEach(campo => {
  campo.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') { ev.preventDefault(); resolver(); }
  });
});

/* ============================================================================
   9) LOGO INSTITUCIONAL
   ----------------------------------------------------------------------------
   El logo se toma del archivo logo-puce.png que acompaña al proyecto. Si no
   está, el recuadro permite elegir una imagen a mano, que se reduce y se
   guarda en el navegador para que siga ahí al recargar.
   ========================================================================== */

const LOGO_CLAVE = 'softwareVectores.logo';

/** Lado máximo del logo. El recuadro mide 96 px, así que 256 basta y sobra. */
const LOGO_LADO_MAX = 256;

/**
 * Reduce la imagen antes de mostrarla y guardarla.
 * Una foto de varios megabytes en base64 no cabe en localStorage (el límite
 * ronda los 5 MB) y además tarda en pintarse; redimensionada pesa unos pocos
 * kilobytes y se ve igual dentro del recuadro.
 * Si algo falla, devuelve la imagen original sin tocar.
 */
function reducirImagen(dataURL) {
  return new Promise((resolve) => {
    const img = new Image();

    img.onload = () => {
      const ladoMayor = Math.max(img.width, img.height);
      if (!ladoMayor || ladoMayor <= LOGO_LADO_MAX) { resolve(dataURL); return; }

      const factor = LOGO_LADO_MAX / ladoMayor;
      const lienzo = document.createElement('canvas');
      lienzo.width  = Math.round(img.width  * factor);
      lienzo.height = Math.round(img.height * factor);

      const c = lienzo.getContext('2d');
      c.imageSmoothingEnabled = true;
      c.imageSmoothingQuality = 'high';
      c.drawImage(img, 0, 0, lienzo.width, lienzo.height);

      try { resolve(lienzo.toDataURL('image/png')); }
      catch (e) { resolve(dataURL); }
    };

    img.onerror = () => resolve(dataURL);
    img.src = dataURL;
  });
}

/** Ruta del logo que viene con el proyecto (junto a index.html). */
const LOGO_POR_DEFECTO = dom.logoImg.getAttribute('src');

/**
 * Muestra una imagen en el recuadro.
 * `personalizada` indica que la eligió el usuario, no la que trae el proyecto:
 * en ese caso aparece la × para volver al logo original.
 */
function pintarLogo(datosImagen, personalizada) {
  dom.logoImg.src = datosImagen;
  dom.logoImg.classList.remove('oculto');
  dom.logoVacio.classList.add('oculto');
  dom.logoSlot.classList.add('con-logo');
  dom.logoSlot.classList.toggle('personalizado', !!personalizada);
}

/** Muestra el marcador de posición: no hay ninguna imagen disponible. */
function mostrarRecuadroVacio() {
  dom.logoImg.classList.add('oculto');
  dom.logoVacio.classList.remove('oculto');
  dom.logoSlot.classList.remove('con-logo', 'personalizado');
}

/** Descarta el logo elegido a mano y vuelve al que trae el proyecto. */
function borrarLogo() {
  dom.logoArchivo.value = '';
  try { localStorage.removeItem(LOGO_CLAVE); } catch (e) { /* almacenamiento no disponible */ }
  pintarLogo(LOGO_POR_DEFECTO, false);
}

/**
 * Si el archivo del logo no está en la carpeta, el navegador no puede
 * cargarlo: en ese caso se muestra el recuadro para elegir una imagen.
 */
dom.logoImg.addEventListener('error', () => {
  if (!dom.logoSlot.classList.contains('personalizado')) mostrarRecuadroVacio();
});

dom.logoImg.addEventListener('load', () => {
  dom.logoSlot.classList.add('con-logo');
  dom.logoVacio.classList.add('oculto');
});

/** Deja el recuadro en su estado inicial correcto al abrir la página. */
function recuperarLogo() {
  // Si el usuario eligió un logo en una sesión anterior, ese tiene prioridad.
  try {
    const guardado = localStorage.getItem(LOGO_CLAVE);
    if (guardado) { pintarLogo(guardado, true); return; }
  } catch (e) { /* almacenamiento no disponible (modo privado, etc.) */ }

  // El navegador empieza a cargar el <img> mientras lee el HTML, antes de que
  // este script exista, así que el evento 'error' puede haberse disparado ya.
  // Por eso se consulta el estado de la imagen en lugar de solo esperarlo.
  if (dom.logoImg.complete) {
    if (dom.logoImg.naturalWidth === 0) mostrarRecuadroVacio();   // no se encontró
    else {
      dom.logoSlot.classList.add('con-logo');
      dom.logoVacio.classList.add('oculto');
    }
  }
}

// Clic o Enter sobre el recuadro: abre el selector de archivos
dom.logoSlot.addEventListener('click', (ev) => {
  if (ev.target === dom.logoQuitar) return;   // la × no debe abrir el selector
  dom.logoArchivo.click();
});

dom.logoSlot.addEventListener('keydown', (ev) => {
  if (ev.key === 'Enter' || ev.key === ' ') {
    ev.preventDefault();
    dom.logoArchivo.click();
  }
});

// Lectura de la imagen elegida
dom.logoArchivo.addEventListener('change', (ev) => {
  const archivo = ev.target.files && ev.target.files[0];
  if (!archivo) return;

  const lector = new FileReader();
  lector.onload = (e) => {
    reducirImagen(e.target.result).then((imagen) => {
      pintarLogo(imagen, true);
      try { localStorage.setItem(LOGO_CLAVE, imagen); } catch (err) { /* sin espacio o sin permiso */ }
    });
  };
  lector.readAsDataURL(archivo);
});

dom.logoQuitar.addEventListener('click', (ev) => {
  ev.stopPropagation();
  borrarLogo();
});

/* ---------- Arranque ---------- */

let yaIniciado = false;

function iniciar() {
  if (yaIniciado) return;          // evita una doble inicialización
  yaIniciado = true;

  recuperarLogo();
  construirEjemplos();
  redimensionarLienzo();
  actualizarInterfaz();
  ajustarEscalaAutomatica();
  dibujar();
  resolver();   // muestra un primer ejemplo resuelto con los valores por defecto
}

window.addEventListener('DOMContentLoaded', iniciar);

// Si el script se carga después de DOMContentLoaded, se inicia de inmediato.
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  iniciar();
}
