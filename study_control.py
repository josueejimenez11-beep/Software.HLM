# -*- coding: utf-8 -*-
"""
===============================================================================
                              S T U D Y   C O N T R O L
===============================================================================
 Sistema Inteligente para la Gestion Academica de Estudiantes
 -----------------------------------------------------------------------------
 Institucion : Pontificia Universidad Catolica del Ecuador
 Autores     : Steveen Culquicondor - Angel Nunez
 Catedra     : Fundamentos de Programacion
 Version     : 1.0
 Tecnologia  : Python 3 + Tkinter + ttk
 -----------------------------------------------------------------------------
 DESCRIPCION GENERAL
 -----------------------------------------------------------------------------
 Study Control es una aplicacion de escritorio disenada para que un estudiante
 universitario administre por completo su vida academica desde un solo lugar:

   Modulo 1 -> Registro de Materias        (materias.json)
   Modulo 2 -> Control de Tareas           (tareas.json)
   Modulo 3 -> Calculadora de Promedios    (notas.json)
   Modulo 4 -> Nota Necesaria              (calculo en tiempo real)
   Modulo 5 -> Horario Semanal             (horario.json)
   Modulo 6 -> Estadisticas Generales      (calculo automatico)
   Modulo 7 -> Informacion del Sistema     (messagebox)

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
APP_NOMBRE = "Study Control"
APP_VERSION = "1.0"
APP_SUBTITULO = "Sistema Inteligente para la Gestion Academica de Estudiantes"
APP_UNIVERSIDAD = "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR"
APP_AUTORES = "STEVEEN CULQUICONDOR  -  ANGEL NUNEZ"
APP_CATEDRA = "FUNDAMENTOS DE PROGRAMACION"

# ------------------------- Dimensiones de ventanas ---------------------------
VENTANA_ANCHO = 1100                        # Ancho solicitado en el requisito
VENTANA_ALTO = 700                          # Alto solicitado en el requisito

# ------------------------------ Paleta oscura --------------------------------
# Estilo moderno: azul muy oscuro / negro con acentos morados y violetas.
COLORES = {
    "fondo":          "#0A0E1A",            # Fondo principal (casi negro azulado)
    "fondo_alt":      "#0F1526",            # Fondo secundario de paneles
    "superficie":     "#151C31",            # Tarjetas y contenedores
    "superficie_alt": "#1C2540",            # Tarjetas resaltadas / hover suave
    "borde":          "#26314F",            # Lineas divisorias y bordes
    "borde_activo":   "#7C3AED",            # Borde cuando un control esta activo
    "morado":         "#7C3AED",            # Acento principal (morado)
    "morado_claro":   "#A78BFA",            # Acento claro (textos destacados)
    "morado_oscuro":  "#5B21B6",            # Acento profundo (sombras)
    "morado_hover":   "#8B5CF6",            # Acento para efecto hover
    "azul":           "#2563EB",            # Azul de apoyo
    "azul_claro":     "#60A5FA",            # Azul claro informativo
    "cian":           "#22D3EE",            # Detalles y separadores
    "texto":          "#EDF0FA",            # Texto principal (blanco frio)
    "texto_suave":    "#98A3C4",            # Texto secundario
    "texto_tenue":    "#5F6B8C",            # Texto muy secundario
    "exito":          "#22C55E",            # Verde (aprobado / completado)
    "exito_hover":    "#16A34A",            # Verde oscuro para hover
    "error":          "#EF4444",            # Rojo (reprobado / eliminar)
    "error_hover":    "#DC2626",            # Rojo oscuro para hover
    "alerta":         "#F59E0B",            # Naranja (advertencias)
    "alerta_hover":   "#D97706",            # Naranja oscuro para hover
    "blanco":         "#FFFFFF",            # Blanco puro
    "negro":          "#05070F",            # Negro de la barra superior
}

# --------------------------- Escala de calificacion --------------------------
NOTA_MINIMA = 0.0                           # Nota mas baja posible
NOTA_MAXIMA = 20.0                          # Nota mas alta posible (escala /20)
NOTA_APROBACION = 14.0                      # Nota minima para aprobar la materia

# ------------------------------ Archivos JSON --------------------------------
# Se guardan en la misma carpeta del script para que el proyecto sea portable.
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MATERIAS = os.path.join(CARPETA_BASE, "materias.json")
ARCHIVO_TAREAS = os.path.join(CARPETA_BASE, "tareas.json")
ARCHIVO_HORARIO = os.path.join(CARPETA_BASE, "horario.json")
ARCHIVO_NOTAS = os.path.join(CARPETA_BASE, "notas.json")

# ------------------- Nombres posibles del logo institucional -----------------
# El usuario puede colocar cualquiera de estos archivos PNG junto al script y
# la aplicacion lo cargara automaticamente en el encabezado.
NOMBRES_LOGO = ("logo_puce.png", "logo.png", "puce.png", "logo_puce.PNG")

# ------------------------------ Listas fijas ---------------------------------
DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
PRIORIDADES = ["Alta", "Media", "Baja"]
ESTADOS_TAREA = ["Pendiente", "En proceso", "Completada"]

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
        print("[Study Control] No se pudo leer '%s': %s" % (ruta, error))
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
        print("[Study Control] No se pudo escribir '%s': %s" % (ruta, error))
        messagebox.showerror(
            "Error de guardado",
            "No fue posible guardar la informacion en el archivo:\n\n%s\n\nDetalle: %s"
            % (os.path.basename(ruta), error)
        )
        return False


class BaseDeDatos:
    """
    Repositorio central de informacion de Study Control.

    Mantiene en memoria las cuatro colecciones del sistema (materias, tareas,
    horario y notas) y sincroniza cada cambio con su archivo JSON. Todos los
    modulos trabajan sobre esta misma instancia, por lo que la informacion
    siempre esta actualizada en cualquier ventana.
    """

    def __init__(self):
        # Colecciones en memoria (se llenan al llamar cargar_todo()).
        self.materias = []
        self.tareas = []
        self.horario = []
        self.notas = []

    # ------------------------------------------------------------------ carga
    def cargar_todo(self):
        """Carga automaticamente los cuatro archivos JSON al iniciar."""
        self.materias = leer_json(ARCHIVO_MATERIAS)
        self.tareas = leer_json(ARCHIVO_TAREAS)
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
        for coleccion in (self.materias, self.tareas, self.horario, self.notas):
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

    def guardar_tareas(self):
        """Escritura automatica de tareas.json."""
        return escribir_json(ARCHIVO_TAREAS, self.tareas)

    def guardar_horario(self):
        """Escritura automatica de horario.json."""
        return escribir_json(ARCHIVO_HORARIO, self.horario)

    def guardar_notas(self):
        """Escritura automatica de notas.json."""
        return escribir_json(ARCHIVO_NOTAS, self.notas)

    def guardar_todo(self):
        """Guarda las cuatro colecciones (usado al cerrar la aplicacion)."""
        self.guardar_materias()
        self.guardar_tareas()
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

    def nombres_de_materias(self):
        """
        Lista ordenada con los nombres de las materias registradas.

        Se usa para llenar los combobox de tareas, horario y promedios,
        evitando que el usuario escriba el nombre de la materia a mano.
        """
        nombres = sorted({str(m.get("materia", "")).strip()
                          for m in self.materias if str(m.get("materia", "")).strip()})
        return nombres


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


def validar_fecha(valor, nombre_campo):
    """
    Valida una fecha en formato DD/MM/AAAA usando el modulo datetime.

    Acepta separadores '/', '-' y '.' para que el usuario escriba con comodidad.
    """
    texto = str(valor).strip().replace("-", "/").replace(".", "/")
    if not texto:
        return False, "El campo '%s' no puede estar vacio." % nombre_campo
    partes = texto.split("/")
    if len(partes) != 3:
        return False, "El campo '%s' debe tener el formato DD/MM/AAAA." % nombre_campo
    if not all(parte.isdigit() for parte in partes):
        return False, "El campo '%s' solo acepta numeros en formato DD/MM/AAAA." % nombre_campo
    dia, mes, anio = int(partes[0]), int(partes[1]), int(partes[2])
    if anio < 100:                                # Permite escribir 26 en vez de 2026
        anio += 2000
    try:
        fecha = datetime.date(anio, mes, dia)
    except ValueError:
        return False, "La fecha ingresada en '%s' no existe en el calendario." % nombre_campo
    return True, fecha.strftime("%d/%m/%Y")


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


def fecha_a_ordenable(fecha):
    """
    Convierte 'DD/MM/AAAA' en 'AAAAMMDD' (entero) para poder ordenar fechas.

    Si la fecha no es valida devuelve 0 para que aparezca al final.
    """
    try:
        dia, mes, anio = str(fecha).split("/")
        return int(anio) * 10000 + int(mes) * 100 + int(dia)
    except (ValueError, AttributeError):
        return 0


def dias_restantes(fecha):
    """
    Calcula cuantos dias faltan para una fecha 'DD/MM/AAAA'.

    Devuelve None si la fecha no se puede interpretar.
    """
    try:
        dia, mes, anio = [int(p) for p in str(fecha).split("/")]
        objetivo = datetime.date(anio, mes, dia)
        return (objetivo - datetime.date.today()).days
    except (ValueError, AttributeError):
        return None


def texto_dias_restantes(fecha):
    """Describe en palabras cuanto tiempo falta para la fecha de una tarea."""
    faltan = dias_restantes(fecha)
    if faltan is None:
        return "Sin fecha"
    if faltan < 0:
        return "Vencida (%d d)" % abs(faltan)
    if faltan == 0:
        return "Vence HOY"
    if faltan == 1:
        return "Manana"
    return "En %d dias" % faltan


def promedio_de(lista_numeros):
    """Calcula el promedio aritmetico protegiendo contra divisiones por cero."""
    if not lista_numeros:
        return 0.0
    return sum(lista_numeros) / float(len(lista_numeros))


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
        print("[Study Control] Se omitio la %s: %s" % (descripcion, error))
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
        insertcolor=COLORES["morado_claro"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        borderwidth=1,
        relief="flat",
        padding=4,
    )
    estilo.map(
        "Study.TEntry",
        bordercolor=[("focus", COLORES["morado"])],
        lightcolor=[("focus", COLORES["morado"])],
        darkcolor=[("focus", COLORES["morado"])],
        fieldbackground=[("focus", COLORES["superficie_alt"])],
    )

    # ------------------------------ Combobox ---------------------------------
    estilo.configure(
        "Study.TCombobox",
        fieldbackground=COLORES["superficie_alt"],
        background=COLORES["superficie_alt"],
        foreground=COLORES["texto"],
        arrowcolor=COLORES["morado_claro"],
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
        bordercolor=[("focus", COLORES["morado"]), ("hover", COLORES["morado_claro"])],
        arrowcolor=[("hover", COLORES["morado"])],
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
        background=COLORES["morado_oscuro"],
        foreground=COLORES["blanco"],
        relief="flat",
        borderwidth=0,
        padding=(6, 10),
        font=("TkDefaultFont", 10, "bold"),
    )
    estilo.map(
        "Study.Treeview.Heading",
        background=[("active", COLORES["morado"])],
    )
    estilo.map(
        "Study.Treeview",
        background=[("selected", COLORES["morado"])],
        foreground=[("selected", COLORES["blanco"])],
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
        arrowcolor=COLORES["morado_claro"],
        borderwidth=0,
        width=12,
    )
    estilo.map(
        "Study.Vertical.TScrollbar",
        background=[("active", COLORES["morado"])],
    )
    estilo.configure(
        "Study.Horizontal.TScrollbar",
        background=COLORES["superficie_alt"],
        troughcolor=COLORES["fondo_alt"],
        bordercolor=COLORES["fondo_alt"],
        arrowcolor=COLORES["morado_claro"],
        borderwidth=0,
    )
    estilo.map(
        "Study.Horizontal.TScrollbar",
        background=[("active", COLORES["morado"])],
    )

    # ----------------------------- Barra de progreso -------------------------
    estilo.configure(
        "Study.Horizontal.TProgressbar",
        troughcolor=COLORES["fondo_alt"],
        bordercolor=COLORES["fondo_alt"],
        background=COLORES["morado"],
        lightcolor=COLORES["morado_claro"],
        darkcolor=COLORES["morado_oscuro"],
        thickness=14,
    )

    # ------------------------------ Separadores ------------------------------
    estilo.configure("Study.TSeparator", background=COLORES["borde"])

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
        color = color or COLORES["morado"]
        color_hover = color_hover or COLORES["morado_hover"]
        color_texto = color_texto or COLORES["blanco"]
        borde = borde or color

        super().__init__(padre, bg=color, width=ancho, height=alto,
                         highlightthickness=1, highlightbackground=borde,
                         highlightcolor=borde, cursor="hand2")
        self.pack_propagate(False)              # Respeta el ancho/alto fijados

        # Guardamos los colores para poder alternarlos en el hover.
        self.color_normal = color
        self.color_hover = color_hover
        self.borde_normal = borde
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
        self.configure(bg=self.color_hover, highlightbackground=COLORES["morado_claro"])
        self.etiqueta.configure(bg=self.color_hover)

    def _al_salir(self, _evento=None):
        """Devuelve el boton a su color original."""
        if not self.habilitado:
            return
        self.configure(bg=self.color_normal, highlightbackground=self.borde_normal)
        self.etiqueta.configure(bg=self.color_normal)

    def _al_presionar(self, _evento=None):
        """Retroalimentacion visual al hacer clic (oscurece ligeramente)."""
        if not self.habilitado:
            return
        self.configure(bg=self.color_normal)
        self.etiqueta.configure(bg=self.color_normal)

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
        self.cuerpo.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        self.icono = tk.Label(self.cuerpo, text=icono, bg=COLORES["superficie"],
                              fg=color_acento, font=FUENTES["icono_medio"])
        self.icono.pack(anchor="w")

        self.titulo = tk.Label(self.cuerpo, text=titulo, bg=COLORES["superficie"],
                               fg=COLORES["texto"], font=FUENTES["texto_bold"],
                               anchor="w", justify="left", wraplength=210)
        self.titulo.pack(anchor="w", pady=(4, 0))

        self.descripcion = tk.Label(self.cuerpo, text=descripcion,
                                    bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                                    font=FUENTES["pequena"], anchor="w", justify="left",
                                    wraplength=210)
        self.descripcion.pack(anchor="w")

        # Todos los hijos deben reaccionar al mouse para que el hover sea fluido.
        self._widgets = [self, self.cuerpo, self.icono, self.titulo, self.descripcion]
        for widget in self._widgets:
            widget.bind("<Enter>", self._al_entrar)
            widget.bind("<Leave>", self._al_salir)
            widget.bind("<Button-1>", self._al_hacer_clic)
            widget.configure(cursor="hand2")

    def _pintar(self, color_fondo, color_titulo, color_borde, ancho_franja):
        """Aplica un juego de colores a toda la tarjeta (uso interno)."""
        self.configure(bg=color_fondo, highlightbackground=color_borde)
        self.cuerpo.configure(bg=color_fondo)
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

    Se usa en el modulo de Estadisticas y en los resultados de la calculadora:
    icono + valor grande + descripcion corta.
    """

    def __init__(self, padre, icono, titulo, valor="0", color=None, ancho=190, alto=110):
        color = color or COLORES["morado_claro"]
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

    tk.Label(fila, text=icono, bg=COLORES["fondo"], fg=COLORES["morado_claro"],
             font=FUENTES["texto_bold"]).pack(side="left")
    tk.Label(fila, text=texto.upper(), bg=COLORES["fondo"], fg=COLORES["texto"],
             font=FUENTES["seccion"]).pack(side="left", padx=(8, 0))

    if descripcion:
        tk.Label(contenedor, text=descripcion, bg=COLORES["fondo"],
                 fg=COLORES["texto_tenue"], font=FUENTES["pequena"],
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
                     highlightthickness=1, highlightbackground=COLORES["morado_oscuro"])
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
                           outline=COLORES["morado"], width=2)
        lienzo.create_oval(margen + 6, margen + 6, tamano - margen - 6, tamano - margen - 6,
                           outline=COLORES["cian"], width=1)
        lienzo.create_text(tamano / 2, tamano / 2 - 4, text="PUCE",
                           fill=COLORES["blanco"], font=("TkDefaultFont", 11, "bold"))
        lienzo.create_text(tamano / 2, tamano / 2 + 11, text="LOGO",
                           fill=COLORES["texto_tenue"], font=("TkDefaultFont", 6))
    return marco


