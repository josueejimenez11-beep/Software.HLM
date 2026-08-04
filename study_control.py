# -*- coding: utf-8 -*-
"""
===============================================================================
                        S I S T E M A   D E   E S T U D I O
===============================================================================
 Sistema de Gestion PUCE
 -----------------------------------------------------------------------------
 Institucion : Pontificia Universidad Catolica del Ecuador
 Autores     : Steveen Culquicondor - Angel Nunez - Ricardo Garrido
 Catedra     : Fundamentos de Programacion
 Version     : 1.0
 Tecnologia  : Python 3 + Tkinter + ttk
 -----------------------------------------------------------------------------
 DESCRIPCION GENERAL
 -----------------------------------------------------------------------------
 Sistema de Estudio es una aplicacion de escritorio disenada para que un
 estudiante universitario organice su semestre desde un solo lugar:

   Modulo 1 -> Registro de Materias        (materias.json)
   Modulo 2 -> Horario Semanal             (horario.json)
   Modulo 3 -> Calculadora de Promedios    (notas.json)
   Modulo 4 -> Informacion del Sistema     (messagebox)

 La informacion se guarda automaticamente en archivos JSON ubicados junto al
 script y se carga de forma automatica cada vez que el programa inicia.

 EJECUCION:  python study_control.py
===============================================================================
"""

# =============================================================================
# SECCION 1 : IMPORTACIONES
# =============================================================================
# Se importan unicamente librerias estandar de Python 3 para garantizar que el
# programa funcione en cualquier computador sin instalar dependencias extra.
# =============================================================================

import os                                   # Rutas y verificacion de archivos
import sys                                  # Informacion del interprete
import json                                 # Persistencia de datos en JSON
import datetime                             # Fechas, horas y reloj del sistema
import traceback                            # Reporte detallado de errores

import tkinter as tk                        # Nucleo de la interfaz grafica
from tkinter import ttk                     # Componentes con estilo (ttk)
from tkinter import messagebox              # Cuadros de dialogo del sistema
from tkinter import font as tkfont          # Manejo avanzado de tipografias


# =============================================================================
# SECCION 2 : CONFIGURACION GLOBAL DE LA APLICACION
# =============================================================================
# Aqui se centralizan TODOS los valores constantes del programa (paleta de
# colores, medidas, nombres de archivos, escalas de calificacion, etc.).
# Centralizar estos valores evita repetir codigo y permite cambiar la
# apariencia de toda la aplicacion modificando un solo bloque.
# =============================================================================

# ----------------------------- Identidad visual ------------------------------
APP_NOMBRE = "Sistema de Estudio"
APP_VERSION = "1.0"
APP_SUBTITULO = "Sistema de Gestion PUCE"
APP_UNIVERSIDAD = "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR"
APP_AUTORES = "STEVEEN CULQUICONDOR  -  ANGEL NUNEZ  -  RICARDO GARRIDO"
APP_CATEDRA = "FUNDAMENTOS DE PROGRAMACION"

# ------------------------- Dimensiones de ventanas ---------------------------
VENTANA_ANCHO = 1100                        # Ancho solicitado en el requisito
VENTANA_ALTO = 700                          # Alto solicitado en el requisito

# ---------------------- Paleta: gris 18%, blanco y celeste ------------------
# El fondo general usa el gris medio fotografico (gris 18 %). Sobre el se
# apoyan paneles de gris mas oscuro, para que el texto blanco conserve
# contraste, y todos los bordes van en celeste claro.
COLORES = {
    "fondo":           "#808080",           # Gris 18 % (fondo de la interfaz)
    "fondo_alt":       "#707070",           # Franjas de titulo y zonas de apoyo
    "superficie":      "#4A4A4A",           # Tarjetas, paneles y tablas
    "superficie_alt":  "#3C3C3C",           # Campos de texto y filas alternas
    "borde":           "#7DD3FC",           # Borde celeste claro (toda la interfaz)
    "borde_suave":     "#9AA3A8",           # Borde interno discreto
    "celeste":         "#7DD3FC",           # Acento principal (celeste claro)
    "celeste_claro":   "#BAE6FD",           # Celeste muy claro para destacados
    "celeste_oscuro":  "#0369A1",           # Celeste profundo (encabezados)
    "celeste_hover":   "#38BDF8",           # Celeste para el efecto hover
    "azul":            "#0369A1",           # Azul de apoyo (boton editar)
    "azul_claro":      "#93C5FD",           # Azul claro informativo
    "cian":            "#BAE6FD",           # Detalles y separadores
    "texto":           "#FFFFFF",           # Texto principal (blanco)
    "texto_suave":     "#E9EDEF",           # Texto secundario
    "texto_tenue":     "#CBD2D6",           # Texto muy secundario (sobre paneles)
    "texto_sobre_gris": "#1F2A2F",          # Texto secundario sobre el gris 18 %
    "exito":           "#4ADE80",           # Verde (aprobado / guardar)
    "exito_hover":     "#22C55E",           # Verde intenso para hover
    "error":           "#F87171",           # Rojo (reprobado / eliminar)
    "error_hover":     "#EF4444",           # Rojo intenso para hover
    "alerta":          "#FBBF24",           # Naranja (advertencias)
    "alerta_hover":    "#F59E0B",           # Naranja intenso para hover
    "blanco":          "#FFFFFF",           # Blanco puro
    "negro":           "#333333",           # Gris oscuro de la barra superior
}

# --------------------------- Escala de calificacion --------------------------
# La escala va de 0 a 50 y se traduce a una calificacion literal. Solo la
# letra D reprueba; a partir de 21 puntos la materia queda aprobada.
NOTA_MINIMA = 0.0                           # Nota mas baja posible
NOTA_MAXIMA = 50.0                          # Nota mas alta posible (escala /50)
NOTA_APROBACION = 20.0                      # Hay que superar este valor para aprobar

# Cada tramo indica: limite superior, letra, si aprueba y su comentario.
ESCALA_LITERAL = [
    (20.0, "D", False, "Reprueba"),
    (30.0, "C", True, "Aprobado, estudia mas"),
    (40.0, "B", True, "Aprobado"),
    (50.0, "A", True, "Aprobado"),
]

# ------------------------------ Archivos JSON --------------------------------
# Se guardan en la misma carpeta del script para que el proyecto sea portable.
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MATERIAS = os.path.join(CARPETA_BASE, "materias.json")
ARCHIVO_HORARIO = os.path.join(CARPETA_BASE, "horario.json")
ARCHIVO_NOTAS = os.path.join(CARPETA_BASE, "notas.json")

# ------------------- Nombres posibles del logo institucional -----------------
# El usuario puede colocar cualquiera de estos archivos PNG junto al script y
# la aplicacion lo cargara automaticamente en el encabezado.
NOMBRES_LOGO = ("logo_puce.png", "logo.png", "puce.png", "logo_puce.PNG")

# ------------------------------ Listas fijas ---------------------------------
DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

# Asignaturas del semestre. El estudiante las escoge de esta lista en los tres
# modulos, de modo que el nombre de la materia siempre se escribe igual.
MATERIAS_DISPONIBLES = [
    "SISTEMAS OPERATIVOS",
    "HABILIDADES LOGICO MATEMATICAS",
    "SEGUNDA LENGUA",
    "INTRODUCCION AL DESARROLLO WEB",
    "ALGEBRA",
    "FUNDAMENTOS DE PROGRAMACION",
    "HERRAMIENTAS DIGITALES APLICADAS",
    "COMUNICACION ORAL Y ESCRITA",
]

# --------------------- Diccionario global de tipografias ---------------------
# Se llena en configurar_fuentes() una vez que la ventana raiz existe, porque
# Tkinter necesita un root activo para consultar las fuentes del sistema.
FUENTES = {}

# ------------------- Referencias globales de imagenes (PNG) ------------------
# Tkinter elimina las imagenes de memoria si no se conserva una referencia.
IMAGENES_EN_MEMORIA = []


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
# SECCION 4 : CAPA DE PERSISTENCIA (ARCHIVOS JSON)
# =============================================================================
# Todo lo que el usuario registra se guarda en archivos JSON. Estas funciones
# encapsulan la lectura y escritura para que ningun modulo tenga que repetir
# el manejo de archivos ni el control de errores.
# =============================================================================

def leer_json(ruta):
    """
    Lee una lista de diccionarios desde un archivo JSON.

    - Si el archivo no existe, devuelve una lista vacia (primer arranque).
    - Si el archivo esta danado o tiene otro formato, devuelve lista vacia y
      avisa por consola, evitando que la aplicacion se cierre por un error.
    """
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        # Solo aceptamos listas de diccionarios: cualquier otra cosa se ignora.
        if isinstance(contenido, list):
            return [registro for registro in contenido if isinstance(registro, dict)]
        return []
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as error:
        print("[Sistema de Estudio] No se pudo leer '%s': %s" % (ruta, error))
        return []


def escribir_json(ruta, datos):
    """
    Guarda una lista de diccionarios en un archivo JSON con formato legible.

    Devuelve True si la operacion fue exitosa y False si ocurrio un problema
    (por ejemplo, permisos de escritura o disco lleno).
    """
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except (OSError, TypeError) as error:
        print("[Sistema de Estudio] No se pudo escribir '%s': %s" % (ruta, error))
        messagebox.showerror(
            "Error de guardado",
            "No fue posible guardar la informacion en el archivo:\n\n%s\n\nDetalle: %s"
            % (os.path.basename(ruta), error)
        )
        return False


class BaseDeDatos:
    """
    Repositorio central de informacion del Sistema de Estudio.

    Mantiene en memoria las tres colecciones del sistema (materias, horario
    y notas) y sincroniza cada cambio con su archivo JSON. Todos los
    modulos trabajan sobre esta misma instancia, por lo que la informacion
    siempre esta actualizada en cualquier ventana.
    """

    def __init__(self):
        # Colecciones en memoria (se llenan al llamar cargar_todo()).
        self.materias = []
        self.horario = []
        self.notas = []

    # ------------------------------------------------------------------ carga
    def cargar_todo(self):
        """Carga automaticamente los tres archivos JSON al iniciar."""
        self.materias = leer_json(ARCHIVO_MATERIAS)
        self.horario = leer_json(ARCHIVO_HORARIO)
        self.notas = leer_json(ARCHIVO_NOTAS)
        self.reparar_identificadores()

    def reparar_identificadores(self):
        """
        Garantiza que cada registro tenga un identificador unico.

        Si el archivo JSON fue editado a mano y algun registro perdio su 'id',
        aqui se le asigna uno nuevo para que las operaciones de editar y
        eliminar sigan funcionando correctamente.
        """
        for coleccion in (self.materias, self.horario, self.notas):
            usados = set()
            siguiente = 1
            for registro in coleccion:
                identificador = registro.get("id")
                if not isinstance(identificador, int) or identificador in usados:
                    while siguiente in usados:
                        siguiente += 1
                    identificador = siguiente
                    registro["id"] = identificador
                usados.add(identificador)

    # --------------------------------------------------------------- guardado
    def guardar_materias(self):
        """Escritura automatica de materias.json."""
        return escribir_json(ARCHIVO_MATERIAS, self.materias)

    def guardar_horario(self):
        """Escritura automatica de horario.json."""
        return escribir_json(ARCHIVO_HORARIO, self.horario)

    def guardar_notas(self):
        """Escritura automatica de notas.json."""
        return escribir_json(ARCHIVO_NOTAS, self.notas)

    def guardar_todo(self):
        """Guarda las tres colecciones (usado al cerrar la aplicacion)."""
        self.guardar_materias()
        self.guardar_horario()
        self.guardar_notas()

    # -------------------------------------------------------------- utilidades
    @staticmethod
    def nuevo_id(coleccion):
        """Genera un identificador consecutivo unico para una coleccion."""
        if not coleccion:
            return 1
        return max(int(registro.get("id", 0)) for registro in coleccion) + 1

    @staticmethod
    def buscar_por_id(coleccion, identificador):
        """Devuelve el registro cuyo 'id' coincide, o None si no existe."""
        for registro in coleccion:
            if int(registro.get("id", -1)) == int(identificador):
                return registro
        return None

    @staticmethod
    def eliminar_por_id(coleccion, identificador):
        """Elimina de la lista el registro indicado. Devuelve True si borro."""
        registro = BaseDeDatos.buscar_por_id(coleccion, identificador)
        if registro is not None:
            coleccion.remove(registro)
            return True
        return False


# Instancia unica utilizada por toda la aplicacion.
DATOS = BaseDeDatos()


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
# SECCION 7 : ESTILOS ttk PERSONALIZADOS
# =============================================================================

