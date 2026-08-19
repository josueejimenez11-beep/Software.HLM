/* ============================================
   FUNCIONES DE LA PAGINA TRAVEL EXPLORE
   - abrir y cerrar el detalle de cada actividad
   - validar el formulario de consulta
   ============================================ */

/* Abre la ventana con la informacion de la actividad.
   Cada ventana tiene su propio id en el HTML. */
function verActividad(id) {
    document.getElementById(id).style.display = "block";
}

/* Cierra la ventana */
function cerrarActividad(id) {
    document.getElementById(id).style.display = "none";
}

/* Cuando tocamos "Consultar" en una actividad,
   el formulario de abajo ya queda con esa opcion elegida */
function elegirActividad(actividad) {
    document.getElementById("actividad").value = actividad;
    document.getElementById("consultas").scrollIntoView();
}

/* ============================================
   FORMULARIO DE CONSULTA
   ============================================ */

function consultarActividad() {

    var nombre = document.getElementById("nombre").value;
    var telefono = document.getElementById("telefono").value;
    var correo = document.getElementById("correo").value;
    var actividad = document.getElementById("actividad").value;
    var participantes = document.getElementById("participantes").value;
    var fecha = document.getElementById("fecha").value;
    var comentarios = document.getElementById("comentarios").value;

    if (nombre == "") {
        alert("Por favor escribe tu nombre.");
        return false;
    }

    if (telefono == "") {
        alert("Por favor escribe tu telefono.");
        return false;
    }

    if (telefonoValido(telefono) == false) {
        alert("El telefono no parece correcto. Debe tener al menos 7 numeros.");
        return false;
    }

    if (correo != "" && correoValido(correo) == false) {
        alert("El correo no es valido. Ejemplo: nombre@correo.com");
        return false;
    }

    if (actividad == "") {
        alert("Elige la actividad que te interesa.");
        return false;
    }

    if (participantes == "" || participantes < 1) {
        alert("Escribe cuantas personas van a participar.");
        return false;
    }

    if (fecha == "") {
        alert("Elige una fecha.");
        return false;
    }

    var mensaje = "CONSULTA DE ACTIVIDAD - Chimborazo Rey";
    mensaje = mensaje + "\nNombre: " + nombre;
    mensaje = mensaje + "\nTelefono: " + telefono;

    if (correo != "") {
        mensaje = mensaje + "\nCorreo: " + correo;
    }

    mensaje = mensaje + "\nActividad: " + actividad;
    mensaje = mensaje + "\nParticipantes: " + participantes;
    mensaje = mensaje + "\nFecha: " + fecha;

    if (comentarios != "") {
        mensaje = mensaje + "\nComentarios: " + comentarios;
    }

    enviarWhatsApp(mensaje);
    return false;
}
