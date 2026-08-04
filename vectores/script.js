/* ============================================================
   UTILIDADES
   ============================================================ */
const $ = id => document.getElementById(id);
const nf = (n, d = 2) => {
  if (!isFinite(n)) return "—";
  const r = Math.round(n * 10 ** d) / 10 ** d;
  return Object.is(r, -0) ? "0" : String(r);
};
const vecTxt = v => "(" + nf(v.x) + ", " + nf(v.y) + ")";
const mag  = v => Math.hypot(v.x, v.y);
const dot  = (a, b) => a.x * b.x + a.y * b.y;
const cruz = (a, b) => a.x * b.y - a.y * b.x;
const angDir = v => {
  let d = Math.atan2(v.y, v.x) * 180 / Math.PI;
  return d < 0 ? d + 360 : d;
};
const sgn = n => (n < 0 ? "(" + nf(n) + ")" : nf(n));

/* Logo institucional opcional */
$("logoSlot").addEventListener("click", () => $("logoFile").click());
$("logoFile").addEventListener("change", e => {
  const f = e.target.files[0];
  if (!f) return;
  const r = new FileReader();
  r.onload = ev => { $("logoSlot").innerHTML = '<img src="' + ev.target.result + '" alt="logo">'; };
  r.readAsDataURL(f);
});

/* ============================================================
   ESTADO
   ============================================================ */
let A = {x:4, y:3}, B = {x:-2, y:5}, K = 2, OP = "suma";
let R = null;          // vector resultante a dibujar (si aplica)
let AUX = null;        // vector auxiliar (proyección)
let escala = 34;       // píxeles por unidad
let cx = 0, cy = 0;    // desplazamiento del origen

const lienzo = $("lienzo"), ctx = lienzo.getContext("2d"), tip = $("tooltip");

/* ============================================================
   LECTURA DE DATOS
   ============================================================ */
function leer() {
  const n = v => { const x = parseFloat(v); return isFinite(x) ? x : NaN; };
  A = {x:n($("ax").value), y:n($("ay").value)};
  B = {x:n($("bx").value), y:n($("by").value)};
  K = n($("k").value);
  OP = $("op").value;

  if ([A.x, A.y, B.x, B.y].some(isNaN)) return "Completa las cuatro componentes con números válidos.";
  if (OP === "escalar" && isNaN(K)) return "Ingresa un valor numérico para el escalar k.";
  if (["angulo","proyeccion"].includes(OP) && mag(B) === 0) return "El vector B⃗ no puede ser nulo para esta operación.";
  if (["angulo","unitario","magnitud"].includes(OP) && mag(A) === 0) return "El vector A⃗ no puede ser nulo para esta operación.";
  return null;
}

function aviso(txt, tipo) {
  const m = $("msg");
  if (!txt) { m.className = ""; m.style.display = "none"; return; }
  m.className = tipo;
  m.textContent = txt;
}

/* ============================================================
   RESOLVER
   ============================================================ */