def aplicar_estilos():
    """
    Define la apariencia de todos los componentes ttk de la aplicacion.

    Se utiliza el tema 'clam' porque es el unico tema multiplataforma que
    permite personalizar por completo colores de Treeview, Combobox y Entry.
    """
    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass                                    # Si no existe se usa el tema actual

    # ---------------------------- Marcos y textos ----------------------------
    estilo.configure("Fondo.TFrame", background=COLORES["fondo"])
    estilo.configure("Panel.TFrame", background=COLORES["superficie"])

    # -------------------------- Campos de entrada ----------------------------
    estilo.configure(
        "Study.TEntry",
        fieldbackground=COLORES["superficie_alt"],
        background=COLORES["superficie_alt"],
        foreground=COLORES["texto"],
        insertcolor=COLORES["celeste_claro"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        borderwidth=1,
        relief="flat",
        padding=4,
    )
    estilo.map(
        "Study.TEntry",
        bordercolor=[("focus", COLORES["celeste"])],
        lightcolor=[("focus", COLORES["celeste"])],
        darkcolor=[("focus", COLORES["celeste"])],
        fieldbackground=[("focus", COLORES["superficie_alt"])],
    )

    # ------------------------------ Combobox ---------------------------------
    estilo.configure(
        "Study.TCombobox",
        fieldbackground=COLORES["superficie_alt"],
        background=COLORES["superficie_alt"],
        foreground=COLORES["texto"],
        arrowcolor=COLORES["celeste_claro"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        selectbackground=COLORES["superficie_alt"],
        selectforeground=COLORES["texto"],
        borderwidth=1,
        padding=4,
    )
    estilo.map(
        "Study.TCombobox",
        bordercolor=[("focus", COLORES["celeste"]), ("hover", COLORES["celeste_claro"])],
        arrowcolor=[("hover", COLORES["celeste"])],
        fieldbackground=[("readonly", COLORES["superficie_alt"])],
        foreground=[("readonly", COLORES["texto"])],
    )

    # ------------------------------ Treeview ---------------------------------
    estilo.configure(
        "Study.Treeview",
        background=COLORES["superficie"],
        fieldbackground=COLORES["superficie"],
        foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
        borderwidth=0,
        rowheight=28,
        font=("TkDefaultFont", 10),
    )
    estilo.configure(
        "Study.Treeview.Heading",
        background=COLORES["celeste_oscuro"],
        foreground=COLORES["blanco"],
        relief="flat",
        borderwidth=0,
        padding=(6, 10),
        font=("TkDefaultFont", 10, "bold"),
    )
    estilo.map(
        "Study.Treeview.Heading",
        background=[("active", COLORES["azul"])],
    )
    # La fila seleccionada se pinta de celeste claro, por eso su texto va en
    # negro para mantener la legibilidad.
    estilo.map(
        "Study.Treeview",
        background=[("selected", COLORES["celeste"])],
        foreground=[("selected", COLORES["negro"])],
    )
    estilo.layout("Study.Treeview", [
        ("Study.Treeview.treearea", {"sticky": "nswe"})
    ])

    # ------------------------------ Scrollbars -------------------------------
    estilo.configure(
        "Study.Vertical.TScrollbar",
        background=COLORES["superficie_alt"],
        troughcolor=COLORES["fondo_alt"],
        bordercolor=COLORES["fondo_alt"],
        arrowcolor=COLORES["celeste_claro"],
        borderwidth=0,
        width=12,
    )
    estilo.map(
        "Study.Vertical.TScrollbar",
        background=[("active", COLORES["celeste"])],
    )
    estilo.configure(
        "Study.Horizontal.TScrollbar",
        background=COLORES["superficie_alt"],
        troughcolor=COLORES["fondo_alt"],
        bordercolor=COLORES["fondo_alt"],
        arrowcolor=COLORES["celeste_claro"],
        borderwidth=0,
    )
    estilo.map(
        "Study.Horizontal.TScrollbar",
        background=[("active", COLORES["celeste"])],
    )

    # ----------------------------- Barra de progreso -------------------------
    estilo.configure(
        "Study.Horizontal.TProgressbar",
        troughcolor=COLORES["fondo_alt"],
        bordercolor=COLORES["fondo_alt"],
        background=COLORES["celeste"],
        lightcolor=COLORES["celeste_claro"],
        darkcolor=COLORES["celeste_oscuro"],
        thickness=14,
    )

    # ------------------------------ Separadores ------------------------------
    estilo.configure("Study.TSeparator", background=COLORES["borde"])

    # --------- Lista desplegable de los combobox (es un widget Tk clasico) ---
    # Sin esto la lista de materias se abriria con los colores blancos del
    # sistema operativo y rompería la estetica de la aplicacion.
    raiz = tk._default_root
    if raiz is not None:
        raiz.option_add("*TCombobox*Listbox.background", COLORES["superficie_alt"])
        raiz.option_add("*TCombobox*Listbox.foreground", COLORES["texto"])
        raiz.option_add("*TCombobox*Listbox.selectBackground", COLORES["celeste"])
        raiz.option_add("*TCombobox*Listbox.selectForeground", COLORES["negro"])
        raiz.option_add("*TCombobox*Listbox.borderWidth", 0)

    return estilo


# =============================================================================
# SECCION 8 : COMPONENTES VISUALES REUTILIZABLES
# =============================================================================
# Estas clases evitan repetir codigo: se construyen una sola vez y se usan en
# todos los modulos (botones con hover, campos de formulario, tarjetas, etc.).
# =============================================================================

class BotonModerno(tk.Frame):
    """
    Boton personalizado con efecto hover, icono y esquinas planas modernas.

    Se construye sobre un Frame + Label porque asi se controla al 100% el
    color de fondo, el color del texto y la transicion al pasar el mouse,
    algo que el boton estandar de Tkinter no permite en todos los sistemas.
    """

    def __init__(self, padre, texto, comando, icono="", ancho=170, alto=42,
                 color=None, color_hover=None, color_texto=None,
                 fuente=None, borde=None):
        color = color or COLORES["celeste"]
        color_hover = color_hover or COLORES["celeste_hover"]
        color_texto = color_texto or contraste_de(color)
        borde = borde or color

        super().__init__(padre, bg=color, width=ancho, height=alto,
                         highlightthickness=1, highlightbackground=borde,
                         highlightcolor=borde, cursor="hand2")
        self.pack_propagate(False)              # Respeta el ancho/alto fijados

        # Guardamos los colores para poder alternarlos en el hover.
        self.color_normal = color
        self.color_hover = color_hover
        self.borde_normal = borde
        self.texto_normal = color_texto
        self.texto_hover = contraste_de(color_hover)
        self.comando = comando
        self.habilitado = True

        etiqueta_texto = ("%s  %s" % (icono, texto)).strip() if icono else texto
        self.etiqueta = tk.Label(
            self,
            text=etiqueta_texto,
            bg=color,
            fg=color_texto,
            font=fuente or FUENTES["boton"],
            cursor="hand2",
        )
        self.etiqueta.pack(expand=True, fill="both")

        # Se enlazan los eventos tanto al Frame como al Label para que el
        # efecto funcione sin importar sobre que parte este el puntero.
        for widget in (self, self.etiqueta):
            widget.bind("<Enter>", self._al_entrar)
            widget.bind("<Leave>", self._al_salir)
            widget.bind("<Button-1>", self._al_presionar)
            widget.bind("<ButtonRelease-1>", self._al_soltar)

    # ------------------------------------------------------------ eventos ---
    def _al_entrar(self, _evento=None):
        """Efecto hover: aclara el fondo y resalta el borde."""
        if not self.habilitado:
            return
        self.configure(bg=self.color_hover, highlightbackground=COLORES["celeste_claro"])
        self.etiqueta.configure(bg=self.color_hover, fg=self.texto_hover)

    def _al_salir(self, _evento=None):
        """Devuelve el boton a su color original."""
        if not self.habilitado:
            return
        self.configure(bg=self.color_normal, highlightbackground=self.borde_normal)
        self.etiqueta.configure(bg=self.color_normal, fg=self.texto_normal)

    def _al_presionar(self, _evento=None):
        """Retroalimentacion visual al hacer clic (oscurece ligeramente)."""
        if not self.habilitado:
            return
        self.configure(bg=self.color_normal)
        self.etiqueta.configure(bg=self.color_normal, fg=self.texto_normal)

    def _al_soltar(self, _evento=None):
        """Ejecuta el comando asociado cuando se suelta el boton del mouse."""
        if not self.habilitado:
            return
        self._al_entrar()
        if callable(self.comando):
            self.comando()

    # ---------------------------------------------------------- utilidades ---
    def cambiar_texto(self, texto_nuevo):
        """Permite actualizar la leyenda del boton en tiempo de ejecucion."""
        self.etiqueta.configure(text=texto_nuevo)


class TarjetaMenu(tk.Frame):
    """
    Tarjeta grande del menu principal con icono, titulo, descripcion y hover.

    Cada tarjeta abre un modulo distinto mediante una ventana Toplevel.
    """

    def __init__(self, padre, icono, titulo, descripcion, comando, color_acento):
        super().__init__(padre, bg=COLORES["superficie"],
                         highlightthickness=1,
                         highlightbackground=COLORES["borde"],
                         cursor="hand2")
        self.comando = comando
        self.color_acento = color_acento

        # -------- Franja vertical de color que identifica cada modulo --------
        self.franja = tk.Frame(self, bg=color_acento, width=5)
        self.franja.pack(side="left", fill="y")

        # ----------------------- Contenido de la tarjeta ---------------------
        self.cuerpo = tk.Frame(self, bg=COLORES["superficie"])
        self.cuerpo.pack(side="left", fill="both", expand=True)

        # El interior se centra verticalmente dentro de la tarjeta, de modo que
        # el texto no quede pegado al borde superior cuando la tarjeta es alta.
        self.interior = tk.Frame(self.cuerpo, bg=COLORES["superficie"])
        self.interior.pack(expand=True, fill="x", padx=16)

        self.icono = tk.Label(self.interior, text=icono, bg=COLORES["superficie"],
                              fg=color_acento, font=FUENTES["icono_medio"])
        self.icono.pack(anchor="w")

        self.titulo = tk.Label(self.interior, text=titulo, bg=COLORES["superficie"],
                               fg=COLORES["texto"], font=FUENTES["texto_bold"],
                               anchor="w", justify="left", wraplength=210)
        self.titulo.pack(anchor="w", pady=(6, 0))

        self.descripcion = tk.Label(self.interior, text=descripcion,
                                    bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                                    font=FUENTES["pequena"], anchor="w", justify="left",
                                    wraplength=210)
        self.descripcion.pack(anchor="w", pady=(2, 0))

        # Todos los hijos deben reaccionar al mouse para que el hover sea fluido.
        self._widgets = [self, self.cuerpo, self.interior,
                         self.icono, self.titulo, self.descripcion]
        for widget in self._widgets:
            widget.bind("<Enter>", self._al_entrar)
            widget.bind("<Leave>", self._al_salir)
            widget.bind("<Button-1>", self._al_hacer_clic)
            widget.configure(cursor="hand2")

    def _pintar(self, color_fondo, color_titulo, color_borde, ancho_franja):
        """Aplica un juego de colores a toda la tarjeta (uso interno)."""
        self.configure(bg=color_fondo, highlightbackground=color_borde)
        self.cuerpo.configure(bg=color_fondo)
        self.interior.configure(bg=color_fondo)
        self.icono.configure(bg=color_fondo)
        self.titulo.configure(bg=color_fondo, fg=color_titulo)
        self.descripcion.configure(bg=color_fondo)
        self.franja.configure(width=ancho_franja)

    def _al_entrar(self, _evento=None):
        """Efecto hover: se ilumina el fondo y crece la franja de color."""
        self._pintar(COLORES["superficie_alt"], COLORES["blanco"], self.color_acento, 9)
        self.descripcion.configure(fg=COLORES["texto_suave"])

    def _al_salir(self, _evento=None):
        """Restaura la apariencia normal de la tarjeta."""
        self._pintar(COLORES["superficie"], COLORES["texto"], COLORES["borde"], 5)
        self.descripcion.configure(fg=COLORES["texto_tenue"])

    def _al_hacer_clic(self, _evento=None):
        """Ejecuta la accion del modulo asociado a la tarjeta."""
        if callable(self.comando):
            self.comando()


class CampoFormulario:
    """
    Campo de formulario reutilizable: etiqueta + Entry o Combobox.

    Encapsular el campo permite crear formularios completos en pocas lineas
    y ofrece metodos uniformes: obtener(), asignar() y limpiar().
    """

    def __init__(self, padre, etiqueta, tipo="entrada", valores=None,
                 icono="", ancho=26, fila=0, columna=0, columnas_ocupadas=1):
        self.tipo = tipo

        # ------------------------- Contenedor del campo ----------------------
        self.contenedor = tk.Frame(padre, bg=COLORES["superficie"])
        self.contenedor.grid(row=fila, column=columna, columnspan=columnas_ocupadas,
                             sticky="ew", padx=8, pady=2)

        texto_etiqueta = ("%s %s" % (icono, etiqueta)).strip() if icono else etiqueta
        self.etiqueta = tk.Label(
            self.contenedor, text=texto_etiqueta.upper(),
            bg=COLORES["superficie"], fg=COLORES["texto_suave"],
            font=FUENTES["pequena_bold"], anchor="w",
        )
        self.etiqueta.pack(anchor="w", pady=(0, 2))

        self.variable = tk.StringVar()

        # -------------------- Creacion del control adecuado ------------------
        if tipo == "combo":
            self.control = ttk.Combobox(
                self.contenedor, textvariable=self.variable,
                values=list(valores or []), state="readonly",
                style="Study.TCombobox", width=ancho, font=FUENTES["texto"],
            )
        else:
            self.control = ttk.Entry(
                self.contenedor, textvariable=self.variable,
                style="Study.TEntry", width=ancho, font=FUENTES["texto"],
            )
        self.control.pack(fill="x")

    # ------------------------------------------------------------ acceso ----
    def obtener(self):
        """Devuelve el contenido actual del campo, sin espacios sobrantes."""
        return self.variable.get().strip()

    def asignar(self, valor):
        """Escribe un valor en el campo (usado al editar un registro)."""
        self.variable.set("" if valor is None else str(valor))

    def limpiar(self):
        """Vacia el campo."""
        self.variable.set("")

    def actualizar_valores(self, valores):
        """Refresca la lista de opciones de un combobox."""
        if self.tipo == "combo":
            self.control.configure(values=list(valores))

    def enfocar(self):
        """Coloca el cursor del teclado en este campo."""
        ejecutar_seguro(self.control.focus_set, "asignacion de foco")


class TarjetaIndicador(tk.Frame):
    """
    Tarjeta compacta que muestra un indicador numerico (KPI).

    Se usa para presentar los resultados de la calculadora de promedios:
    icono + valor grande + descripcion corta.
    """

    def __init__(self, padre, icono, titulo, valor="0", color=None, ancho=190, alto=110):
        color = color or COLORES["celeste_claro"]
        super().__init__(padre, bg=COLORES["superficie"], width=ancho, height=alto,
                         highlightthickness=1, highlightbackground=COLORES["borde"])
        self.pack_propagate(False)

        # Franja superior de color para identificar visualmente el indicador.
        tk.Frame(self, bg=color, height=4).pack(fill="x")

        contenido = tk.Frame(self, bg=COLORES["superficie"])
        contenido.pack(fill="both", expand=True, padx=14, pady=10)

        encabezado = tk.Frame(contenido, bg=COLORES["superficie"])
        encabezado.pack(fill="x")
        tk.Label(encabezado, text=icono, bg=COLORES["superficie"], fg=color,
                 font=FUENTES["texto_bold"]).pack(side="left")
        tk.Label(encabezado, text=titulo.upper(), bg=COLORES["superficie"],
                 fg=COLORES["texto_tenue"], font=FUENTES["micro"]).pack(side="left", padx=(6, 0))

        self.etiqueta_valor = tk.Label(contenido, text=str(valor), bg=COLORES["superficie"],
                                       fg=COLORES["texto"], font=FUENTES["titulo"])
        self.etiqueta_valor.pack(anchor="w", pady=(6, 0))

    def actualizar(self, valor, color=None):
        """Cambia el valor mostrado y opcionalmente su color."""
        self.etiqueta_valor.configure(text=str(valor))
        if color:
            self.etiqueta_valor.configure(fg=color)


def crear_titulo_seccion(padre, icono, texto, descripcion=""):
    """
    Crea un encabezado de seccion uniforme dentro de los modulos.

    Devuelve el Frame creado por si el modulo necesita agregar controles
    adicionales a la derecha del titulo.
    """
    contenedor = tk.Frame(padre, bg=COLORES["fondo"])
    fila = tk.Frame(contenedor, bg=COLORES["fondo"])
    fila.pack(fill="x")

    tk.Label(fila, text=icono, bg=COLORES["fondo"], fg=COLORES["celeste_claro"],
             font=FUENTES["texto_bold"]).pack(side="left")
    tk.Label(fila, text=texto.upper(), bg=COLORES["fondo"], fg=COLORES["texto"],
             font=FUENTES["seccion"]).pack(side="left", padx=(8, 0))

    if descripcion:
        tk.Label(contenedor, text=descripcion, bg=COLORES["fondo"],
                 fg=COLORES["texto_sobre_gris"], font=FUENTES["pequena"],
                 anchor="w", justify="left").pack(anchor="w", pady=(2, 0))

    return contenedor


def crear_tabla(padre, columnas, anchos, alineaciones=None, altura=11,
                columna_elastica=None):
    """
    Construye un Treeview con scrollbars y estilo oscuro personalizado.

    Parametros:
        columnas     : lista de titulos visibles
        anchos       : lista de anchos en pixeles (misma longitud que columnas)
        alineaciones : lista opcional de anclas ('w', 'center', 'e')
        altura       : numero de filas visibles
        columna_elastica : indice de la columna que absorbe el espacio sobrante
                           (por omision, la ultima)

    Devuelve la tupla (contenedor, tabla) para que el modulo la posicione.
    """
    contenedor = tk.Frame(padre, bg=COLORES["superficie"],
                          highlightthickness=1, highlightbackground=COLORES["borde"])

    identificadores = ["col%d" % indice for indice in range(len(columnas))]
    tabla = ttk.Treeview(contenedor, columns=identificadores, show="headings",
                         height=altura, style="Study.Treeview", selectmode="browse")

    # Una columna se estira para ocupar el espacio sobrante, de modo que la
    # tabla nunca necesita una barra de desplazamiento horizontal.
    alineaciones = alineaciones or ["w"] * len(columnas)
    if columna_elastica is None:
        columna_elastica = len(columnas) - 1
    for indice, titulo in enumerate(columnas):
        tabla.heading(identificadores[indice], text=titulo.upper())
        tabla.column(identificadores[indice], width=anchos[indice],
                     minwidth=anchos[indice], anchor=alineaciones[indice],
                     stretch=(indice == columna_elastica))

    barra_vertical = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview,
                                   style="Study.Vertical.TScrollbar")
    tabla.configure(yscrollcommand=barra_vertical.set)

    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)

    # Etiquetas de color reutilizables en todos los modulos.
    tabla.tag_configure("par", background=COLORES["superficie"])
    tabla.tag_configure("impar", background=COLORES["fondo_alt"])
    tabla.tag_configure("exito", foreground=COLORES["exito"])
    tabla.tag_configure("error", foreground=COLORES["error"])
    tabla.tag_configure("alerta", foreground=COLORES["alerta"])
    tabla.tag_configure("info", foreground=COLORES["azul_claro"])

    return contenedor, tabla


