# -*- coding: utf-8 -*-
"""
===============================================================================
 M O D U L O   2   -   H O R A R I O   S E M A N A L
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Ventana para armar el horario de clases por dia y hora, detectando
 los cruces entre bloques.
===============================================================================
"""

import json                                # Persistencia de datos en JSON
import datetime                            # Fechas, horas y reloj del sistema

import tkinter as tk                        # Nucleo de la interfaz grafica
from tkinter import ttk                     # Componentes con estilo (ttk)

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import COLORES, DIAS_SEMANA, FUENTES, MATERIAS_DISPONIBLES
from utilidades import (
    hora_a_minutos, limpiar_seleccion, manejar_errores, validar_hora,
    validar_opcion, validar_texto)
from datos import DATOS
from interfaz import (
    BotonModerno, CampoFormulario, VentanaModulo, crear_tabla,
    crear_titulo_seccion, llenar_tabla, obtener_id_seleccionado)


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
# AVISO PARA QUIEN EJECUTE ESTE ARCHIVO POR EQUIVOCACION
# =============================================================================
# Este archivo es una PIEZA del Sistema de Estudio: guarda la ventana del Modulo 2
# y por si solo no abre ninguna ventana. El programa se inicia siempre desde
# study_control.py. El bloque de abajo solo sirve para avisarlo con claridad.
# =============================================================================

if __name__ == "__main__":
    print("")
    print("  Este archivo (modulo_horario.py) es una pieza del Sistema de Estudio.")
    print("  Por si solo no abre ninguna ventana.")
    print("")
    print("  Para iniciar el programa ejecute:")
    print("")
    print("      python study_control.py")
    print("")
