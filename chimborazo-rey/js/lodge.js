/* ==========================================================================
   CHIMBORAZO REY · lodge.js
   Consulta de disponibilidad por habitación, cálculo de noches y formulario
   de solicitud de hospedaje.
   ========================================================================== */

'use strict';

(() => {

  const MS_PER_NIGHT = 1000 * 60 * 60 * 24;

  /* ----------------------------------------------------------------------
     Cálculo de noches entre las fechas de entrada y salida
     ---------------------------------------------------------------------- */
  function initNightsCounter() {
    const checkin = CR.$('#lodge-entrada');
    const checkout = CR.$('#lodge-salida');
    const output = CR.$('#lodge-noches');

    if (!checkin || !checkout || !output) return;

    const update = () => {
      if (!checkin.value || !checkout.value) {
        output.classList.remove('is-visible');
        return;
      }

      const nights = Math.round(
        (new Date(checkout.value) - new Date(checkin.value)) / MS_PER_NIGHT
      );

      if (nights <= 0) {
        output.classList.remove('is-visible');
        return;
      }

      output.textContent = `${CR.t('lodge.booking.nights')} ${nights}`;
      output.dataset.nights = String(nights);
      output.classList.add('is-visible');
    };

    checkin.addEventListener('change', update);
    checkout.addEventListener('change', update);

    // Mantiene el texto traducido si el visitante cambia de idioma.
    document.addEventListener('cr:langchange', () => {
      if (output.classList.contains('is-visible')) update();
    });
  }

  /* ----------------------------------------------------------------------
     Botones «Consultar disponibilidad» de cada habitación:
     preseleccionan el tipo de habitación y llevan al formulario.
     ---------------------------------------------------------------------- */
  function initRoomButtons() {
    const select = CR.$('#lodge-habitacion');

    CR.$$('[data-room]').forEach((button) => {
      button.addEventListener('click', () => {
        if (select) select.value = button.dataset.room;

        const target = CR.$('#reservas');
        if (!target) return;

        target.scrollIntoView({
          behavior: CR.prefersReducedMotion() ? 'auto' : 'smooth',
          block: 'start'
        });

        // Enfoca el primer campo tras el desplazamiento.
        window.setTimeout(() => {
          const firstField = CR.$('#lodge-nombre');
          if (firstField) firstField.focus({ preventScroll: true });
        }, CR.prefersReducedMotion() ? 0 : 600);
      });
    });
  }

  /* ----------------------------------------------------------------------
     Arranque
     ---------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', () => {
    initNightsCounter();
    initRoomButtons();

    CR.initForm('#form-hospedaje', {
      titleKey: 'lodge.booking.waMsg',
      rows: (form) => {
        const roomOption = form.habitacion.options[form.habitacion.selectedIndex];
        return [
          ['form.name', form.nombre.value.trim()],
          ['lodge.booking.nationality', form.nacionalidad.value.trim()],
          ['form.phone', form.telefono.value.trim()],
          ['form.email', form.correo.value.trim()],
          ['lodge.booking.roomType', roomOption ? roomOption.textContent.trim() : ''],
          ['lodge.booking.guests', form.huespedes.value],
          ['lodge.booking.checkin', form.entrada.value],
          ['lodge.booking.checkout', form.salida.value],
          ['form.comments', form.comentarios.value.trim()]
        ];
      }
    });
  });
})();
