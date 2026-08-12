/* ==========================================================================
   CHIMBORAZO REY · main.js
   Núcleo compartido por las cuatro páginas:
   navbar, idiomas, animaciones, lightbox, modales, formularios y contacto.

   Expone el espacio de nombres global `CR` para que los scripts de cada
   página (restaurante.js, lodge.js, travel.js) reutilicen sus utilidades.
   ========================================================================== */

'use strict';

const CR = (() => {

  /* ----------------------------------------------------------------------
     Datos de contacto reales del negocio.
     Modifica únicamente este bloque si cambian los datos oficiales.
     ---------------------------------------------------------------------- */
  const CONTACT = {
    phoneDisplay: '0968596592',
    phoneTel: '+593968596592',
    whatsapp: '593968596592',        // formato internacional sin signos
    email: 'gustavocc1982@hotmail.com',
    // Enlace de indicaciones basado en la ubicación descrita (sin coordenadas inventadas).
    mapsQuery: 'Cruz del Arenal, Guaranda, Bolívar, Ecuador'
  };

  const STORAGE_KEY = 'chimborazo-rey-lang';

  /* Acceso tolerante a localStorage: algunos navegadores lo bloquean
     en modo privado o con las cookies deshabilitadas. */
  const storage = {
    get(key) {
      try { return localStorage.getItem(key); } catch { return null; }
    },
    set(key, value) {
      try { localStorage.setItem(key, value); } catch { /* preferencia no persistida */ }
    }
  };

  /* ----------------------------------------------------------------------
     Utilidades generales
     ---------------------------------------------------------------------- */
  const $  = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

  const prefersReducedMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /** Ejecuta un callback como máximo una vez por frame de animación. */
  const rafThrottle = (fn) => {
    let ticking = false;
    return (...args) => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(() => {
        fn(...args);
        ticking = false;
      });
    };
  };

  /* ----------------------------------------------------------------------
     Sistema multiidioma
     ---------------------------------------------------------------------- */
  const i18n = {
    current: DEFAULT_LANG,

    /** Devuelve la traducción de una clave con retorno seguro. */
    t(key, lang = i18n.current) {
      const dict = translations[lang] || translations[DEFAULT_LANG];
      if (key in dict) return dict[key];
      const fallback = translations[DEFAULT_LANG][key];
      if (fallback !== undefined) return fallback;
      console.warn(`[i18n] Clave sin traducción: ${key}`);
      return key;
    },

    /**
     * Devuelve el idioma guardado por el visitante.
     * Si todavía no ha elegido ninguno, el sitio arranca siempre en español.
     */
    detect() {
      const stored = storage.get(STORAGE_KEY);
      return stored && translations[stored] ? stored : DEFAULT_LANG;
    },

    /** Aplica las traducciones a un contenedor (por defecto, todo el documento). */
    apply(scope = document) {
      const lang = i18n.current;

      $$('[data-i18n]', scope).forEach((el) => {
        el.textContent = i18n.t(el.dataset.i18n, lang);
      });

      $$('[data-i18n-html]', scope).forEach((el) => {
        el.innerHTML = i18n.t(el.dataset.i18nHtml, lang);
      });

      const attrMap = {
        'data-i18n-placeholder': 'placeholder',
        'data-i18n-aria-label': 'aria-label',
        'data-i18n-title': 'title',
        'data-i18n-alt': 'alt',
        'data-i18n-content': 'content',
        'data-i18n-value': 'value'
      };

      Object.entries(attrMap).forEach(([dataAttr, htmlAttr]) => {
        $$(`[${dataAttr}]`, scope).forEach((el) => {
          el.setAttribute(htmlAttr, i18n.t(el.getAttribute(dataAttr), lang));
        });
      });
    },

    /** Cambia el idioma activo, lo guarda y notifica al resto de scripts. */
    set(lang) {
      if (!translations[lang]) return;

      i18n.current = lang;
      storage.set(STORAGE_KEY, lang);
      document.documentElement.lang = lang;

      if (document.title) {
        const titleKey = document.documentElement.dataset.titleKey;
        if (titleKey) document.title = i18n.t(titleKey, lang);
      }

      i18n.apply();
      updateLangUI(lang);

      // Permite que cada página vuelva a renderizar su contenido dinámico.
      document.dispatchEvent(new CustomEvent('cr:langchange', { detail: { lang } }));
    }
  };

  /** Sincroniza el selector del navbar y los botones del footer. */
  function updateLangUI(lang) {
    const meta = LANGS[lang];

    const currentFlag = $('.lang__current-flag');
    const currentCode = $('.lang__current-code');
    if (currentFlag) currentFlag.textContent = meta.flag;
    if (currentCode) currentCode.textContent = meta.code;

    $$('.lang__option').forEach((btn) => {
      btn.setAttribute('aria-selected', String(btn.dataset.lang === lang));
    });

    $$('.footer__lang-btn').forEach((btn) => {
      btn.setAttribute('aria-pressed', String(btn.dataset.lang === lang));
    });
  }

  /* ----------------------------------------------------------------------
     Navbar: scroll, menú móvil y selector de idioma
     ---------------------------------------------------------------------- */
  function initNavbar() {
    const navbar = $('.navbar');
    if (!navbar) return;

    const burger = $('.navbar__burger', navbar);
    const nav = $('.navbar__nav', navbar);
    const langToggle = $('.lang__toggle', navbar);
    const langList = $('.lang__list', navbar);

    /* --- Fondo del navbar al desplazarse --- */
    const solidFromStart = navbar.dataset.solid === 'true';

    const onScroll = rafThrottle(() => {
      navbar.classList.toggle('is-scrolled', solidFromStart || window.scrollY > 40);
    });

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    /* --- Menú hamburguesa --- */
    const closeNav = () => {
      if (!burger || !nav) return;
      burger.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      document.body.classList.remove('is-nav-open');
    };

    if (burger && nav) {
      burger.addEventListener('click', () => {
        const open = burger.getAttribute('aria-expanded') === 'true';
        burger.setAttribute('aria-expanded', String(!open));
        nav.classList.toggle('is-open', !open);
        document.body.classList.toggle('is-nav-open', !open);
      });

      // Al pulsar un enlace del menú móvil se cierra la navegación.
      $$('.navbar__link, .navbar__actions .btn', nav).forEach((el) => {
        el.addEventListener('click', closeNav);
      });

      window.addEventListener('resize', rafThrottle(() => {
        if (window.innerWidth > 960) closeNav();
      }), { passive: true });
    }

    /* --- Selector de idioma --- */
    const closeLang = () => {
      if (!langToggle || !langList) return;
      langToggle.setAttribute('aria-expanded', 'false');
      langList.classList.remove('is-open');
    };

    if (langToggle && langList) {
      langToggle.addEventListener('click', (event) => {
        event.stopPropagation();
        const open = langToggle.getAttribute('aria-expanded') === 'true';
        langToggle.setAttribute('aria-expanded', String(!open));
        langList.classList.toggle('is-open', !open);
      });

      langList.addEventListener('click', (event) => {
        const option = event.target.closest('.lang__option');
        if (!option) return;
        i18n.set(option.dataset.lang);
        closeLang();
      });

      document.addEventListener('click', (event) => {
        if (!event.target.closest('.lang')) closeLang();
      });
    }

    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') return;
      closeLang();
      closeNav();
    });

    /* --- Botones de idioma del footer --- */
    $$('.footer__lang-btn').forEach((btn) => {
      btn.addEventListener('click', () => i18n.set(btn.dataset.lang));
    });
  }

  /* ----------------------------------------------------------------------
     Animaciones al hacer scroll
     ---------------------------------------------------------------------- */
  let revealObserver = null;

  function initReveal() {
    const targets = $$('[data-animate]');
    if (!targets.length) return;

    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
      targets.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const delay = Number(entry.target.dataset.animateDelay || 0);
        if (delay) entry.target.style.transitionDelay = `${delay}ms`;

        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    targets.forEach((el) => revealObserver.observe(el));
  }

  /** Registra elementos creados dinámicamente (tarjetas del menú, etc.). */
  function observeReveal(elements) {
    const list = Array.isArray(elements) ? elements : [elements];
    if (!revealObserver) {
      list.forEach((el) => el && el.classList.add('is-visible'));
      return;
    }
    list.forEach((el) => el && revealObserver.observe(el));
  }

  /* ----------------------------------------------------------------------
     Gestión de superposiciones (modales y lightbox)
     ---------------------------------------------------------------------- */
  const overlay = {
    active: null,
    lastFocus: null,

    open(element) {
      overlay.lastFocus = document.activeElement;
      overlay.active = element;
      element.classList.add('is-open');
      element.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      const focusable = element.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusable) focusable.focus({ preventScroll: true });
    },

    close() {
      if (!overlay.active) return;
      overlay.active.classList.remove('is-open');
      overlay.active.setAttribute('aria-hidden', 'true');
      overlay.active = null;
      document.body.style.overflow = '';

      if (overlay.lastFocus) {
        overlay.lastFocus.focus({ preventScroll: true });
        overlay.lastFocus = null;
      }
    },

    /** Mantiene el foco dentro de la superposición abierta. */
    trapFocus(event) {
      if (!overlay.active || event.key !== 'Tab') return;

      const focusables = Array.from(overlay.active.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])'
      )).filter((el) => el.offsetParent !== null);

      if (!focusables.length) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  };

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') overlay.close();
    overlay.trapFocus(event);
  });

  /* ----------------------------------------------------------------------
     Lightbox de galerías
     ---------------------------------------------------------------------- */
  function initLightbox() {
    const gallery = $('[data-lightbox]');
    if (!gallery) return;

    const box = $('#lightbox');
    if (!box) return;

    const image = $('.lightbox__img', box);
    const caption = $('.lightbox__caption', box);
    let items = [];
    let index = 0;

    const render = () => {
      const item = items[index];
      if (!item) return;
      image.src = item.src;
      image.alt = item.alt;
      caption.textContent = item.alt;
    };

    const move = (step) => {
      index = (index + step + items.length) % items.length;
      render();
    };

    gallery.addEventListener('click', (event) => {
      const trigger = event.target.closest('.gallery__item');
      if (!trigger) return;

      items = $$('.gallery__item img', gallery).map((img) => ({
        src: img.dataset.full || img.src,
        alt: img.alt
      }));

      index = $$('.gallery__item', gallery).indexOf(trigger);
      render();
      overlay.open(box);
    });

    $('.lightbox__btn--close', box).addEventListener('click', () => overlay.close());
    $('.lightbox__btn--prev', box).addEventListener('click', () => move(-1));
    $('.lightbox__btn--next', box).addEventListener('click', () => move(1));

    box.addEventListener('click', (event) => {
      if (event.target === box) overlay.close();
    });

    document.addEventListener('keydown', (event) => {
      if (overlay.active !== box) return;
      if (event.key === 'ArrowLeft') move(-1);
      if (event.key === 'ArrowRight') move(1);
    });
  }

  /* ----------------------------------------------------------------------
     Formularios: validación en el navegador y envío por WhatsApp
     ---------------------------------------------------------------------- */
  const PATTERNS = {
    email: /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i,
    phone: /^[+\d][\d\s().-]{6,19}$/
  };

  const todayISO = () => new Date().toISOString().slice(0, 10);

  function setFieldError(field, messageKey) {
    const wrapper = field.closest('.field');
    if (!wrapper) return;

    const errorBox = $('.field__error', wrapper);
    const hasError = Boolean(messageKey);

    wrapper.classList.toggle('has-error', hasError);
    field.setAttribute('aria-invalid', String(hasError));

    if (errorBox) {
      errorBox.textContent = hasError ? i18n.t(messageKey) : '';
      // Guarda la clave para poder retraducir el mensaje al cambiar de idioma.
      if (hasError) errorBox.dataset.errorKey = messageKey;
      else delete errorBox.dataset.errorKey;
    }
  }

  /** Valida un campo individual y devuelve true si es válido. */
  function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');

    if (isRequired && !value) {
      setFieldError(field, 'form.required');
      return false;
    }

    if (!value) {
      setFieldError(field, null);
      return true;
    }

    if (field.type === 'email' && !PATTERNS.email.test(value)) {
      setFieldError(field, 'form.invalidEmail');
      return false;
    }

    if (field.dataset.validate === 'phone' && !PATTERNS.phone.test(value)) {
      setFieldError(field, 'form.invalidPhone');
      return false;
    }

    if (field.type === 'number') {
      const num = Number(value);
      const min = field.min !== '' ? Number(field.min) : -Infinity;
      const max = field.max !== '' ? Number(field.max) : Infinity;
      if (Number.isNaN(num) || num < min || num > max) {
        setFieldError(field, 'form.invalidNumber');
        return false;
      }
    }

    if (field.type === 'date' && field.dataset.notPast === 'true' && value < todayISO()) {
      setFieldError(field, 'form.pastDate');
      return false;
    }

    if (field.dataset.after) {
      const reference = $(field.dataset.after);
      if (reference && reference.value && value <= reference.value) {
        setFieldError(field, 'form.dateOrder');
        return false;
      }
    }

    setFieldError(field, null);
    return true;
  }

  /** Valida el formulario completo y enfoca el primer campo con error. */
  function validateForm(form) {
    const fields = $$('input, select, textarea', form);
    let firstInvalid = null;

    fields.forEach((field) => {
      if (!validateField(field) && !firstInvalid) firstInvalid = field;
    });

    if (firstInvalid) {
      firstInvalid.focus({ preventScroll: false });
      return false;
    }
    return true;
  }

  /** Muestra el mensaje de resultado bajo el formulario. */
  function showFeedback(form, type, messageKey) {
    const box = $('.form__feedback', form);
    if (!box) return;

    box.classList.remove('is-success', 'is-error');
    box.classList.add('is-visible', type === 'success' ? 'is-success' : 'is-error');
    box.dataset.i18n = messageKey;
    box.textContent = i18n.t(messageKey);
    box.setAttribute('role', 'status');
  }

  /** Construye el texto del mensaje a partir de pares etiqueta/valor. */
  function buildMessage(titleKey, rows) {
    const lines = [i18n.t(titleKey), ''];
    rows.forEach(([labelKey, value]) => {
      if (value === '' || value === null || value === undefined) return;
      lines.push(`${i18n.t(labelKey)}: ${value}`);
    });
    return lines.join('\n');
  }

  /** Abre WhatsApp con un mensaje prellenado. */
  function openWhatsApp(text) {
    const url = `https://wa.me/${CONTACT.whatsapp}?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank', 'noopener');
  }

  /**
   * Conecta un formulario con la validación y el envío por WhatsApp.
   * No existe backend: los datos nunca se almacenan ni se envían solos.
   */
  function initForm(formSelector, { titleKey, rows }) {
    const form = $(formSelector);
    if (!form) return;

    // Impide seleccionar fechas pasadas desde el propio control del navegador.
    $$('input[type="date"][data-not-past="true"]', form).forEach((input) => {
      input.min = todayISO();
    });

    // Validación en vivo una vez que el campo ha perdido el foco al menos una vez.
    $$('input, select, textarea', form).forEach((field) => {
      field.addEventListener('blur', () => validateField(field), { passive: true });
      field.addEventListener('input', () => {
        if (field.closest('.field')?.classList.contains('has-error')) validateField(field);
      });
    });

    form.addEventListener('submit', (event) => {
      event.preventDefault();

      if (!validateForm(form)) {
        showFeedback(form, 'error', 'form.errorSummary');
        return;
      }

      openWhatsApp(buildMessage(titleKey, rows(form)));
      showFeedback(form, 'success', 'form.success');
    });

    // Botón alternativo: consulta directa por WhatsApp sin validar el formulario.
    const waButton = $('[data-wa-direct]', form);
    if (waButton) {
      waButton.addEventListener('click', () => openWhatsApp(i18n.t(titleKey)));
    }
  }

  /* ----------------------------------------------------------------------
     Enlaces de contacto y año del footer
     ---------------------------------------------------------------------- */
  function initContactLinks() {
    $$('[data-contact="tel"]').forEach((el) => {
      el.href = `tel:${CONTACT.phoneTel}`;
      if (el.dataset.fill === 'true') el.textContent = CONTACT.phoneDisplay;
    });

    $$('[data-contact="email"]').forEach((el) => {
      el.href = `mailto:${CONTACT.email}`;
      if (el.dataset.fill === 'true') el.textContent = CONTACT.email;
    });

    $$('[data-contact="whatsapp"]').forEach((el) => {
      el.href = `https://wa.me/${CONTACT.whatsapp}`;
      el.target = '_blank';
      el.rel = 'noopener';
    });

    $$('[data-contact="maps"]').forEach((el) => {
      el.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(CONTACT.mapsQuery)}`;
      el.target = '_blank';
      el.rel = 'noopener';
    });

    const year = $('[data-year]');
    if (year) year.textContent = new Date().getFullYear();
  }

  /* ----------------------------------------------------------------------
     Desplazamiento suave para enlaces internos
     ---------------------------------------------------------------------- */
  function initSmoothScroll() {
    document.addEventListener('click', (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;

      const id = link.getAttribute('href');
      if (id.length < 2) return;

      const target = document.querySelector(id);
      if (!target) return;

      event.preventDefault();
      target.scrollIntoView({
        behavior: prefersReducedMotion() ? 'auto' : 'smooth',
        block: 'start'
      });
      // Mantiene la accesibilidad por teclado tras el desplazamiento.
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    });
  }

  /* ----------------------------------------------------------------------
     Arranque
     ---------------------------------------------------------------------- */
  function init() {
    i18n.current = i18n.detect();
    document.documentElement.lang = i18n.current;

    const titleKey = document.documentElement.dataset.titleKey;
    if (titleKey) document.title = i18n.t(titleKey);

    i18n.apply();
    updateLangUI(i18n.current);

    initNavbar();
    initReveal();
    initLightbox();
    initContactLinks();
    initSmoothScroll();
  }

  document.addEventListener('DOMContentLoaded', init);

  // Retraduce los mensajes de error visibles al cambiar de idioma.
  document.addEventListener('cr:langchange', () => {
    $$('.field__error[data-error-key]').forEach((box) => {
      box.textContent = i18n.t(box.dataset.errorKey);
    });
  });

  /* API pública utilizada por los scripts de cada página. */
  return {
    CONTACT,
    $, $$,
    t: (key) => i18n.t(key),
    get lang() { return i18n.current; },
    setLang: (lang) => i18n.set(lang),
    applyTranslations: (scope) => i18n.apply(scope),
    observeReveal,
    overlay,
    initForm,
    validateForm,
    validateField,
    openWhatsApp,
    buildMessage,
    showFeedback,
    prefersReducedMotion
  };
})();

/* --------------------------------------------------------------------------
   Señal de «JavaScript operativo»
   --------------------------------------------------------------------------
   Esta línea es la ÚLTIMA del archivo a propósito: sólo se ejecuta si todo lo
   anterior —incluido idiomas.js, del que depende— se cargó y evaluó sin
   errores. La clase `.cr-js` es lo que autoriza a global.css a ocultar los
   bloques con `data-animate` para animarlos después.

   Si falta un script, la ruta es incorrecta o el visitante tiene el
   JavaScript desactivado, la clase nunca llega a añadirse y la página se ve
   completa, sin animaciones. Nunca queda en blanco.
   -------------------------------------------------------------------------- */
document.documentElement.classList.add('cr-js');
