# -*- coding: utf-8 -*-
"""
===============================================================================
 M O D U L O   3   -   C A L C U L A D O R A   D E   P R O M E D I O S
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Ventana que calcula el promedio de una materia, su nota mayor y
 menor, y determina si el estudiante aprueba.
===============================================================================
"""

import json                                # Persistencia de datos en JSON
import datetime                            # Fechas, horas y reloj del sistema

import tkinter as tk                        # Nucleo de la interfaz grafica

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import (
    COLORES, ESCALA_LITERAL, FUENTES, MATERIAS_DISPONIBLES, NOTA_APROBACION,
    NOTA_MAXIMA, NOTA_MINIMA)
from utilidades import (
    evaluar_nota, formato_numero, manejar_errores, promedio_de,
    validar_lista_de_notas)
from datos import DATOS
from interfaz import (
    BotonModerno, CampoFormulario, TarjetaIndicador, VentanaModulo,
    crear_tabla, crear_titulo_seccion, llenar_tabla, obtener_id_seleccionado)


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
