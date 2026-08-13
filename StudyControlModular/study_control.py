# -*- coding: utf-8 -*-
"""
===============================================================================
 P R O G R A M A   P R I N C I P A L
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Archivo que se ejecuta:  python study_control.py
 Construye el menu principal, enlaza los cuatro modulos y arranca el
 bucle de eventos de Tkinter.
 -----------------------------------------------------------------------------
 ORGANIZACION DEL PROYECTO
 -----------------------------------------------------------------------------
 El programa esta repartido en nueve archivos, cada uno con una sola
 responsabilidad. Cada archivo solo usa a los que estan por encima suyo, de
 modo que la dependencia siempre va en un sentido y nunca en circulo:

   configuracion.py        Colores, medidas, rutas y escala de notas
   utilidades.py           Tipografias, validaciones y calculos de apoyo
   datos.py                Lectura y escritura de los archivos JSON
   interfaz.py             Estilos, botones, tablas, logo y ventana base
   modulo_materias.py      Modulo 1 - Registro de materias
   modulo_horario.py       Modulo 2 - Horario semanal
   modulo_promedios.py     Modulo 3 - Calculadora de promedios
   modulo_informacion.py   Modulo 4 - Informacion del sistema
   study_control.py        Menu principal y arranque (este archivo)

 Los nueve archivos deben estar en la misma carpeta junto a los archivos
 materias.json, horario.json y notas.json.
===============================================================================
"""

import traceback                           # Reporte detallado de errores

import tkinter as tk                        # Nucleo de la interfaz grafica
from tkinter import ttk                     # Componentes con estilo (ttk)
from tkinter import messagebox              # Cuadros de dialogo del sistema

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import (
    APP_AUTORES, APP_CATEDRA, APP_NOMBRE, APP_SUBTITULO, APP_VERSION,
    COLORES, FUENTES, VENTANA_ALTO, VENTANA_ANCHO)
from utilidades import (
    centrar_ventana, configurar_fuentes, formato_numero, manejar_errores,
    promedio_de)
from datos import DATOS, crear_archivos_si_no_existen
from interfaz import (
    BotonModerno, TarjetaMenu, aplicar_estilos, crear_barra_institucional)
from modulo_materias import VentanaMaterias
from modulo_horario import VentanaHorario
from modulo_promedios import VentanaPromedios
from modulo_informacion import mostrar_informacion


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
