# -*- coding: utf-8 -*-
"""
===============================================================================
 C O M P O N E N T E S   D E   I N T E R F A Z
===============================================================================
 Sistema de Estudio - Pontificia Universidad Catolica del Ecuador (Ambato)
 Catedra: Fundamentos de Programacion
 -----------------------------------------------------------------------------
 Piezas visuales reutilizadas por los cuatro modulos: estilos ttk,
 botones, tarjetas, formularios, tablas, el logo institucional y la
 ventana base de la que heredan todos los modulos.
===============================================================================
"""

import os                                  # Rutas y verificacion de archivos
import io                                  # Lectura del logo incrustado en memoria
import base64                              # Decodifica el logo incrustado en el codigo

import tkinter as tk                        # Nucleo de la interfaz grafica
from tkinter import ttk                     # Componentes con estilo (ttk)
from tkinter import messagebox              # Cuadros de dialogo del sistema

# Pillow es opcional: si esta instalado permite leer el logo en JPG/JPEG
# ademas de PNG. Si no esta, el programa funciona igual con tk.PhotoImage.
try:
    from PIL import Image, ImageTk          # Soporte extendido de imagenes
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

# --------------------- Modulos propios del proyecto ---------------------
from configuracion import (
    APP_AUTORES, APP_CATEDRA, APP_NOMBRE, APP_UNIVERSIDAD, CARPETA_BASE,
    COLORES, FUENTES, IMAGENES_EN_MEMORIA, NOMBRES_LOGO, VENTANA_ALTO,
    VENTANA_ANCHO)
from utilidades import (
    centrar_ventana, contraste_de, ejecutar_seguro, manejar_errores)


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


# =============================================================================
# LOGOTIPO INSTITUCIONAL INCRUSTADO
# =============================================================================
# El escudo oficial de la PUCE Ambato (PNG de 240x240 px) esta guardado aqui
# convertido a texto con la codificacion base64. Se hizo asi para que el logo
# viaje DENTRO del programa: aunque se copie unicamente study_control.py a
# otro computador, el encabezado seguira mostrando el escudo de la
# universidad. Si ademas existe un archivo de imagen en la carpeta (ver
# NOMBRES_LOGO), ese archivo tiene prioridad y este texto queda de respaldo.
# =============================================================================

LOGO_PUCE_BASE64 = """
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
"""


def logo_desde_codigo(tamano=70):
    """
    Construye el logo de la PUCE Ambato a partir de LOGO_PUCE_BASE64.

    A diferencia de cargar_imagen_logo(), esta version NO depende de ningun
    archivo externo: la imagen viaja dentro del propio study_control.py. Por
    eso el escudo se ve aunque el programa se copie solo, se envie por correo
    o se ejecute desde otra carpeta.
    """
    datos = "".join(LOGO_PUCE_BASE64.split())      # Quita saltos de linea

    # --------- Intento 1: Pillow (mejor calidad de reduccion) ---------
    if PIL_DISPONIBLE:
        try:
            imagen_pil = Image.open(io.BytesIO(base64.b64decode(datos))).convert("RGB")
            imagen_pil.thumbnail((tamano, tamano), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(imagen_pil)
            IMAGENES_EN_MEMORIA.append(imagen)
            print("[Sistema de Estudio] Logo incrustado cargado con Pillow.")
            return imagen
        except Exception as error:
            print("[Sistema de Estudio] Logo incrustado: fallo Pillow (%s)" % error)

    # --------- Intento 2: Tkinter nativo (acepta PNG en base64) ---------
    try:
        imagen = tk.PhotoImage(data=datos)
        factor = max(1, int(max(imagen.width(), imagen.height()) / float(tamano)))
        if factor > 1:
            imagen = imagen.subsample(factor, factor)
        IMAGENES_EN_MEMORIA.append(imagen)
        print("[Sistema de Estudio] Logo incrustado cargado con Tkinter.")
        return imagen
    except tk.TclError as error:
        print("[Sistema de Estudio] Logo incrustado: fallo Tkinter (%s)" % error)

    return None


def cargar_imagen_logo(tamano=70):
    """
    Obtiene el logotipo institucional para el encabezado.

    Orden de busqueda:
      1. Un archivo de imagen (NOMBRES_LOGO) junto al script, por si el
         estudiante quiere reemplazar el escudo por otra version.
      2. El logo incrustado en el propio codigo (LOGO_PUCE_BASE64), que
         siempre esta disponible.

    Solo devuelve None si ambas vias fallan, y en ese caso el encabezado
    dibuja un marcador de posicion. Se imprime en consola que se probo y por
    que fallo, para poder diagnosticar facilmente cualquier problema.
    """
    print("[Sistema de Estudio] Buscando logo en:", CARPETA_BASE)
    intentos = []
    for nombre in NOMBRES_LOGO:
        ruta = os.path.join(CARPETA_BASE, nombre)
        if not os.path.exists(ruta):
            intentos.append("%s -> no existe" % nombre)
            continue

        # --------- Intento 1: Pillow (soporta PNG, JPG, JPEG, etc.) ---------
        if PIL_DISPONIBLE:
            try:
                imagen_pil = Image.open(ruta).convert("RGB")
                imagen_pil.thumbnail((tamano, tamano), Image.LANCZOS)
                imagen = ImageTk.PhotoImage(imagen_pil)
                IMAGENES_EN_MEMORIA.append(imagen)
                print("[Sistema de Estudio] Logo cargado con Pillow:", ruta)
                return imagen
            except Exception as error:
                intentos.append("%s -> error con Pillow: %s" % (nombre, error))
                continue

        # --------- Intento 2: tk.PhotoImage nativo (solo PNG/GIF) ---------
        try:
            imagen = tk.PhotoImage(file=ruta)
            factor = max(1, int(max(imagen.width(), imagen.height()) / float(tamano)))
            if factor > 1:
                imagen = imagen.subsample(factor, factor)
            IMAGENES_EN_MEMORIA.append(imagen)
            print("[Sistema de Estudio] Logo cargado con Tkinter:", ruta)
            return imagen
        except tk.TclError as error:
            intentos.append("%s -> error con Tkinter: %s" % (nombre, error))
            continue

    print("[Sistema de Estudio] No se hallo archivo de logo en la carpeta. Detalle:")
    for detalle in intentos:
        print("   -", detalle)
    if not PIL_DISPONIBLE:
        print("[Sistema de Estudio] Sugerencia: instala Pillow para leer JPG/JPEG -> pip install Pillow")

    # Ningun archivo sirvio: se usa el logo que viene dentro del codigo.
    print("[Sistema de Estudio] Se usara el logo incrustado en el programa.")
    return logo_desde_codigo(tamano)


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
# AVISO PARA QUIEN EJECUTE ESTE ARCHIVO POR EQUIVOCACION
# =============================================================================
# Este archivo es una PIEZA del Sistema de Estudio: guarda los componentes visuales reutilizables
# y por si solo no abre ninguna ventana. El programa se inicia siempre desde
# study_control.py. El bloque de abajo solo sirve para avisarlo con claridad.
# =============================================================================

if __name__ == "__main__":
    print("")
    print("  Este archivo (interfaz.py) es una pieza del Sistema de Estudio.")
    print("  Por si solo no abre ninguna ventana.")
    print("")
    print("  Para iniciar el programa ejecute:")
    print("")
    print("      python study_control.py")
    print("")
