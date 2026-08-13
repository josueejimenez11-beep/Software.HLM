# -*- coding: utf-8 -*-
"""
===============================================================================
 M O D U L O   4   -   I N F O R M A C I O N
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Cuadro de dialogo con los datos del proyecto, los autores y la
 version del programa.
===============================================================================
"""

import sys                                 # Informacion del interprete

from tkinter import messagebox              # Cuadros de dialogo del sistema

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import APP_NOMBRE, APP_SUBTITULO, APP_VERSION
from datos import DATOS


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
        "   •  Angel Nuñez\n\n"
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
# AVISO PARA QUIEN EJECUTE ESTE ARCHIVO POR EQUIVOCACION
# =============================================================================
# Este archivo es una PIEZA del Sistema de Estudio: guarda el cuadro de dialogo del Modulo 4
# y por si solo no abre ninguna ventana. El programa se inicia siempre desde
# study_control.py. El bloque de abajo solo sirve para avisarlo con claridad.
# =============================================================================

if __name__ == "__main__":
    print("")
    print("  Este archivo (modulo_informacion.py) es una pieza del Sistema de Estudio.")
    print("  Por si solo no abre ninguna ventana.")
    print("")
    print("  Para iniciar el programa ejecute:")
    print("")
    print("      python study_control.py")
    print("")
