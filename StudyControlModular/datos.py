# -*- coding: utf-8 -*-
"""
===============================================================================
 C A P A   D E   D A T O S
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Todo lo relacionado con guardar y recuperar informacion en los
 archivos materias.json, horario.json y notas.json. Ningun otro modulo
 abre archivos directamente: todos pasan por aqui.
===============================================================================
"""

import os                                  # Rutas y verificacion de archivos
import json                                # Persistencia de datos en JSON

from tkinter import messagebox              # Cuadros de dialogo del sistema

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import ARCHIVO_HORARIO, ARCHIVO_MATERIAS, ARCHIVO_NOTAS


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


def crear_archivos_si_no_existen():
    """
    Garantiza que los tres archivos JSON existan desde el primer arranque.

    Si no existen se crean vacios, de modo que el usuario pueda verlos en la
    carpeta del proyecto y el programa nunca falle al intentar leerlos.
    """
    for ruta in (ARCHIVO_MATERIAS, ARCHIVO_HORARIO, ARCHIVO_NOTAS):
        if not os.path.exists(ruta):
            escribir_json(ruta, [])

# =============================================================================
# AVISO PARA QUIEN EJECUTE ESTE ARCHIVO POR EQUIVOCACION
# =============================================================================
# Este archivo es una PIEZA del Sistema de Estudio: guarda la lectura y escritura de los archivos JSON
# y por si solo no abre ninguna ventana. El programa se inicia siempre desde
# study_control.py. El bloque de abajo solo sirve para avisarlo con claridad.
# =============================================================================

if __name__ == "__main__":
    print("")
    print("  Este archivo (datos.py) es una pieza del Sistema de Estudio.")
    print("  Por si solo no abre ninguna ventana.")
    print("")
    print("  Para iniciar el programa ejecute:")
    print("")
    print("      python study_control.py")
    print("")