function resolver() {
  const err = leer();
  if (err) { aviso(err, "err"); return; }
  aviso("Operación resuelta correctamente.", "ok");

  const mA = mag(A), mB = mag(B), d = dot(A, B), cz = cruz(A, B);
  R = null; AUX = null;

  const pasos = [];
  const props = [];
  let resHTML = "";
  let etiqueta = "";

  const P = (t, cuerpo) => pasos.push({t, cuerpo});
  const F  = s => '<div class="formula">' + s + '</div>';
  const FF = s => '<div class="formula fin">' + s + '</div>';
  const N  = s => '<p class="nota">' + s + '</p>';
  const p  = s => '<p>' + s + '</p>';

  /* --- Paso común: datos --- */
  P("Datos del problema",
    p("Se identifican las componentes rectangulares de cada vector.") +
    F("A⃗ = " + vecTxt(A) + "   →   A⃗ = " + nf(A.x) + "î + " + nf(A.y) + "ĵ") +
    (["magnitud","unitario"].includes(OP) ? "" : F("B⃗ = " + vecTxt(B) + "   →   B⃗ = " + nf(B.x) + "î + " + nf(B.y) + "ĵ")) +
    (OP === "escalar" ? F("k = " + nf(K)) : "")
  );

  switch (OP) {

    case "suma": {
      R = {x:A.x + B.x, y:A.y + B.y};
      etiqueta = "A⃗ + B⃗";
      P("Fórmula de la suma",
        p("La suma de vectores se realiza componente a componente.") +
        F("A⃗ + B⃗ = (a₁ + b₁ , a₂ + b₂)"));
      P("Sustitución de valores",
        F("A⃗ + B⃗ = (" + nf(A.x) + " + " + sgn(B.x) + " , " + nf(A.y) + " + " + sgn(B.y) + ")"));
      P("Operación",
        F("A⃗ + B⃗ = (" + nf(R.x) + " , " + nf(R.y) + ")"));
      P("Magnitud y dirección de la resultante",
        F("|R⃗| = √(" + sgn(R.x) + "² + " + sgn(R.y) + "²) = √" + nf(R.x**2 + R.y**2) + " = " + nf(mag(R))) +
        F("θ = arctan(" + nf(R.y) + " / " + nf(R.x) + ") = " + nf(angDir(R)) + "°") +
        FF("R⃗ = " + vecTxt(R) + "   ·   |R⃗| = " + nf(mag(R)) + "   ·   θ = " + nf(angDir(R)) + "°") +
        N("Gráficamente la resultante es la diagonal del paralelogramo formado por A⃗ y B⃗."));
      resHTML = '<span class="big">R⃗ = A⃗ + B⃗ = ' + vecTxt(R) + '</span>' +
                '<p>La resultante tiene una magnitud de <b>' + nf(mag(R)) + '</b> unidades y una dirección de <b>' + nf(angDir(R)) + '°</b> respecto al eje x positivo.</p>';
      break;
    }

    case "resta": {
      R = {x:A.x - B.x, y:A.y - B.y};
      etiqueta = "A⃗ − B⃗";
      P("Fórmula de la resta",
        p("Restar equivale a sumar el vector opuesto: A⃗ − B⃗ = A⃗ + (−B⃗).") +
        F("A⃗ − B⃗ = (a₁ − b₁ , a₂ − b₂)"));
      P("Vector opuesto de B⃗",
        F("−B⃗ = (" + nf(-B.x) + " , " + nf(-B.y) + ")"));
      P("Sustitución y operación",
        F("A⃗ − B⃗ = (" + nf(A.x) + " − " + sgn(B.x) + " , " + nf(A.y) + " − " + sgn(B.y) + ")") +
        F("A⃗ − B⃗ = (" + nf(R.x) + " , " + nf(R.y) + ")"));
      P("Magnitud y dirección",
        F("|R⃗| = √(" + sgn(R.x) + "² + " + sgn(R.y) + "²) = " + nf(mag(R))) +
        F("θ = " + nf(angDir(R)) + "°") +
        FF("R⃗ = " + vecTxt(R)));
      resHTML = '<span class="big">R⃗ = A⃗ − B⃗ = ' + vecTxt(R) + '</span>' +
                '<p>Magnitud <b>' + nf(mag(R)) + '</b> · dirección <b>' + nf(angDir(R)) + '°</b>. Este vector va desde el extremo de B⃗ hasta el extremo de A⃗.</p>';
      break;
    }

    case "escalar": {
      R = {x:K * A.x, y:K * A.y};
      etiqueta = nf(K) + "·A⃗";
      P("Fórmula del producto por un escalar",
        p("Cada componente del vector se multiplica por el escalar k.") +
        F("k·A⃗ = (k·a₁ , k·a₂)"));
      P("Sustitución",
        F(nf(K) + "·A⃗ = (" + nf(K) + "·" + sgn(A.x) + " , " + nf(K) + "·" + sgn(A.y) + ")"));
      P("Operación",
        F(nf(K) + "·A⃗ = (" + nf(R.x) + " , " + nf(R.y) + ")"));
      P("Efecto sobre la magnitud",
        F("|A⃗| = " + nf(mA) + "   →   |k·A⃗| = |k|·|A⃗| = " + nf(Math.abs(K)) + " · " + nf(mA) + " = " + nf(mag(R))) +
        FF(nf(K) + "A⃗ = " + vecTxt(R)) +
        N(K < 0 ? "Como k es negativo, el vector conserva la dirección pero invierte su sentido."
                : "Como k es positivo, el vector conserva dirección y sentido; solo cambia su tamaño."));
      resHTML = '<span class="big">' + nf(K) + '·A⃗ = ' + vecTxt(R) + '</span>' +
                '<p>La magnitud pasó de <b>' + nf(mA) + '</b> a <b>' + nf(mag(R)) + '</b>. ' +
                (K < 0 ? 'El sentido se <b>invirtió</b> por ser k negativo.' : 'El sentido se <b>mantiene</b>.') + '</p>';
      break;
    }

    case "punto": {
      etiqueta = "A⃗ · B⃗";
      P("Fórmula del producto punto",
        p("El producto punto (o escalar) da como resultado un número real, no un vector.") +
        F("A⃗ · B⃗ = a₁·b₁ + a₂·b₂"));
      P("Sustitución",
        F("A⃗ · B⃗ = (" + nf(A.x) + ")(" + nf(B.x) + ") + (" + nf(A.y) + ")(" + nf(B.y) + ")"));
      P("Operación",
        F("A⃗ · B⃗ = " + nf(A.x * B.x) + " + " + sgn(A.y * B.y)) +
        FF("A⃗ · B⃗ = " + nf(d)));
      P("Interpretación",
        F("A⃗ · B⃗ = |A⃗|·|B⃗|·cos θ = " + nf(mA) + " · " + nf(mB) + " · cos θ") +
        N(Math.abs(d) < 1e-9 ? "El resultado es cero: los vectores son PERPENDICULARES (θ = 90°)."
          : d > 0 ? "El resultado es positivo: el ángulo entre los vectores es agudo (menor a 90°)."
                  : "El resultado es negativo: el ángulo entre los vectores es obtuso (mayor a 90°)."));
      resHTML = '<span class="big">A⃗ · B⃗ = ' + nf(d) + '</span>' +
                '<p>' + (Math.abs(d) < 1e-9 ? 'Los vectores son <b>perpendiculares</b> entre sí.'
                : 'El ángulo entre ellos es de <b>' + nf(Math.acos(Math.max(-1,Math.min(1, d/(mA*mB)))) * 180/Math.PI) + '°</b>.') + '</p>';
      break;
    }

    case "angulo": {
      const c = Math.max(-1, Math.min(1, d / (mA * mB)));
      const th = Math.acos(c) * 180 / Math.PI;
      etiqueta = "ángulo θ";
      P("Fórmula del ángulo entre vectores",
        p("Se despeja el ángulo a partir de la definición del producto punto.") +
        F("cos θ = (A⃗ · B⃗) / (|A⃗| · |B⃗|)"));
      P("Producto punto",
        F("A⃗ · B⃗ = (" + nf(A.x) + ")(" + nf(B.x) + ") + (" + nf(A.y) + ")(" + nf(B.y) + ") = " + nf(d)));
      P("Magnitudes",
        F("|A⃗| = √(" + sgn(A.x) + "² + " + sgn(A.y) + "²) = " + nf(mA)) +
        F("|B⃗| = √(" + sgn(B.x) + "² + " + sgn(B.y) + "²) = " + nf(mB)));
      P("Sustitución y resultado",
        F("cos θ = " + nf(d) + " / (" + nf(mA) + " · " + nf(mB) + ") = " + nf(c, 4)) +
        F("θ = arccos(" + nf(c, 4) + ")") +
        FF("θ = " + nf(th) + "°") +
        N("El ángulo siempre se mide entre 0° y 180°."));
      resHTML = '<span class="big">θ = ' + nf(th) + '°</span>' +
                '<p>Los vectores forman un ángulo <b>' +
                (Math.abs(th - 90) < 0.01 ? 'recto (perpendiculares)' : th < 90 ? 'agudo' : 'obtuso') +
                '</b> entre sí.</p>';
      break;
    }

    case "magnitud": {
      etiqueta = "|A⃗| y θ";
      P("Fórmula de la magnitud",
        p("Se aplica el teorema de Pitágoras a las componentes del vector.") +
        F("|A⃗| = √(a₁² + a₂²)"));
      P("Sustitución",
        F("|A⃗| = √((" + nf(A.x) + ")² + (" + nf(A.y) + ")²)") +
        F("|A⃗| = √(" + nf(A.x**2) + " + " + nf(A.y**2) + ") = √" + nf(A.x**2 + A.y**2)));
      P("Magnitud",
        FF("|A⃗| = " + nf(mA) + " unidades"));
      P("Dirección del vector",
        F("θ = arctan(a₂ / a₁) = arctan(" + nf(A.y) + " / " + nf(A.x) + ")") +
        FF("θ = " + nf(angDir(A)) + "°") +
        N("Ángulo medido desde el eje x positivo en sentido antihorario. El vector se ubica en el " +
          (A.x >= 0 && A.y >= 0 ? "I" : A.x < 0 && A.y >= 0 ? "II" : A.x < 0 ? "III" : "IV") + " cuadrante."));
      resHTML = '<span class="big">|A⃗| = ' + nf(mA) + '  ·  θ = ' + nf(angDir(A)) + '°</span>' +
                '<p>El vector A⃗ mide <b>' + nf(mA) + '</b> unidades y apunta en la dirección de <b>' + nf(angDir(A)) + '°</b>.</p>';
      break;
    }

    case "unitario": {
      R = {x:A.x / mA, y:A.y / mA};
      etiqueta = "û";
      P("Fórmula del vector unitario",
        p("Un vector unitario tiene magnitud 1 y la misma dirección del vector original.") +
        F("û = A⃗ / |A⃗|"));
      P("Cálculo de la magnitud",
        F("|A⃗| = √((" + nf(A.x) + ")² + (" + nf(A.y) + ")²) = " + nf(mA)));
      P("División de cada componente",
        F("û = (" + nf(A.x) + "/" + nf(mA) + " , " + nf(A.y) + "/" + nf(mA) + ")") +
        FF("û = (" + nf(R.x, 4) + " , " + nf(R.y, 4) + ")"));
      P("Comprobación",
        F("|û| = √(" + nf(R.x,4) + "² + " + nf(R.y,4) + "²) = " + nf(mag(R), 4)) +
        N("La magnitud resulta 1, lo que confirma que el vector es unitario."));
      resHTML = '<span class="big">û = (' + nf(R.x, 4) + ', ' + nf(R.y, 4) + ')</span>' +
                '<p>Vector de magnitud <b>1</b> con la misma dirección de A⃗ (<b>' + nf(angDir(A)) + '°</b>).</p>';
      break;
    }

    case "proyeccion": {
      const esc = d / (mB * mB);
      R = {x:esc * B.x, y:esc * B.y};
      AUX = R;
      etiqueta = "proy";
      P("Fórmula de la proyección",
        p("La proyección de A⃗ sobre B⃗ es la 'sombra' de A⃗ en la dirección de B⃗.") +
        F("proy_B A⃗ = [ (A⃗ · B⃗) / |B⃗|² ] · B⃗"));
      P("Producto punto y magnitud de B⃗",
        F("A⃗ · B⃗ = (" + nf(A.x) + ")(" + nf(B.x) + ") + (" + nf(A.y) + ")(" + nf(B.y) + ") = " + nf(d)) +
        F("|B⃗|² = " + sgn(B.x) + "² + " + sgn(B.y) + "² = " + nf(mB * mB)));
      P("Escalar de proyección",
        F("(A⃗ · B⃗) / |B⃗|² = " + nf(d) + " / " + nf(mB*mB) + " = " + nf(esc, 4)));
      P("Vector proyección",
        F("proy_B A⃗ = " + nf(esc, 4) + " · (" + nf(B.x) + " , " + nf(B.y) + ")") +
        FF("proy_B A⃗ = " + vecTxt(R)) +
        F("Componente escalar:  comp_B A⃗ = (A⃗·B⃗)/|B⃗| = " + nf(d / mB)));
      resHTML = '<span class="big">proy_B A⃗ = ' + vecTxt(R) + '</span>' +
                '<p>La componente escalar de A⃗ en la dirección de B⃗ es <b>' + nf(d / mB) + '</b>.</p>';
      break;
    }

    case "cruz": {
      etiqueta = "A⃗ × B⃗";
      P("Fórmula del producto cruz en el plano",
        p("En dos dimensiones el producto cruz es un escalar que corresponde al determinante de las componentes.") +
        F("A⃗ × B⃗ = | a₁  a₂ |\n          | b₁  b₂ |  = a₁·b₂ − a₂·b₁"));
      P("Sustitución",
        F("A⃗ × B⃗ = (" + nf(A.x) + ")(" + nf(B.y) + ") − (" + nf(A.y) + ")(" + nf(B.x) + ")"));
      P("Operación",
        F("A⃗ × B⃗ = " + nf(A.x * B.y) + " − " + sgn(A.y * B.x)) +
        FF("A⃗ × B⃗ = " + nf(cz)));
      P("Interpretación geométrica",
        F("Área del paralelogramo = |A⃗ × B⃗| = " + nf(Math.abs(cz)) + " u²") +
        F("Área del triángulo = |A⃗ × B⃗| / 2 = " + nf(Math.abs(cz) / 2) + " u²") +
        N(Math.abs(cz) < 1e-9 ? "El resultado es cero: los vectores son PARALELOS (colineales)."
                              : "El signo indica el sentido de giro: positivo antihorario, negativo horario."));
      resHTML = '<span class="big">A⃗ × B⃗ = ' + nf(cz) + '</span>' +
                '<p>Área del paralelogramo: <b>' + nf(Math.abs(cz)) + ' u²</b> · Área del triángulo: <b>' + nf(Math.abs(cz) / 2) + ' u²</b>.</p>';
      break;
    }
  }

  /* --------- Características --------- */
  const cosT = (mA && mB) ? Math.max(-1, Math.min(1, d / (mA * mB))) : NaN;
  const th   = isNaN(cosT) ? NaN : Math.acos(cosT) * 180 / Math.PI;

  props.push(["Vector A⃗", vecTxt(A), "cel"]);
  props.push(["Vector B⃗", vecTxt(B), "roj"]);
  props.push(["Magnitud |A⃗|", nf(mA), "cel"]);
  props.push(["Magnitud |B⃗|", nf(mB), "roj"]);
  props.push(["Dirección de A⃗", nf(angDir(A)) + "°", "cel"]);
  props.push(["Dirección de B⃗", nf(angDir(B)) + "°", "roj"]);
  props.push(["Producto punto", nf(d), ""]);
  props.push(["Ángulo entre A⃗ y B⃗", isNaN(th) ? "—" : nf(th) + "°", ""]);
  props.push(["Producto cruz", nf(cz), ""]);
  props.push(["Área paralelogramo", nf(Math.abs(cz)) + " u²", ""]);
  props.push(["¿Perpendiculares?", Math.abs(d) < 1e-9 ? "Sí (90°)" : "No", ""]);
  props.push(["¿Paralelos?", Math.abs(cz) < 1e-9 ? "Sí (colineales)" : "No", ""]);
  if (R) props.push(["Resultado", vecTxt(R), ""]);

  /* --------- Render --------- */
  $("pasos").innerHTML = pasos.map(x => '<li class="paso"><h3>' + x.t + '</h3>' + x.cuerpo + '</li>').join("");
  $("props").innerHTML = props.map(x => '<div class="prop"><div class="k">' + x[0] + '</div><div class="v ' + x[2] + '">' + x[1] + '</div></div>').join("");
  $("resultado").innerHTML = '<div class="k">Respuesta final</div>' + resHTML;
  $("tagGraf").textContent = etiqueta;

  tabla(A, B, K);
  ajustarEscala();
  dibujar();
}

