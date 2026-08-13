# -*- coding: utf-8 -*-
"""
===============================================================================
 M O D U L O   1   -   R E G I S T R O   D E   M A T E R I A S
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Ventana para registrar, editar y eliminar las asignaturas del
 semestre, con su docente, aula y numero de creditos.
===============================================================================
"""

import json                                # Persistencia de datos en JSON

import tkinter as tk                        # Nucleo de la interfaz grafica

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import COLORES, FUENTES, MATERIAS_DISPONIBLES
from utilidades import (
    limpiar_seleccion, manejar_errores, validar_opcion, validar_texto)
from datos import DATOS
from interfaz import (
    BotonModerno, CampoFormulario, VentanaModulo, crear_tabla,
    crear_titulo_seccion, llenar_tabla, obtener_id_seleccionado)


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
# AVISO PARA QUIEN EJECUTE ESTE ARCHIVO POR EQUIVOCACION
# =============================================================================
# Este archivo es una PIEZA del Sistema de Estudio: guarda la ventana del Modulo 1
# y por si solo no abre ninguna ventana. El programa se inicia siempre desde
# study_control.py. El bloque de abajo solo sirve para avisarlo con claridad.
# =============================================================================

if __name__ == "__main__":
    print("")
    print("  Este archivo (modulo_materias.py) es una pieza del Sistema de Estudio.")
    print("  Por si solo no abre ninguna ventana.")
    print("")
    print("  Para iniciar el programa ejecute:")
    print("")
    print("      python study_control.py")
    print("")
