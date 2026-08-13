# -*- coding: utf-8 -*-
"""
===============================================================================
 U T I L I D A D E S   G E N E R A L E S
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Funciones de apoyo que no dibujan nada en pantalla: tipografias,
 validacion de lo que escribe el usuario, formato de numeros, calculo
 de promedios y manejo de errores.
===============================================================================
"""

import traceback                           # Reporte detallado de errores

import tkinter as tk                        # Nucleo de la interfaz grafica
from tkinter import messagebox              # Cuadros de dialogo del sistema
from tkinter import font as tkfont          # Manejo avanzado de tipografias

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import (
    COLORES, ESCALA_LITERAL, FUENTES, NOTA_MAXIMA, NOTA_MINIMA, VENTANA_ALTO,
    VENTANA_ANCHO)


# =============================================================================
# SECCION 3 : UTILIDADES DE TIPOGRAFIA
# =============================================================================

def elegir_familia(*candidatas):
    """
    Devuelve la primera familia tipografica disponible en el sistema.

    Windows suele tener 'Segoe UI', macOS 'Helvetica Neue' y Linux
    'DejaVu Sans'. Al comprobar la disponibilidad evitamos que la interfaz se
    vea distinta o genere advertencias en otros sistemas operativos.
    """
    try:
        disponibles = set(f.lower() for f in tkfont.families())
    except Exception:
        # Si por alguna razon no se pueden consultar, usamos un valor seguro.
        return "Arial"
    for familia in candidatas:
        if familia.lower() in disponibles:
            return familia
    return "Arial"


def configurar_fuentes():
    """
    Construye el diccionario global FUENTES con todos los estilos de texto.

    Se define una unica vez y se reutiliza en toda la aplicacion para mantener
    coherencia visual (mismo tamano de titulos, subtitulos, tablas, etc.).
    """
    principal = elegir_familia("Segoe UI", "Helvetica Neue", "DejaVu Sans", "Arial")
    display = elegir_familia("Segoe UI Semibold", "Segoe UI", "DejaVu Sans", "Arial")
    monoespaciada = elegir_familia("Consolas", "DejaVu Sans Mono", "Courier New")

    FUENTES.update({
        "titulo_gigante": (display, 40, "bold"),
        "titulo_grande":  (display, 28, "bold"),
        "titulo":         (display, 20, "bold"),
        "subtitulo":      (principal, 13),
        "seccion":        (display, 13, "bold"),
        "etiqueta":       (principal, 10),
        "etiqueta_bold":  (principal, 10, "bold"),
        "texto":          (principal, 11),
        "texto_bold":     (principal, 11, "bold"),
        "pequena":        (principal, 9),
        "pequena_bold":   (principal, 9, "bold"),
        "micro":          (principal, 8),
        "boton":          (principal, 11, "bold"),
        "boton_pequeno":  (principal, 10, "bold"),
        "icono_grande":   (principal, 30),
        "icono_medio":    (principal, 20),
        "mono":           (monoespaciada, 11),
        "mono_grande":    (monoespaciada, 22, "bold"),
        "resultado":      (display, 30, "bold"),
    })


# =============================================================================
# SECCION 5 : UTILIDADES DE VALIDACION
# =============================================================================
# Reglas de negocio para impedir campos vacios, letras donde van numeros,
# horas invalidas o fechas mal escritas. Todas devuelven una tupla
# (valido, valor_o_mensaje) para poder reutilizarlas facilmente.
# =============================================================================

def validar_texto(valor, nombre_campo, minimo=1, maximo=60):
    """
    Valida un campo de texto obligatorio.

    Comprueba que no este vacio y que su longitud sea razonable.
    Devuelve (True, texto_limpio) o (False, mensaje_de_error).
    """
    texto = str(valor).strip()
    if not texto:
        return False, "El campo '%s' no puede estar vacio." % nombre_campo
    if len(texto) < minimo:
        return False, "El campo '%s' debe tener al menos %d caracteres." % (nombre_campo, minimo)
    if len(texto) > maximo:
        return False, "El campo '%s' no puede superar %d caracteres." % (nombre_campo, maximo)
    return True, texto


def validar_entero(valor, nombre_campo, minimo=None, maximo=None):
    """
    Valida que el texto recibido sea un numero entero dentro de un rango.

    Impide explicitamente que el usuario escriba letras o simbolos.
    """
    texto = str(valor).strip()
    if not texto:
        return False, "El campo '%s' no puede estar vacio." % nombre_campo
    try:
        numero = int(texto)
    except ValueError:
        return False, "El campo '%s' solo acepta numeros enteros (sin letras)." % nombre_campo
    if minimo is not None and numero < minimo:
        return False, "El campo '%s' debe ser mayor o igual a %d." % (nombre_campo, minimo)
    if maximo is not None and numero > maximo:
        return False, "El campo '%s' debe ser menor o igual a %d." % (nombre_campo, maximo)
    return True, numero


