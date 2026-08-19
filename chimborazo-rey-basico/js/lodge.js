/* ============================================
   FUNCIONES DE LA PAGINA DEL LODGE HOTEL
   - elegir la habitacion desde las tarjetas
   - validar el formulario de hospedaje
   ============================================ */

/* Cuando tocamos "Consultar" en una habitacion,
   el formulario de abajo ya queda con esa opcion elegida */
function elegirHabitacion(tipo) {
    document.getElementById("tipo").value = tipo;

    /* Bajamos hasta el formulario */
    document.getElementById("reservas").scrollIntoView();
}

/* ============================================
   FORMULARIO DE HOSPEDAJE
   ============================================ */

function solicitarHospedaje() {

    var nombre = document.getElementById("nombre").value;
    var nacionalidad = document.getElementById("nacionalidad").value;
    var telefono = document.getElementById("telefono").value;
    var correo = document.getElementById("correo").value;
    var tipo = document.getElementById("tipo").value;
    var huespedes = document.getElementById("huespedes").value;
    var entrada = document.getElementById("entrada").value;
    var salida = document.getElementById("salida").value;
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

    if (correo == "") {
        alert("Por favor escribe tu correo.");
        return false;
    }

    if (correoValido(correo) == false) {
        alert("El correo no es valido. Ejemplo: nombre@correo.com");
        return false;
    }

    if (tipo == "") {
        alert("Elige el tipo de habitacion.");
        return false;
    }

    if (huespedes == "" || huespedes < 1) {
        alert("Escribe cuantas personas van a alojarse.");
        return false;
    }

    if (entrada == "") {
        alert("Elige la fecha de entrada.");
        return false;
    }

    if (salida == "") {
        alert("Elige la fecha de salida.");
        return false;
    }

    /* La fecha de salida tiene que ser despues de la de entrada.
       Como las fechas vienen en formato 2026-08-14 se pueden comparar
       igual que si fueran texto. */
    if (salida <= entrada) {
        alert("La fecha de salida debe ser despues de la fecha de entrada.");
        return false;
    }

    var mensaje = "SOLICITUD DE HOSPEDAJE - Chimborazo Rey";
    mensaje = mensaje + "\nNombre: " + nombre;

    if (nacionalidad != "") {
        mensaje = mensaje + "\nNacionalidad: " + nacionalidad;
    }

    mensaje = mensaje + "\nTelefono: " + telefono;
    mensaje = mensaje + "\nCorreo: " + correo;
    mensaje = mensaje + "\nHabitacion: " + tipo;
    mensaje = mensaje + "\nHuespedes: " + huespedes;
    mensaje = mensaje + "\nEntrada: " + entrada;
    mensaje = mensaje + "\nSalida: " + salida;

    if (comentarios != "") {
        mensaje = mensaje + "\nComentarios: " + comentarios;
    }

    enviarWhatsApp(mensaje);
    return false;
}