def llenar_tabla(tabla, filas):
    """
    Vacia un Treeview y lo vuelve a llenar con las filas indicadas.

    Cada elemento de 'filas' es una tupla (identificador, valores, etiqueta):
        identificador -> id del registro (se usa como iid del Treeview)
        valores       -> tupla con el contenido de cada columna
        etiqueta      -> nombre de un tag de color, o None
    """
    tabla.delete(*tabla.get_children())
    for indice, (identificador, valores, etiqueta) in enumerate(filas):
        etiquetas = ["par" if indice % 2 == 0 else "impar"]
        if etiqueta:
            etiquetas.append(etiqueta)
        tabla.insert("", "end", iid=str(identificador), values=valores, tags=tuple(etiquetas))


def obtener_id_seleccionado(tabla):
    """Devuelve el id (entero) de la fila seleccionada o None si no hay ninguna."""
    seleccion = tabla.selection()
    if not seleccion:
        return None
    try:
        return int(seleccion[0])
    except ValueError:
        return None


def cargar_imagen_logo(tamano=70):
    """
    Intenta cargar el logotipo institucional en formato PNG.

    Busca los nombres definidos en NOMBRES_LOGO dentro de la carpeta del
    script. Si encuentra uno lo escala proporcionalmente; si no encuentra
    ninguno devuelve None y el encabezado dibuja un marcador de posicion.
    """
    for nombre in NOMBRES_LOGO:
        ruta = os.path.join(CARPETA_BASE, nombre)
        if not os.path.exists(ruta):
            continue
        try:
            imagen = tk.PhotoImage(file=ruta)
            # subsample solo acepta enteros: se calcula el factor mas cercano.
            factor = max(1, int(max(imagen.width(), imagen.height()) / float(tamano)))
            if factor > 1:
                imagen = imagen.subsample(factor, factor)
            IMAGENES_EN_MEMORIA.append(imagen)      # Evita el borrado automatico
            return imagen
        except tk.TclError:
            continue
    return None


def crear_espacio_logo(padre, tamano=70):
    """
    Crea el area del logo de la PUCE en la esquina superior izquierda.

    Si existe el PNG lo muestra; si no, dibuja un escudo generado con Canvas
    que queda listo para ser reemplazado por la imagen oficial.
    """
    marco = tk.Frame(padre, bg=COLORES["negro"], width=tamano, height=tamano,
                     highlightthickness=1, highlightbackground=COLORES["celeste_oscuro"])
    marco.pack_propagate(False)

    imagen = cargar_imagen_logo(tamano - 8)
    if imagen is not None:
        etiqueta = tk.Label(marco, image=imagen, bg=COLORES["negro"])
        etiqueta.imagen = imagen                    # Referencia adicional
        etiqueta.pack(expand=True)
    else:
        # ------- Marcador de posicion dibujado (listo para el PNG real) ------
        lienzo = tk.Canvas(marco, width=tamano, height=tamano, bg=COLORES["negro"],
                           highlightthickness=0)
        lienzo.pack(expand=True, fill="both")
        margen = 10
        lienzo.create_oval(margen, margen, tamano - margen, tamano - margen,
                           outline=COLORES["celeste"], width=2)
        lienzo.create_oval(margen + 6, margen + 6, tamano - margen - 6, tamano - margen - 6,
                           outline=COLORES["cian"], width=1)
        lienzo.create_text(tamano / 2, tamano / 2 - 4, text="PUCE",
                           fill=COLORES["blanco"], font=("TkDefaultFont", 11, "bold"))
        lienzo.create_text(tamano / 2, tamano / 2 + 11, text="LOGO",
                           fill=COLORES["texto_tenue"], font=("TkDefaultFont", 6))
    return marco


def crear_barra_institucional(padre):
    """
    Barra superior comun a TODAS las ventanas del sistema.

    Contiene el espacio del logo, el nombre de la universidad, la catedra y
    los autores del proyecto.
    """
    barra = tk.Frame(padre, bg=COLORES["negro"], height=86)
    barra.pack_propagate(False)

    # ------------------------------ Lado izquierdo ---------------------------
    izquierda = tk.Frame(barra, bg=COLORES["negro"])
    izquierda.pack(side="left", fill="y", padx=18, pady=8)

    logo = crear_espacio_logo(izquierda, 68)
    logo.pack(side="left")

    textos = tk.Frame(izquierda, bg=COLORES["negro"])
    textos.pack(side="left", padx=14)
    tk.Label(textos, text=APP_UNIVERSIDAD, bg=COLORES["negro"], fg=COLORES["texto"],
             font=FUENTES["etiqueta_bold"]).pack(anchor="w", pady=(10, 0))
    tk.Label(textos, text=APP_CATEDRA, bg=COLORES["negro"], fg=COLORES["celeste_claro"],
             font=FUENTES["micro"]).pack(anchor="w")
    tk.Label(textos, text=APP_AUTORES, bg=COLORES["negro"], fg=COLORES["texto_tenue"],
             font=FUENTES["micro"]).pack(anchor="w")

    return barra


# =============================================================================
# SECCION 9 : VENTANA BASE PARA LOS MODULOS (Toplevel)
# =============================================================================