def validar_decimal(valor, nombre_campo, minimo=None, maximo=None):
    """
    Valida que el texto recibido sea un numero decimal dentro de un rango.

    Acepta coma o punto como separador decimal para comodidad del usuario.
    """
    texto = str(valor).strip().replace(",", ".")
    if not texto:
        return False, "El campo '%s' no puede estar vacio." % nombre_campo
    try:
        numero = float(texto)
    except ValueError:
        return False, "El campo '%s' solo acepta numeros (sin letras ni simbolos)." % nombre_campo
    if minimo is not None and numero < minimo:
        return False, "El campo '%s' debe ser mayor o igual a %s." % (nombre_campo, formato_numero(minimo))
    if maximo is not None and numero > maximo:
        return False, "El campo '%s' debe ser menor o igual a %s." % (nombre_campo, formato_numero(maximo))
    return True, numero


def validar_opcion(valor, nombre_campo, opciones):
    """Valida que el valor seleccionado pertenezca a una lista permitida."""
    texto = str(valor).strip()
    if not texto:
        return False, "Debe seleccionar una opcion en el campo '%s'." % nombre_campo
    if texto not in opciones:
        return False, "El valor '%s' no es valido para '%s'." % (texto, nombre_campo)
    return True, texto


def validar_hora(valor, nombre_campo):
    """
    Valida una hora escrita en formato de 24 horas HH:MM.

    Devuelve la hora normalizada con dos digitos (por ejemplo 7:5 -> 07:05).
    """
    texto = str(valor).strip()
    if not texto:
        return False, "El campo '%s' no puede estar vacio." % nombre_campo
    texto = texto.replace(".", ":").replace("-", ":").replace(" ", "")
    if ":" not in texto:
        return False, "El campo '%s' debe tener el formato HH:MM (ejemplo 07:30)." % nombre_campo
    partes = texto.split(":")
    if len(partes) != 2:
        return False, "El campo '%s' debe tener el formato HH:MM (ejemplo 07:30)." % nombre_campo
    if not partes[0].isdigit() or not partes[1].isdigit():
        return False, "El campo '%s' solo acepta numeros en formato HH:MM." % nombre_campo
    horas, minutos = int(partes[0]), int(partes[1])
    if not (0 <= horas <= 23):
        return False, "Las horas del campo '%s' deben estar entre 00 y 23." % nombre_campo
    if not (0 <= minutos <= 59):
        return False, "Los minutos del campo '%s' deben estar entre 00 y 59." % nombre_campo
    return True, "%02d:%02d" % (horas, minutos)


def validar_lista_de_notas(valor):
    """
    Convierte un texto con notas separadas por comas en una lista de flotantes.

    Ejemplo de entrada valida:  "15, 18.5, 12, 20"
    Rechaza letras, valores fuera de la escala y listas vacias.
    """
    texto = str(valor).strip()
    if not texto:
        return False, "Debe ingresar al menos una nota separada por comas."

    # Se aceptan comas, punto y coma o espacios como separadores.
    texto = texto.replace(";", ",").replace("\n", ",")
    crudos = [parte.strip() for parte in texto.split(",")]
    crudos = [parte for parte in crudos if parte]

    if not crudos:
        return False, "No se detectaron notas validas en el texto ingresado."

    notas = []
    for indice, crudo in enumerate(crudos, start=1):
        try:
            numero = float(crudo.replace(",", "."))
        except ValueError:
            return False, ("El valor '%s' (posicion %d) no es un numero valido.\n"
                           "Escriba unicamente numeros separados por comas." % (crudo, indice))
        if numero < NOTA_MINIMA or numero > NOTA_MAXIMA:
            return False, ("La nota %s (posicion %d) esta fuera de la escala permitida (%s a %s)."
                           % (formato_numero(numero), indice,
                              formato_numero(NOTA_MINIMA), formato_numero(NOTA_MAXIMA)))
        notas.append(round(numero, 2))
    return True, notas


# =============================================================================
# SECCION 6 : UTILIDADES GENERALES DE APOYO
# =============================================================================

def formato_numero(numero, decimales=2):
    """Convierte un numero a texto con decimales fijos (ejemplo 14.5 -> 14.50)."""
    try:
        return ("%." + str(decimales) + "f") % float(numero)
    except (TypeError, ValueError):
        return "0.00"


