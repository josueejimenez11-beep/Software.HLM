/* ==========================================================================
   CHIMBORAZO REY · travel.js
   Tarjetas de actividades, modal de detalle y formulario de consulta.
   ========================================================================== */

'use strict';

(() => {

  /* ----------------------------------------------------------------------
     Catálogo de actividades.

     Sólo se incluyen los datos disponibles en la documentación de
     Chimborazo Rey. Los campos con valor `null` se muestran como pendientes:
     complétalos cuando dispongas del dato oficial (duración exacta, altitudes,
     punto de encuentro, itinerario y terreno de cada salida).

     NOTA SOBRE LA DIFICULTAD: los niveles se muestran como referencia y deben
     confirmarse con la documentación oficial antes de publicar el sitio.

     Estructura:
       id            → identificador único
       titleKey      → clave del nombre de la actividad
       shortKey      → clave de la descripción breve
       imgKey/image  → texto alternativo y ruta de la fotografía
       difficulty    → 'bajo' | 'bajo-medio' | 'medio' | 'medio-alto'
       price         → número, objeto {from, to} para rangos, o null
       priceNoteKey  → aclaración opcional del precio
       duration      → texto libre o null si aún no está confirmado
       altitude      → texto libre o null
       meeting       → texto libre o null
       terrain       → texto libre o null
       attractions[] → claves de los atractivos
       itinerary[]   → claves de los pasos del itinerario (vacío si no se conoce)
       includes[]    → claves de los servicios incluidos
       equipment[]   → claves del equipamiento
       bring[]       → claves de lo que debe llevar el visitante (vacío si no se conoce)
       recommendations[] → claves de las recomendaciones

     Las listas vacías no se muestran: basta con añadir las claves para que la
     sección correspondiente aparezca en el modal.
     ---------------------------------------------------------------------- */
  const ACTIVITIES = [
    {
      id: 'cumbre-chimborazo',
      titleKey: 'travel.a1.title',
      shortKey: 'travel.a1.short',
      altKey: 'travel.a1.alt',
      image: 'images/travel/actividad-cumbre-chimborazo.svg',
      difficulty: 'medio-alto',
      price: 300,
      duration: null,
      altitude: null,
      meeting: null,
      terrain: null,
      attractions: ['travel.a1.attr1', 'travel.a1.attr2', 'travel.a1.attr3'],
      includes: ['travel.a1.inc1', 'travel.a1.inc2', 'travel.a1.inc3'],
      equipment: ['travel.a1.eq1', 'travel.a1.eq2', 'travel.a1.eq3',
                  'travel.a1.eq4', 'travel.a1.eq5', 'travel.a1.eq6'],
      recommendations: ['travel.a1.rec1', 'travel.a1.rec2', 'travel.a1.rec3']
    },
    {
      id: 'cumbre-carihuairazo',
      titleKey: 'travel.a2.title',
      shortKey: 'travel.a2.short',
      altKey: 'travel.a2.alt',
      image: 'images/travel/actividad-carihuairazo.svg',
      difficulty: 'medio',
      price: 140,
      duration: null,
      altitude: null,
      meeting: null,
      terrain: null,
      attractions: ['travel.a2.attr1', 'travel.a2.attr2', 'travel.a2.attr3'],
      includes: ['travel.a2.inc1', 'travel.a2.inc2', 'travel.a2.inc3'],
      equipment: ['travel.a2.eq1', 'travel.a2.eq2', 'travel.a2.eq3', 'travel.a2.eq4'],
      recommendations: ['travel.a2.rec1', 'travel.a2.rec2']
    },
    {
      id: 'cabalgatas',
      titleKey: 'travel.a3.title',
      shortKey: 'travel.a3.short',
      altKey: 'travel.a3.alt',
      image: 'images/travel/actividad-cabalgatas.svg',
      difficulty: 'bajo',
      price: { from: 35, to: 60 },
      priceNoteKey: 'travel.a3.priceNote',
      duration: null,
      altitude: null,
      meeting: null,
      terrain: null,
      attractions: ['travel.a3.attr1', 'travel.a3.attr2', 'travel.a3.attr3',
                    'travel.a3.attr4', 'travel.a3.attr5'],
      includes: ['travel.a3.inc1', 'travel.a3.inc2', 'travel.a3.inc3'],
      equipment: [],
      recommendations: ['travel.a3.rec1', 'travel.a3.rec2', 'travel.a3.rec3']
    },
    {
      id: 'ciclismo',
      titleKey: 'travel.a4.title',
      shortKey: 'travel.a4.short',
      altKey: 'travel.a4.alt',
      image: 'images/travel/actividad-ciclismo.svg',
      difficulty: 'bajo-medio',
      price: 50,
      duration: null,
      altitude: null,
      meeting: null,
      terrain: null,
      attractions: ['travel.a4.attr1', 'travel.a4.attr2', 'travel.a4.attr3'],
      includes: ['travel.a4.inc1', 'travel.a4.inc2', 'travel.a4.inc3', 'travel.a4.inc4'],
      equipment: [],
      recommendations: ['travel.a4.rec1', 'travel.a4.rec2']
    },
    {
      id: 'trekking-nocturno',
      titleKey: 'travel.a5.title',
      shortKey: 'travel.a5.short',
      altKey: 'travel.a5.alt',
      image: 'images/travel/actividad-trekking-nocturno.svg',
      difficulty: 'bajo-medio',
      price: null,               // El documento no especifica un valor.
      duration: null,
      altitude: null,
      meeting: null,
      terrain: null,
      attractions: ['travel.a5.attr1', 'travel.a5.attr2', 'travel.a5.attr3'],
      includes: ['travel.a5.inc1', 'travel.a5.inc2', 'travel.a5.inc3'],
      equipment: [],
      recommendations: ['travel.a5.rec1', 'travel.a5.rec2']
    }
  ];

  const DIFFICULTY = {
    'bajo':       { labelKey: 'travel.difficulty.low',     className: 'badge--dif-bajo' },
    'bajo-medio': { labelKey: 'travel.difficulty.lowMid',  className: 'badge--dif-bajo-medio' },
    'medio':      { labelKey: 'travel.difficulty.mid',     className: 'badge--dif-medio' },
    'medio-alto': { labelKey: 'travel.difficulty.midHigh', className: 'badge--dif-medio-alto' }
  };

  let grid = null;
  let modal = null;

  /* ----------------------------------------------------------------------
     Formato de precios
     ---------------------------------------------------------------------- */
  function formatPrice(price) {
    if (price === null || price === undefined) return null;
    if (typeof price === 'object') return `$${price.from} – $${price.to}`;
    return `$${price}`;
  }

  const escapeHtml = (text) => String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

  /* ----------------------------------------------------------------------
     Tarjetas de actividad
     ---------------------------------------------------------------------- */
  function buildCard(activity) {
    const level = DIFFICULTY[activity.difficulty];
    const price = formatPrice(activity.price);

    const card = document.createElement('article');
    card.className = 'adventure-card';
    card.dataset.animate = 'fade-up';

    card.innerHTML = `
      <div class="adventure-card__media">
        <img src="${activity.image}" alt="${escapeHtml(CR.t(activity.altKey))}"
             width="1000" height="750" loading="lazy" decoding="async" data-alt-key="${activity.altKey}">
        <span class="badge ${level.className} adventure-card__difficulty">
          <span class="badge__dot" aria-hidden="true"></span>
          <span data-i18n="${level.labelKey}">${CR.t(level.labelKey)}</span>
        </span>
        ${price ? `<span class="adventure-card__price">${price}</span>` : ''}
      </div>
      <div class="adventure-card__body">
        <h3 class="adventure-card__title" data-i18n="${activity.titleKey}">${CR.t(activity.titleKey)}</h3>
        <p class="adventure-card__text" data-i18n="${activity.shortKey}">${CR.t(activity.shortKey)}</p>
        <dl class="adventure-card__meta">
          <div>
            <dt data-i18n="travel.meta.difficulty">${CR.t('travel.meta.difficulty')}</dt>
            <dd data-i18n="${level.labelKey}">${CR.t(level.labelKey)}</dd>
          </div>
          <div>
            <dt data-i18n="travel.meta.price">${CR.t('travel.meta.price')}</dt>
            <dd ${price ? '' : `data-i18n="travel.activities.pricePending"`}>${price || CR.t('travel.activities.pricePending')}</dd>
          </div>
        </dl>
        <div class="adventure-card__foot">
          <button type="button" class="btn btn--sm" data-activity="${activity.id}"
                  data-i18n="travel.activities.viewMore">${CR.t('travel.activities.viewMore')}</button>
          <button type="button" class="btn btn--sm btn--ghost" data-consult="${activity.id}"
                  data-i18n="travel.activities.consult">${CR.t('travel.activities.consult')}</button>
        </div>
      </div>
    `;

    return card;
  }

  function renderActivities() {
    const fragment = document.createDocumentFragment();
    const cards = ACTIVITIES.map((activity) => {
      const card = buildCard(activity);
      fragment.appendChild(card);
      return card;
    });

    grid.innerHTML = '';
    grid.appendChild(fragment);
    CR.observeReveal(cards);
  }

  /* ----------------------------------------------------------------------
     Modal de detalle
     ---------------------------------------------------------------------- */
  function buildFact(labelKey, value) {
    const content = value || CR.t('travel.modal.pending');
    return `
      <div class="adventure-modal__fact">
        <dt>${CR.t(labelKey)}</dt>
        <dd>${escapeHtml(content)}</dd>
      </div>
    `;
  }

  function buildList(titleKey, keys, modifier = '') {
    if (!keys || !keys.length) return '';
    return `
      <section class="adventure-modal__section">
        <h3>${CR.t(titleKey)}</h3>
        <ul class="adventure-modal__list ${modifier}">
          ${keys.map((key) => `<li>${escapeHtml(CR.t(key))}</li>`).join('')}
        </ul>
      </section>
    `;
  }

  function openActivity(activityId) {
    const activity = ACTIVITIES.find((item) => item.id === activityId);
    if (!activity || !modal) return;

    const level = DIFFICULTY[activity.difficulty];
    const price = formatPrice(activity.price);
    const body = CR.$('#activity-modal-body', modal);

    body.innerHTML = `
      <div class="adventure-modal__header">
        <h2 class="adventure-modal__title" id="activity-modal-title">${escapeHtml(CR.t(activity.titleKey))}</h2>
        <span class="badge ${level.className}">
          <span class="badge__dot" aria-hidden="true"></span>${escapeHtml(CR.t(level.labelKey))}
        </span>
      </div>

      <div class="adventure-modal__media">
        <img src="${activity.image}" alt="${escapeHtml(CR.t(activity.altKey))}"
             width="1000" height="563" loading="lazy" decoding="async">
      </div>

      <dl class="adventure-modal__facts">
        ${buildFact('travel.meta.duration', activity.duration)}
        ${buildFact('travel.meta.altitude', activity.altitude)}
        ${buildFact('travel.meta.meeting', activity.meeting)}
        ${buildFact('travel.meta.terrain', activity.terrain)}
      </dl>

      <section class="adventure-modal__section">
        <h3>${CR.t('travel.modal.description')}</h3>
        <p>${escapeHtml(CR.t(activity.shortKey))}</p>
      </section>

      ${buildList('travel.modal.attractions', activity.attractions)}
      ${buildList('travel.modal.itinerary', activity.itinerary, 'adventure-modal__list--steps')}
      ${buildList('travel.modal.includes', activity.includes)}
      ${buildList('travel.modal.equipment', activity.equipment)}
      ${buildList('travel.modal.bring', activity.bring)}
      ${buildList('travel.modal.recommendations', activity.recommendations)}

      <section class="adventure-modal__section">
        <h3>${CR.t('travel.modal.safety')}</h3>
        <p>${escapeHtml(CR.t('travel.modal.safetyText'))}</p>
      </section>

      <div class="adventure-modal__foot">
        <p class="adventure-modal__price">
          ${price || escapeHtml(CR.t('travel.activities.pricePending'))}
          <small>${price ? escapeHtml(CR.t('travel.modal.perPerson')) : ''}</small>
          ${activity.priceNoteKey ? `<small>${escapeHtml(CR.t(activity.priceNoteKey))}</small>` : ''}
        </p>
        <button type="button" class="btn" data-consult="${activity.id}">
          ${escapeHtml(CR.t('travel.activities.consult'))}
        </button>
      </div>
    `;

    CR.overlay.open(modal);
  }

  /* ----------------------------------------------------------------------
     Botón «Consultar»: preselecciona la actividad y lleva al formulario
     ---------------------------------------------------------------------- */
  function consultActivity(activityId) {
    CR.overlay.close();

    const select = CR.$('#travel-actividad');
    if (select) select.value = activityId;

    const target = CR.$('#consultas');
    if (!target) return;

    target.scrollIntoView({
      behavior: CR.prefersReducedMotion() ? 'auto' : 'smooth',
      block: 'start'
    });

    window.setTimeout(() => {
      const firstField = CR.$('#travel-nombre');
      if (firstField) firstField.focus({ preventScroll: true });
    }, CR.prefersReducedMotion() ? 0 : 600);
  }

  /* ----------------------------------------------------------------------
     Arranque
     ---------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', () => {
    grid = CR.$('#adventures-grid');
    modal = CR.$('#activity-modal');

    if (grid) {
      renderActivities();

      grid.addEventListener('click', (event) => {
        const detail = event.target.closest('[data-activity]');
        if (detail) { openActivity(detail.dataset.activity); return; }

        const consult = event.target.closest('[data-consult]');
        if (consult) consultActivity(consult.dataset.consult);
      });

      // Al cambiar de idioma se vuelven a construir las tarjetas.
      document.addEventListener('cr:langchange', () => {
        renderActivities();
        CR.overlay.close();
      });
    }

    if (modal) {
      CR.$('.modal__close', modal).addEventListener('click', () => CR.overlay.close());

      modal.addEventListener('click', (event) => {
        if (event.target === modal) { CR.overlay.close(); return; }

        const consult = event.target.closest('[data-consult]');
        if (consult) consultActivity(consult.dataset.consult);
      });
    }

    /* Opciones del selector de actividades del formulario de consulta */
    const select = CR.$('#travel-actividad');
    if (select) {
      const fillOptions = () => {
        const current = select.value;
        select.innerHTML =
          `<option value="" data-i18n="form.selectOption">${CR.t('form.selectOption')}</option>` +
          ACTIVITIES.map((activity) =>
            `<option value="${activity.id}">${CR.t(activity.titleKey)}</option>`
          ).join('');
        select.value = current;
      };

      fillOptions();
      document.addEventListener('cr:langchange', fillOptions);
    }

    /* Formulario de consulta de experiencias */
    CR.initForm('#form-travel', {
      titleKey: 'travel.contact.waMsg',
      rows: (form) => {
        const option = form.actividad.options[form.actividad.selectedIndex];
        return [
          ['form.name', form.nombre.value.trim()],
          ['form.phone', form.telefono.value.trim()],
          ['form.email', form.correo.value.trim()],
          ['travel.contact.activity', option && option.value ? option.textContent.trim() : ''],
          ['travel.contact.people', form.participantes.value],
          ['travel.contact.date', form.fecha.value],
          ['form.comments', form.comentarios.value.trim()]
        ];
      }
    });
  });
})();