class VentanaModulo(tk.Toplevel):
    """
    Plantilla comun de todas las ventanas de modulo.

    Garantiza que cada modulo tenga exactamente el mismo diseno:
        - Barra institucional con el logo y los datos de la universidad
        - Franja de titulo del modulo con icono y descripcion
        - Area de contenido (self.cuerpo) que llena cada modulo
        - Pie de ventana con el boton REGRESAR al menu principal

    Ademas oculta el menu principal mientras el modulo esta abierto y lo
    vuelve a mostrar al regresar, logrando una navegacion clara.
    """

    def __init__(self, aplicacion, titulo, descripcion, icono="✦", color_acento=None):
        super().__init__(aplicacion.raiz)
        self.aplicacion = aplicacion
        self.color_acento = color_acento or COLORES["celeste"]

        # ------------------------- Configuracion base ------------------------
        self.title("%s  |  %s" % (APP_NOMBRE, titulo))
        self.configure(bg=COLORES["fondo"])
        self.resizable(False, False)             # Tamano fijo en todas las ventanas
        centrar_ventana(self, VENTANA_ANCHO, VENTANA_ALTO)
        self.protocol("WM_DELETE_WINDOW", self.regresar)
        self.bind("<Escape>", lambda evento=None: self.regresar())

        # Se oculta el menu principal para simular navegacion entre pantallas.
        # Importante: esta ventana NO se declara 'transient' del menu, porque
        # Tk oculta automaticamente las ventanas transient cuando su ventana
        # maestra se oculta, y el modulo quedaria invisible al usuario.
        aplicacion.raiz.withdraw()

        # --------------------------- Barra superior --------------------------
        crear_barra_institucional(self).pack(fill="x")

        tk.Frame(self, bg=self.color_acento, height=3).pack(fill="x")

        # ----------------------- Franja de titulo del modulo -----------------
        franja = tk.Frame(self, bg=COLORES["fondo_alt"], height=70)
        franja.pack(fill="x")
        franja.pack_propagate(False)

        bloque_titulo = tk.Frame(franja, bg=COLORES["fondo_alt"])
        bloque_titulo.pack(side="left", padx=22, pady=8)

        tk.Label(bloque_titulo, text=icono, bg=COLORES["fondo_alt"],
                 fg=self.color_acento, font=FUENTES["icono_medio"]).pack(side="left")

        textos = tk.Frame(bloque_titulo, bg=COLORES["fondo_alt"])
        textos.pack(side="left", padx=12)
        tk.Label(textos, text=titulo.upper(), bg=COLORES["fondo_alt"],
                 fg=COLORES["texto"], font=FUENTES["titulo"]).pack(anchor="w")
        tk.Label(textos, text=descripcion, bg=COLORES["fondo_alt"],
                 fg=COLORES["texto_suave"], font=FUENTES["pequena"]).pack(anchor="w")

        # Espacio a la derecha de la franja por si el modulo agrega controles.
        self.zona_titulo_derecha = tk.Frame(franja, bg=COLORES["fondo_alt"])
        self.zona_titulo_derecha.pack(side="right", padx=22)

        # ------------------------------ Pie fijo -----------------------------
        pie = tk.Frame(self, bg=COLORES["negro"], height=58)
        pie.pack(side="bottom", fill="x")
        pie.pack_propagate(False)

        BotonModerno(
            pie, "REGRESAR AL MENU", self.regresar,
            ancho=200, alto=38,
            color=COLORES["superficie_alt"], color_hover=COLORES["celeste"],
            color_texto=COLORES["texto"], borde=COLORES["borde"],
            fuente=FUENTES["boton_pequeno"],
        ).pack(side="left", padx=18, pady=10)

        self.mensaje_pie = tk.Label(
            pie, text="Los cambios se guardan automaticamente en archivos JSON",
            bg=COLORES["negro"], fg=COLORES["texto_tenue"], font=FUENTES["pequena"],
        )
        self.mensaje_pie.pack(side="right", padx=22)

        # --------------------------- Cuerpo del modulo -----------------------
        self.cuerpo = tk.Frame(self, bg=COLORES["fondo"])
        self.cuerpo.pack(fill="both", expand=True, padx=22, pady=8)

        self.after(60, self._enfocar_ventana)

    # ------------------------------------------------------------ acciones ---
    def _enfocar_ventana(self):
        """Trae la ventana al frente al abrirse (comportamiento profesional)."""
        def traer_al_frente():
            self.lift()
            self.focus_force()
        ejecutar_seguro(traer_al_frente, "elevacion de la ventana")

    @manejar_errores
    def regresar(self):
        """Cierra el modulo y vuelve a mostrar el menu principal."""
        def restaurar_menu():
            self.aplicacion.raiz.deiconify()
            self.aplicacion.raiz.lift()
            self.aplicacion.actualizar_resumen()
        ejecutar_seguro(restaurar_menu, "restauracion del menu principal")
        self.destroy()

    def actualizar_mensaje(self, texto, color=None):
        """Muestra un mensaje de estado en el pie de la ventana."""
        self.mensaje_pie.configure(text=texto, fg=color or COLORES["texto_tenue"])

    # --------------------------------------------------- ayudas de dialogo ---
    def informar(self, titulo, mensaje):
        """Cuadro de dialogo informativo asociado a esta ventana."""
        messagebox.showinfo(titulo, mensaje, parent=self)

    def advertir(self, titulo, mensaje):
        """Cuadro de dialogo de advertencia asociado a esta ventana."""
        messagebox.showwarning(titulo, mensaje, parent=self)

    def error(self, titulo, mensaje):
        """Cuadro de dialogo de error asociado a esta ventana."""
        messagebox.showerror(titulo, mensaje, parent=self)

    def confirmar(self, titulo, mensaje):
        """Cuadro de confirmacion Si/No asociado a esta ventana."""
        return messagebox.askyesno(titulo, mensaje, parent=self)


# =============================================================================
# SECCION 10 : MODULO 1 - REGISTRO DE MATERIAS
# =============================================================================
# Permite registrar, editar y eliminar las materias del semestre con su
# docente, aula y horario general. Toda la informacion se muestra
# en un Treeview y se guarda automaticamente en materias.json.
# =============================================================================

class VentanaMaterias(VentanaModulo):
    """Modulo 1: administracion completa de las materias del estudiante."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Registro de Materias",
            descripcion="Administre las asignaturas del semestre, sus docentes y sus aulas",
            icono="📚",
            color_acento=COLORES["celeste"],
        )
        self.id_seleccionado = None              # Registro actualmente en edicion
        self.construir_interfaz()
        self.refrescar_tabla()

    # ------------------------------------------------------------ interfaz ---
    def construir_interfaz(self):
        """Arma el formulario de la izquierda y la tabla de la derecha."""
        contenedor = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        # ============================ PANEL IZQUIERDO ========================
        panel_formulario = tk.Frame(contenedor, bg=COLORES["superficie"], width=330,
                                    highlightthickness=1, highlightbackground=COLORES["borde"])
        panel_formulario.pack(side="left", fill="y")
        panel_formulario.pack_propagate(False)

        tk.Frame(panel_formulario, bg=COLORES["celeste"], height=4).pack(fill="x")

        encabezado = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        encabezado.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(encabezado, text="📝 DATOS DE LA MATERIA", bg=COLORES["superficie"],
                 fg=COLORES["texto"], font=FUENTES["seccion"]).pack(anchor="w")
        tk.Label(encabezado, text="Escoja la materia y complete los datos",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"]).pack(anchor="w", pady=(2, 0))

        formulario = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        formulario.pack(fill="x", pady=(6, 0))
        formulario.grid_columnconfigure(0, weight=1)
        formulario.grid_columnconfigure(1, weight=1)

        # ------------------------- Campos del formulario ---------------------
        self.campo_materia = CampoFormulario(formulario, "Materia", tipo="combo",
                                             valores=MATERIAS_DISPONIBLES, icono="📘",
                                             fila=0, columnas_ocupadas=2)
        self.campo_docente = CampoFormulario(formulario, "Docente", icono="👨‍🏫",
                                             fila=1, columnas_ocupadas=2)
        self.campo_aula = CampoFormulario(formulario, "Aula", icono="🏫",
                                          fila=2, columnas_ocupadas=2)
        self.campo_horario = CampoFormulario(formulario, "Horario", icono="🕐",
                                             fila=3, columnas_ocupadas=2)

        tk.Label(panel_formulario,
                 text="Ejemplo:  Lunes y Miercoles 07:00 - 09:00",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["micro"]).pack(anchor="w", padx=18, pady=(2, 0))

        # ----------------------------- Botonera ------------------------------
        botonera = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        botonera.pack(side="bottom", fill="x", padx=14, pady=(4, 8))

        # Cada fila de la botonera contiene dos botones del mismo tamano.
        fila_uno = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_uno.pack(fill="x", pady=3)
        BotonModerno(fila_uno, "GUARDAR", self.guardar_materia,
                     ancho=140, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila_uno, "EDITAR", self.editar_materia,
                     ancho=140, alto=36, color=COLORES["azul"],
                     color_hover=COLORES["azul_claro"]).pack(side="right")

        fila_dos = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_dos.pack(fill="x", pady=3)
        BotonModerno(fila_dos, "ELIMINAR", self.eliminar_materia,
                     ancho=140, alto=36, color=COLORES["error"],
                     color_hover=COLORES["error_hover"]).pack(side="left")
        BotonModerno(fila_dos, "LIMPIAR", self.limpiar_formulario,
                     ancho=140, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["celeste"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"]).pack(side="right")

        # ============================ PANEL DERECHO ==========================
        panel_tabla = tk.Frame(contenedor, bg=COLORES["fondo"])
        panel_tabla.pack(side="left", fill="both", expand=True, padx=(18, 0))

        cabecera_tabla = tk.Frame(panel_tabla, bg=COLORES["fondo"])
        cabecera_tabla.pack(fill="x", pady=(0, 10))
        crear_titulo_seccion(
            cabecera_tabla, "📋", "Materias registradas",
            "Seleccione una fila para cargarla en el formulario"
        ).pack(side="left")

        self.etiqueta_contador = tk.Label(
            cabecera_tabla, text="0 materias", bg=COLORES["fondo"],
            fg=COLORES["celeste_oscuro"], font=FUENTES["texto_bold"],
        )
        self.etiqueta_contador.pack(side="right", pady=6)

        contenedor_tabla, self.tabla = crear_tabla(
            panel_tabla,
            columnas=["#", "Materia", "Docente", "Aula", "Horario"],
            anchos=[30, 238, 122, 58, 216],
            alineaciones=["center", "w", "w", "center", "w"],
            altura=11,
        )
        contenedor_tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)
        self.tabla.bind("<Double-1>", lambda evento=None: self.editar_materia())

        # ------------------------ Resumen inferior ---------------------------
        resumen = tk.Frame(panel_tabla, bg=COLORES["fondo_alt"],
                           highlightthickness=1, highlightbackground=COLORES["borde"])
        resumen.pack(fill="x", pady=(12, 0))
        self.etiqueta_resumen = tk.Label(
            resumen, text="", bg=COLORES["fondo_alt"], fg=COLORES["texto_suave"],
            font=FUENTES["pequena"], anchor="w",
        )
        self.etiqueta_resumen.pack(fill="x", padx=14, pady=10)

    # ---------------------------------------------------------------- datos --
    def refrescar_tabla(self):
        """Vuelve a dibujar la tabla con la informacion actual de la memoria."""
        materias_ordenadas = sorted(DATOS.materias,
                                    key=lambda registro: str(registro.get("materia", "")).lower())
        filas = []
        for indice, materia in enumerate(materias_ordenadas, start=1):
            filas.append((
                materia.get("id"),
                (
                    indice,
                    materia.get("materia", ""),
                    materia.get("docente", ""),
                    materia.get("aula", ""),
                    materia.get("horario", ""),
                ),
                None,
            ))
        llenar_tabla(self.tabla, filas)

        # ------------------------- Indicadores del panel ---------------------
        total = len(DATOS.materias)
        docentes = len({str(m.get("docente", "")).strip().lower()
                        for m in DATOS.materias if str(m.get("docente", "")).strip()})

        self.etiqueta_contador.configure(text="%d materia%s" % (total, "" if total == 1 else "s"))
        self.etiqueta_resumen.configure(
            text="Total de materias registradas: %d               "
                 "Docentes distintos: %d" % (total, docentes)
        )

    def leer_formulario(self):
        """
        Valida todos los campos del formulario.

        Devuelve un diccionario listo para guardar, o None si alguna
        validacion fallo (en ese caso ya se mostro el messagebox).
        """
        valido, materia = validar_opcion(self.campo_materia.obtener(), "Materia",
                                         MATERIAS_DISPONIBLES)
        if not valido:
            self.advertir("Validacion", materia)
            self.campo_materia.enfocar()
            return None

        valido, docente = validar_texto(self.campo_docente.obtener(), "Docente", minimo=3)
        if not valido:
            self.advertir("Validacion", docente)
            self.campo_docente.enfocar()
            return None

        valido, aula = validar_texto(self.campo_aula.obtener(), "Aula", minimo=1, maximo=20)
        if not valido:
            self.advertir("Validacion", aula)
            self.campo_aula.enfocar()
            return None

        valido, horario = validar_texto(self.campo_horario.obtener(), "Horario", minimo=3)
        if not valido:
            self.advertir("Validacion", horario)
            self.campo_horario.enfocar()
            return None

        return {
            "materia": materia,
            "docente": docente,
            "aula": aula,
            "horario": horario,
        }

    def existe_materia(self, nombre, excluir_id=None):
        """Comprueba si ya existe otra materia con el mismo nombre."""
        nombre = nombre.strip().lower()
        for registro in DATOS.materias:
            if excluir_id is not None and int(registro.get("id", -1)) == int(excluir_id):
                continue
            if str(registro.get("materia", "")).strip().lower() == nombre:
                return True
        return False

    # ------------------------------------------------------------- acciones --
    @manejar_errores
    def guardar_materia(self):
        """Registra una nueva materia y la guarda en materias.json."""
        datos = self.leer_formulario()
        if datos is None:
            return

        if self.existe_materia(datos["materia"]):
            self.advertir(
                "Materia duplicada",
                "La materia '%s' ya se encuentra registrada.\n\n"
                "Si desea modificarla, seleccionela en la tabla y use el boton EDITAR."
                % datos["materia"]
            )
            return

        datos["id"] = DATOS.nuevo_id(DATOS.materias)
        DATOS.materias.append(datos)
        DATOS.guardar_materias()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("✔ Materia '%s' guardada correctamente" % datos["materia"],
                                COLORES["exito"])
        self.informar("Registro exitoso",
                      "La materia '%s' fue registrada correctamente." % datos["materia"])

    @manejar_errores
    def editar_materia(self):
        """Actualiza la materia seleccionada con los datos del formulario."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion",
                          "Seleccione en la tabla la materia que desea editar.")
            return

        registro = DATOS.buscar_por_id(DATOS.materias, identificador)
        if registro is None:
            self.error("Registro no encontrado", "La materia seleccionada ya no existe.")
            self.refrescar_tabla()
            return

        datos = self.leer_formulario()
        if datos is None:
            return

        if self.existe_materia(datos["materia"], excluir_id=identificador):
            self.advertir("Materia duplicada",
                          "Ya existe otra materia registrada con el nombre '%s'." % datos["materia"])
            return

        if not self.confirmar("Confirmar edicion",
                              "Se actualizara la materia:\n\n%s\n\nDesea continuar?"
                              % registro.get("materia", "")):
            return

        nombre_anterior = registro.get("materia", "")
        registro.update(datos)
        DATOS.guardar_materias()

        # Si cambio el nombre, se actualizan las referencias en otros modulos.
        if nombre_anterior != datos["materia"]:
            self.propagar_cambio_de_nombre(nombre_anterior, datos["materia"])

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("✔ Materia actualizada correctamente", COLORES["azul_claro"])
        self.informar("Edicion exitosa", "La materia fue actualizada correctamente.")

    def propagar_cambio_de_nombre(self, anterior, nuevo):
        """
        Mantiene la coherencia de los datos al renombrar una materia.

        Actualiza el horario y los promedios guardados para que sigan
        apuntando a la materia correcta despues de la edicion.
        """
        for bloque in DATOS.horario:
            if bloque.get("materia") == anterior:
                bloque["materia"] = nuevo
        for nota in DATOS.notas:
            if nota.get("materia") == anterior:
                nota["materia"] = nuevo
        DATOS.guardar_horario()
        DATOS.guardar_notas()

    @manejar_errores
    def eliminar_materia(self):
        """Elimina la materia seleccionada previa confirmacion del usuario."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion",
                          "Seleccione en la tabla la materia que desea eliminar.")
            return

        registro = DATOS.buscar_por_id(DATOS.materias, identificador)
        if registro is None:
            self.error("Registro no encontrado", "La materia seleccionada ya no existe.")
            self.refrescar_tabla()
            return

        nombre = registro.get("materia", "")
        bloques_asociados = sum(1 for h in DATOS.horario if h.get("materia") == nombre)

        aviso = ""
        if bloques_asociados:
            aviso = ("\n\nAtencion: esta materia tiene %d bloque(s) de horario asociados. "
                     "Esos registros se conservaran." % bloques_asociados)

        if not self.confirmar("Confirmar eliminacion",
                              "Desea eliminar definitivamente la materia:\n\n%s%s" % (nombre, aviso)):
            return

        DATOS.eliminar_por_id(DATOS.materias, identificador)
        DATOS.guardar_materias()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("🗑 Materia '%s' eliminada" % nombre, COLORES["error"])
        self.informar("Eliminacion exitosa", "La materia '%s' fue eliminada." % nombre)

    @manejar_errores
    def limpiar_formulario(self, silencioso=False):
        """Vacia todos los campos y quita la seleccion de la tabla."""
        for campo in (self.campo_materia, self.campo_docente,
                      self.campo_aula, self.campo_horario):
            campo.limpiar()
        self.id_seleccionado = None
        limpiar_seleccion(self.tabla)
        self.campo_materia.enfocar()
        if not silencioso:
            self.actualizar_mensaje("🧹 Formulario limpio", COLORES["texto_suave"])

    @manejar_errores
    def al_seleccionar_fila(self, _evento=None):
        """Carga en el formulario los datos de la fila seleccionada."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            return
        registro = DATOS.buscar_por_id(DATOS.materias, identificador)
        if registro is None:
            return
        self.id_seleccionado = identificador
        self.campo_materia.asignar(registro.get("materia", ""))
        self.campo_docente.asignar(registro.get("docente", ""))
        self.campo_aula.asignar(registro.get("aula", ""))
        self.campo_horario.asignar(registro.get("horario", ""))
        self.actualizar_mensaje("✏ Editando: %s" % registro.get("materia", ""),
                                COLORES["celeste_claro"])