/* ============================================================
   TABLA RESUMEN
   ============================================================ */
function tabla(A, B, K) {
  const mA = mag(A), mB = mag(B), d = dot(A, B), cz = cruz(A, B);
  const cosT = (mA && mB) ? Math.max(-1, Math.min(1, d / (mA * mB))) : NaN;
  const filas = [
    ["Suma", "(a₁+b₁, a₂+b₂)", "(" + nf(A.x) + "+" + sgn(B.x) + ", " + nf(A.y) + "+" + sgn(B.y) + ")", vecTxt({x:A.x+B.x, y:A.y+B.y})],
    ["Resta", "(a₁−b₁, a₂−b₂)", "(" + nf(A.x) + "−" + sgn(B.x) + ", " + nf(A.y) + "−" + sgn(B.y) + ")", vecTxt({x:A.x-B.x, y:A.y-B.y})],
    ["Escalar k·A⃗", "(k·a₁, k·a₂)", "(" + nf(K) + "·" + sgn(A.x) + ", " + nf(K) + "·" + sgn(A.y) + ")", isNaN(K) ? "—" : vecTxt({x:K*A.x, y:K*A.y})],
    ["Magnitud |A⃗|", "√(a₁²+a₂²)", "√(" + nf(A.x**2) + "+" + nf(A.y**2) + ")", nf(mA)],
    ["Magnitud |B⃗|", "√(b₁²+b₂²)", "√(" + nf(B.x**2) + "+" + nf(B.y**2) + ")", nf(mB)],
    ["Dirección de A⃗", "arctan(a₂/a₁)", "arctan(" + nf(A.y) + "/" + nf(A.x) + ")", nf(angDir(A)) + "°"],
    ["Producto punto", "a₁b₁ + a₂b₂", nf(A.x) + "·" + sgn(B.x) + " + " + nf(A.y) + "·" + sgn(B.y), nf(d)],
    ["Ángulo θ", "arccos(A·B / |A||B|)", "arccos(" + nf(d) + "/" + nf(mA*mB) + ")", isNaN(cosT) ? "—" : nf(Math.acos(cosT)*180/Math.PI) + "°"],
    ["Producto cruz", "a₁b₂ − a₂b₁", nf(A.x) + "·" + sgn(B.y) + " − " + nf(A.y) + "·" + sgn(B.x), nf(cz)],
    ["Vector unitario û", "A⃗ / |A⃗|", "(" + nf(A.x) + ", " + nf(A.y) + ")/" + nf(mA), mA ? "(" + nf(A.x/mA,3) + ", " + nf(A.y/mA,3) + ")" : "—"],
    ["Proyección de A⃗ en B⃗", "[(A·B)/|B|²]·B⃗", "[" + nf(d) + "/" + nf(mB*mB) + "]·B⃗", mB ? vecTxt({x:(d/(mB*mB))*B.x, y:(d/(mB*mB))*B.y}) : "—"],
    ["Área del paralelogramo", "|A⃗ × B⃗|", "|" + nf(cz) + "|", nf(Math.abs(cz)) + " u²"]
  ];
  $("tbody").innerHTML = filas.map(f =>
    '<tr><td class="op">' + f[0] + '</td><td>' + f[1] + '</td><td>' + f[2] + '</td><td><b>' + f[3] + '</b></td></tr>').join("");
}

