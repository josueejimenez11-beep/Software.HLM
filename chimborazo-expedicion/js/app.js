/* ============================================================================
   EXPEDICIÓN CUMBRE CHIMBORAZO — Chimborazo Rey · Travel Explore
   Lógica de interfaz: teaser de portada, navegación, galería, cotizador,
   pestañas, acordeón y formulario de reserva.
   ========================================================================== */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  var MENOS_MOVIMIENTO = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Datos de contacto — punto único de edición */
  var CONTACTO = {
    whatsapp: '593968596592',
    correo:   'gustavocc1982@hotmail.com',
    empresa:  'Chimborazo Rey · Travel Explore'
  };

  /* ==========================================================================
     1. PORTADA: video de fondo con teaser cinematográfico de respaldo
     ========================================================================== */
  function iniciarPortada() {
    var hero   = $('.hero');
    var video  = $('#heroVideo');
    var teaser = $('#heroTeaser');
    if (!hero || !teaser) return;

    var tomas = $$('.hero__toma', teaser);
    var indice = 0;
    var temporizador = null;

    function activarTeaser() {
      if (hero.classList.contains('sin-video')) return;
      hero.classList.add('sin-video');
      if (video) { try { video.pause(); } catch (e) {} }
      if (!tomas.length) return;

      tomas[0].classList.add('viva');
      if (MENOS_MOVIMIENTO || tomas.length === 1) return;

      temporizador = setInterval(function () {
        tomas[indice].classList.remove('viva');
        indice = (indice + 1) % tomas.length;
        // reinicia la animación Ken Burns de la nueva toma
        var siguiente = tomas[indice];
        siguiente.style.animation = 'none';
        void siguiente.offsetWidth;
        siguiente.style.animation = '';
        siguiente.classList.add('viva');
      }, 6500);
    }

    if (!video) { activarTeaser(); return; }

    // Si el navegador no logra cargar ninguna fuente de video, se usa el teaser.
    var fuentes = $$('source', video);
    var fallidas = 0;
    fuentes.forEach(function (f) {
      f.addEventListener('error', function () {
        fallidas++;
        if (fallidas >= fuentes.length) activarTeaser();
      });
    });
    video.addEventListener('error', activarTeaser);

    // Margen de gracia: si en 2,5 s no hay datos suficientes, se asume ausencia de archivo.
    setTimeout(function () {
      if (video.readyState < 2) activarTeaser();
    }, 2500);

    // Algunos navegadores bloquean la autorreproducción incluso en silencio.
    var intento = video.play();
    if (intento && typeof intento.catch === 'function') {
      intento.catch(function () { activarTeaser(); });
    }

    // Libera recursos cuando la portada sale de pantalla.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          if (hero.classList.contains('sin-video')) {
            if (temporizador && !e.isIntersecting) { clearInterval(temporizador); temporizador = null; }
            else if (!temporizador && e.isIntersecting && !MENOS_MOVIMIENTO) { activarTeaserReanudar(); }
          } else if (video) {
            if (e.isIntersecting) { video.play().catch(function () {}); } else { video.pause(); }
          }
        });
      }, { threshold: 0.05 }).observe(hero);
    }

    function activarTeaserReanudar() {
      if (temporizador || tomas.length < 2) return;
      temporizador = setInterval(function () {
        tomas[indice].classList.remove('viva');
        indice = (indice + 1) % tomas.length;
        tomas[indice].classList.add('viva');
      }, 6500);
    }
  }

  /* ==========================================================================
     2. NAVEGACIÓN: fondo sólido, menú móvil, sección activa y progreso
     ========================================================================== */
  function iniciarNavegacion() {
    var nav    = $('#nav');
    var menu   = $('#menu');
    var boton  = $('#hamburguesa');
    var barra  = $('#progresoBarra');
    var arriba = $('#arriba');
    var enlaces = $$('#menu a[href^="#"]');
    var secciones = enlaces
      .map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); })
      .filter(Boolean);

    function alDesplazar() {
      var y = window.scrollY || document.documentElement.scrollTop;

      if (nav) nav.classList.toggle('solida', y > 40);
      if (arriba) arriba.classList.toggle('visible', y > 700);

      if (barra) {
        var alto = document.documentElement.scrollHeight - window.innerHeight;
        barra.style.width = (alto > 0 ? (y / alto) * 100 : 0) + '%';
      }

      var actual = '';
      secciones.forEach(function (s) {
        if (s.offsetTop - 140 <= y) actual = s.id;
      });
      enlaces.forEach(function (a) {
        a.classList.toggle('activo', a.getAttribute('href') === '#' + actual);
      });
    }

    var pendiente = false;
    window.addEventListener('scroll', function () {
      if (pendiente) return;
      pendiente = true;
      requestAnimationFrame(function () { alDesplazar(); pendiente = false; });
    }, { passive: true });
    alDesplazar();

    if (boton && menu) {
      boton.addEventListener('click', function () {
        var abierto = menu.classList.toggle('abierto');
        boton.setAttribute('aria-expanded', String(abierto));
        boton.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
      });
      menu.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') {
          menu.classList.remove('abierto');
          boton.setAttribute('aria-expanded', 'false');
        }
      });
    }

    if (arriba) {
      arriba.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: MENOS_MOVIMIENTO ? 'auto' : 'smooth' });
      });
    }
  }

  /* ==========================================================================
     3. REVELADO PROGRESIVO AL DESPLAZAR
     ========================================================================== */
  function iniciarRevelado() {
    var elementos = $$('.reveal');
    if (!elementos.length) return;

    if (!('IntersectionObserver' in window) || MENOS_MOVIMIENTO) {
      elementos.forEach(function (el) { el.classList.add('visible'); });
      return;
    }

    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        var hermanos = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
        e.target.style.transitionDelay = Math.min(hermanos % 4, 3) * 90 + 'ms';
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    elementos.forEach(function (el) { obs.observe(el); });
  }

  /* ==========================================================================
     4. CONTADORES DE LA PORTADA
     ========================================================================== */
  function iniciarContadores() {
    var nodos = $$('[data-contador]');
    if (!nodos.length) return;

    function animar(nodo) {
      var destino = parseInt(nodo.getAttribute('data-contador'), 10) || 0;
      var sufijo  = nodo.getAttribute('data-sufijo') || '';
      if (MENOS_MOVIMIENTO) { nodo.textContent = destino.toLocaleString('es-EC') + sufijo; return; }

      var inicio = null, duracion = 1500;
      function paso(t) {
        if (inicio === null) inicio = t;
        var p = Math.min((t - inicio) / duracion, 1);
        var suave = 1 - Math.pow(1 - p, 3);
        nodo.textContent = Math.round(destino * suave).toLocaleString('es-EC') + sufijo;
        if (p < 1) requestAnimationFrame(paso);
      }
      requestAnimationFrame(paso);
    }

    if (!('IntersectionObserver' in window)) { nodos.forEach(animar); return; }
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        animar(e.target);
        obs.unobserve(e.target);
      });
    }, { threshold: 0.5 });
    nodos.forEach(function (n) { obs.observe(n); });
  }

  /* ==========================================================================
     5. GALERÍA: filtros y visor de imágenes
     ========================================================================== */
  function iniciarGaleria() {
    var contenedor = $('#galeriaGrid');
    if (!contenedor) return;

    var fotos = $$('.foto', contenedor);

    /* --- Filtros por categoría --- */
    $$('#filtros .filtro').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-filtro');
        $$('#filtros .filtro').forEach(function (b) { b.classList.remove('activo'); });
        btn.classList.add('activo');
        fotos.forEach(function (f) {
          f.classList.toggle('oculta', cat !== 'todas' && f.getAttribute('data-cat') !== cat);
        });
      });
    });

    /* --- Visor --- */
    var visor     = $('#visor');
    var lienzo    = $('#visorLienzo');
    var titulo    = $('#visorTitulo');
    var pie       = $('#visorPie');
    var contador  = $('#visorContador');
    if (!visor) return;

    var actual = 0;
    var ultimoFoco = null;

    function visibles() { return fotos.filter(function (f) { return !f.classList.contains('oculta'); }); }

    function pintar(i) {
      var lista = visibles();
      if (!lista.length) return;
      actual = (i + lista.length) % lista.length;
      var foto = lista[actual];

      lienzo.innerHTML = '';
      var img  = foto.querySelector('img');
      var arte = foto.querySelector('.arte svg');
      if (img) {
        var copia = document.createElement('img');
        copia.src = img.currentSrc || img.src;
        copia.alt = img.alt;
        lienzo.appendChild(copia);
      } else if (arte) {
        var svg = arte.cloneNode(true);
        svg.setAttribute('width', '620');
        svg.setAttribute('height', '620');
        lienzo.appendChild(svg);
      }

      titulo.textContent   = foto.getAttribute('data-titulo') || '';
      pie.textContent      = foto.getAttribute('data-pie') || '';
      contador.textContent = String(actual + 1).padStart(2, '0') + ' / ' + String(lista.length).padStart(2, '0');
    }

    function abrir(i) {
      ultimoFoco = document.activeElement;
      visor.hidden = false;
      pintar(i);
      requestAnimationFrame(function () { visor.classList.add('abierto'); });
      document.body.style.overflow = 'hidden';
      $('#visorCerrar').focus();
    }

    function cerrar() {
      visor.classList.remove('abierto');
      document.body.style.overflow = '';
      setTimeout(function () { visor.hidden = true; lienzo.innerHTML = ''; }, 300);
      if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
    }

    fotos.forEach(function (f) {
      f.setAttribute('tabindex', '0');
      f.setAttribute('role', 'button');
      f.addEventListener('click', function () { abrir(visibles().indexOf(f)); });
      f.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrir(visibles().indexOf(f)); }
      });
    });

    $('#visorCerrar').addEventListener('click', cerrar);
    $('#visorPrev').addEventListener('click', function () { pintar(actual - 1); });
    $('#visorNext').addEventListener('click', function () { pintar(actual + 1); });
    visor.addEventListener('click', function (e) { if (e.target === visor) cerrar(); });

    document.addEventListener('keydown', function (e) {
      if (visor.hidden) return;
      if (e.key === 'Escape')     cerrar();
      if (e.key === 'ArrowLeft')  pintar(actual - 1);
      if (e.key === 'ArrowRight') pintar(actual + 1);
    });
  }

  /* ==========================================================================
     6. PESTAÑAS DE EQUIPO Y SEGURIDAD
     ========================================================================== */
  function iniciarPestanas() {
    var raiz = $('#pestanas');
    if (!raiz) return;
    var botones = $$('[role="tab"]', raiz);

    function activar(btn) {
      botones.forEach(function (b) {
        var elegido = b === btn;
        b.setAttribute('aria-selected', String(elegido));
        var panel = document.getElementById(b.getAttribute('aria-controls'));
        if (!panel) return;
        panel.hidden = !elegido;
        panel.classList.toggle('activo', elegido);
      });
    }

    botones.forEach(function (btn, i) {
      btn.addEventListener('click', function () { activar(btn); });
      btn.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var sig = botones[(i + d + botones.length) % botones.length];
        sig.focus();
        activar(sig);
      });
    });
  }

  /* ==========================================================================
     7. ACORDEÓN DE PREGUNTAS FRECUENTES
     ========================================================================== */
  function iniciarAcordeon() {
    var raiz = $('#acordeon');
    if (!raiz) return;

    $$('.item__btn', raiz).forEach(function (btn) {
      var panel = btn.nextElementSibling;
      btn.addEventListener('click', function () {
        var abierto = btn.getAttribute('aria-expanded') === 'true';

        $$('.item__btn', raiz).forEach(function (otro) {
          otro.setAttribute('aria-expanded', 'false');
          otro.nextElementSibling.style.maxHeight = null;
        });

        if (!abierto) {
          btn.setAttribute('aria-expanded', 'true');
          panel.style.maxHeight = panel.scrollHeight + 'px';
        }
      });
    });

    window.addEventListener('resize', function () {
      $$('.item__btn[aria-expanded="true"]', raiz).forEach(function (b) {
        b.nextElementSibling.style.maxHeight = b.nextElementSibling.scrollHeight + 'px';
      });
    });
  }

  /* ==========================================================================
     8. COTIZADOR
     ========================================================================== */
  var BASE = 300; // Cumbre Chimborazo, USD por persona

  function estadoCotizador() {
    var pax = parseInt(($('#cotPax') || {}).value, 10);
    if (isNaN(pax) || pax < 1) pax = 1;
    if (pax > 6) pax = 6;

    var extras = $$('.cot-extra:checked').map(function (c) {
      return { nombre: c.getAttribute('data-nombre'), precio: parseFloat(c.getAttribute('data-precio')) || 0 };
    });

    var porPersona = BASE + extras.reduce(function (a, e) { return a + e.precio; }, 0);
    return { pax: pax, extras: extras, porPersona: porPersona, total: porPersona * pax };
  }

  function iniciarCotizador() {
    var pax   = $('#cotPax');
    var total = $('#cotTotal');
    var det   = $('#cotDetalle');
    if (!pax || !total) return;

    function refrescar() {
      var e = estadoCotizador();
      total.textContent = 'USD ' + e.total.toLocaleString('es-EC');
      var partes = [e.pax + (e.pax === 1 ? ' montañista' : ' montañistas'), 'USD ' + e.porPersona + ' p/p'];
      det.textContent = partes.join(' · ') +
        (e.extras.length ? ' · ' + e.extras.length + (e.extras.length === 1 ? ' complemento' : ' complementos') : ' · programa base');
    }

    pax.addEventListener('input', refrescar);
    pax.addEventListener('change', function () {
      var v = parseInt(pax.value, 10);
      if (isNaN(v) || v < 1) pax.value = 1;
      if (v > 6) pax.value = 6;
      refrescar();
    });
    $$('.cot-extra').forEach(function (c) { c.addEventListener('change', refrescar); });

    // Al pasar a reserva, arrastra el número de montañistas
    var ir = $('#cotIrReserva');
    if (ir) {
      ir.addEventListener('click', function () {
        var campo = $('#fPax');
        if (campo) campo.value = estadoCotizador().pax;
      });
    }

    refrescar();
  }

  /* ==========================================================================
     9. FORMULARIO DE RESERVA
     ========================================================================== */
  function iniciarFormulario() {
    var form = $('#formulario');
    if (!form) return;
    var aviso = $('#avisoForm');

    var REGLAS = {
      fNombre: function (v) {
        if (!v.trim()) return 'Indique su nombre completo.';
        if (v.trim().length < 3) return 'El nombre es demasiado corto.';
        return '';
      },
      fEmail: function (v) {
        if (!v.trim()) return 'Necesitamos un correo para enviarle la cotización.';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())) return 'El formato del correo no es válido.';
        return '';
      },
      fTelefono: function (v) {
        if (v.trim() && !/^[+]?[\d\s()-]{7,20}$/.test(v.trim())) return 'Revise el número telefónico.';
        return '';
      },
      fFecha: function (v) {
        if (!v) return 'Seleccione una fecha tentativa.';
        var hoy = new Date(); hoy.setHours(0, 0, 0, 0);
        if (new Date(v + 'T00:00:00') < hoy) return 'La fecha debe ser posterior a hoy.';
        return '';
      },
      fPax: function (v) {
        var n = parseInt(v, 10);
        if (isNaN(n) || n < 1) return 'Indique al menos un montañista.';
        if (n > 6) return 'Máximo seis montañistas por salida. Escríbanos para grupos mayores.';
        return '';
      }
    };

    function validarCampo(id) {
      var campo = document.getElementById(id);
      if (!campo || !REGLAS[id]) return true;
      var msj = REGLAS[id](campo.value);
      var salida = $('[data-error="' + id + '"]');
      if (salida) salida.textContent = msj;
      campo.classList.toggle('invalido', !!msj);
      campo.setAttribute('aria-invalid', msj ? 'true' : 'false');
      return !msj;
    }

    Object.keys(REGLAS).forEach(function (id) {
      var campo = document.getElementById(id);
      if (!campo) return;
      campo.addEventListener('blur', function () { validarCampo(id); });
      campo.addEventListener('input', function () {
        if (campo.classList.contains('invalido')) validarCampo(id);
      });
    });

    function validarTodo() {
      return Object.keys(REGLAS).map(validarCampo).every(Boolean);
    }

    function datos() {
      var cot = estadoCotizador();
      return {
        nombre:      ($('#fNombre') || {}).value || '',
        email:       ($('#fEmail') || {}).value || '',
        telefono:    ($('#fTelefono') || {}).value || '—',
        fecha:       ($('#fFecha') || {}).value || '—',
        pax:         ($('#fPax') || {}).value || '1',
        experiencia: ($('#fExperiencia') || {}).value || '—',
        mensaje:     ($('#fMensaje') || {}).value || '—',
        extras:      cot.extras.map(function (e) { return e.nombre; }).join(', ') || 'ninguno'
      };
    }

    function resumen(d) {
      return [
        'SOLICITUD — EXPEDICIÓN CUMBRE CHIMBORAZO 6.268 m',
        '',
        'Nombre: ' + d.nombre,
        'Correo: ' + d.email,
        'Teléfono: ' + d.telefono,
        'Fecha tentativa: ' + d.fecha,
        'N.º de montañistas: ' + d.pax,
        'Experiencia previa: ' + d.experiencia,
        'Complementos de interés: ' + d.extras,
        '',
        'Mensaje: ' + d.mensaje
      ].join('\n');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validarTodo()) {
        aviso.className = 'aviso-form mal';
        aviso.textContent = 'Revise los campos marcados antes de enviar la solicitud.';
        var primero = $('.invalido', form);
        if (primero) primero.focus();
        return;
      }

      var d = datos();
      var asunto = 'Solicitud Cumbre Chimborazo — ' + d.nombre + ' (' + d.fecha + ')';
      window.location.href = 'mailto:' + CONTACTO.correo +
        '?subject=' + encodeURIComponent(asunto) +
        '&body=' + encodeURIComponent(resumen(d));

      aviso.className = 'aviso-form ok';
      aviso.textContent = 'Gracias, ' + d.nombre.split(' ')[0] +
        '. Se abrió su gestor de correo con la solicitud lista para enviar. ' +
        'Si no ocurrió, escríbanos a ' + CONTACTO.correo + ' o por WhatsApp.';
    });

    var whats = $('#btnWhats');
    if (whats) {
      whats.addEventListener('click', function () {
        if (!validarTodo()) {
          aviso.className = 'aviso-form mal';
          aviso.textContent = 'Complete los campos obligatorios para armar el mensaje de WhatsApp.';
          var primero = $('.invalido', form);
          if (primero) primero.focus();
          return;
        }
        var url = 'https://wa.me/' + CONTACTO.whatsapp + '?text=' + encodeURIComponent(resumen(datos()));
        window.open(url, '_blank', 'noopener');
        aviso.className = 'aviso-form ok';
        aviso.textContent = 'Abrimos WhatsApp con su solicitud. Le respondemos el mismo día.';
      });
    }

    // Fecha mínima = mañana
    var fecha = $('#fFecha');
    if (fecha) {
      var m = new Date();
      m.setDate(m.getDate() + 1);
      fecha.min = m.toISOString().slice(0, 10);
    }
  }

  /* ==========================================================================
     10. VARIOS
     ========================================================================== */
  function iniciarVarios() {
    var anio = $('#anio');
    if (anio) anio.textContent = new Date().getFullYear();
  }

  /* ========================================================================== */
  function iniciar() {
    iniciarPortada();
    iniciarNavegacion();
    iniciarRevelado();
    iniciarContadores();
    iniciarGaleria();
    iniciarPestanas();
    iniciarAcordeon();
    iniciarCotizador();
    iniciarFormulario();
    iniciarVarios();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
