# -*- coding: utf-8 -*-
"""
===============================================================================
 C O N F I G U R A C I O N   G L O B A L
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Valores constantes de todo el programa: paleta de colores, medidas de
 las ventanas, rutas de los archivos JSON, escala de calificaciones y
 lista de materias. Cambiar algo aqui cambia la apariencia completa de
 la aplicacion, sin tocar ningun otro archivo.
===============================================================================
"""

import os                                  # Rutas y verificacion de archivos


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
APP_AUTORES = "STEVEEN CULQUICONDOR  -  ANGEL NUÑEZ  -  RICARDO GARRIDO"
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
    (29.0, "D", False, "Reprueba"),
    (30.0, "C", True, "Aprobado, estudia mas >:["),
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
# El usuario puede colocar cualquiera de estos archivos junto al script y
# la aplicacion lo cargara automaticamente en el encabezado. Los formatos
# JPG/JPEG solo se pueden leer si Pillow esta instalado (ver PIL_DISPONIBLE).
NOMBRES_LOGO = (
    "logo.png", "puce.png", "logo_puce.png", "logo_puce.PNG",
    "PUCE.png", "PUCE.jpg", "PUCE.jpeg", "logo.jpg", "logo.jpeg", "puce.jpg",
)

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