# =============================================================================
# SECCION 11 : MODULO 2 - HORARIO SEMANAL
# =============================================================================
# Registro de los bloques de clase: materia, dia, hora de inicio, hora de fin
# y docente. Detecta cruces de horario, calcula la duracion de cada bloque y
# guarda automaticamente en horario.json.
# =============================================================================

class VentanaHorario(VentanaModulo):
    """Modulo 5: construccion y control del horario semanal de clases."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Horario Semanal",
            descripcion="Organice sus bloques de clase y detecte cruces de horario",
            icono="📅",
            color_acento=COLORES["azul"],
        )
        self.filtro_dia = tk.StringVar(value="Todos")
        self.construir_interfaz()
        self.refrescar_tabla()

    # ------------------------------------------------------------ interfaz ---
    def construir_interfaz(self):
        """Arma el formulario del bloque y la tabla del horario."""
        contenedor = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        # ============================ PANEL IZQUIERDO ========================
        panel = tk.Frame(contenedor, bg=COLORES["superficie"], width=330,
                         highlightthickness=1, highlightbackground=COLORES["borde"])
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        tk.Frame(panel, bg=COLORES["azul"], height=4).pack(fill="x")

        encabezado = tk.Frame(panel, bg=COLORES["superficie"])
        encabezado.pack(fill="x", padx=16, pady=(14, 2))
        tk.Label(encabezado, text="🕐 BLOQUE DE CLASE", bg=COLORES["superficie"],
                 fg=COLORES["texto"], font=FUENTES["seccion"]).pack(anchor="w")
        tk.Label(encabezado, text="Las horas se escriben en formato 24h (HH:MM)",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"]).pack(anchor="w", pady=(3, 0))

        formulario = tk.Frame(panel, bg=COLORES["superficie"])
        formulario.pack(fill="x", pady=(6, 0))
        formulario.grid_columnconfigure(0, weight=1)
        formulario.grid_columnconfigure(1, weight=1)

        self.campo_materia = CampoFormulario(formulario, "Materia", tipo="combo",
                                             valores=MATERIAS_DISPONIBLES,
                                             icono="📘", fila=0, columnas_ocupadas=2)
        self.campo_dia = CampoFormulario(formulario, "Dia", tipo="combo",
                                         valores=DIAS_SEMANA, icono="📆",
                                         fila=1, columnas_ocupadas=2)
        self.campo_inicio = CampoFormulario(formulario, "Hora de inicio",
                                            icono="▶", fila=2, columna=0, ancho=12)
        self.campo_fin = CampoFormulario(formulario, "Hora de fin", icono="⏹",
                                         fila=2, columna=1, ancho=12)
        self.campo_docente = CampoFormulario(formulario, "Docente", icono="👨‍🏫",
                                             fila=3, columnas_ocupadas=2)

        # Valores iniciales frecuentes.
        self.campo_dia.asignar("Lunes")
        self.campo_inicio.asignar("07:00")
        self.campo_fin.asignar("09:00")

        # ----------------------------- Botonera ------------------------------
        botonera = tk.Frame(panel, bg=COLORES["superficie"])
        botonera.pack(side="bottom", fill="x", padx=14, pady=(4, 8))

        fila_uno = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_uno.pack(fill="x", pady=3)
        BotonModerno(fila_uno, "GUARDAR", self.guardar_bloque,
                     ancho=140, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila_uno, "EDITAR", self.editar_bloque,
                     ancho=140, alto=36, color=COLORES["azul"],
                     color_hover=COLORES["azul_claro"]).pack(side="right")

        fila_dos = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_dos.pack(fill="x", pady=3)
        BotonModerno(fila_dos, "ELIMINAR", self.eliminar_bloque,
                     ancho=140, alto=36, color=COLORES["error"],
                     color_hover=COLORES["error_hover"]).pack(side="left")
        BotonModerno(fila_dos, "LIMPIAR", self.limpiar_formulario,
                     ancho=140, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["celeste"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"]).pack(side="right")

        # ============================ PANEL DERECHO ==========================
        derecha = tk.Frame(contenedor, bg=COLORES["fondo"])
        derecha.pack(side="left", fill="both", expand=True, padx=(18, 0))

        cabecera = tk.Frame(derecha, bg=COLORES["fondo"])
        cabecera.pack(fill="x", pady=(0, 10))
        crear_titulo_seccion(cabecera, "📋", "Bloques registrados",
                             "Ordenados por dia de la semana y hora de inicio").pack(side="left")

        filtros = tk.Frame(cabecera, bg=COLORES["fondo"])
        filtros.pack(side="right", pady=4)
        tk.Label(filtros, text="DIA:", bg=COLORES["fondo"], fg=COLORES["texto_sobre_gris"],
                 font=FUENTES["micro"]).pack(side="left", padx=(0, 6))
        combo = ttk.Combobox(filtros, textvariable=self.filtro_dia, state="readonly",
                             values=["Todos"] + DIAS_SEMANA, style="Study.TCombobox",
                             width=12, font=FUENTES["pequena"])
        combo.pack(side="left")
        combo.bind("<<ComboboxSelected>>", lambda evento=None: self.refrescar_tabla())

        contenedor_tabla, self.tabla = crear_tabla(
            derecha,
            columnas=["#", "Materia", "Dia", "Inicio", "Fin", "Dur.", "Docente"],
            anchos=[30, 190, 74, 56, 52, 78, 142],
            alineaciones=["center", "w", "center", "center", "center", "center", "w"],
            columna_elastica=1,
            altura=7,
        )
        contenedor_tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)
        self.tabla.bind("<Double-1>", lambda evento=None: self.editar_bloque())

        # -------------------- Vista rapida de la semana ----------------------
        crear_titulo_seccion(derecha, "🗓", "Distribucion semanal",
                             "Cantidad de bloques y horas por dia").pack(anchor="w", pady=(12, 8))

        self.lienzo_semana = tk.Canvas(derecha, height=88, bg=COLORES["superficie"],
                                       highlightthickness=1,
                                       highlightbackground=COLORES["borde"])
        self.lienzo_semana.pack(fill="both", expand=True)

        # Resumen numerico de la carga semanal (se actualiza automaticamente).
        self.etiqueta_carga = tk.Label(
            derecha, text="", bg=COLORES["fondo"], fg=COLORES["texto_sobre_gris"],
            font=FUENTES["pequena"], anchor="w",
        )
        self.etiqueta_carga.pack(fill="x", pady=(6, 0))

    # ---------------------------------------------------------------- datos --
    def bloques_ordenados(self):
        """Devuelve los bloques ordenados por dia de la semana y hora."""
        def clave(bloque):
            dia = bloque.get("dia", "")
            indice_dia = DIAS_SEMANA.index(dia) if dia in DIAS_SEMANA else 99
            return (indice_dia, hora_a_minutos(bloque.get("inicio", "00:00")))
        return sorted(DATOS.horario, key=clave)

    def refrescar_tabla(self):
        """Actualiza la tabla, el resumen de carga y el grafico semanal."""
        filtro = self.filtro_dia.get()
        filas = []
        contador = 0
        for bloque in self.bloques_ordenados():
            if filtro != "Todos" and bloque.get("dia") != filtro:
                continue
            contador += 1
            minutos = hora_a_minutos(bloque.get("fin", "")) - hora_a_minutos(bloque.get("inicio", ""))
            duracion = "%dh %02dmin" % (minutos // 60, minutos % 60) if minutos > 0 else "--"
            filas.append((
                bloque.get("id"),
                (
                    contador,
                    bloque.get("materia", ""),
                    bloque.get("dia", ""),
                    bloque.get("inicio", ""),
                    bloque.get("fin", ""),
                    duracion,
                    bloque.get("docente", ""),
                ),
                "info" if bloque.get("dia") == self.dia_actual() else None,
            ))
        llenar_tabla(self.tabla, filas)

        # ------------------------- Resumen de carga --------------------------
        total_bloques = len(DATOS.horario)
        minutos_totales = sum(max(0, hora_a_minutos(b.get("fin", "")) -
                                  hora_a_minutos(b.get("inicio", "")))
                              for b in DATOS.horario)
        materias_distintas = len({b.get("materia", "") for b in DATOS.horario
                                  if b.get("materia")})
        cruces = len(self.detectar_cruces())

        self.etiqueta_carga.configure(
            text="📊  Bloques: %d      ⏱  Carga semanal: %dh %02dmin      "
                 "📘  Materias: %d      ⚠  Cruces detectados: %d"
                 % (total_bloques, minutos_totales // 60, minutos_totales % 60,
                    materias_distintas, cruces),
            fg=COLORES["error_hover"] if cruces else COLORES["texto_sobre_gris"],
        )

        self.dibujar_semana()

    @staticmethod
    def dia_actual():
        """Devuelve el nombre del dia de hoy tal como se usa en el sistema."""
        return DIAS_SEMANA[datetime.date.today().weekday()]

    def detectar_cruces(self, excluir_id=None, candidato=None):
        """
        Busca solapamientos entre bloques del mismo dia.

        Si se entrega 'candidato', comprueba unicamente ese bloque contra los
        ya registrados; en caso contrario revisa todo el horario.
        Devuelve una lista de descripciones de los cruces encontrados.
        """
        cruces = []

        if candidato is not None:
            inicio_nuevo = hora_a_minutos(candidato["inicio"])
            fin_nuevo = hora_a_minutos(candidato["fin"])
            for bloque in DATOS.horario:
                if excluir_id is not None and int(bloque.get("id", -1)) == int(excluir_id):
                    continue
                if bloque.get("dia") != candidato["dia"]:
                    continue
                inicio = hora_a_minutos(bloque.get("inicio", "00:00"))
                fin = hora_a_minutos(bloque.get("fin", "00:00"))
                if inicio_nuevo < fin and inicio < fin_nuevo:
                    cruces.append("%s  %s - %s  (%s)"
                                  % (bloque.get("materia", ""), bloque.get("inicio", ""),
                                     bloque.get("fin", ""), bloque.get("dia", "")))
            return cruces

        # Revision general de todo el horario (para el contador del resumen).
        bloques = self.bloques_ordenados()
        for indice, bloque in enumerate(bloques):
            for otro in bloques[indice + 1:]:
                if bloque.get("dia") != otro.get("dia"):
                    continue
                if (hora_a_minutos(bloque.get("inicio", "")) < hora_a_minutos(otro.get("fin", ""))
                        and hora_a_minutos(otro.get("inicio", "")) < hora_a_minutos(bloque.get("fin", ""))):
                    cruces.append("%s vs %s (%s)" % (bloque.get("materia", ""),
                                                     otro.get("materia", ""),
                                                     bloque.get("dia", "")))
        return cruces

    def dibujar_semana(self):
        """Dibuja un grafico de barras con las horas de clase por dia."""
        lienzo = self.lienzo_semana
        lienzo.delete("all")
        lienzo.update_idletasks()

        ancho_total = max(lienzo.winfo_width(), 700)
        alto_total = max(lienzo.winfo_height(), 70)   # Se adapta al espacio real
        ancho_columna = ancho_total / float(len(DIAS_SEMANA))

        # Minutos de clase acumulados por dia.
        minutos_por_dia = {}
        for dia in DIAS_SEMANA:
            minutos_por_dia[dia] = sum(
                max(0, hora_a_minutos(b.get("fin", "")) - hora_a_minutos(b.get("inicio", "")))
                for b in DATOS.horario if b.get("dia") == dia
            )
        maximo = max(minutos_por_dia.values()) if any(minutos_por_dia.values()) else 1

        hoy = self.dia_actual()
        for indice, dia in enumerate(DIAS_SEMANA):
            minutos = minutos_por_dia[dia]
            centro_x = ancho_columna * indice + ancho_columna / 2.0
            altura_barra = (minutos / float(maximo)) * (alto_total - 52)
            # El dia de hoy se resalta en blanco para diferenciarlo del resto.
            color = COLORES["blanco"] if dia == hoy else COLORES["celeste"]

            base_y = alto_total - 26
            if minutos > 0:
                lienzo.create_rectangle(centro_x - 20, base_y - altura_barra,
                                        centro_x + 20, base_y,
                                        fill=color, outline=color)
                lienzo.create_text(centro_x, base_y - altura_barra - 10,
                                   text="%dh%02d" % (minutos // 60, minutos % 60),
                                   fill=COLORES["texto"], font=("TkDefaultFont", 8, "bold"))
            else:
                lienzo.create_line(centro_x - 20, base_y, centro_x + 20, base_y,
                                   fill=COLORES["borde"], width=2)

            lienzo.create_text(centro_x, alto_total - 12, text=dia[:3].upper(),
                               fill=COLORES["blanco"] if dia == hoy else COLORES["texto_tenue"],
                               font=("TkDefaultFont", 8, "bold"))

    def leer_formulario(self):
        """Valida el formulario del bloque de clase."""
        valido, materia = validar_opcion(self.campo_materia.obtener(), "Materia",
                                         MATERIAS_DISPONIBLES)
        if not valido:
            self.advertir("Validacion", materia)
            self.campo_materia.enfocar()
            return None

        valido, dia = validar_opcion(self.campo_dia.obtener(), "Dia", DIAS_SEMANA)
        if not valido:
            self.advertir("Validacion", dia)
            return None

        valido, inicio = validar_hora(self.campo_inicio.obtener(), "Hora de inicio")
        if not valido:
            self.advertir("Validacion", inicio)
            self.campo_inicio.enfocar()
            return None

        valido, fin = validar_hora(self.campo_fin.obtener(), "Hora de fin")
        if not valido:
            self.advertir("Validacion", fin)
            self.campo_fin.enfocar()
            return None

        if hora_a_minutos(fin) <= hora_a_minutos(inicio):
            self.advertir("Horario invalido",
                          "La hora de fin (%s) debe ser posterior a la hora de inicio (%s)."
                          % (fin, inicio))
            self.campo_fin.enfocar()
            return None

        valido, docente = validar_texto(self.campo_docente.obtener(), "Docente", minimo=3)
        if not valido:
            self.advertir("Validacion", docente)
            self.campo_docente.enfocar()
            return None

        return {"materia": materia, "dia": dia, "inicio": inicio,
                "fin": fin, "docente": docente}

    def confirmar_cruce(self, datos, excluir_id=None):
        """
        Avisa al usuario si el bloque se cruza con otro ya registrado.

        Devuelve True si se puede continuar con el guardado.
        """
        cruces = self.detectar_cruces(excluir_id=excluir_id, candidato=datos)
        if not cruces:
            return True
        return self.confirmar(
            "Cruce de horario",
            "El bloque %s %s - %s se cruza con:\n\n%s\n\nDesea guardarlo de todas formas?"
            % (datos["dia"], datos["inicio"], datos["fin"], "\n".join(cruces))
        )

    # ------------------------------------------------------------- acciones --
    @manejar_errores
    def guardar_bloque(self):
        """Registra un nuevo bloque en horario.json."""
        datos = self.leer_formulario()
        if datos is None:
            return
        if not self.confirmar_cruce(datos):
            return

        datos["id"] = DATOS.nuevo_id(DATOS.horario)
        DATOS.horario.append(datos)
        DATOS.guardar_horario()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("✔ Bloque de %s guardado" % datos["materia"], COLORES["exito"])
        self.informar("Bloque registrado",
                      "El bloque de '%s' (%s %s - %s) fue guardado correctamente."
                      % (datos["materia"], datos["dia"], datos["inicio"], datos["fin"]))

    @manejar_errores
    def editar_bloque(self):
        """Actualiza el bloque seleccionado."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion", "Seleccione el bloque que desea editar.")
            return

        registro = DATOS.buscar_por_id(DATOS.horario, identificador)
        if registro is None:
            self.error("Registro no encontrado", "El bloque seleccionado ya no existe.")
            self.refrescar_tabla()
            return

        datos = self.leer_formulario()
        if datos is None:
            return
        if not self.confirmar_cruce(datos, excluir_id=identificador):
            return
        if not self.confirmar("Confirmar edicion",
                              "Se actualizara el bloque de '%s'.\n\nDesea continuar?"
                              % registro.get("materia", "")):
            return

        registro.update(datos)
        DATOS.guardar_horario()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("✔ Bloque actualizado", COLORES["azul_claro"])
        self.informar("Edicion exitosa", "El bloque de horario fue actualizado.")

    @manejar_errores
    def eliminar_bloque(self):
        """Elimina el bloque seleccionado previa confirmacion."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion", "Seleccione el bloque que desea eliminar.")
            return

        registro = DATOS.buscar_por_id(DATOS.horario, identificador)
        if registro is None:
            self.error("Registro no encontrado", "El bloque seleccionado ya no existe.")
            self.refrescar_tabla()
            return

        if not self.confirmar("Confirmar eliminacion",
                              "Desea eliminar el bloque:\n\n%s  |  %s  %s - %s"
                              % (registro.get("materia", ""), registro.get("dia", ""),
                                 registro.get("inicio", ""), registro.get("fin", ""))):
            return

        DATOS.eliminar_por_id(DATOS.horario, identificador)
        DATOS.guardar_horario()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("🗑 Bloque eliminado", COLORES["error"])
        self.informar("Eliminacion exitosa", "El bloque fue eliminado del horario.")

    @manejar_errores
    def limpiar_formulario(self, silencioso=False):
        """Restablece el formulario del horario."""
        self.campo_materia.limpiar()
        self.campo_dia.asignar("Lunes")
        self.campo_inicio.asignar("07:00")
        self.campo_fin.asignar("09:00")
        self.campo_docente.limpiar()
        limpiar_seleccion(self.tabla)
        self.campo_materia.enfocar()
        if not silencioso:
            self.actualizar_mensaje("🧹 Formulario limpio", COLORES["texto_suave"])

    @manejar_errores
    def al_seleccionar_fila(self, _evento=None):
        """Carga el bloque seleccionado dentro del formulario."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            return
        registro = DATOS.buscar_por_id(DATOS.horario, identificador)
        if registro is None:
            return
        self.campo_materia.asignar(registro.get("materia", ""))
        self.campo_dia.asignar(registro.get("dia", "Lunes"))
        self.campo_inicio.asignar(registro.get("inicio", ""))
        self.campo_fin.asignar(registro.get("fin", ""))
        self.campo_docente.asignar(registro.get("docente", ""))
        self.actualizar_mensaje("✏ Editando bloque de %s" % registro.get("materia", ""),
                                COLORES["celeste_claro"])


