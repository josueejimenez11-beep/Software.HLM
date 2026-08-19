/* ============================================
   FUNCIONES QUE USAN TODAS LAS PAGINAS
   - cambiar el idioma
   - abrir el menu en el celular
   - cambiar el color del menu al bajar
   - poner el ano en el pie de pagina
   ============================================ */

/* Numero de WhatsApp de la empresa (con el codigo de Ecuador) */
var whatsapp = "593968596592";

/* ============================================
   IDIOMAS
   ============================================ */

/* Cambia todos los textos de la pagina al idioma elegido */
function cambiarIdioma(idioma) {

    /* Guardamos el idioma para que se mantenga en las otras paginas */
    localStorage.setItem("idioma", idioma);
    document.documentElement.lang = idioma;

    /* Buscamos todos los elementos que tengan data-texto y los cambiamos */
    var elementos = document.querySelectorAll("[data-texto]");

    for (var i = 0; i < elementos.length; i++) {
        var clave = elementos[i].getAttribute("data-texto");

        /* Solo cambiamos el texto si la palabra existe en el diccionario */
        if (textos[idioma][clave] != undefined) {
            elementos[i].textContent = textos[idioma][clave];
        }
    }

    /* Marcamos en negrita el boton del idioma que esta activo */
    var botones = document.querySelectorAll(".idiomas button");

    for (var j = 0; j < botones.length; j++) {
        if (botones[j].getAttribute("data-idioma") == idioma) {
            botones[j].style.fontWeight = "bold";
        } else {
            botones[j].style.fontWeight = "normal";
        }
    }
}

/* Al abrir la pagina revisamos si el usuario ya habia elegido un idioma */
function cargarIdioma() {
    var guardado = localStorage.getItem("idioma");

    if (guardado == null) {
        /* Si es la primera vez que entra, la pagina se ve en espanol */
        cambiarIdioma("es");
    } else {
        cambiarIdioma(guardado);
    }
}

/* ============================================
   MENU DEL CELULAR
   ============================================ */

/* Muestra o esconde el menu cuando tocamos el boton de las rayitas */
function abrirMenu() {
    var menu = document.getElementById("menu");
    menu.classList.toggle("abierto");
}

/* ============================================
   MENU QUE CAMBIA DE COLOR AL BAJAR
   ============================================ */

window.onscroll = function () {
    var navbar = document.getElementById("navbar");

    /* Si bajamos mas de 50 pixeles el menu se pone blanco */
    if (window.scrollY > 50) {
        navbar.classList.add("blanco");
    } else {
        navbar.classList.remove("blanco");
    }
};

/* ============================================
   ANO DEL PIE DE PAGINA
   ============================================ */

/* Pone el ano actual para no tener que cambiarlo a mano cada ano */
function ponerAnio() {
    var anio = document.getElementById("anio");

    if (anio != null) {
        anio.textContent = new Date().getFullYear();
    }
}

/* ============================================
   ENVIAR UN MENSAJE POR WHATSAPP
   ============================================ */

/* Abre WhatsApp con el mensaje ya escrito.
   La pagina no tiene servidor, por eso los formularios
   funcionan asi en lugar de guardar los datos. */
function enviarWhatsApp(mensaje) {
    var direccion = "https://wa.me/" + whatsapp + "?text=" + encodeURIComponent(mensaje);
    window.open(direccion, "_blank");
}

/* ============================================
   VALIDACIONES DE LOS FORMULARIOS
   ============================================ */

/* Revisa que el correo tenga arroba y un punto despues */
function correoValido(correo) {
    if (correo.indexOf("@") > 0 && correo.indexOf(".") > correo.indexOf("@")) {
        return true;
    } else {
        return false;
    }
}

/* Revisa que el telefono tenga por lo menos 7 numeros */
function telefonoValido(telefono) {
    var numeros = 0;

    for (var i = 0; i < telefono.length; i++) {
        if (telefono[i] >= "0" && telefono[i] <= "9") {
            numeros = numeros + 1;
        }
    }

    if (numeros >= 7) {
        return true;
    } else {
        return false;
    }
}

/* ============================================
   ARRANQUE
   Esto se ejecuta cuando la pagina termina de cargar
   ============================================ */

window.onload = function () {
    cargarIdioma();
    ponerAnio();
};