/* ============================================================
   GRÁFICA
   ============================================================ */
function ajustarEscala() {
  const pts = [A, B, R, AUX].filter(Boolean);
  if (["suma","resta"].includes(OP)) pts.push({x:A.x + B.x, y:A.y + B.y});
  const m = Math.max(3, ...pts.map(v => Math.max(Math.abs(v.x), Math.abs(v.y))));
  const w = lienzo.clientWidth || 600, h = 460;
  escala = Math.min(w, h) / (2.6 * m);
  cx = 0; cy = 0;
}

function ajustarLienzo() {
  const dpr = window.devicePixelRatio || 1;
  const w = lienzo.clientWidth, h = lienzo.clientHeight;
  lienzo.width = w * dpr; lienzo.height = h * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return {w, h};
}

const X = (x, o) => o.ox + x * escala;
const Y = (y, o) => o.oy - y * escala;

function flecha(x1, y1, x2, y2, color, grosor, punteada) {
  ctx.save();
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = grosor;
  ctx.setLineDash(punteada ? [6, 6] : []);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  ctx.setLineDash([]);
  const ang = Math.atan2(y2 - y1, x2 - x1), L = 13;
  if (Math.hypot(x2 - x1, y2 - y1) > 6) {
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - L * Math.cos(ang - .38), y2 - L * Math.sin(ang - .38));
    ctx.lineTo(x2 - L * Math.cos(ang + .38), y2 - L * Math.sin(ang + .38));
    ctx.closePath(); ctx.fill();
  }
  ctx.restore();
}

