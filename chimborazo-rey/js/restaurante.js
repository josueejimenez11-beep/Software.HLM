/* ==========================================================================
   CHIMBORAZO REY · restaurante.js
   Menú interactivo con filtros por categoría y formulario de reserva de mesa.
   ========================================================================== */

'use strict';

(() => {

  /* ----------------------------------------------------------------------
     Categorías de la carta.
     El orden de este arreglo define el orden de los filtros en pantalla.
     ---------------------------------------------------------------------- */
  const CATEGORIES = [
    { id: 'pollo',          labelKey: 'resto.menu.pollo' },
    { id: 'cerdo',          labelKey: 'resto.menu.cerdo' },
    { id: 'carnes',         labelKey: 'resto.menu.carnes' },
    { id: 'pescados',       labelKey: 'resto.menu.pescados' },
    { id: 'camarones',      labelKey: 'resto.menu.camarones' },
    { id: 'tradicionales',  labelKey: 'resto.menu.tradicionales' },
    { id: 'desayunos',      labelKey: 'resto.menu.desayunos' },
    { id: 'almuerzos',      labelKey: 'resto.menu.almuerzos' },
    { id: 'cafeteria',      labelKey: 'resto.menu.cafeteria' }
  ];

  const PLACEHOLDER_IMAGE = 'images/restaurante/plato-generico.svg';

  /* ----------------------------------------------------------------------
     ⚠️  CONTENIDO PENDIENTE DE CARGA  ⚠️
     Los platos y los precios deben tomarse del menú oficial de Chimborazo Rey
     (documento «menu chimborazo rey final»). Mientras no esté disponible se
     generan tarjetas marcadas como pendientes para que la sección funcione.

     Estructura de cada plato:
       id        → identificador único
       category  → id de una categoría de CATEGORIES
       name      → nombre del plato tal como aparece en la carta (no se traduce)
       nameKey   → alternativa a `name` cuando el texto sí debe traducirse
       desc      → descripción breve (opcional)
       descKey   → alternativa traducible de `desc` (opcional)
       price     → número en dólares, o null si aún no está confirmado
       image     → ruta de la fotografía
       tagKey    → etiqueta opcional mostrada sobre la imagen

     Ejemplo de plato real, listo para copiar y adaptar:
       {
         id: 'pollo-01',
         category: 'pollo',
         name: 'Nombre exacto del plato',
         desc: 'Descripción breve tomada de la carta',
         price: 0.00,
         image: 'images/restaurante/plato-generico.svg'
       }
     ---------------------------------------------------------------------- */
  const MENU_ITEMS = CATEGORIES.flatMap((category) =>
    [1, 2].map((n) => ({
      id: `${category.id}-${n}`,
      category: category.id,
      nameKey: 'resto.menu.dishPending',
      descKey: 'resto.menu.dishPendingText',
      price: null,
      image: PLACEHOLDER_IMAGE,
      tagKey: category.labelKey
    }))
  );

  /* Referencias del DOM, asignadas durante el arranque. */
  let filtersBox = null;
  let grid = null;
  let emptyBox = null;
  let activeCategory = 'all';

  /* ----------------------------------------------------------------------
     Utilidades de presentación
     ---------------------------------------------------------------------- */
  const dishName = (item) => (item.nameKey ? CR.t(item.nameKey) : item.name || '');
  const dishDesc = (item) => (item.descKey ? CR.t(item.descKey) : item.desc || '');

  const formatPrice = (price) =>
    price === null || price === undefined ? null : `$${Number(price).toFixed(2)}`;

  const countByCategory = (categoryId) =>
    categoryId === 'all'
      ? MENU_ITEMS.length
      : MENU_ITEMS.filter((item) => item.category === categoryId).length;

  /* ----------------------------------------------------------------------
     Filtros de categoría
     ---------------------------------------------------------------------- */
  function renderFilters() {
    const options = [{ id: 'all', labelKey: 'resto.menu.all' }, ...CATEGORIES]
      .filter((option) => option.id === 'all' || countByCategory(option.id) > 0);

    filtersBox.innerHTML = options.map((option) => `
      <button type="button" class="menu-filter" data-category="${option.id}"
              aria-pressed="${option.id === activeCategory}">
        <span data-i18n="${option.labelKey}">${CR.t(option.labelKey)}</span>
        <span class="menu-filter__count">${countByCategory(option.id)}</span>
      </button>
    `).join('');
  }

  /* ----------------------------------------------------------------------
     Tarjetas de platos
     ---------------------------------------------------------------------- */
  function buildCard(item) {
    const card = document.createElement('article');
    card.className = 'dish-card';
    card.dataset.category = item.category;
    card.dataset.animate = 'fade-up';

    const price = formatPrice(item.price);
    const priceClass = price ? 'dish-card__price' : 'dish-card__price dish-card__price--pending';

    card.innerHTML = `
      <div class="dish-card__media">
        <img src="${item.image}" alt="${CR.t('resto.menu.dishAlt')}"
             width="800" height="600" loading="lazy" decoding="async">
        ${item.tagKey ? `<span class="dish-card__tag" data-tag-key="${item.tagKey}">${CR.t(item.tagKey)}</span>` : ''}
      </div>
      <div class="dish-card__body">
        <h3 class="dish-card__title" data-dish-name>${dishName(item)}</h3>
        <p class="dish-card__text" data-dish-desc>${dishDesc(item)}</p>
        <div class="dish-card__foot">
          <span class="${priceClass}" data-dish-price>${price || CR.t('resto.menu.pricePending')}</span>
        </div>
      </div>
    `;

    return card;
  }

  function renderMenu() {
    const fragment = document.createDocumentFragment();
    const cards = MENU_ITEMS.map((item) => {
      const card = buildCard(item);
      fragment.appendChild(card);
      return card;
    });

    grid.innerHTML = '';
    grid.appendChild(fragment);
    CR.observeReveal(cards);
  }

  /* ----------------------------------------------------------------------
     Aplicación del filtro activo
     ---------------------------------------------------------------------- */
  function applyFilter(categoryId) {
    activeCategory = categoryId;
    let visible = 0;

    CR.$$('.dish-card', grid).forEach((card) => {
      const show = categoryId === 'all' || card.dataset.category === categoryId;
      card.classList.toggle('is-hidden', !show);
      if (show) visible++;
    });

    CR.$$('.menu-filter', filtersBox).forEach((btn) => {
      btn.setAttribute('aria-pressed', String(btn.dataset.category === categoryId));
    });

    if (emptyBox) emptyBox.hidden = visible > 0;
  }

  /* ----------------------------------------------------------------------
     Retraducción del contenido generado dinámicamente
     ---------------------------------------------------------------------- */
  function retranslateMenu() {
    CR.$$('.dish-card', grid).forEach((card, index) => {
      const item = MENU_ITEMS[index];
      if (!item) return;

      CR.$('[data-dish-name]', card).textContent = dishName(item);
      CR.$('[data-dish-desc]', card).textContent = dishDesc(item);
      CR.$('[data-dish-price]', card).textContent =
        formatPrice(item.price) || CR.t('resto.menu.pricePending');

      const tag = CR.$('.dish-card__tag', card);
      if (tag) tag.textContent = CR.t(tag.dataset.tagKey);

      if (item.nameKey) CR.$('img', card).alt = CR.t('resto.menu.dishAlt');
    });

    CR.$$('.menu-filter span[data-i18n]', filtersBox).forEach((span) => {
      span.textContent = CR.t(span.dataset.i18n);
    });
  }

  /* ----------------------------------------------------------------------
     Arranque (después de que main.js haya inicializado el idioma)
     ---------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', () => {
    filtersBox = CR.$('#menu-filters');
    grid = CR.$('#menu-grid');
    emptyBox = CR.$('#menu-empty');

    if (filtersBox && grid) {
      renderFilters();
      renderMenu();
      applyFilter('all');

      filtersBox.addEventListener('click', (event) => {
        const button = event.target.closest('.menu-filter');
        if (button) applyFilter(button.dataset.category);
      });

      document.addEventListener('cr:langchange', retranslateMenu);
    }

    /* Formulario de reserva de mesa */
    CR.initForm('#form-reserva', {
      titleKey: 'resto.reserve.waMsg',
      rows: (form) => [
        ['form.name', form.nombre.value.trim()],
        ['form.phone', form.telefono.value.trim()],
        ['form.email', form.correo.value.trim()],
        ['resto.reserve.people', form.personas.value],
        ['resto.reserve.date', form.fecha.value],
        ['resto.reserve.time', form.hora.value],
        ['form.comments', form.comentarios.value.trim()]
      ]
    });

    /* Botones «Ver menú» / accesos directos al menú */
    CR.$$('[data-scroll-menu]').forEach((btn) => {
      btn.addEventListener('click', () => applyFilter('all'));
    });
  });
})();