def hora_a_minutos(hora):
    """Convierte una hora 'HH:MM' a minutos totales para poder compararla."""
    try:
        horas, minutos = str(hora).split(":")
        return int(horas) * 60 + int(minutos)
    except (ValueError, AttributeError):
        return 0


def evaluar_nota(nota):
    """
    Traduce una calificacion numerica a su equivalente literal.

    Devuelve la tupla (letra, aprobado, comentario) segun ESCALA_LITERAL:
        0 a 20  -> D  Reprueba
        21 a 30 -> C  Aprobado (estudia mas)
        31 a 40 -> B  Aprobado
        41 a 50 -> A  Aprobado
    """
    for limite, letra, aprobado, comentario in ESCALA_LITERAL:
        if nota <= limite:
            return letra, aprobado, comentario
    limite, letra, aprobado, comentario = ESCALA_LITERAL[-1]
    return letra, aprobado, comentario


def promedio_de(lista_numeros):
    """Calcula el promedio aritmetico protegiendo contra divisiones por cero."""
    if not lista_numeros:
        return 0.0
    return sum(lista_numeros) / float(len(lista_numeros))


def contraste_de(color_fondo):
    """
    Devuelve el color de letra que mejor se lee sobre el fondo indicado.

    Calcula la luminancia percibida del color: sobre los celestes claros
    devuelve negro y sobre los tonos oscuros devuelve blanco. Asi ningun
    boton queda con texto ilegible al cambiar la paleta.
    """
    color = str(color_fondo).lstrip("#")
    try:
        rojo, verde, azul = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return COLORES["blanco"]
    luminancia = (0.299 * rojo + 0.587 * verde + 0.114 * azul) / 255.0
    return COLORES["negro"] if luminancia > 0.6 else COLORES["blanco"]


def centrar_ventana(ventana, ancho=VENTANA_ANCHO, alto=VENTANA_ALTO):
    """
    Coloca una ventana exactamente en el centro de la pantalla.

    Se usa tanto para la ventana principal como para todas las ventanas
    Toplevel de los modulos, cumpliendo el requisito de diseno uniforme.
    """
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    posicion_x = max(0, int((pantalla_ancho - ancho) / 2))
    posicion_y = max(0, int((pantalla_alto - alto) / 2) - 20)
    ventana.geometry("%dx%d+%d+%d" % (ancho, alto, posicion_x, posicion_y))


def ejecutar_seguro(accion, descripcion="operacion de interfaz"):
    """
    Ejecuta una accion de la interfaz tolerando widgets ya destruidos.

    Tkinter lanza TclError cuando se manipula un widget que el usuario acaba
    de cerrar. Esta funcion centraliza ese control para no repetirlo en cada
    modulo y devuelve True si la accion se completo.
    """
    try:
        accion()
        return True
    except tk.TclError as error:
        print("[Sistema de Estudio] Se omitio la %s: %s" % (descripcion, error))
        return False


def limpiar_seleccion(tabla):
    """Quita de forma segura la fila seleccionada de un Treeview."""
    return ejecutar_seguro(lambda: tabla.selection_remove(tabla.selection()),
                           "limpieza de seleccion")


def manejar_errores(funcion):
    """
    Decorador de seguridad para los comandos de los botones.

    Envuelve cualquier accion de la interfaz: si ocurre un error inesperado
    se muestra un messagebox explicativo en lugar de cerrar el programa.
    Esto cumple el requisito de "evitar que el programa se cierre por errores".
    """
    def envoltura(*argumentos, **claves):
        try:
            return funcion(*argumentos, **claves)
        except Exception as error:                       # Captura total controlada
            traceback.print_exc()
            messagebox.showerror(
                "Error inesperado",
                "Ocurrio un problema al ejecutar la accion.\n\n"
                "Detalle tecnico: %s\n\nLa aplicacion continuara funcionando."
                % error
            )
            return None
    envoltura.__name__ = getattr(funcion, "__name__", "envoltura")
    envoltura.__doc__ = funcion.__doc__
    return envoltura

# =============================================================================
# AVISO PARA QUIEN EJECUTE ESTE ARCHIVO POR EQUIVOCACION
# =============================================================================
# Este archivo es una PIEZA del Sistema de Estudio: guarda las validaciones y calculos de apoyo
# y por si solo no abre ninguna ventana. El programa se inicia siempre desde
# study_control.py. El bloque de abajo solo sirve para avisarlo con claridad.
# =============================================================================

if __name__ == "__main__":
    print("")
    print("  Este archivo (utilidades.py) es una pieza del Sistema de Estudio.")
    print("  Por si solo no abre ninguna ventana.")
    print("")
    print("  Para iniciar el programa ejecute:")
    print("")
    print("      python study_control.py")
    print("")