function rotulo(txt, x, y, color) {
  ctx.save();
  ctx.font = "bold 14px Consolas, monospace";
  const w = ctx.measureText(txt).width;
  ctx.fillStyle = "rgba(3,6,12,.85)";
  ctx.fillRect(x - 4, y - 14, w + 8, 19);
  ctx.strokeStyle = color; ctx.lineWidth = 1;
  ctx.strokeRect(x - 4, y - 14, w + 8, 19);
  ctx.fillStyle = color;
  ctx.fillText(txt, x, y);
  ctx.restore();
}

function dibujar() {
  const {w, h} = ajustarLienzo();
  const o = {ox: w / 2 + cx, oy: h / 2 + cy};
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#02040a"; ctx.fillRect(0, 0, w, h);

  /* --- cuadrícula --- */
  if ($("chkGrid").checked) {
    let paso = 1;
    while (paso * escala < 26) paso *= 2;
    ctx.strokeStyle = "rgba(56,189,248,.09)"; ctx.lineWidth = 1;
    ctx.beginPath();
    for (let x = Math.ceil(-o.ox / escala / paso) * paso; X(x, o) < w; x += paso) { ctx.moveTo(X(x, o), 0); ctx.lineTo(X(x, o), h); }
    for (let y = Math.floor((o.oy - h) / escala / paso) * paso; Y(y, o) > 0; y += paso) { ctx.moveTo(0, Y(y, o)); ctx.lineTo(w, Y(y, o)); }
    ctx.stroke();

    /* números de los ejes */
    ctx.fillStyle = "#6b7d94"; ctx.font = "11px Consolas, monospace"; ctx.textAlign = "center";
    for (let x = Math.ceil(-o.ox / escala / paso) * paso; X(x, o) < w; x += paso)
      if (x !== 0) ctx.fillText(nf(x, 1), X(x, o), Math.min(Math.max(o.oy + 14, 12), h - 4));
    ctx.textAlign = "right";
    for (let y = Math.floor((o.oy - h) / escala / paso) * paso; Y(y, o) > 0; y += paso)
      if (y !== 0) ctx.fillText(nf(y, 1), Math.min(Math.max(o.ox - 7, 24), w - 4), Y(y, o) + 4);
    ctx.textAlign = "left";
  }

  /* --- ejes --- */
  ctx.strokeStyle = "#4a5a70"; ctx.lineWidth = 1.6;
  ctx.beginPath();
  ctx.moveTo(0, o.oy); ctx.lineTo(w, o.oy);
  ctx.moveTo(o.ox, 0); ctx.lineTo(o.ox, h);
  ctx.stroke();
  ctx.fillStyle = "#9fb0c6"; ctx.font = "italic bold 13px Georgia, serif";
  ctx.fillText("x", w - 14, o.oy - 8);
  ctx.fillText("y", o.ox + 8, 15);
  ctx.fillText("O", o.ox + 6, o.oy + 15);

  const Ax = X(A.x, o), Ay = Y(A.y, o), Bx = X(B.x, o), By = Y(B.y, o);

  /* --- paralelogramo (suma) --- */
  if ($("chkParalelo").checked && ["suma","resta"].includes(OP)) {
    const S = OP === "suma" ? {x:A.x + B.x, y:A.y + B.y} : {x:A.x - B.x, y:A.y - B.y};
    const nB = OP === "suma" ? B : {x:-B.x, y:-B.y};
    const nBx = X(nB.x, o), nBy = Y(nB.y, o);
    ctx.save();
    ctx.fillStyle = "rgba(56,189,248,.07)";
    ctx.beginPath();
    ctx.moveTo(o.ox, o.oy); ctx.lineTo(Ax, Ay); ctx.lineTo(X(S.x, o), Y(S.y, o)); ctx.lineTo(nBx, nBy);
    ctx.closePath(); ctx.fill();
    ctx.restore();
    flecha(Ax, Ay, X(S.x, o), Y(S.y, o), "rgba(239,68,68,.5)", 1.6, true);
    flecha(nBx, nBy, X(S.x, o), Y(S.y, o), "rgba(56,189,248,.5)", 1.6, true);
    if (OP === "resta") flecha(o.ox, o.oy, nBx, nBy, "rgba(239,68,68,.55)", 1.8, true);
  }

  /* --- componentes --- */
  if ($("chkComp").checked) {
    ctx.save();
    ctx.setLineDash([4, 5]); ctx.lineWidth = 1.3;
    ctx.strokeStyle = "rgba(56,189,248,.55)";
    ctx.beginPath(); ctx.moveTo(Ax, Ay); ctx.lineTo(Ax, o.oy); ctx.moveTo(Ax, Ay); ctx.lineTo(o.ox, Ay); ctx.stroke();
    ctx.strokeStyle = "rgba(239,68,68,.55)";
    ctx.beginPath(); ctx.moveTo(Bx, By); ctx.lineTo(Bx, o.oy); ctx.moveTo(Bx, By); ctx.lineTo(o.ox, By); ctx.stroke();
    ctx.restore();
  }

  /* --- proyección --- */
  if (OP === "proyeccion" && AUX) {
    ctx.save();
    ctx.setLineDash([5, 5]); ctx.strokeStyle = "rgba(251,191,36,.75)"; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(Ax, Ay); ctx.lineTo(X(AUX.x, o), Y(AUX.y, o)); ctx.stroke();
    ctx.restore();
    flecha(o.ox, o.oy, X(AUX.x, o), Y(AUX.y, o), "#fbbf24", 4, false);
    rotulo("proy " + vecTxt(AUX), X(AUX.x, o) + 8, Y(AUX.y, o) + 20, "#fbbf24");
  }

  /* --- ángulo entre vectores --- */
  if (OP === "angulo" && mag(A) && mag(B)) {
    const r = Math.min(46, escala * .9);
    const a1 = Math.atan2(-A.y, A.x), a2 = Math.atan2(-B.y, B.x);
    ctx.save();
    ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.arc(o.ox, o.oy, r, a1, a2, cruz(A, B) > 0);
    ctx.stroke();
    const c = Math.max(-1, Math.min(1, dot(A,B)/(mag(A)*mag(B))));
    const med = (a1 + a2) / 2;
    rotulo(nf(Math.acos(c) * 180 / Math.PI) + "°", o.ox + (r + 14) * Math.cos(med) - 10, o.oy + (r + 14) * Math.sin(med) + 5, "#fbbf24");
    ctx.restore();
  }

  /* --- vectores principales --- */
  if (!["magnitud","unitario"].includes(OP)) {
    flecha(o.ox, o.oy, Bx, By, "#ef4444", 3.4, false);
    rotulo("B⃗ " + vecTxt(B), Bx + 9, By - 6, "#ef4444");
  }
  flecha(o.ox, o.oy, Ax, Ay, "#38bdf8", 3.4, false);
  rotulo("A⃗ " + vecTxt(A), Ax + 9, Ay - 6, "#38bdf8");

  /* --- resultante --- */
  if (R && OP !== "proyeccion") {
    flecha(o.ox, o.oy, X(R.x, o), Y(R.y, o), "#ffffff", 4, false);
    rotulo("R⃗ " + vecTxt(R), X(R.x, o) + 9, Y(R.y, o) + 20, "#ffffff");
  }

  /* --- magnitud sobre el vector A --- */
  if (["magnitud","unitario"].includes(OP)) {
    ctx.save();
    ctx.setLineDash([4, 5]); ctx.strokeStyle = "rgba(251,191,36,.7)"; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(Ax, Ay); ctx.lineTo(Ax, o.oy); ctx.lineTo(o.ox, o.oy); ctx.stroke();
    ctx.restore();
    rotulo("|A⃗| = " + nf(mag(A)), (o.ox + Ax) / 2 - 30, (o.oy + Ay) / 2 - 10, "#fbbf24");
  }
}

