/* ============================================
   FUNCIONES DE LA PAGINA DEL RESTAURANTE
   - filtrar los platos por categoria
   - ver las fotos en grande
   - validar el formulario de reserva
   ============================================ */

/* ============================================
   FILTRAR LOS PLATOS
   ============================================ */

/* Muestra solo los platos de la categoria que elegimos */
function filtrarPlatos(categoria, boton) {

    var platos = document.querySelectorAll(".plato");

    for (var i = 0; i < platos.length; i++) {

        /* Si el boton es "todos" mostramos todo,
           si no, comparamos la categoria de cada plato */
        if (categoria == "todos") {
            platos[i].style.display = "block";
        } else if (platos[i].getAttribute("data-categoria") == categoria) {
            platos[i].style.display = "block";
        } else {
            platos[i].style.display = "none";
        }
    }

    /* Pintamos de naranja el boton que tocamos y despintamos los demas */
    var botones = document.querySelectorAll(".filtros button");

    for (var j = 0; j < botones.length; j++) {
        botones[j].classList.remove("seleccionado");
    }

    boton.classList.add("seleccionado");
}

/* ============================================
   VER LAS FOTOS EN GRANDE
   ============================================ */

/* Abre la ventana con la foto que tocamos */
function verFoto(imagen) {
    var ventana = document.getElementById("ventanaFoto");
    var fotoGrande = document.getElementById("fotoGrande");

    fotoGrande.src = imagen.src;
    fotoGrande.alt = imagen.alt;
    ventana.style.display = "block";
}

/* Cierra la ventana de la foto */
function cerrarFoto() {
    document.getElementById("ventanaFoto").style.display = "none";
}

/* ============================================
   FORMULARIO DE RESERVA DE MESA
   ============================================ */

/* Revisa que todo este lleno antes de enviar.
   Si algo falta muestra un aviso y no envia. */
function reservarMesa() {

    /* Guardamos en variables lo que escribio el usuario */
    var nombre = document.getElementById("nombre").value;
    var telefono = document.getElementById("telefono").value;
    var correo = document.getElementById("correo").value;
    var personas = document.getElementById("personas").value;
    var fecha = document.getElementById("fecha").value;
    var hora = document.getElementById("hora").value;
    var comentarios = document.getElementById("comentarios").value;

    /* Revisamos campo por campo */
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

    /* El correo no es obligatorio, pero si lo escribe debe estar bien */
    if (correo != "" && correoValido(correo) == false) {
        alert("El correo no es valido. Ejemplo: nombre@correo.com");
        return false;
    }

    if (personas == "" || personas < 1) {
        alert("Escribe cuantas personas van a venir.");
        return false;
    }

    if (fecha == "") {
        alert("Elige la fecha de la reserva.");
        return false;
    }

    if (hora == "") {
        alert("Elige la hora de la reserva.");
        return false;
    }

    /* Armamos el mensaje que se va a enviar por WhatsApp */
    var mensaje = "RESERVA DE MESA - Chimborazo Rey";
    mensaje = mensaje + "\nNombre: " + nombre;
    mensaje = mensaje + "\nTelefono: " + telefono;

    if (correo != "") {
        mensaje = mensaje + "\nCorreo: " + correo;
    }

    mensaje = mensaje + "\nPersonas: " + personas;
    mensaje = mensaje + "\nFecha: " + fecha;
    mensaje = mensaje + "\nHora: " + hora;

    if (comentarios != "") {
        mensaje = mensaje + "\nComentarios: " + comentarios;
    }

    enviarWhatsApp(mensaje);

    /* Devolvemos false para que la pagina no se recargue */
    return false;
}