def crear_barra_institucional(padre, mostrar_reloj=True):
    """
    Barra superior negra comun a TODAS las ventanas del sistema.

    Contiene el espacio del logo, el nombre de la universidad, la catedra y
    un reloj digital en el extremo derecho.
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
    tk.Label(textos, text=APP_CATEDRA, bg=COLORES["negro"], fg=COLORES["morado_claro"],
             font=FUENTES["micro"]).pack(anchor="w")
    tk.Label(textos, text=APP_AUTORES, bg=COLORES["negro"], fg=COLORES["texto_tenue"],
             font=FUENTES["micro"]).pack(anchor="w")

    # ------------------------------ Lado derecho -----------------------------
    derecha = tk.Frame(barra, bg=COLORES["negro"])
    derecha.pack(side="right", fill="y", padx=20)

    etiqueta_reloj = None
    if mostrar_reloj:
        etiqueta_reloj = tk.Label(derecha, text="", bg=COLORES["negro"],
                                  fg=COLORES["cian"], font=FUENTES["mono"])
        etiqueta_reloj.pack(anchor="e", pady=(22, 0))
        tk.Label(derecha, text="SISTEMA ACADEMICO v%s" % APP_VERSION, bg=COLORES["negro"],
                 fg=COLORES["texto_tenue"], font=FUENTES["micro"]).pack(anchor="e")

    return barra, etiqueta_reloj


def iniciar_reloj(ventana, etiqueta):
    """
    Actualiza cada segundo la etiqueta con la fecha y hora del sistema.

    Se protege con try/except porque la ventana puede cerrarse mientras el
    temporizador esta programado.
    """
    def actualizar():
        try:
            if not etiqueta.winfo_exists():
                return
            ahora = datetime.datetime.now()
            etiqueta.configure(text=ahora.strftime("%d/%m/%Y   %H:%M:%S"))
            ventana.after(1000, actualizar)
        except tk.TclError:
            return
    actualizar()


# =============================================================================
# SECCION 9 : VENTANA BASE PARA LOS MODULOS (Toplevel)
# =============================================================================

class VentanaModulo(tk.Toplevel):
    """
    Plantilla comun de todas las ventanas de modulo.

    Garantiza que cada modulo tenga exactamente el mismo diseno:
        - Barra institucional negra con logo y reloj
        - Franja de titulo del modulo con icono y descripcion
        - Area de contenido (self.cuerpo) que llena cada modulo
        - Pie de ventana con el boton REGRESAR al menu principal

    Ademas oculta el menu principal mientras el modulo esta abierto y lo
    vuelve a mostrar al regresar, logrando una navegacion clara.
    """

    def __init__(self, aplicacion, titulo, descripcion, icono="✦", color_acento=None):
        super().__init__(aplicacion.raiz)
        self.aplicacion = aplicacion
        self.color_acento = color_acento or COLORES["morado"]

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
        barra, etiqueta_reloj = crear_barra_institucional(self)
        barra.pack(fill="x")
        if etiqueta_reloj is not None:
            iniciar_reloj(self, etiqueta_reloj)

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
            pie, "REGRESAR AL MENU", self.regresar, icono="⬅",
            ancho=200, alto=38,
            color=COLORES["superficie_alt"], color_hover=COLORES["morado"],
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
# docente, creditos, aula y horario general. Toda la informacion se muestra
# en un Treeview y se guarda automaticamente en materias.json.
# =============================================================================

class VentanaMaterias(VentanaModulo):
    """Modulo 1: administracion completa de las materias del estudiante."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Registro de Materias",
            descripcion="Administre las asignaturas del semestre, sus docentes, creditos y aulas",
            icono="📚",
            color_acento=COLORES["morado"],
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

        tk.Frame(panel_formulario, bg=COLORES["morado"], height=4).pack(fill="x")

        encabezado = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        encabezado.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(encabezado, text="📝 DATOS DE LA MATERIA", bg=COLORES["superficie"],
                 fg=COLORES["texto"], font=FUENTES["seccion"]).pack(anchor="w")
        tk.Label(encabezado, text="Complete todos los campos obligatorios",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"]).pack(anchor="w", pady=(2, 0))

        formulario = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        formulario.pack(fill="x", pady=(6, 0))
        formulario.grid_columnconfigure(0, weight=1)
        formulario.grid_columnconfigure(1, weight=1)

        # --- Campos del formulario (creditos y aula comparten una misma fila) -
        self.campo_materia = CampoFormulario(formulario, "Materia", icono="📘",
                                             fila=0, columnas_ocupadas=2)
        self.campo_docente = CampoFormulario(formulario, "Docente", icono="👨‍🏫",
                                             fila=1, columnas_ocupadas=2)
        self.campo_creditos = CampoFormulario(formulario, "Creditos", icono="🎓",
                                              fila=2, columna=0, ancho=12)
        self.campo_aula = CampoFormulario(formulario, "Aula", icono="🏫",
                                          fila=2, columna=1, ancho=12)
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
        BotonModerno(fila_uno, "GUARDAR", self.guardar_materia, icono="💾",
                     ancho=140, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila_uno, "EDITAR", self.editar_materia, icono="✏",
                     ancho=140, alto=36, color=COLORES["azul"],
                     color_hover=COLORES["azul_claro"]).pack(side="right")

        fila_dos = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_dos.pack(fill="x", pady=3)
        BotonModerno(fila_dos, "ELIMINAR", self.eliminar_materia, icono="🗑",
                     ancho=140, alto=36, color=COLORES["error"],
                     color_hover=COLORES["error_hover"]).pack(side="left")
        BotonModerno(fila_dos, "LIMPIAR", self.limpiar_formulario, icono="🧹",
                     ancho=140, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["morado"], color_texto=COLORES["texto"],
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
            fg=COLORES["morado_claro"], font=FUENTES["texto_bold"],
        )
        self.etiqueta_contador.pack(side="right", pady=6)

        contenedor_tabla, self.tabla = crear_tabla(
            panel_tabla,
            columnas=["#", "Materia", "Docente", "Cr.", "Aula", "Horario"],
            anchos=[36, 172, 148, 42, 68, 150],
            alineaciones=["center", "w", "w", "center", "center", "w"],
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
                    materia.get("creditos", 0),
                    materia.get("aula", ""),
                    materia.get("horario", ""),
                ),
                None,
            ))
        llenar_tabla(self.tabla, filas)

        # ------------------------- Indicadores del panel ---------------------
        total = len(DATOS.materias)
        creditos = sum(int(m.get("creditos", 0) or 0) for m in DATOS.materias)
        docentes = len({str(m.get("docente", "")).strip().lower()
                        for m in DATOS.materias if str(m.get("docente", "")).strip()})

        self.etiqueta_contador.configure(text="%d materia%s" % (total, "" if total == 1 else "s"))
        self.etiqueta_resumen.configure(
            text="📊  Total de materias: %d          🎓  Creditos acumulados: %d          "
                 "👨‍🏫  Docentes distintos: %d" % (total, creditos, docentes)
        )

    def leer_formulario(self):
        """
        Valida todos los campos del formulario.

        Devuelve un diccionario listo para guardar, o None si alguna
        validacion fallo (en ese caso ya se mostro el messagebox).
        """
        valido, materia = validar_texto(self.campo_materia.obtener(), "Materia", minimo=3)
        if not valido:
            self.advertir("Validacion", materia)
            self.campo_materia.enfocar()
            return None

        valido, docente = validar_texto(self.campo_docente.obtener(), "Docente", minimo=3)
        if not valido:
            self.advertir("Validacion", docente)
            self.campo_docente.enfocar()
            return None

        valido, creditos = validar_entero(self.campo_creditos.obtener(), "Creditos",
                                          minimo=1, maximo=20)
        if not valido:
            self.advertir("Validacion", creditos)
            self.campo_creditos.enfocar()
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
            "creditos": creditos,
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

        Actualiza tareas, horario y notas para que sigan apuntando a la
        materia correcta despues de la edicion.
        """
        for tarea in DATOS.tareas:
            if tarea.get("materia") == anterior:
                tarea["materia"] = nuevo
        for bloque in DATOS.horario:
            if bloque.get("materia") == anterior:
                bloque["materia"] = nuevo
        for nota in DATOS.notas:
            if nota.get("materia") == anterior:
                nota["materia"] = nuevo
        DATOS.guardar_tareas()
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
        tareas_asociadas = sum(1 for t in DATOS.tareas if t.get("materia") == nombre)
        bloques_asociados = sum(1 for h in DATOS.horario if h.get("materia") == nombre)

        aviso = ""
        if tareas_asociadas or bloques_asociados:
            aviso = ("\n\nAtencion: esta materia tiene %d tarea(s) y %d bloque(s) de horario "
                     "asociados. Esos registros se conservaran." % (tareas_asociadas, bloques_asociados))

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
        for campo in (self.campo_materia, self.campo_docente, self.campo_creditos,
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
        self.campo_creditos.asignar(registro.get("creditos", ""))
        self.campo_aula.asignar(registro.get("aula", ""))
        self.campo_horario.asignar(registro.get("horario", ""))
        self.actualizar_mensaje("✏ Editando: %s" % registro.get("materia", ""),
                                COLORES["morado_claro"])


# =============================================================================
# SECCION 11 : MODULO 2 - CONTROL DE TAREAS
# =============================================================================
# Registro de tareas academicas con materia, nombre, fecha de entrega,
# prioridad y estado. Incluye filtros, marcado rapido como completada y
# guardado automatico en tareas.json.
# =============================================================================

class VentanaTareas(VentanaModulo):
    """Modulo 2: control y seguimiento de las tareas del estudiante."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Control de Tareas",
            descripcion="Registre sus deberes, controle prioridades y fechas de entrega",
            icono="📝",
            color_acento=COLORES["cian"],
        )
        self.filtro_actual = tk.StringVar(value="Todas")
        self.construir_interfaz()
        self.refrescar_tabla()

    # ------------------------------------------------------------ interfaz ---
    def construir_interfaz(self):
        """Construye el formulario, los filtros y la tabla de tareas."""
        contenedor = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        # ============================ PANEL IZQUIERDO ========================
        panel_formulario = tk.Frame(contenedor, bg=COLORES["superficie"], width=330,
                                    highlightthickness=1, highlightbackground=COLORES["borde"])
        panel_formulario.pack(side="left", fill="y")
        panel_formulario.pack_propagate(False)

        tk.Frame(panel_formulario, bg=COLORES["cian"], height=4).pack(fill="x")

        encabezado = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        encabezado.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(encabezado, text="🗒 DATOS DE LA TAREA", bg=COLORES["superficie"],
                 fg=COLORES["texto"], font=FUENTES["seccion"]).pack(anchor="w")
        tk.Label(encabezado, text="La fecha debe escribirse como DD/MM/AAAA",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"]).pack(anchor="w", pady=(2, 0))

        formulario = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        formulario.pack(fill="x", pady=(6, 0))
        formulario.grid_columnconfigure(0, weight=1)
        formulario.grid_columnconfigure(1, weight=1)

        # Las materias disponibles provienen del Modulo 1.
        materias = DATOS.nombres_de_materias()
        self.campo_materia = CampoFormulario(formulario, "Materia", tipo="combo",
                                             valores=materias, icono="📘",
                                             fila=0, columnas_ocupadas=2)
        self.campo_tarea = CampoFormulario(formulario, "Nombre de la tarea",
                                           icono="✍", fila=1, columnas_ocupadas=2)
        self.campo_fecha = CampoFormulario(formulario, "Fecha de entrega",
                                           icono="📅", fila=2, columna=0, ancho=12)
        self.campo_prioridad = CampoFormulario(formulario, "Prioridad", tipo="combo",
                                               valores=PRIORIDADES, icono="⚡",
                                               fila=2, columna=1, ancho=10)
        self.campo_estado = CampoFormulario(formulario, "Estado", tipo="combo",
                                            valores=ESTADOS_TAREA, icono="🔖",
                                            fila=3, columnas_ocupadas=2)

        # Valores por defecto comodos para el usuario.
        self.campo_fecha.asignar(datetime.date.today().strftime("%d/%m/%Y"))
        self.campo_prioridad.asignar("Media")
        self.campo_estado.asignar("Pendiente")

        if not materias:
            tk.Label(panel_formulario,
                     text="⚠ Aun no hay materias registradas.\nRegistre materias en el Modulo 1.",
                     bg=COLORES["superficie"], fg=COLORES["alerta"],
                     font=FUENTES["micro"], justify="left").pack(anchor="w", padx=20, pady=(4, 0))

        # ----------------------------- Botonera ------------------------------
        botonera = tk.Frame(panel_formulario, bg=COLORES["superficie"])
        botonera.pack(side="bottom", fill="x", padx=14, pady=(4, 8))

        fila_uno = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_uno.pack(fill="x", pady=3)
        BotonModerno(fila_uno, "AGREGAR", self.agregar_tarea, icono="➕",
                     ancho=140, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila_uno, "EDITAR", self.editar_tarea, icono="✏",
                     ancho=140, alto=36, color=COLORES["azul"],
                     color_hover=COLORES["azul_claro"]).pack(side="right")

        fila_dos = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_dos.pack(fill="x", pady=3)
        BotonModerno(fila_dos, "ELIMINAR", self.eliminar_tarea, icono="🗑",
                     ancho=140, alto=36, color=COLORES["error"],
                     color_hover=COLORES["error_hover"]).pack(side="left")
        BotonModerno(fila_dos, "LIMPIAR", self.limpiar_formulario, icono="🧹",
                     ancho=140, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["morado"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"]).pack(side="right")

        BotonModerno(botonera, "MARCAR COMO COMPLETADA", self.completar_tarea,
                     icono="✅", ancho=290, alto=36, color=COLORES["morado"],
                     color_hover=COLORES["morado_hover"]).pack(pady=(6, 0))

        # ============================ PANEL DERECHO ==========================
        panel_tabla = tk.Frame(contenedor, bg=COLORES["fondo"])
        panel_tabla.pack(side="left", fill="both", expand=True, padx=(18, 0))

        cabecera = tk.Frame(panel_tabla, bg=COLORES["fondo"])
        cabecera.pack(fill="x", pady=(0, 10))
        crear_titulo_seccion(cabecera, "📋", "Listado de tareas",
                             "Doble clic sobre una tarea para marcarla como completada").pack(side="left")

        # ------------------------- Filtros rapidos ---------------------------
        filtros = tk.Frame(cabecera, bg=COLORES["fondo"])
        filtros.pack(side="right", pady=4)
        tk.Label(filtros, text="FILTRAR:", bg=COLORES["fondo"], fg=COLORES["texto_tenue"],
                 font=FUENTES["micro"]).pack(side="left", padx=(0, 6))
        combo_filtro = ttk.Combobox(
            filtros, textvariable=self.filtro_actual, state="readonly",
            values=["Todas", "Pendiente", "En proceso", "Completada",
                    "Prioridad alta", "Vencidas"],
            style="Study.TCombobox", width=14, font=FUENTES["pequena"],
        )
        combo_filtro.pack(side="left")
        combo_filtro.bind("<<ComboboxSelected>>", lambda evento=None: self.refrescar_tabla())

        contenedor_tabla, self.tabla = crear_tabla(
            panel_tabla,
            columnas=["#", "Materia", "Tarea", "Fecha", "Plazo", "Prior.", "Estado"],
            anchos=[32, 130, 126, 90, 104, 62, 92],
            alineaciones=["center", "w", "w", "center", "center", "center", "center"],
            altura=10,
            columna_elastica=2,
        )
        contenedor_tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)
        self.tabla.bind("<Double-1>", lambda evento=None: self.completar_tarea())

        # ------------------- Barra de progreso de avance ---------------------
        progreso = tk.Frame(panel_tabla, bg=COLORES["fondo_alt"],
                            highlightthickness=1, highlightbackground=COLORES["borde"])
        progreso.pack(fill="x", pady=(12, 0))

        fila_progreso = tk.Frame(progreso, bg=COLORES["fondo_alt"])
        fila_progreso.pack(fill="x", padx=14, pady=10)

        self.etiqueta_progreso = tk.Label(
            fila_progreso, text="", bg=COLORES["fondo_alt"], fg=COLORES["texto_suave"],
            font=FUENTES["pequena"], anchor="w",
        )
        self.etiqueta_progreso.pack(fill="x")

        self.barra_progreso = ttk.Progressbar(
            progreso, style="Study.Horizontal.TProgressbar",
            orient="horizontal", mode="determinate", maximum=100,
        )
        self.barra_progreso.pack(fill="x", padx=14, pady=(0, 12))

    # ---------------------------------------------------------------- datos --
    def tareas_filtradas(self):
        """Aplica el filtro seleccionado y ordena por fecha de entrega."""
        filtro = self.filtro_actual.get()
        seleccionadas = []

        for tarea in DATOS.tareas:
            estado = tarea.get("estado", "Pendiente")
            prioridad = tarea.get("prioridad", "Media")
            faltan = dias_restantes(tarea.get("fecha", ""))

            if filtro == "Todas":
                seleccionadas.append(tarea)
            elif filtro in ESTADOS_TAREA and estado == filtro:
                seleccionadas.append(tarea)
            elif filtro == "Prioridad alta" and prioridad == "Alta":
                seleccionadas.append(tarea)
            elif filtro == "Vencidas" and estado != "Completada" and faltan is not None and faltan < 0:
                seleccionadas.append(tarea)

        # Orden: primero lo pendiente y lo mas urgente por fecha.
        peso_estado = {"Pendiente": 0, "En proceso": 1, "Completada": 2}
        seleccionadas.sort(key=lambda t: (peso_estado.get(t.get("estado", "Pendiente"), 0),
                                          fecha_a_ordenable(t.get("fecha", ""))))
        return seleccionadas

    def etiqueta_de_color(self, tarea):
        """Determina el color de la fila segun estado, prioridad y vencimiento."""
        estado = tarea.get("estado", "Pendiente")
        if estado == "Completada":
            return "exito"
        faltan = dias_restantes(tarea.get("fecha", ""))
        if faltan is not None and faltan < 0:
            return "error"
        if tarea.get("prioridad") == "Alta":
            return "alerta"
        if estado == "En proceso":
            return "info"
        return None

    def refrescar_tabla(self):
        """Actualiza tabla, contador y barra de progreso."""
        # El combo de materias se refresca por si se registraron nuevas.
        self.campo_materia.actualizar_valores(DATOS.nombres_de_materias())

        filas = []
        for indice, tarea in enumerate(self.tareas_filtradas(), start=1):
            filas.append((
                tarea.get("id"),
                (
                    indice,
                    tarea.get("materia", ""),
                    tarea.get("tarea", ""),
                    tarea.get("fecha", ""),
                    texto_dias_restantes(tarea.get("fecha", "")),
                    tarea.get("prioridad", ""),
                    tarea.get("estado", ""),
                ),
                self.etiqueta_de_color(tarea),
            ))
        llenar_tabla(self.tabla, filas)

        # --------------------------- Indicadores -----------------------------
        total = len(DATOS.tareas)
        completadas = sum(1 for t in DATOS.tareas if t.get("estado") == "Completada")
        pendientes = total - completadas
        vencidas = sum(1 for t in DATOS.tareas
                       if t.get("estado") != "Completada"
                       and (dias_restantes(t.get("fecha", "")) or 0) < 0
                       and dias_restantes(t.get("fecha", "")) is not None)
        porcentaje = (completadas / float(total) * 100.0) if total else 0.0

        self.barra_progreso["value"] = porcentaje
        self.etiqueta_progreso.configure(
            text="📈  Avance: %s%%     ✅ Completadas: %d     ⏳ Pendientes: %d     "
                 "⚠ Vencidas: %d     Σ Total: %d"
                 % (formato_numero(porcentaje, 1), completadas, pendientes, vencidas, total)
        )

    def leer_formulario(self):
        """Valida el formulario de tareas y devuelve el diccionario resultante."""
        valido, materia = validar_texto(self.campo_materia.obtener(), "Materia", minimo=2)
        if not valido:
            self.advertir("Validacion", materia)
            self.campo_materia.enfocar()
            return None

        valido, nombre = validar_texto(self.campo_tarea.obtener(), "Nombre de la tarea",
                                       minimo=3, maximo=80)
        if not valido:
            self.advertir("Validacion", nombre)
            self.campo_tarea.enfocar()
            return None

        valido, fecha = validar_fecha(self.campo_fecha.obtener(), "Fecha de entrega")
        if not valido:
            self.advertir("Validacion", fecha)
            self.campo_fecha.enfocar()
            return None

        valido, prioridad = validar_opcion(self.campo_prioridad.obtener(),
                                           "Prioridad", PRIORIDADES)
        if not valido:
            self.advertir("Validacion", prioridad)
            return None

        valido, estado = validar_opcion(self.campo_estado.obtener(), "Estado", ESTADOS_TAREA)
        if not valido:
            self.advertir("Validacion", estado)
            return None

        return {
            "materia": materia,
            "tarea": nombre,
            "fecha": fecha,
            "prioridad": prioridad,
            "estado": estado,
        }

    # ------------------------------------------------------------- acciones --
    @manejar_errores
    def agregar_tarea(self):
        """Registra una nueva tarea y actualiza tareas.json."""
        if not DATOS.materias:
            self.advertir("Sin materias",
                          "Primero debe registrar al menos una materia en el Modulo 1 "
                          "(Registrar Materias).")
            return

        datos = self.leer_formulario()
        if datos is None:
            return

        datos["id"] = DATOS.nuevo_id(DATOS.tareas)
        datos["registro"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        DATOS.tareas.append(datos)
        DATOS.guardar_tareas()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("✔ Tarea agregada correctamente", COLORES["exito"])
        self.informar("Tarea registrada",
                      "La tarea '%s' fue agregada correctamente." % datos["tarea"])

    @manejar_errores
    def editar_tarea(self):
        """Modifica la tarea seleccionada con los valores del formulario."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion", "Seleccione la tarea que desea editar.")
            return

        registro = DATOS.buscar_por_id(DATOS.tareas, identificador)
        if registro is None:
            self.error("Registro no encontrado", "La tarea seleccionada ya no existe.")
            self.refrescar_tabla()
            return

        datos = self.leer_formulario()
        if datos is None:
            return

        if not self.confirmar("Confirmar edicion",
                              "Se actualizara la tarea:\n\n%s\n\nDesea continuar?"
                              % registro.get("tarea", "")):
            return

        registro.update(datos)
        DATOS.guardar_tareas()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("✔ Tarea actualizada", COLORES["azul_claro"])
        self.informar("Edicion exitosa", "La tarea fue actualizada correctamente.")

    @manejar_errores
    def eliminar_tarea(self):
        """Elimina la tarea seleccionada previa confirmacion."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion", "Seleccione la tarea que desea eliminar.")
            return

        registro = DATOS.buscar_por_id(DATOS.tareas, identificador)
        if registro is None:
            self.error("Registro no encontrado", "La tarea seleccionada ya no existe.")
            self.refrescar_tabla()
            return

        if not self.confirmar("Confirmar eliminacion",
                              "Desea eliminar definitivamente la tarea:\n\n%s"
                              % registro.get("tarea", "")):
            return

        nombre = registro.get("tarea", "")
        DATOS.eliminar_por_id(DATOS.tareas, identificador)
        DATOS.guardar_tareas()

        self.refrescar_tabla()
        self.limpiar_formulario(silencioso=True)
        self.actualizar_mensaje("🗑 Tarea '%s' eliminada" % nombre, COLORES["error"])
        self.informar("Eliminacion exitosa", "La tarea fue eliminada correctamente.")

    @manejar_errores
    def completar_tarea(self):
        """Marca la tarea seleccionada como completada."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            self.advertir("Sin seleccion",
                          "Seleccione la tarea que desea marcar como completada.")
            return

        registro = DATOS.buscar_por_id(DATOS.tareas, identificador)
        if registro is None:
            self.error("Registro no encontrado", "La tarea seleccionada ya no existe.")
            self.refrescar_tabla()
            return

        if registro.get("estado") == "Completada":
            self.informar("Tarea completada",
                          "La tarea '%s' ya estaba marcada como completada."
                          % registro.get("tarea", ""))
            return

        registro["estado"] = "Completada"
        registro["completada_el"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        DATOS.guardar_tareas()

        self.campo_estado.asignar("Completada")
        self.refrescar_tabla()
        self.actualizar_mensaje("✅ Tarea completada: %s" % registro.get("tarea", ""),
                                COLORES["exito"])
        self.informar("Excelente trabajo",
                      "La tarea '%s' fue marcada como COMPLETADA." % registro.get("tarea", ""))

    @manejar_errores
    def limpiar_formulario(self, silencioso=False):
        """Restablece el formulario a sus valores por defecto."""
        self.campo_materia.limpiar()
        self.campo_tarea.limpiar()
        self.campo_fecha.asignar(datetime.date.today().strftime("%d/%m/%Y"))
        self.campo_prioridad.asignar("Media")
        self.campo_estado.asignar("Pendiente")
        limpiar_seleccion(self.tabla)
        self.campo_tarea.enfocar()
        if not silencioso:
            self.actualizar_mensaje("🧹 Formulario limpio", COLORES["texto_suave"])

    @manejar_errores
    def al_seleccionar_fila(self, _evento=None):
        """Carga la tarea seleccionada dentro del formulario."""
        identificador = obtener_id_seleccionado(self.tabla)
        if identificador is None:
            return
        registro = DATOS.buscar_por_id(DATOS.tareas, identificador)
        if registro is None:
            return
        self.campo_materia.asignar(registro.get("materia", ""))
        self.campo_tarea.asignar(registro.get("tarea", ""))
        self.campo_fecha.asignar(registro.get("fecha", ""))
        self.campo_prioridad.asignar(registro.get("prioridad", "Media"))
        self.campo_estado.asignar(registro.get("estado", "Pendiente"))
        self.actualizar_mensaje("✏ Editando: %s" % registro.get("tarea", ""),
                                COLORES["morado_claro"])


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
                 text="Escriba las notas separadas por comas.\nEjemplo:  15, 18.5, 12, 20",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"], justify="left").pack(anchor="w", pady=(3, 0))

        # ------------------------ Caja de texto de notas ---------------------
        caja = tk.Frame(panel, bg=COLORES["superficie_alt"],
                        highlightthickness=1, highlightbackground=COLORES["borde"])
        caja.pack(fill="x", padx=16, pady=12)

        self.texto_notas = tk.Text(
            caja, height=4, bg=COLORES["superficie_alt"], fg=COLORES["texto"],
            insertbackground=COLORES["morado_claro"], relief="flat",
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
            valores=DATOS.nombres_de_materias(), icono="📘", fila=0,
        )

        tk.Label(panel,
                 text="Escala vigente: %s a %s   |   Nota minima de aprobacion: %s"
                      % (formato_numero(NOTA_MINIMA, 0), formato_numero(NOTA_MAXIMA, 0),
                         formato_numero(NOTA_APROBACION)),
                 bg=COLORES["superficie"], fg=COLORES["morado_claro"],
                 font=FUENTES["micro"], wraplength=310, justify="left").pack(anchor="w", padx=20)

        # ----------------------------- Botonera ------------------------------
        botonera = tk.Frame(panel, bg=COLORES["superficie"])
        botonera.pack(side="bottom", fill="x", padx=14, pady=(4, 8))

        BotonModerno(botonera, "CALCULAR PROMEDIO", self.calcular, icono="🧮",
                     ancho=320, alto=42, color=COLORES["morado"],
                     color_hover=COLORES["morado_hover"]).pack(pady=(0, 6))

        fila = tk.Frame(botonera, bg=COLORES["superficie"])
        fila.pack(fill="x")
        BotonModerno(fila, "GUARDAR", self.guardar_en_historial, icono="💾",
                     ancho=155, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila, "LIMPIAR", self.limpiar, icono="🧹",
                     ancho=155, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["morado"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"]).pack(side="right")

        # ============================ PANEL DERECHO ==========================
        derecha = tk.Frame(contenedor, bg=COLORES["fondo"])
        derecha.pack(side="left", fill="both", expand=True, padx=(18, 0))

        # ------------------------ Tarjetas de resultado ----------------------
        tarjetas = tk.Frame(derecha, bg=COLORES["fondo"])
        tarjetas.pack(fill="x")

        self.tarjeta_promedio = TarjetaIndicador(tarjetas, "🎯", "Promedio", "0.00",
                                                 COLORES["morado"], ancho=160, alto=96)
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
            columnas=["Pos", "Nota", "Estado", "Diferencia"],
            anchos=[46, 62, 88, 100],
            alineaciones=["center", "center", "center", "center"],
            altura=7,
        )
        contenedor_tabla.pack(fill="both", expand=True)

        # Derecha: promedios ya guardados en notas.json.
        columna_derecha = tk.Frame(zona_tablas, bg=COLORES["fondo"])
        columna_derecha.pack(side="left", fill="both", expand=True, padx=(14, 0))

        crear_titulo_seccion(columna_derecha, "🗂", "Promedios guardados",
                             "Alimentan el modulo de Estadisticas").pack(anchor="w", pady=(0, 6))

        contenedor_historial, self.tabla_historial = crear_tabla(
            columna_derecha,
            columnas=["Materia", "Notas", "Prom.", "Estado"],
            anchos=[100, 70, 56, 86],
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
        aprueba = promedio >= NOTA_APROBACION

        self.notas_calculadas = notas
        self.promedio_calculado = promedio

        # --------------------------- Tarjetas KPI ----------------------------
        color_promedio = COLORES["exito"] if aprueba else COLORES["error"]
        self.tarjeta_promedio.actualizar(formato_numero(promedio), color_promedio)
        self.tarjeta_mayor.actualizar(formato_numero(mayor), COLORES["exito"])
        self.tarjeta_menor.actualizar(formato_numero(menor), COLORES["error"])
        self.tarjeta_cantidad.actualizar(str(cantidad), COLORES["cian"])

        # ------------------------- Franja de veredicto -----------------------
        if aprueba:
            mensaje = ("✅  APROBADO   |   Promedio %s   |   Supera el minimo por %s puntos"
                       % (formato_numero(promedio),
                          formato_numero(promedio - NOTA_APROBACION)))
            self.pintar_estado(mensaje, COLORES["exito"])
        else:
            mensaje = ("❌  REPROBADO   |   Promedio %s   |   Le faltan %s puntos para aprobar"
                       % (formato_numero(promedio),
                          formato_numero(NOTA_APROBACION - promedio)))
            self.pintar_estado(mensaje, COLORES["error"])

        # ------------------------ Tabla de notas ordenadas -------------------
        ordenadas = sorted(notas, reverse=True)
        filas = []
        for posicion, nota in enumerate(ordenadas, start=1):
            diferencia = nota - NOTA_APROBACION
            if nota >= NOTA_APROBACION:
                condicion, etiqueta = "Aprobada", "exito"
                texto_diferencia = "+%s puntos" % formato_numero(diferencia)
            else:
                condicion, etiqueta = "Reprobada", "error"
                texto_diferencia = "-%s puntos" % formato_numero(abs(diferencia))
            filas.append((posicion, (posicion, formato_numero(nota), condicion,
                                     texto_diferencia), etiqueta))
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
            "estado": "Aprobado" if self.promedio_calculado >= NOTA_APROBACION else "Reprobado",
            "fecha": datetime.date.today().strftime("%d/%m/%Y"),
        })
        DATOS.guardar_notas()

        self.refrescar_historial()
        self.actualizar_mensaje("💾 Promedio de '%s' guardado" % materia, COLORES["exito"])
        self.informar("Promedio guardado",
                      "El promedio de '%s' (%s) fue guardado correctamente.\n\n"
                      "Este dato se vera reflejado en el modulo de Estadisticas."
                      % (materia, formato_numero(self.promedio_calculado)))

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
        self.campo_materia.actualizar_valores(DATOS.nombres_de_materias())
        registros = sorted(DATOS.notas,
                           key=lambda r: float(r.get("promedio", 0)), reverse=True)
        filas = []
        for registro in registros:
            notas = registro.get("notas", [])
            texto_notas = ", ".join(formato_numero(n, 1) for n in notas)
            if len(texto_notas) > 11:
                texto_notas = texto_notas[:8] + "..."
            aprobado = float(registro.get("promedio", 0)) >= NOTA_APROBACION
            filas.append((
                registro.get("id"),
                (
                    registro.get("materia", ""),
                    texto_notas,
                    formato_numero(registro.get("promedio", 0)),
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
# SECCION 13 : MODULO 4 - NOTA NECESARIA
# =============================================================================
# Responde a la pregunta clasica del estudiante: "que nota necesito en el
# examen para aprobar la materia?". Utiliza la formula de ponderacion:
#
#     nota_necesaria = (nota_minima - promedio_actual * %acumulado) / %examen
#
# Los porcentajes se trabajan en forma decimal (por ejemplo 70 % -> 0.70).
# =============================================================================

class VentanaNotaNecesaria(VentanaModulo):
    """Modulo 4: proyeccion de la nota requerida en el examen final."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Nota Necesaria",
            descripcion="Calcule que calificacion necesita obtener en su examen final",
            icono="🎯",
            color_acento=COLORES["alerta"],
        )
        self.construir_interfaz()

    # ------------------------------------------------------------ interfaz ---
    def construir_interfaz(self):
        """Crea el formulario de ponderaciones y el panel de resultados."""
        contenedor = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        # ============================ PANEL IZQUIERDO ========================
        panel = tk.Frame(contenedor, bg=COLORES["superficie"], width=360,
                         highlightthickness=1, highlightbackground=COLORES["borde"])
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        tk.Frame(panel, bg=COLORES["alerta"], height=4).pack(fill="x")

        encabezado = tk.Frame(panel, bg=COLORES["superficie"])
        encabezado.pack(fill="x", padx=16, pady=(14, 2))
        tk.Label(encabezado, text="⚙ PARAMETROS DEL CALCULO", bg=COLORES["superficie"],
                 fg=COLORES["texto"], font=FUENTES["seccion"]).pack(anchor="w")
        tk.Label(encabezado,
                 text="Los porcentajes deben sumar 100 %",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"]).pack(anchor="w", pady=(3, 0))

        formulario = tk.Frame(panel, bg=COLORES["superficie"])
        formulario.pack(fill="x", pady=(10, 0))
        formulario.grid_columnconfigure(0, weight=1)

        self.campo_materia = CampoFormulario(formulario, "Materia (opcional)", tipo="combo",
                                             valores=DATOS.nombres_de_materias(),
                                             icono="📘", fila=0)
        self.campo_promedio = CampoFormulario(formulario, "Promedio actual",
                                              icono="📈", fila=1)
        self.campo_acumulado = CampoFormulario(formulario, "Porcentaje acumulado (%)",
                                               icono="📦", fila=2)
        self.campo_examen = CampoFormulario(formulario, "Porcentaje del examen (%)",
                                            icono="📝", fila=3)
        self.campo_minima = CampoFormulario(formulario, "Nota minima para aprobar",
                                            icono="🎯", fila=4)

        # Valores iniciales tipicos de la universidad.
        self.campo_acumulado.asignar("70")
        self.campo_examen.asignar("30")
        self.campo_minima.asignar(formato_numero(NOTA_APROBACION))

        # Al cambiar cualquier valor se recalcula automaticamente.
        for campo in (self.campo_promedio, self.campo_acumulado,
                      self.campo_examen, self.campo_minima):
            campo.variable.trace_add("write", self._al_cambiar_campo)

        # ----------------------------- Botonera ------------------------------
        botonera = tk.Frame(panel, bg=COLORES["superficie"])
        botonera.pack(side="bottom", fill="x", padx=14, pady=(4, 8))

        BotonModerno(botonera, "CALCULAR NOTA NECESARIA", self.calcular, icono="🧮",
                     ancho=320, alto=42, color=COLORES["morado"],
                     color_hover=COLORES["morado_hover"]).pack(pady=(0, 6))

        fila = tk.Frame(botonera, bg=COLORES["superficie"])
        fila.pack(fill="x")
        BotonModerno(fila, "USAR PROMEDIO", self.usar_promedio_guardado, icono="📥",
                     ancho=190, alto=36, color=COLORES["azul"],
                     color_hover=COLORES["azul_claro"]).pack(side="left")
        BotonModerno(fila, "LIMPIAR", self.limpiar, icono="🧹",
                     ancho=126, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["morado"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"]).pack(side="right")

        # ============================ PANEL DERECHO ==========================
        derecha = tk.Frame(contenedor, bg=COLORES["fondo"])
        derecha.pack(side="left", fill="both", expand=True, padx=(18, 0))

        # ------------------------- Panel de resultado ------------------------
        self.panel_resultado = tk.Frame(derecha, bg=COLORES["superficie"],
                                        highlightthickness=2,
                                        highlightbackground=COLORES["borde"])
        self.panel_resultado.pack(fill="x")

        self.franja_resultado = tk.Frame(self.panel_resultado, bg=COLORES["morado"], height=5)
        self.franja_resultado.pack(fill="x")

        interior = tk.Frame(self.panel_resultado, bg=COLORES["superficie"])
        interior.pack(fill="x", padx=22, pady=8)

        tk.Label(interior, text="NOTA QUE NECESITA EN EL EXAMEN",
                 bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena_bold"]).pack(anchor="w")

        self.etiqueta_resultado = tk.Label(
            interior, text="--", bg=COLORES["superficie"],
            fg=COLORES["texto"], font=FUENTES["resultado"],
        )
        self.etiqueta_resultado.pack(anchor="w", pady=(4, 2))

        self.etiqueta_veredicto = tk.Label(
            interior, text="Complete los campos para obtener el calculo",
            bg=COLORES["superficie"], fg=COLORES["texto_suave"],
            font=FUENTES["texto_bold"], anchor="w", justify="left", wraplength=620,
        )
        self.etiqueta_veredicto.pack(anchor="w", pady=(4, 0))

        self.etiqueta_detalle = tk.Label(
            interior, text="", bg=COLORES["superficie"], fg=COLORES["texto_tenue"],
            font=FUENTES["pequena"], anchor="w", justify="left", wraplength=620,
        )
        self.etiqueta_detalle.pack(anchor="w", pady=(8, 0))

        # ----------------------- Desglose de la formula ----------------------
        crear_titulo_seccion(derecha, "🧾", "Desglose del calculo",
                             "Detalle de la ponderacion utilizada").pack(anchor="w", pady=(10, 6))

        contenedor_tabla, self.tabla_desglose = crear_tabla(
            derecha,
            columnas=["Concepto", "Valor", "Descripcion"],
            anchos=[195, 95, 300],
            alineaciones=["w", "center", "w"],
            altura=3,
        )
        contenedor_tabla.pack(fill="both", expand=True)

        # --------------------- Escenarios de referencia ----------------------
        crear_titulo_seccion(derecha, "🔮", "Escenarios posibles",
                             "Nota final que obtendria segun la calificacion del examen"
                             ).pack(anchor="w", pady=(10, 6))

        self.lienzo_escenarios = tk.Canvas(
            derecha, height=76, bg=COLORES["superficie"], highlightthickness=1,
            highlightbackground=COLORES["borde"],
        )
        self.lienzo_escenarios.pack(fill="both", expand=True)

        self.limpiar_resultados()

    # -------------------------------------------------------------- calculo --
    def _al_cambiar_campo(self, *_argumentos):
        """
        Recalcula en silencio cada vez que el usuario escribe.

        No muestra messagebox: si los datos aun estan incompletos simplemente
        deja el resultado en espera. El calculo formal se hace con el boton.
        """
        try:
            self.calcular(silencioso=True)
        except Exception as error:
            # El calculo silencioso nunca debe interrumpir la escritura.
            print("[Study Control] Recalculo automatico omitido: %s" % error)

    def leer_parametros(self, silencioso):
        """
        Valida los cuatro parametros del calculo.

        Devuelve una tupla (promedio, acumulado, examen, minima) o None.
        En modo silencioso no muestra advertencias.
        """
        valido, promedio = validar_decimal(self.campo_promedio.obtener(),
                                           "Promedio actual", NOTA_MINIMA, NOTA_MAXIMA)
        if not valido:
            if not silencioso:
                self.advertir("Validacion", promedio)
                self.campo_promedio.enfocar()
            return None

        valido, acumulado = validar_decimal(self.campo_acumulado.obtener(),
                                            "Porcentaje acumulado", 0, 100)
        if not valido:
            if not silencioso:
                self.advertir("Validacion", acumulado)
                self.campo_acumulado.enfocar()
            return None

        valido, examen = validar_decimal(self.campo_examen.obtener(),
                                         "Porcentaje del examen", 0.01, 100)
        if not valido:
            if not silencioso:
                self.advertir("Validacion", examen)
                self.campo_examen.enfocar()
            return None

        valido, minima = validar_decimal(self.campo_minima.obtener(),
                                         "Nota minima para aprobar", NOTA_MINIMA, NOTA_MAXIMA)
        if not valido:
            if not silencioso:
                self.advertir("Validacion", minima)
                self.campo_minima.enfocar()
            return None

        # Se avisa (sin bloquear) cuando los porcentajes no suman 100 %.
        if abs((acumulado + examen) - 100.0) > 0.01 and not silencioso:
            self.advertir(
                "Porcentajes inconsistentes",
                "El porcentaje acumulado (%s %%) y el del examen (%s %%) suman %s %%.\n\n"
                "Lo habitual es que sumen 100 %%. El calculo se realizara igualmente "
                "con los valores ingresados."
                % (formato_numero(acumulado, 1), formato_numero(examen, 1),
                   formato_numero(acumulado + examen, 1))
            )

        return promedio, acumulado, examen, minima

    @manejar_errores
    def calcular(self, silencioso=False):
        """
        Aplica la formula de ponderacion y muestra un mensaje inteligente.

        Casos contemplados:
            - Ya aprobaste           (el acumulado alcanza la nota minima)
            - No es posible aprobar  (la nota requerida supera la escala)
            - Necesitas obtener...   (calificacion exacta requerida)
        """
        parametros = self.leer_parametros(silencioso)
        if parametros is None:
            if silencioso:
                self.limpiar_resultados()
            return

        promedio, acumulado, examen, minima = parametros

        # ------------------------- Formula principal -------------------------
        aporte_acumulado = promedio * (acumulado / 100.0)
        factor_examen = examen / 100.0
        necesaria = (minima - aporte_acumulado) / factor_examen

        # ------------------------ Interpretacion -----------------------------
        if aporte_acumulado >= minima:
            titulo = "✅  YA APROBASTE"
            mensaje = ("Con tu acumulado ya alcanzas la nota minima de %s. "
                       "Aunque obtengas %s en el examen, la materia esta aprobada."
                       % (formato_numero(minima), formato_numero(NOTA_MINIMA, 0)))
            valor_mostrado = formato_numero(max(0.0, necesaria))
            color = COLORES["exito"]
        elif necesaria > NOTA_MAXIMA:
            titulo = "❌  NO ES POSIBLE APROBAR"
            mensaje = ("Necesitarias obtener %s en el examen, pero la nota maxima "
                       "de la escala es %s. Matematicamente no alcanzas el minimo de %s."
                       % (formato_numero(necesaria), formato_numero(NOTA_MAXIMA, 0),
                          formato_numero(minima)))
            valor_mostrado = formato_numero(necesaria)
            color = COLORES["error"]
        elif necesaria <= NOTA_MINIMA:
            titulo = "✅  YA APROBASTE"
            mensaje = ("Tu acumulado es suficiente: cualquier calificacion en el examen "
                       "te mantiene sobre la nota minima de %s." % formato_numero(minima))
            valor_mostrado = formato_numero(max(0.0, necesaria))
            color = COLORES["exito"]
        else:
            titulo = "🎯  NECESITAS OBTENER %s" % formato_numero(necesaria)
            exigencia = necesaria / NOTA_MAXIMA * 100.0
            if exigencia >= 85:
                comentario = "Es una meta exigente: organiza un plan de estudio intensivo."
            elif exigencia >= 60:
                comentario = "Es una meta alcanzable con estudio constante."
            else:
                comentario = "Es una meta comoda: manten el ritmo y aseguras la materia."
            mensaje = ("Debes obtener al menos %s sobre %s en el examen para alcanzar "
                       "la nota minima de %s. %s"
                       % (formato_numero(necesaria), formato_numero(NOTA_MAXIMA, 0),
                          formato_numero(minima), comentario))
            valor_mostrado = formato_numero(necesaria)
            color = COLORES["alerta"] if necesaria >= NOTA_APROBACION else COLORES["azul_claro"]

        # ------------------------- Pintado del panel -------------------------
        self.etiqueta_resultado.configure(text=valor_mostrado, fg=color)
        self.etiqueta_veredicto.configure(text=titulo, fg=color)
        self.etiqueta_detalle.configure(text=mensaje, fg=COLORES["texto_suave"])
        self.panel_resultado.configure(highlightbackground=color)
        self.franja_resultado.configure(bg=color)

        # --------------------------- Tabla desglose --------------------------
        nota_maxima_posible = aporte_acumulado + NOTA_MAXIMA * factor_examen
        filas = [
            (1, ("Promedio actual", formato_numero(promedio),
                 "Calificacion obtenida hasta el momento"), "info"),
            (2, ("Porcentaje acumulado", "%s %%" % formato_numero(acumulado, 1),
                 "Peso del promedio actual sobre la nota final"), None),
            (3, ("Aporte del acumulado", formato_numero(aporte_acumulado),
                 "Puntos ya asegurados en la nota final"), "exito"),
            (4, ("Porcentaje del examen", "%s %%" % formato_numero(examen, 1),
                 "Peso del examen sobre la nota final"), None),
            (5, ("Nota minima requerida", formato_numero(minima),
                 "Meta que se debe alcanzar en la materia"), "alerta"),
            (6, ("Nota maxima alcanzable", formato_numero(nota_maxima_posible),
                 "Resultado final si obtiene %s en el examen"
                 % formato_numero(NOTA_MAXIMA, 0)),
             "exito" if nota_maxima_posible >= minima else "error"),
        ]
        llenar_tabla(self.tabla_desglose, filas)

        # --------------------------- Escenarios ------------------------------
        self.dibujar_escenarios(aporte_acumulado, factor_examen, minima)

        if not silencioso:
            self.actualizar_mensaje("🎯 Calculo actualizado correctamente", color)

    def dibujar_escenarios(self, aporte_acumulado, factor_examen, minima):
        """
        Dibuja en un Canvas la nota final segun distintas notas de examen.

        Es una ayuda visual: muestra cinco escenarios (0, 5, 10, 15 y 20)
        pintados de verde si aprueban y de rojo si no.
        """
        lienzo = self.lienzo_escenarios
        lienzo.delete("all")
        lienzo.update_idletasks()

        ancho_total = max(lienzo.winfo_width(), 700)
        alto_total = max(lienzo.winfo_height(), 60)
        escenarios = [0.0, 5.0, 10.0, 15.0, 20.0]
        ancho_columna = ancho_total / float(len(escenarios))

        # Las alturas son proporcionales para que el grafico se adapte al
        # espacio realmente disponible en la ventana.
        fila_titulo = alto_total * 0.22
        fila_valor = alto_total * 0.53
        fila_estado = alto_total * 0.84

        for indice, nota_examen in enumerate(escenarios):
            final = aporte_acumulado + nota_examen * factor_examen
            aprueba = final >= minima
            color = COLORES["exito"] if aprueba else COLORES["error"]

            centro_x = ancho_columna * indice + ancho_columna / 2.0

            lienzo.create_text(centro_x, fila_titulo,
                               text="Examen %s" % formato_numero(nota_examen, 0),
                               fill=COLORES["texto_tenue"], font=("TkDefaultFont", 8))
            lienzo.create_text(centro_x, fila_valor, text=formato_numero(final),
                               fill=color, font=("TkDefaultFont", 15, "bold"))
            lienzo.create_text(centro_x, fila_estado,
                               text="APRUEBA" if aprueba else "NO APRUEBA",
                               fill=color, font=("TkDefaultFont", 8, "bold"))

            if indice < len(escenarios) - 1:
                separador_x = ancho_columna * (indice + 1)
                lienzo.create_line(separador_x, alto_total * 0.12,
                                   separador_x, alto_total * 0.9, fill=COLORES["borde"])

    # ------------------------------------------------------------- acciones --
    @manejar_errores
    def usar_promedio_guardado(self):
        """Toma el promedio guardado de la materia seleccionada (Modulo 3)."""
        materia = self.campo_materia.obtener()
        if not materia:
            self.advertir("Sin materia",
                          "Seleccione primero una materia para recuperar su promedio guardado.")
            return

        for registro in DATOS.notas:
            if str(registro.get("materia", "")).lower() == materia.lower():
                self.campo_promedio.asignar(formato_numero(registro.get("promedio", 0)))
                self.calcular(silencioso=True)
                self.actualizar_mensaje("📥 Promedio de '%s' cargado" % materia,
                                        COLORES["azul_claro"])
                self.informar("Promedio cargado",
                              "Se cargo el promedio %s de la materia '%s'."
                              % (formato_numero(registro.get("promedio", 0)), materia))
                return

        self.advertir("Sin datos",
                      "La materia '%s' no tiene un promedio guardado.\n\n"
                      "Puede calcularlo y guardarlo en el modulo Calculadora de Promedios."
                      % materia)

    @manejar_errores
    def limpiar(self):
        """Restablece los valores por defecto del modulo."""
        self.campo_materia.limpiar()
        self.campo_promedio.limpiar()
        self.campo_acumulado.asignar("70")
        self.campo_examen.asignar("30")
        self.campo_minima.asignar(formato_numero(NOTA_APROBACION))
        self.limpiar_resultados()
        self.campo_promedio.enfocar()
        self.actualizar_mensaje("🧹 Parametros reiniciados", COLORES["texto_suave"])

    def limpiar_resultados(self):
        """Deja el panel de resultados en su estado neutro de espera."""
        self.etiqueta_resultado.configure(text="--", fg=COLORES["texto"])
        self.etiqueta_veredicto.configure(
            text="Complete los campos para obtener el calculo", fg=COLORES["texto_suave"])
        self.etiqueta_detalle.configure(text="")
        self.panel_resultado.configure(highlightbackground=COLORES["borde"])
        self.franja_resultado.configure(bg=COLORES["morado"])
        llenar_tabla(self.tabla_desglose, [])
        self.lienzo_escenarios.delete("all")
        self.lienzo_escenarios.create_text(
            350, max(self.lienzo_escenarios.winfo_height(), 60) / 2,
            text="Los escenarios apareceran despues del calculo",
            fill=COLORES["texto_tenue"], font=("TkDefaultFont", 9),
        )


# =============================================================================
# SECCION 14 : MODULO 5 - HORARIO SEMANAL
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
                                             valores=DATOS.nombres_de_materias(),
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
        BotonModerno(fila_uno, "GUARDAR", self.guardar_bloque, icono="💾",
                     ancho=140, alto=36, color=COLORES["exito"],
                     color_hover=COLORES["exito_hover"]).pack(side="left")
        BotonModerno(fila_uno, "EDITAR", self.editar_bloque, icono="✏",
                     ancho=140, alto=36, color=COLORES["azul"],
                     color_hover=COLORES["azul_claro"]).pack(side="right")

        fila_dos = tk.Frame(botonera, bg=COLORES["superficie"])
        fila_dos.pack(fill="x", pady=3)
        BotonModerno(fila_dos, "ELIMINAR", self.eliminar_bloque, icono="🗑",
                     ancho=140, alto=36, color=COLORES["error"],
                     color_hover=COLORES["error_hover"]).pack(side="left")
        BotonModerno(fila_dos, "LIMPIAR", self.limpiar_formulario, icono="🧹",
                     ancho=140, alto=36, color=COLORES["superficie_alt"],
                     color_hover=COLORES["morado"], color_texto=COLORES["texto"],
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
        tk.Label(filtros, text="DIA:", bg=COLORES["fondo"], fg=COLORES["texto_tenue"],
                 font=FUENTES["micro"]).pack(side="left", padx=(0, 6))
        combo = ttk.Combobox(filtros, textvariable=self.filtro_dia, state="readonly",
                             values=["Todos"] + DIAS_SEMANA, style="Study.TCombobox",
                             width=12, font=FUENTES["pequena"])
        combo.pack(side="left")
        combo.bind("<<ComboboxSelected>>", lambda evento=None: self.refrescar_tabla())

        contenedor_tabla, self.tabla = crear_tabla(
            derecha,
            columnas=["#", "Materia", "Dia", "Inicio", "Fin", "Dur.", "Docente"],
            anchos=[34, 140, 84, 68, 62, 74, 148],
            alineaciones=["center", "w", "center", "center", "center", "center", "w"],
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
            derecha, text="", bg=COLORES["fondo"], fg=COLORES["texto_suave"],
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
        self.campo_materia.actualizar_valores(DATOS.nombres_de_materias())

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
            fg=COLORES["alerta"] if cruces else COLORES["texto_suave"],
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
            color = COLORES["morado"] if dia != hoy else COLORES["cian"]

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
                               fill=COLORES["cian"] if dia == hoy else COLORES["texto_tenue"],
                               font=("TkDefaultFont", 8, "bold"))

    def leer_formulario(self):
        """Valida el formulario del bloque de clase."""
        valido, materia = validar_texto(self.campo_materia.obtener(), "Materia", minimo=2)
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
        if not DATOS.materias:
            self.advertir("Sin materias",
                          "Primero registre sus materias en el Modulo 1 (Registrar Materias).")
            return

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
                                COLORES["morado_claro"])


# =============================================================================
# SECCION 15 : MODULO 6 - ESTADISTICAS GENERALES
# =============================================================================
# Consolida la informacion de los demas modulos y la presenta en tarjetas,
# graficos dibujados con Canvas y una tabla comparativa por materia. Todos
# los valores se calculan automaticamente a partir de los archivos JSON.
# =============================================================================

class VentanaEstadisticas(VentanaModulo):
    """Modulo 6: panel de control academico con indicadores automaticos."""

    def __init__(self, aplicacion):
        super().__init__(
            aplicacion,
            titulo="Estadisticas Generales",
            descripcion="Resumen automatico de su desempeno academico",
            icono="📈",
            color_acento=COLORES["exito"],
        )
        self.construir_interfaz()
        self.calcular_estadisticas()

    # ------------------------------------------------------------ interfaz ---
    def construir_interfaz(self):
        """Crea las tarjetas de indicadores, los graficos y la tabla."""
        # ------------------------- Fila de indicadores -----------------------
        fila_tarjetas = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        fila_tarjetas.pack(fill="x")

        self.tarjeta_materias = TarjetaIndicador(fila_tarjetas, "📚", "Materias", "0",
                                                 COLORES["morado"], ancho=200, alto=96)
        self.tarjeta_materias.pack(side="left", padx=(0, 10))

        self.tarjeta_tareas = TarjetaIndicador(fila_tarjetas, "📝", "Tareas totales", "0",
                                               COLORES["cian"], ancho=200, alto=96)
        self.tarjeta_tareas.pack(side="left", padx=(0, 10))

        self.tarjeta_completadas = TarjetaIndicador(fila_tarjetas, "✅", "Completadas", "0",
                                                    COLORES["exito"], ancho=200, alto=96)
        self.tarjeta_completadas.pack(side="left", padx=(0, 10))

        self.tarjeta_pendientes = TarjetaIndicador(fila_tarjetas, "⏳", "Pendientes", "0",
                                                   COLORES["alerta"], ancho=200, alto=96)
        self.tarjeta_pendientes.pack(side="left", padx=(0, 10))

        self.tarjeta_promedio = TarjetaIndicador(fila_tarjetas, "🎯", "Promedio general", "0.00",
                                                 COLORES["azul_claro"], ancho=200, alto=96)
        self.tarjeta_promedio.pack(side="left")

        # -------------------------- Zona intermedia --------------------------
        zona = tk.Frame(self.cuerpo, bg=COLORES["fondo"])
        zona.pack(fill="both", expand=True, pady=10)

        # ---- Izquierda: grafico de avance y distribucion de prioridades -----
        izquierda = tk.Frame(zona, bg=COLORES["fondo"], width=430)
        izquierda.pack(side="left", fill="both")
        izquierda.pack_propagate(False)

        crear_titulo_seccion(izquierda, "📊", "Avance de tareas",
                             "Porcentaje de tareas completadas").pack(anchor="w", pady=(0, 8))

        self.lienzo_avance = tk.Canvas(izquierda, height=128, bg=COLORES["superficie"],
                                       highlightthickness=1,
                                       highlightbackground=COLORES["borde"])
        self.lienzo_avance.pack(fill="x")

        crear_titulo_seccion(izquierda, "⚡", "Tareas por prioridad",
                             "Distribucion de la carga academica").pack(anchor="w", pady=(10, 6))

        self.lienzo_prioridad = tk.Canvas(izquierda, height=106, bg=COLORES["superficie"],
                                          highlightthickness=1,
                                          highlightbackground=COLORES["borde"])
        self.lienzo_prioridad.pack(fill="x")

        # ------------------ Derecha: detalle por materia ---------------------
        derecha = tk.Frame(zona, bg=COLORES["fondo"])
        derecha.pack(side="left", fill="both", expand=True, padx=(18, 0))

        crear_titulo_seccion(derecha, "🔎", "Detalle por materia",
                             "Comparativa de tareas, creditos y promedios").pack(anchor="w",
                                                                                  pady=(0, 8))

        contenedor_tabla, self.tabla = crear_tabla(
            derecha,
            columnas=["Materia", "Cr.", "Tareas", "Hechas", "Pend.", "Prom.", "Estado"],
            anchos=[145, 42, 72, 72, 60, 66, 92],
            alineaciones=["w", "center", "center", "center", "center", "center", "center"],
            altura=4,
            columna_elastica=0,
        )
        contenedor_tabla.pack(fill="both", expand=True)

        # ------------------------ Panel de conclusiones ----------------------
        panel_conclusion = tk.Frame(derecha, bg=COLORES["superficie"],
                                    highlightthickness=1, highlightbackground=COLORES["borde"])
        panel_conclusion.pack(fill="x", pady=(12, 0))

        tk.Frame(panel_conclusion, bg=COLORES["exito"], height=3).pack(fill="x")
        self.etiqueta_conclusion = tk.Label(
            panel_conclusion, text="", bg=COLORES["superficie"], fg=COLORES["texto_suave"],
            font=FUENTES["pequena"], justify="left", anchor="w", wraplength=560,
        )
        self.etiqueta_conclusion.pack(fill="x", padx=14, pady=12)

        # ---------------------- Boton de actualizacion -----------------------
        BotonModerno(self.zona_titulo_derecha, "ACTUALIZAR DATOS", self.calcular_estadisticas,
                     icono="🔄", ancho=185, alto=38, color=COLORES["superficie_alt"],
                     color_hover=COLORES["morado"], color_texto=COLORES["texto"],
                     borde=COLORES["borde"], fuente=FUENTES["boton_pequeno"]).pack(pady=12)

    # ------------------------------------------------------------- calculos --
    @manejar_errores
    def calcular_estadisticas(self):
        """Recalcula todos los indicadores a partir de la informacion actual."""
        total_materias = len(DATOS.materias)
        total_tareas = len(DATOS.tareas)
        completadas = sum(1 for t in DATOS.tareas if t.get("estado") == "Completada")
        pendientes = total_tareas - completadas

        promedios = [float(n.get("promedio", 0)) for n in DATOS.notas]
        promedio_general = promedio_de(promedios)

        # --------------------------- Tarjetas KPI ----------------------------
        self.tarjeta_materias.actualizar(total_materias, COLORES["texto"])
        self.tarjeta_tareas.actualizar(total_tareas, COLORES["texto"])
        self.tarjeta_completadas.actualizar(completadas, COLORES["exito"])
        self.tarjeta_pendientes.actualizar(pendientes,
                                           COLORES["alerta"] if pendientes else COLORES["exito"])

        if promedios:
            color_promedio = (COLORES["exito"] if promedio_general >= NOTA_APROBACION
                              else COLORES["error"])
            self.tarjeta_promedio.actualizar(formato_numero(promedio_general), color_promedio)
        else:
            self.tarjeta_promedio.actualizar("--", COLORES["texto_tenue"])

        # ------------------------------ Graficos -----------------------------
        porcentaje = (completadas / float(total_tareas) * 100.0) if total_tareas else 0.0
        self.dibujar_avance(porcentaje, completadas, pendientes)
        self.dibujar_prioridades()

        # -------------------------- Tabla por materia ------------------------
        self.llenar_detalle()

        # --------------------------- Conclusiones ----------------------------
        self.escribir_conclusiones(total_materias, total_tareas, completadas,
                                   pendientes, promedios, promedio_general)

        self.actualizar_mensaje("🔄 Estadisticas actualizadas el %s"
                                % datetime.datetime.now().strftime("%d/%m/%Y a las %H:%M"),
                                COLORES["exito"])

    def dibujar_avance(self, porcentaje, completadas, pendientes):
        """Dibuja un anillo de progreso con el porcentaje de tareas completadas."""
        lienzo = self.lienzo_avance
        lienzo.delete("all")
        lienzo.update_idletasks()

        ancho = max(lienzo.winfo_width(), 400)
        centro_x, centro_y, radio = 80, 64, 44

        # Anillo base (gris) y anillo de avance (morado / verde).
        lienzo.create_oval(centro_x - radio, centro_y - radio,
                           centro_x + radio, centro_y + radio,
                           outline=COLORES["fondo_alt"], width=14)

        if porcentaje > 0:
            color = COLORES["exito"] if porcentaje >= 70 else (
                COLORES["morado"] if porcentaje >= 35 else COLORES["alerta"])
            lienzo.create_arc(centro_x - radio, centro_y - radio,
                              centro_x + radio, centro_y + radio,
                              start=90, extent=-porcentaje * 3.6,
                              style="arc", outline=color, width=14)
        else:
            color = COLORES["texto_tenue"]

        lienzo.create_text(centro_x, centro_y - 6, text="%s%%" % formato_numero(porcentaje, 0),
                           fill=COLORES["texto"], font=("TkDefaultFont", 18, "bold"))
        lienzo.create_text(centro_x, centro_y + 15, text="completado",
                           fill=COLORES["texto_tenue"], font=("TkDefaultFont", 8))

        # Leyenda al costado derecho del anillo.
        base_x = min(ancho - 150, 190)
        lienzo.create_rectangle(base_x, 40, base_x + 12, 52,
                                fill=COLORES["exito"], outline=COLORES["exito"])
        lienzo.create_text(base_x + 22, 46, anchor="w",
                           text="Completadas: %d" % completadas,
                           fill=COLORES["texto"], font=("TkDefaultFont", 9))

        lienzo.create_rectangle(base_x, 72, base_x + 12, 84,
                                fill=COLORES["alerta"], outline=COLORES["alerta"])
        lienzo.create_text(base_x + 22, 78, anchor="w",
                           text="Pendientes: %d" % pendientes,
                           fill=COLORES["texto"], font=("TkDefaultFont", 9))

    def dibujar_prioridades(self):
        """Dibuja barras horizontales con la cantidad de tareas por prioridad."""
        lienzo = self.lienzo_prioridad
        lienzo.delete("all")
        lienzo.update_idletasks()

        ancho = max(lienzo.winfo_width(), 400)
        colores = {"Alta": COLORES["error"], "Media": COLORES["alerta"], "Baja": COLORES["exito"]}

        conteos = {}
        for prioridad in PRIORIDADES:
            conteos[prioridad] = sum(1 for t in DATOS.tareas
                                     if t.get("prioridad") == prioridad)
        maximo = max(conteos.values()) if any(conteos.values()) else 1

        for indice, prioridad in enumerate(PRIORIDADES):
            posicion_y = 22 + indice * 31
            cantidad = conteos[prioridad]
            largo = (cantidad / float(maximo)) * (ancho - 190)

            lienzo.create_text(16, posicion_y, anchor="w", text=prioridad.upper(),
                               fill=COLORES["texto_suave"], font=("TkDefaultFont", 9, "bold"))
            lienzo.create_rectangle(84, posicion_y - 9, ancho - 90, posicion_y + 9,
                                    fill=COLORES["fondo_alt"], outline=COLORES["fondo_alt"])
            if cantidad > 0:
                lienzo.create_rectangle(84, posicion_y - 9, 84 + max(largo, 4), posicion_y + 9,
                                        fill=colores[prioridad], outline=colores[prioridad])
            lienzo.create_text(ancho - 74, posicion_y, anchor="w",
                               text="%d tarea%s" % (cantidad, "" if cantidad == 1 else "s"),
                               fill=COLORES["texto"], font=("TkDefaultFont", 9))

    def llenar_detalle(self):
        """Construye la tabla comparativa materia por materia."""
        filas = []
        for materia in sorted(DATOS.materias,
                              key=lambda m: str(m.get("materia", "")).lower()):
            nombre = materia.get("materia", "")
            tareas = [t for t in DATOS.tareas if t.get("materia") == nombre]
            completadas = sum(1 for t in tareas if t.get("estado") == "Completada")
            pendientes = len(tareas) - completadas

            promedio = None
            for registro in DATOS.notas:
                if str(registro.get("materia", "")).lower() == nombre.lower():
                    promedio = float(registro.get("promedio", 0))
                    break

            if promedio is None:
                texto_promedio, condicion, etiqueta = "--", "Sin notas", None
            elif promedio >= NOTA_APROBACION:
                texto_promedio, condicion, etiqueta = formato_numero(promedio), "Aprobado", "exito"
            else:
                texto_promedio, condicion, etiqueta = formato_numero(promedio), "Reprobado", "error"

            filas.append((
                materia.get("id"),
                (nombre, materia.get("creditos", 0), len(tareas), completadas,
                 pendientes, texto_promedio, condicion),
                etiqueta,
            ))
        llenar_tabla(self.tabla, filas)

    def escribir_conclusiones(self, materias, tareas, completadas,
                              pendientes, promedios, promedio_general):
        """Genera un texto interpretativo del desempeno del estudiante."""
        lineas = []

        if materias == 0:
            lineas.append("📌  Aun no hay materias registradas. Comience por el modulo "
                          "'Registrar Materias'.")
        else:
            creditos = sum(int(m.get("creditos", 0) or 0) for m in DATOS.materias)
            lineas.append("📌  Cursa %d materia(s) con un total de %d credito(s)."
                          % (materias, creditos))

        if tareas == 0:
            lineas.append("📝  No hay tareas registradas en el sistema.")
        else:
            porcentaje = completadas / float(tareas) * 100.0
            if porcentaje >= 80:
                comentario = "Excelente nivel de cumplimiento, mantenga el ritmo."
            elif porcentaje >= 50:
                comentario = "Buen avance, aun quedan entregas por cerrar."
            else:
                comentario = "Se recomienda priorizar las tareas pendientes."
            lineas.append("📝  Ha completado %d de %d tareas (%s %%). %s"
                          % (completadas, tareas, formato_numero(porcentaje, 1), comentario))

            vencidas = sum(1 for t in DATOS.tareas
                           if t.get("estado") != "Completada"
                           and dias_restantes(t.get("fecha", "")) is not None
                           and dias_restantes(t.get("fecha", "")) < 0)
            if vencidas:
                lineas.append("⚠  Tiene %d tarea(s) vencida(s) sin completar." % vencidas)

        if not promedios:
            lineas.append("🎯  Aun no ha guardado promedios. Utilice el modulo "
                          "'Calculadora de Promedios' para registrarlos.")
        else:
            aprobadas = sum(1 for p in promedios if p >= NOTA_APROBACION)
            estado = "APROBATORIO" if promedio_general >= NOTA_APROBACION else "EN RIESGO"
            lineas.append("🎯  Promedio general de %s sobre %s (%s). Materias aprobadas: %d de %d."
                          % (formato_numero(promedio_general),
                             formato_numero(NOTA_MAXIMA, 0), estado, aprobadas, len(promedios)))

        bloques = len(DATOS.horario)
        if bloques:
            minutos = sum(max(0, hora_a_minutos(b.get("fin", "")) -
                              hora_a_minutos(b.get("inicio", ""))) for b in DATOS.horario)
            lineas.append("📅  Su horario contempla %d bloque(s) con una carga semanal de "
                          "%dh %02dmin." % (bloques, minutos // 60, minutos % 60))
        else:
            lineas.append("📅  El horario semanal aun no tiene bloques registrados.")

        self.etiqueta_conclusion.configure(text="\n".join(lineas))


# =============================================================================
# SECCION 16 : MODULO 7 - INFORMACION DEL SISTEMA
# =============================================================================

def mostrar_informacion(ventana_padre):
    """
    Muestra el cuadro de dialogo institucional del proyecto (Modulo 7).

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
        "   •  Angel Nunez\n\n"
        "CATEDRA:\n"
        "   Fundamentos de Programacion\n\n"
        "TECNOLOGIA:\n"
        "   Desarrollado con Python y Tkinter\n"
        "   Python %s\n\n"
        "MODULOS DEL SISTEMA:\n"
        "   1. Registro de Materias\n"
        "   2. Control de Tareas\n"
        "   3. Calculadora de Promedios\n"
        "   4. Nota Necesaria\n"
        "   5. Horario Semanal\n"
        "   6. Estadisticas Generales\n"
        "   7. Informacion del Sistema\n\n"
        "ALMACENAMIENTO:\n"
        "   materias.json  ·  tareas.json\n"
        "   horario.json   ·  notas.json\n\n"
        "REGISTROS ACTUALES:\n"
        "   Materias: %d   |   Tareas: %d\n"
        "   Bloques de horario: %d   |   Promedios: %d"
        % (APP_NOMBRE, APP_VERSION, APP_SUBTITULO,
           sys.version.split()[0],
           len(DATOS.materias), len(DATOS.tareas),
           len(DATOS.horario), len(DATOS.notas))
    )
    messagebox.showinfo("Informacion del Sistema", detalle, parent=ventana_padre)


# =============================================================================
# SECCION 17 : VENTANA PRINCIPAL (MENU DEL SISTEMA)
# =============================================================================
# Pantalla de inicio de Study Control. Contiene el encabezado institucional,
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
        # ------------------- Barra negra superior (institucional) ------------
        barra, self.etiqueta_reloj = crear_barra_institucional(self.raiz)
        barra.pack(fill="x")
        iniciar_reloj(self.raiz, self.etiqueta_reloj)

        # Linea degradada simulada con tres franjas de color.
        franja = tk.Frame(self.raiz, bg=COLORES["fondo"], height=4)
        franja.pack(fill="x")
        franja.pack_propagate(False)
        tk.Frame(franja, bg=COLORES["morado_oscuro"]).place(relx=0.0, relwidth=0.34, relheight=1)
        tk.Frame(franja, bg=COLORES["morado"]).place(relx=0.34, relwidth=0.33, relheight=1)
        tk.Frame(franja, bg=COLORES["cian"]).place(relx=0.67, relwidth=0.33, relheight=1)

        # ------------------------- Bloque de titulo --------------------------
        hero = tk.Frame(self.raiz, bg=COLORES["fondo_alt"], height=168)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        contenido = tk.Frame(hero, bg=COLORES["fondo_alt"])
        contenido.pack(expand=True)

        # Titulo grande y centrado: STUDY CONTROL
        titulo = tk.Frame(contenido, bg=COLORES["fondo_alt"])
        titulo.pack()
        tk.Label(titulo, text="🎓", bg=COLORES["fondo_alt"], fg=COLORES["morado_claro"],
                 font=FUENTES["titulo_grande"]).pack(side="left", padx=(0, 14))
        tk.Label(titulo, text="STUDY CONTROL", bg=COLORES["fondo_alt"],
                 fg=COLORES["blanco"], font=FUENTES["titulo_gigante"]).pack(side="left")

        # Subtitulo descriptivo del sistema.
        tk.Label(contenido, text=APP_SUBTITULO, bg=COLORES["fondo_alt"],
                 fg=COLORES["morado_claro"], font=FUENTES["subtitulo"]).pack(pady=(4, 0))

        # Separador decorativo entre el subtitulo y los creditos.
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
                 fg=COLORES["texto_tenue"], font=FUENTES["pequena"]).pack(pady=(2, 0))

    # =========================================================================
    # MENU PRINCIPAL
    # =========================================================================
    def definicion_de_modulos(self):
        """
        Devuelve la definicion de las ocho opciones del menu principal.

        Cada elemento contiene: icono, titulo, descripcion, comando y color.
        Tener la definicion en un solo lugar evita repetir codigo al crear
        las tarjetas y facilita agregar nuevos modulos en el futuro.
        """
        return [
            ("📚", "Registrar Materias", "Asignaturas, docentes y creditos",
             self.abrir_materias, COLORES["morado"]),
            ("📝", "Control de Tareas", "Deberes, fechas y prioridades",
             self.abrir_tareas, COLORES["cian"]),
            ("📊", "Calculadora de Promedios", "Analisis de sus calificaciones",
             self.abrir_promedios, COLORES["azul_claro"]),
            ("🎯", "Nota Necesaria", "Proyeccion para el examen final",
             self.abrir_nota_necesaria, COLORES["alerta"]),
            ("📅", "Horario", "Bloques de clase semanales",
             self.abrir_horario, COLORES["azul"]),
            ("📈", "Estadisticas", "Indicadores automaticos",
             self.abrir_estadisticas, COLORES["exito"]),
            ("👤", "Informacion", "Datos del proyecto y autores",
             self.abrir_informacion, COLORES["morado_claro"]),
            ("🚪", "Salir", "Cerrar la aplicacion",
             self.salir, COLORES["error"]),
        ]

    def construir_menu(self):
        """Dibuja la rejilla de tarjetas del menu principal (4 x 2)."""
        contenedor = tk.Frame(self.raiz, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True, padx=26, pady=18)

        # Titulo pequeno de la seccion del menu.
        cabecera = tk.Frame(contenedor, bg=COLORES["fondo"])
        cabecera.pack(fill="x", pady=(0, 12))
        tk.Label(cabecera, text="MENU PRINCIPAL", bg=COLORES["fondo"],
                 fg=COLORES["texto_suave"], font=FUENTES["pequena_bold"]).pack(side="left")
        tk.Label(cabecera, text="Seleccione un modulo para comenzar",
                 bg=COLORES["fondo"], fg=COLORES["texto_tenue"],
                 font=FUENTES["pequena"]).pack(side="left", padx=(12, 0))
        tk.Label(cabecera, text="F1: Informacion    ·    Esc: Salir",
                 bg=COLORES["fondo"], fg=COLORES["texto_tenue"],
                 font=FUENTES["micro"]).pack(side="right")

        rejilla = tk.Frame(contenedor, bg=COLORES["fondo"])
        rejilla.pack(fill="both", expand=True)

        # Cuatro columnas de igual ancho y dos filas de igual alto.
        for columna in range(4):
            rejilla.grid_columnconfigure(columna, weight=1, uniform="columna")
        for fila in range(2):
            rejilla.grid_rowconfigure(fila, weight=1, uniform="fila")

        for indice, (icono, titulo, descripcion, comando, color) in \
                enumerate(self.definicion_de_modulos()):
            tarjeta = TarjetaMenu(rejilla, icono, titulo, descripcion, comando, color)
            tarjeta.grid(row=indice // 4, column=indice % 4, sticky="nsew", padx=7, pady=7)

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
            completadas = sum(1 for t in DATOS.tareas if t.get("estado") == "Completada")
            promedios = [float(n.get("promedio", 0)) for n in DATOS.notas]
            texto_promedio = (formato_numero(promedio_de(promedios)) if promedios else "--")

            self.etiqueta_resumen.configure(
                text="📚 Materias: %d      📝 Tareas: %d  (✅ %d)      "
                     "📅 Bloques: %d      🎯 Promedio general: %s"
                     % (len(DATOS.materias), len(DATOS.tareas), completadas,
                        len(DATOS.horario), texto_promedio)
            )
        except tk.TclError as error:
            print("[Study Control] No se pudo refrescar el resumen: %s" % error)

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
    def abrir_tareas(self):
        """Modulo 2: Control de Tareas."""
        self.abrir_ventana(VentanaTareas)

    @manejar_errores
    def abrir_promedios(self):
        """Modulo 3: Calculadora de Promedios."""
        self.abrir_ventana(VentanaPromedios)

    @manejar_errores
    def abrir_nota_necesaria(self):
        """Modulo 4: Nota Necesaria."""
        self.abrir_ventana(VentanaNotaNecesaria)

    @manejar_errores
    def abrir_horario(self):
        """Modulo 5: Horario Semanal."""
        self.abrir_ventana(VentanaHorario)

    @manejar_errores
    def abrir_estadisticas(self):
        """Modulo 6: Estadisticas Generales."""
        self.abrir_ventana(VentanaEstadisticas)

    @manejar_errores
    def abrir_informacion(self):
        """Modulo 7: Informacion del sistema (MessageBox institucional)."""
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
# SECCION 18 : PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================================

def crear_archivos_si_no_existen():
    """
    Garantiza que los cuatro archivos JSON existan desde el primer arranque.

    Si no existen se crean vacios, de modo que el usuario pueda verlos en la
    carpeta del proyecto y el programa nunca falle al intentar leerlos.
    """
    for ruta in (ARCHIVO_MATERIAS, ARCHIVO_TAREAS, ARCHIVO_HORARIO, ARCHIVO_NOTAS):
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

    print("[Study Control] Aplicacion iniciada correctamente.")
    print("[Study Control] Registros cargados -> materias: %d | tareas: %d | "
          "horario: %d | promedios: %d"
          % (len(DATOS.materias), len(DATOS.tareas), len(DATOS.horario), len(DATOS.notas)))

    # 5) Bucle principal protegido: ningun error cierra la aplicacion en seco.
    try:
        raiz.mainloop()
    except KeyboardInterrupt:
        print("[Study Control] Ejecucion interrumpida por el usuario.")
    finally:
        DATOS.guardar_todo()
        print("[Study Control] Informacion guardada. Hasta pronto.")

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
                "Study Control no pudo iniciarse correctamente.\n\nDetalle: %s" % error_general
            )
        except Exception:
            print("[Study Control] Error critico: %s" % error_general)