# =============================================================================
# SECCION 12 : MODULO 3 - CALCULADORA DE PROMEDIOS
# =============================================================================
# El usuario ingresa sus notas separadas por comas y el sistema entrega la
# lista ordenada, el promedio, la nota mayor, la menor, la cantidad y el
# veredicto APROBADO (verde) o REPROBADO (rojo). Ademas permite guardar el
# resultado en notas.json para alimentar el modulo de estadisticas.
# =============================================================================

class VentanaPromedios(VentanaModulo):
    """Modulo 3: calculo estadistico de las calificaciones del estudiante."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Calculadora de Promedios",
            descripcion="Analice sus calificaciones y conozca su situacion academica",
            icono="📊",
            color_acento=COLORES["azul_claro"],
        )
        self.notas_calculadas = []               # Ultimo calculo realizado
        self.promedio_calculado = 0.0
        self.letra_calculada = ""
        self.construir_interfaz()
        self.refrescar_historial()

    # ------------------------------------------------------------ interfaz ---
    def construir_interfaz(self):
        """Distribuye el panel de ingreso, los indicadores y el historial."""
        contenedor = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        # ============================ PANEL IZQUIERDO ========================
        panel = tk.Frame(contenedor, bg=COLORES["superficie"], width=360,
                         highlightthickness=1, highlightbackground=COLORES["borde"])
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        tk.Frame(panel, bg=COLORES["azul_claro"], height=4).pack(fill="x")

        encabezado = tk.Frame(panel, bg=COLORES["superficie"])
        encabezado.pack(fill="x", padx=16, pady=(14, 2))
        tk.Label(encabezado, text="🔢 INGRESO DE NOTAS", bg=COLORES["superficie"],
                 fg=COLORES["texto"], font=FUENTES["seccion"]).pack(anchor="w")
        tk.Label(encabezado,
                 text="Escriba las notas separadas por comas.\nEjemplo:  35, 42, 28, 50",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"], justify="left").pack(anchor="w", pady=(3, 0))

        # ------------------------ Caja de texto de notas ---------------------
        caja = tk.Frame(panel, bg=COLORES["superficie_alt"],
                        highlightthickness=1, highlightbackground=COLORES["borde"])
        caja.pack(fill="x", padx=16, pady=12)

        self.texto_notas = tk.Text(
            caja, height=4, bg=COLORES["superficie_alt"], fg=COLORES["texto"],
            insertbackground=COLORES["celeste_claro"], relief="flat",
            font=FUENTES["mono"], wrap="word", padx=10, pady=8,
        )
        self.texto_notas.pack(fill="both", expand=True)
        self.texto_notas.bind("<Return>", self._calcular_con_enter)

        # ---------------------- Materia asociada (opcional) ------------------
        formulario = tk.Frame(panel, bg=COLORES["superficie"])
        formulario.pack(fill="x")
        formulario.grid_columnconfigure(0, weight=1)
        self.campo_materia = CampoFormulario(
            formulario, "Materia asociada (opcional)", tipo="combo",
            valores=MATERIAS_DISPONIBLES, icono="📘", fila=0,
        )

        # ------------------- Leyenda de la escala literal --------------------
        leyenda = tk.Frame(panel, bg=COLORES["superficie"])
        leyenda.pack(fill="x", padx=18, pady=(8, 0))

        tk.Label(leyenda, text="ESCALA DE CALIFICACION  (0 a %s)"
                                % formato_numero(NOTA_MAXIMA, 0),
                 bg=COLORES["superficie"], fg=COLORES["celeste_claro"],
                 font=FUENTES["pequena_bold"]).pack(anchor="w", pady=(0, 4))

        # Cada fila de la leyenda se construye a partir de ESCALA_LITERAL, de
        # modo que si la escala cambia el texto se actualiza solo.
        desde = NOTA_MINIMA
        for limite, letra, aprobado, comentario in ESCALA_LITERAL:
            fila_escala = tk.Frame(leyenda, bg=COLORES["superficie"])
            fila_escala.pack(fill="x")
            color = COLORES["exito"] if aprobado else COLORES["error"]
            tk.Label(fila_escala, text="%s - %s" % (formato_numero(desde, 0),
                                                    formato_numero(limite, 0)),
                     bg=COLORES["superficie"], fg=COLORES["texto_suave"],
                     font=FUENTES["micro"], width=8, anchor="w").pack(side="left")
            tk.Label(fila_escala, text=letra, bg=COLORES["superficie"], fg=color,
                     font=FUENTES["pequena_bold"], width=3,
                     anchor="w").pack(side="left")
            tk.Label(fila_escala, text=comentario, bg=COLORES["superficie"],
                     fg=color, font=FUENTES["micro"], anchor="w").pack(side="left")
            desde = limite + 1

        # ----------------------------- Botonera ------------------------------
        botonera = tk.Frame(panel, bg=COLORES["superficie"])
        botonera.pack(side="bottom", fill="x", padx=14, pady=(4, 8))

        BotonModerno(botonera, "CALCULAR PROMEDIO", self.calcular,
                     ancho=320, alto=42, color=COLORES["celeste"],
                     color_hover=COLORES["celeste_hover"]).pack(pady=(0, 6))

        fila = tk.Frame(botonera, bg=COLORES["superficie"])
        fila.pack(fill="x")
        BotonModerno(fila, "GUARDAR", self.guardar_en_historial,
                     ancho=155, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila, "LIMPIAR", self.limpiar,
                     ancho=155, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["celeste"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"]).pack(side="right")

        # ============================ PANEL DERECHO ==========================
        derecha = tk.Frame(contenedor, bg=COLORES["fondo"])
        derecha.pack(side="left", fill="both", expand=True, padx=(18, 0))

        # ------------------------ Tarjetas de resultado ----------------------
        tarjetas = tk.Frame(derecha, bg=COLORES["fondo"])
        tarjetas.pack(fill="x")

        self.tarjeta_promedio = TarjetaIndicador(tarjetas, "🎯", "Promedio", "0.00",
                                                 COLORES["celeste"], ancho=160, alto=96)
        self.tarjeta_promedio.pack(side="left", padx=(0, 10))

        self.tarjeta_mayor = TarjetaIndicador(tarjetas, "🔼", "Nota mayor", "0.00",
                                              COLORES["exito"], ancho=160, alto=96)
        self.tarjeta_mayor.pack(side="left", padx=(0, 10))

        self.tarjeta_menor = TarjetaIndicador(tarjetas, "🔽", "Nota menor", "0.00",
                                              COLORES["error"], ancho=160, alto=96)
        self.tarjeta_menor.pack(side="left", padx=(0, 10))

        self.tarjeta_cantidad = TarjetaIndicador(tarjetas, "#️⃣", "Cantidad", "0",
                                                 COLORES["cian"], ancho=160, alto=96)
        self.tarjeta_cantidad.pack(side="left")

        # ------------------------- Franja de veredicto -----------------------
        self.franja_estado = tk.Frame(derecha, bg=COLORES["fondo_alt"], height=54,
                                      highlightthickness=1,
                                      highlightbackground=COLORES["borde"])
        self.franja_estado.pack(fill="x", pady=8)
        self.franja_estado.pack_propagate(False)

        self.etiqueta_estado = tk.Label(
            self.franja_estado, text="⌛  Ingrese sus notas y presione CALCULAR PROMEDIO",
            bg=COLORES["fondo_alt"], fg=COLORES["texto_suave"], font=FUENTES["texto_bold"],
        )
        self.etiqueta_estado.pack(expand=True)

        # ---------- Dos tablas lado a lado: analisis actual e historial ------
        zona_tablas = tk.Frame(derecha, bg=COLORES["fondo"])
        zona_tablas.pack(fill="both", expand=True)

        # Izquierda: lista ordenada del calculo recien realizado.
        columna_izquierda = tk.Frame(zona_tablas, bg=COLORES["fondo"])
        columna_izquierda.pack(side="left", fill="both", expand=True)

        crear_titulo_seccion(columna_izquierda, "📑", "Lista ordenada de notas",
                             "De la calificacion mas alta a la mas baja").pack(anchor="w",
                                                                                pady=(0, 6))

        contenedor_tabla, self.tabla_notas = crear_tabla(
            columna_izquierda,
            columnas=["Pos", "Nota", "Letra", "Resultado"],
            anchos=[40, 52, 60, 166],
            alineaciones=["center", "center", "center", "center"],
            altura=7,
        )
        contenedor_tabla.pack(fill="both", expand=True)

        # Derecha: promedios ya guardados en notas.json.
        columna_derecha = tk.Frame(zona_tablas, bg=COLORES["fondo"])
        columna_derecha.pack(side="left", fill="both", expand=True, padx=(14, 0))

        crear_titulo_seccion(columna_derecha, "🗂", "Promedios guardados",
                             "Quedan guardados en notas.json").pack(anchor="w", pady=(0, 6))

        contenedor_historial, self.tabla_historial = crear_tabla(
            columna_derecha,
            columnas=["Materia", "Prom.", "Letra", "Estado"],
            anchos=[112, 58, 60, 84],
            alineaciones=["w", "w", "center", "center"],
            altura=7,
            columna_elastica=0,
        )
        contenedor_historial.pack(fill="both", expand=True)
        self.tabla_historial.bind("<Double-1>", lambda evento=None: self.eliminar_del_historial())

    # ------------------------------------------------------------- acciones --
    def _calcular_con_enter(self, _evento=None):
        """Permite calcular presionando Enter dentro de la caja de notas."""
        self.calcular()
        return "break"                            # Evita el salto de linea

    def obtener_texto_notas(self):
        """Devuelve el contenido actual de la caja de texto."""
        return self.texto_notas.get("1.0", "end").strip()

    @manejar_errores
    def calcular(self):
        """
        Valida las notas ingresadas y muestra el analisis completo.

        Calcula promedio, mayor, menor, cantidad y determina si el estudiante
        aprueba (verde) o reprueba (rojo).
        """
        valido, resultado = validar_lista_de_notas(self.obtener_texto_notas())
        if not valido:
            self.advertir("Notas invalidas", resultado)
            self.texto_notas.focus_set()
            return

        notas = resultado
        promedio = promedio_de(notas)
        mayor = max(notas)
        menor = min(notas)
        cantidad = len(notas)
        letra, aprueba, comentario = evaluar_nota(promedio)

        self.notas_calculadas = notas
        self.promedio_calculado = promedio
        self.letra_calculada = letra

        # --------------------------- Tarjetas KPI ----------------------------
        color_promedio = COLORES["exito"] if aprueba else COLORES["error"]
        self.tarjeta_promedio.actualizar("%s   %s" % (formato_numero(promedio), letra),
                                         color_promedio)
        self.tarjeta_mayor.actualizar("%s   %s" % (formato_numero(mayor),
                                                   evaluar_nota(mayor)[0]),
                                      COLORES["exito"])
        self.tarjeta_menor.actualizar("%s   %s" % (formato_numero(menor),
                                                   evaluar_nota(menor)[0]),
                                      COLORES["error"])
        self.tarjeta_cantidad.actualizar(str(cantidad), COLORES["cian"])

        # ------------------------- Franja de veredicto -----------------------
        if aprueba:
            matiz = "" if comentario == "Aprobado" else "   |   %s" % comentario
            mensaje = ("APROBADO   |   Promedio %s   |   Calificacion %s%s"
                       % (formato_numero(promedio), letra, matiz))
            self.pintar_estado(mensaje, COLORES["exito"])
        else:
            mensaje = ("REPROBADO   |   Promedio %s   |   Calificacion %s   |   "
                       "Le faltan %s puntos para superar %s y llegar a C"
                       % (formato_numero(promedio), letra,
                          formato_numero(NOTA_APROBACION - promedio),
                          formato_numero(NOTA_APROBACION)))
            self.pintar_estado(mensaje, COLORES["error"])

        # ------------------------ Tabla de notas ordenadas -------------------
        ordenadas = sorted(notas, reverse=True)
        filas = []
        for posicion, nota in enumerate(ordenadas, start=1):
            letra_nota, nota_aprueba, comentario_nota = evaluar_nota(nota)
            etiqueta = "exito" if nota_aprueba else "error"
            filas.append((posicion, (posicion, formato_numero(nota), letra_nota,
                                     comentario_nota), etiqueta))
        llenar_tabla(self.tabla_notas, filas)

        self.actualizar_mensaje(
            "🧮 Calculo realizado sobre %d nota%s" % (cantidad, "" if cantidad == 1 else "s"),
            COLORES["azul_claro"]
        )

    def pintar_estado(self, mensaje, color):
        """Aplica el color del veredicto a la franja de resultado."""
        self.franja_estado.configure(highlightbackground=color)
        self.etiqueta_estado.configure(text=mensaje, fg=color)

    @manejar_errores
    def guardar_en_historial(self):
        """Guarda el promedio calculado dentro de notas.json."""
        if not self.notas_calculadas:
            self.advertir("Sin calculo",
                          "Primero debe calcular un promedio con el boton CALCULAR PROMEDIO.")
            return

        materia = self.campo_materia.obtener()
        if not materia:
            if not self.confirmar(
                "Materia no seleccionada",
                "No selecciono ninguna materia.\n\n"
                "El promedio se guardara como 'General'. Desea continuar?"
            ):
                return
            materia = "General"

        # Si ya existe un registro de la misma materia se ofrece reemplazarlo.
        existente = None
        for registro in DATOS.notas:
            if str(registro.get("materia", "")).lower() == materia.lower():
                existente = registro
                break

        if existente is not None:
            if not self.confirmar(
                "Registro existente",
                "Ya existe un promedio guardado para '%s' (%s).\n\nDesea reemplazarlo?"
                % (materia, formato_numero(existente.get("promedio", 0)))
            ):
                return
            DATOS.notas.remove(existente)

        DATOS.notas.append({
            "id": DATOS.nuevo_id(DATOS.notas),
            "materia": materia,
            "notas": self.notas_calculadas,
            "promedio": round(self.promedio_calculado, 2),
            "letra": self.letra_calculada,
            "estado": "Aprobado" if evaluar_nota(self.promedio_calculado)[1] else "Reprobado",
            "fecha": datetime.date.today().strftime("%d/%m/%Y"),
        })
        DATOS.guardar_notas()

        self.refrescar_historial()
        self.actualizar_mensaje("💾 Promedio de '%s' guardado" % materia, COLORES["exito"])
        self.informar("Promedio guardado",
                      "El promedio de '%s' fue guardado correctamente.\n\n"
                      "Promedio: %s     Calificacion: %s"
                      % (materia, formato_numero(self.promedio_calculado),
                         self.letra_calculada))

    @manejar_errores
    def eliminar_del_historial(self):
        """Elimina un promedio guardado (doble clic sobre la fila)."""
        identificador = obtener_id_seleccionado(self.tabla_historial)
        if identificador is None:
            return
        registro = DATOS.buscar_por_id(DATOS.notas, identificador)
        if registro is None:
            return
        if not self.confirmar("Eliminar promedio",
                              "Desea eliminar el promedio guardado de '%s'?"
                              % registro.get("materia", "")):
            return
        DATOS.eliminar_por_id(DATOS.notas, identificador)
        DATOS.guardar_notas()
        self.refrescar_historial()
        self.actualizar_mensaje("🗑 Promedio eliminado del historial", COLORES["error"])

    def refrescar_historial(self):
        """Vuelve a dibujar la tabla de promedios guardados."""
        registros = sorted(DATOS.notas,
                           key=lambda r: float(r.get("promedio", 0)), reverse=True)
        filas = []
        for registro in registros:
            nombre_materia = registro.get("materia", "")
            if len(nombre_materia) > 15:
                nombre_materia = nombre_materia[:14] + "..."
            promedio = float(registro.get("promedio", 0))
            letra, aprobado, _comentario = evaluar_nota(promedio)
            filas.append((
                registro.get("id"),
                (
                    nombre_materia,
                    formato_numero(promedio),
                    letra,
                    "Aprobado" if aprobado else "Reprobado",
                ),
                "exito" if aprobado else "error",
            ))
        llenar_tabla(self.tabla_historial, filas)

    @manejar_errores
    def limpiar(self):
        """Restablece la calculadora a su estado inicial."""
        self.texto_notas.delete("1.0", "end")
        self.campo_materia.limpiar()
        self.notas_calculadas = []
        self.promedio_calculado = 0.0
        self.letra_calculada = ""

        self.tarjeta_promedio.actualizar("0.00", COLORES["texto"])
        self.tarjeta_mayor.actualizar("0.00", COLORES["texto"])
        self.tarjeta_menor.actualizar("0.00", COLORES["texto"])
        self.tarjeta_cantidad.actualizar("0", COLORES["texto"])

        self.franja_estado.configure(highlightbackground=COLORES["borde"])
        self.etiqueta_estado.configure(
            text="⌛  Ingrese sus notas y presione CALCULAR PROMEDIO",
            fg=COLORES["texto_suave"],
        )
        llenar_tabla(self.tabla_notas, [])
        self.texto_notas.focus_set()
        self.actualizar_mensaje("🧹 Calculadora reiniciada", COLORES["texto_suave"])


# =============================================================================
# SECCION 13 : MODULO 4 - INFORMACION DEL SISTEMA
# =============================================================================

def mostrar_informacion(ventana_padre):
    """
    Muestra el cuadro de dialogo institucional del proyecto (Modulo 4).

    Cumple el requisito de presentar un MessageBox con los datos del software,
    los autores, la universidad y la tecnologia utilizada.
    """
    detalle = (
        "%s\n"
        "Version %s\n"
        "%s\n\n"
        "Pontificia Universidad Catolica del Ecuador\n\n"
        "DESARROLLADO POR:\n"
        "   •  Steveen Culquicondor\n"
        "   •  Angel Nunez\n"
        "   •  Ricardo Garrido\n\n"
        "CATEDRA:\n"
        "   Fundamentos de Programacion\n\n"
        "TECNOLOGIA:\n"
        "   Desarrollado con Python y Tkinter\n"
        "   Python %s\n\n"
        "MODULOS DEL SISTEMA:\n"
        "   1. Registro de Materias\n"
        "   2. Horario Semanal\n"
        "   3. Calculadora de Promedios\n"
        "   4. Informacion del Sistema\n\n"
        "ALMACENAMIENTO:\n"
        "   materias.json  ·  horario.json  ·  notas.json\n\n"
        "REGISTROS ACTUALES:\n"
        "   Materias: %d   |   Bloques de horario: %d\n"
        "   Promedios guardados: %d"
        % (APP_NOMBRE, APP_VERSION, APP_SUBTITULO,
           sys.version.split()[0],
           len(DATOS.materias), len(DATOS.horario), len(DATOS.notas))
    )
    messagebox.showinfo("Informacion del Sistema", detalle, parent=ventana_padre)


# =============================================================================
# SECCION 14 : VENTANA PRINCIPAL (MENU DEL SISTEMA)
# =============================================================================
# Pantalla de inicio del sistema. Contiene el encabezado institucional,
# el titulo del sistema y las ocho tarjetas que abren cada modulo mediante
# ventanas Toplevel independientes.
# =============================================================================

class AplicacionStudyControl:
    """Controlador principal: construye el menu y coordina todos los modulos."""

    def __init__(self, raiz):
        self.raiz = raiz

        # ------------------------- Configuracion base ------------------------
        self.raiz.title("%s  ·  %s" % (APP_NOMBRE, APP_SUBTITULO))
        self.raiz.configure(bg=COLORES["fondo"])
        self.raiz.resizable(False, False)             # Tamano fijo 1100x700
        centrar_ventana(self.raiz, VENTANA_ANCHO, VENTANA_ALTO)
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)

        # Atajos de teclado del menu principal.
        self.raiz.bind("<F1>", lambda evento=None: self.abrir_informacion())
        self.raiz.bind("<Escape>", lambda evento=None: self.salir())

        # ------------------------ Construccion visual ------------------------
        self.construir_encabezado()
        self.construir_menu()
        self.construir_pie()
        self.actualizar_resumen()

    # =========================================================================
    # ENCABEZADO
    # =========================================================================
    def construir_encabezado(self):
        """
        Construye la cabecera institucional y el bloque de titulo.

        Incluye el espacio para el logo de la PUCE (esquina superior izquierda),
        el nombre de la universidad, el titulo grande del sistema, el subtitulo,
        los autores y la catedra.
        """
        # ---------------- Barra superior institucional (sin reloj) -----------
        crear_barra_institucional(self.raiz).pack(fill="x")

        # Linea degradada simulada con tres franjas de color.
        franja = tk.Frame(self.raiz, bg=COLORES["fondo"], height=4)
        franja.pack(fill="x")
        franja.pack_propagate(False)
        tk.Frame(franja, bg=COLORES["celeste_oscuro"]).place(relx=0.0, relwidth=0.34, relheight=1)
        tk.Frame(franja, bg=COLORES["celeste"]).place(relx=0.34, relwidth=0.33, relheight=1)
        tk.Frame(franja, bg=COLORES["cian"]).place(relx=0.67, relwidth=0.33, relheight=1)

        # ------------------------- Bloque de titulo --------------------------
        hero = tk.Frame(self.raiz, bg=COLORES["fondo_alt"], height=168)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        contenido = tk.Frame(hero, bg=COLORES["fondo_alt"])
        contenido.pack(expand=True)

        # Titulo principal, grande y centrado, sin ningun icono.
        tk.Label(contenido, text="SISTEMA DE ESTUDIO", bg=COLORES["fondo_alt"],
                 fg=COLORES["blanco"], font=FUENTES["titulo_gigante"]).pack()

        # Subtitulo descriptivo del sistema.
        tk.Label(contenido, text=APP_SUBTITULO, bg=COLORES["fondo_alt"],
                 fg=COLORES["celeste_claro"], font=FUENTES["subtitulo"]).pack(pady=(4, 0))

        # Separador decorativo entre el subtitulo y los autores.
        separador = tk.Frame(contenido, bg=COLORES["fondo_alt"])
        separador.pack(pady=8)
        tk.Frame(separador, bg=COLORES["borde"], width=110, height=1).pack(side="left", pady=6)
        tk.Label(separador, text="◆", bg=COLORES["fondo_alt"], fg=COLORES["cian"],
                 font=FUENTES["micro"]).pack(side="left", padx=8)
        tk.Frame(separador, bg=COLORES["borde"], width=110, height=1).pack(side="left", pady=6)

        # Autores y catedra.
        tk.Label(contenido, text=APP_AUTORES, bg=COLORES["fondo_alt"],
                 fg=COLORES["texto"], font=FUENTES["etiqueta_bold"]).pack()
        tk.Label(contenido, text=APP_CATEDRA, bg=COLORES["fondo_alt"],
                 fg=COLORES["texto_sobre_gris"], font=FUENTES["pequena"]).pack(pady=(2, 0))

    # =========================================================================
    # MENU PRINCIPAL
    # =========================================================================
    def definicion_de_modulos(self):
        """
        Devuelve la definicion de los cuatro modulos del menu principal.

        Cada elemento contiene: icono, titulo, descripcion, comando y color.
        Tener la definicion en un solo lugar evita repetir codigo al crear
        las tarjetas y facilita agregar nuevos modulos en el futuro.
        """
        return [
            ("📚", "Registro de Materias", "Asignaturas, docentes y aulas",
             self.abrir_materias, COLORES["celeste"]),
            ("📅", "Horario", "Bloques de clase semanales",
             self.abrir_horario, COLORES["celeste_claro"]),
            ("📊", "Calculadora de Promedios", "Analisis de sus calificaciones",
             self.abrir_promedios, COLORES["azul_claro"]),
            ("👤", "Informacion", "Datos del proyecto y autores",
             self.abrir_informacion, COLORES["celeste_hover"]),
        ]

    def construir_menu(self):
        """Dibuja las cuatro tarjetas del menu y el boton de salida."""
        contenedor = tk.Frame(self.raiz, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True, padx=26, pady=18)

        # Titulo pequeno de la seccion del menu.
        cabecera = tk.Frame(contenedor, bg=COLORES["fondo"])
        cabecera.pack(fill="x", pady=(0, 12))
        tk.Label(cabecera, text="MENU PRINCIPAL", bg=COLORES["fondo"],
                 fg=COLORES["texto"], font=FUENTES["pequena_bold"]).pack(side="left")
        tk.Label(cabecera, text="Seleccione un modulo para comenzar",
                 bg=COLORES["fondo"], fg=COLORES["texto_sobre_gris"],
                 font=FUENTES["pequena"]).pack(side="left", padx=(12, 0))
        tk.Label(cabecera, text="F1: Informacion    ·    Esc: Salir",
                 bg=COLORES["fondo"], fg=COLORES["texto_sobre_gris"],
                 font=FUENTES["micro"]).pack(side="right")

        rejilla = tk.Frame(contenedor, bg=COLORES["fondo"])
        rejilla.pack(fill="both", expand=True)

        # Los cuatro modulos ocupan una sola fila de columnas iguales.
        for columna in range(4):
            rejilla.grid_columnconfigure(columna, weight=1, uniform="columna")
        rejilla.grid_rowconfigure(0, weight=1)

        for indice, (icono, titulo, descripcion, comando, color) in \
                enumerate(self.definicion_de_modulos()):
            tarjeta = TarjetaMenu(rejilla, icono, titulo, descripcion, comando, color)
            tarjeta.grid(row=0, column=indice, sticky="nsew", padx=7, pady=7)

        # Boton de salida, separado de los modulos porque no abre ninguna ventana.
        zona_salida = tk.Frame(contenedor, bg=COLORES["fondo"])
        zona_salida.pack(fill="x", pady=(14, 0))
        BotonModerno(zona_salida, "SALIR DEL SISTEMA", self.salir,
                     ancho=230, alto=42, color=COLORES["error"],
                     color_hover=COLORES["error_hover"]).pack()

    # =========================================================================
    # PIE DE PAGINA
    # =========================================================================
    def construir_pie(self):
        """Barra inferior con el resumen de registros y la version."""
        pie = tk.Frame(self.raiz, bg=COLORES["negro"], height=44)
        pie.pack(fill="x", side="bottom")
        pie.pack_propagate(False)

        self.etiqueta_resumen = tk.Label(
            pie, text="", bg=COLORES["negro"], fg=COLORES["texto_suave"],
            font=FUENTES["pequena"],
        )
        self.etiqueta_resumen.pack(side="left", padx=22)

        tk.Label(pie, text="© 2026  PUCE  ·  Fundamentos de Programacion  ·  v%s" % APP_VERSION,
                 bg=COLORES["negro"], fg=COLORES["texto_tenue"],
                 font=FUENTES["micro"]).pack(side="right", padx=22)

    def actualizar_resumen(self):
        """
        Refresca el contador de registros del pie de pagina.

        Se llama al iniciar y cada vez que se regresa de un modulo, de modo
        que el menu siempre muestra informacion actualizada.
        """
        try:
            promedios = [float(n.get("promedio", 0)) for n in DATOS.notas]
            texto_promedio = (formato_numero(promedio_de(promedios)) if promedios else "--")

            self.etiqueta_resumen.configure(
                text="Materias registradas: %d       Bloques de horario: %d       "
                     "Promedio general: %s"
                     % (len(DATOS.materias), len(DATOS.horario), texto_promedio)
            )
        except tk.TclError as error:
            print("[Sistema de Estudio] No se pudo refrescar el resumen: %s" % error)

    # =========================================================================
    # APERTURA DE MODULOS
    # =========================================================================
    def abrir_ventana(self, clase_ventana):
        """
        Abre un modulo protegiendo la aplicacion ante cualquier fallo.

        Si la creacion de la ventana falla, se restaura el menu principal y se
        informa al usuario sin cerrar el programa.
        """
        try:
            clase_ventana(self)
        except Exception as error:
            traceback.print_exc()
            self.raiz.deiconify()
            messagebox.showerror(
                "Error al abrir el modulo",
                "No fue posible abrir el modulo solicitado.\n\nDetalle: %s" % error
            )

    @manejar_errores
    def abrir_materias(self):
        """Modulo 1: Registro de Materias."""
        self.abrir_ventana(VentanaMaterias)

    @manejar_errores
    def abrir_horario(self):
        """Modulo 2: Horario Semanal."""
        self.abrir_ventana(VentanaHorario)

    @manejar_errores
    def abrir_promedios(self):
        """Modulo 3: Calculadora de Promedios."""
        self.abrir_ventana(VentanaPromedios)

    @manejar_errores
    def abrir_informacion(self):
        """Modulo 4: Informacion del sistema (MessageBox institucional)."""
        mostrar_informacion(self.raiz)

    # =========================================================================
    # SALIDA DEL SISTEMA
    # =========================================================================
    @manejar_errores
    def salir(self):
        """
        Cierra la aplicacion solicitando confirmacion al usuario.

        Antes de cerrar guarda toda la informacion en los archivos JSON para
        que no se pierda ningun cambio.
        """
        if not messagebox.askyesno(
            "Confirmar salida",
            "Desea salir de %s?\n\n"
            "Toda la informacion registrada quedara guardada en los archivos JSON."
            % APP_NOMBRE,
            parent=self.raiz,
        ):
            return

        DATOS.guardar_todo()
        self.raiz.quit()
        self.raiz.destroy()


# =============================================================================
# SECCION 15 : PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================================

def crear_archivos_si_no_existen():
    """
    Garantiza que los tres archivos JSON existan desde el primer arranque.

    Si no existen se crean vacios, de modo que el usuario pueda verlos en la
    carpeta del proyecto y el programa nunca falle al intentar leerlos.
    """
    for ruta in (ARCHIVO_MATERIAS, ARCHIVO_HORARIO, ARCHIVO_NOTAS):
        if not os.path.exists(ruta):
            escribir_json(ruta, [])


def main():
    """
    Funcion principal: prepara el entorno grafico e inicia el bucle de eventos.

    Pasos:
        1. Crear la ventana raiz de Tkinter.
        2. Configurar tipografias y estilos ttk.
        3. Cargar automaticamente la informacion de los archivos JSON.
        4. Construir el menu principal y ejecutar la aplicacion.
    """
    raiz = tk.Tk()
    raiz.withdraw()                               # Se oculta mientras se construye

    # 1) Tipografias y estilos (requieren una ventana raiz activa).
    configurar_fuentes()
    aplicar_estilos()

    # 2) Carga automatica de la informacion guardada.
    crear_archivos_si_no_existen()
    DATOS.cargar_todo()

    # 3) Construccion de la interfaz principal.
    aplicacion = AplicacionStudyControl(raiz)

    # 4) Se muestra la ventana ya terminada (evita parpadeos al iniciar).
    raiz.deiconify()
    raiz.lift()

    print("[Sistema de Estudio] Aplicacion iniciada correctamente.")
    print("[Sistema de Estudio] Registros cargados -> materias: %d | "
          "horario: %d | promedios: %d"
          % (len(DATOS.materias), len(DATOS.horario), len(DATOS.notas)))

    # 5) Bucle principal protegido: ningun error cierra la aplicacion en seco.
    try:
        raiz.mainloop()
    except KeyboardInterrupt:
        print("[Sistema de Estudio] Ejecucion interrumpida por el usuario.")
    finally:
        DATOS.guardar_todo()
        print("[Sistema de Estudio] Informacion guardada. Hasta pronto.")

    return aplicacion


# -----------------------------------------------------------------------------
# Ejecucion directa:  python study_control.py
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as error_general:             # Ultima red de seguridad
        traceback.print_exc()
        try:
            messagebox.showerror(
                "Error critico",
                "El Sistema de Estudio no pudo iniciarse correctamente.\n\n"
                "Detalle: %s" % error_general
            )
        except Exception:
            print("[Sistema de Estudio] Error critico: %s" % error_general)