/* --- interacción con el lienzo --- */
lienzo.addEventListener("mousemove", e => {
  const r = lienzo.getBoundingClientRect();
  const o = {ox: r.width / 2 + cx, oy: r.height / 2 + cy};
  const x = (e.clientX - r.left - o.ox) / escala;
  const y = (o.oy - (e.clientY - r.top)) / escala;
  tip.style.display = "block";
  tip.style.left = Math.min(e.clientX - r.left + 14, r.width - 120) + "px";
  tip.style.top = (e.clientY - r.top - 34) + "px";
  tip.textContent = "(" + nf(x) + ", " + nf(y) + ")";
});
lienzo.addEventListener("mouseleave", () => tip.style.display = "none");

$("btnIn").onclick = () => { escala *= 1.25; dibujar(); };
$("btnOut").onclick = () => { escala /= 1.25; dibujar(); };
$("btnCentrar").onclick = () => { ajustarEscala(); dibujar(); };
["chkParalelo","chkComp","chkGrid"].forEach(id => $(id).onchange = dibujar);
window.addEventListener("resize", dibujar);

/* ============================================================
   EVENTOS
   ============================================================ */
$("btnResolver").onclick = resolver;
["ax","ay","bx","by","k"].forEach(id => $(id).addEventListener("keydown", e => { if (e.key === "Enter") resolver(); }));
$("op").addEventListener("change", resolver);

function cargarEjemplo(el) {
  const [a1, a2] = el.dataset.a.split(",");
  const [b1, b2] = el.dataset.b.split(",");
  $("ax").value = a1; $("ay").value = a2;
  $("bx").value = b1; $("by").value = b2;
  $("op").value = el.dataset.op;
  if (el.dataset.k) $("k").value = el.dataset.k;
  resolver();
  document.querySelector(".grid-2").scrollIntoView({behavior:"smooth", block:"start"});
}
document.querySelectorAll("#chips .chip, .ej .cargar").forEach(b => b.onclick = () => cargarEjemplo(b));

/* --- arranque --- */
resolver();
