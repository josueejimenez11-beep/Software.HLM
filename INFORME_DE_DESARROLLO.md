# Informe de desarrollo y modificaciones

## Sistema de Estudio

**Pontificia Universidad Católica del Ecuador**
Cátedra: Fundamentos de Programación
Autores: Steveen Culquicondor — Ángel Núñez
Tecnología: Python 3 · Tkinter · ttk
Archivo: `study_control.py`

---

## 1. Creación del programa

El proyecto nació como una aplicación de escritorio destinada a que un estudiante
universitario administre su semestre desde un solo lugar, sin depender de internet ni
de programas de pago. Se eligió Python 3 con la biblioteca gráfica Tkinter y sus
componentes con estilo `ttk`, de modo que el programa funcione en cualquier computador
con Python instalado, sin librerías externas.

La primera versión se construyó en un único archivo llamado `study_control.py`, con una
ventana fija de 1100 × 700 píxeles, centrada en la pantalla, y siete módulos que se
abrían en ventanas independientes mediante `Toplevel`: registro de materias, control de
tareas, calculadora de promedios, cálculo de la nota necesaria, horario semanal,
estadísticas generales e información del sistema. Toda la información se guardaba de
forma automática en archivos JSON ubicados junto al programa, y se volvía a cargar sola
al iniciar la aplicación.

Desde el inicio el código se organizó por secciones numeradas y comentadas, separando la
configuración global, la capa de guardado en archivos, las validaciones, los componentes
visuales reutilizables y los módulos propiamente dichos. Esa organización fue la que
después permitió modificar el sistema varias veces sin romperlo.

---

## 2. Primera modificación: rediseño e identidad del sistema

Con la aplicación ya funcionando, se decidió cambiar por completo su apariencia y reducir
su alcance a lo que realmente se iba a utilizar.

El programa pasó a llamarse **Sistema de Estudio**, con el título centrado en la pantalla
principal y sin el ícono de birrete que lo acompañaba. La paleta se rehízo con fondo
negro, letras blancas y bordes en celeste claro, y se retiraron los emojis de los botones
de acción, de manera que la interfaz quedara más sobria y formal.

El menú principal se redujo a cuatro módulos —Registro de Materias, Horario, Calculadora
de Promedios e Información—, ordenados en una sola fila, con el botón de salida separado
del resto porque no abre ninguna ventana. Los módulos de tareas, nota necesaria y
estadísticas se eliminaron junto con todo el código que solo ellos utilizaban, para no
dejar partes muertas dentro del archivo. En el registro de materias se suprimió el campo
de créditos, con su validación, su columna en la tabla y el total acumulado.

Durante la revisión de esta etapa aparecieron dos problemas reales que hubo que corregir.
El primero era que las ventanas de los módulos se declaraban como *transient* de la
ventana principal: al ocultar el menú, Tkinter ocultaba también la ventana hija, de modo
que el módulo podía no aparecer nunca. El segundo era de contraste: varios botones
quedaban con texto blanco sobre fondo claro, prácticamente ilegibles. Para resolverlo se
programó la función `contraste_de()`, que calcula la luminancia del color de fondo y
decide si la letra debe ser negra o blanca; se aplica al estado normal, al efecto *hover*
y a la fila seleccionada de las tablas.

---

## 3. Segunda modificación: fondo gris, materias fijas y barra simplificada

La siguiente ronda de cambios partió de la aplicación ya en funcionamiento sobre Windows.

El fondo general pasó al **gris 18 %** (`#808080`), el gris medio fotográfico. Como el
texto blanco pierde contraste sobre un gris claro, los paneles, tablas y campos se
colocaron en grises más oscuros, de modo que la lectura siguiera siendo cómoda; los
títulos grandes se mantuvieron en blanco y el texto secundario que se apoya directamente
sobre el gris pasó a un tono oscuro.

De la barra superior se eliminaron la fecha, la hora y la leyenda «Sistema Académico
v1.0», junto con la función del reloj que las actualizaba cada segundo. El subtítulo del
título principal se cambió por «Sistema Inteligente para la Gestión PUCE».

El cambio de fondo se acompañó de una mejora en el ingreso de datos: las materias dejaron
de escribirse a mano y pasaron a escogerse de una lista fija de ocho asignaturas del
semestre —Sistemas Operativos, Habilidades Lógico Matemáticas, Segunda Lengua,
Introducción al Desarrollo Web, Álgebra, Fundamentos de Programación, Herramientas
Digitales Aplicadas y Comunicación Oral y Escrita—. La lista es la misma en los tres
módulos, así que el nombre de una materia siempre queda escrito igual y las tablas nunca
guardan dos versiones del mismo nombre.

---

## 4. Tercera modificación: escala de calificación literal

La última modificación cambió la forma de calificar. La calculadora de promedios trabajaba
sobre una escala de 0 a 20; ahora trabaja sobre una escala de **0 a 50 con calificación
por letras**:

| Rango | Letra | Resultado |
|-------|-------|-----------|
| 0 – 20 | D | Reprueba |
| 21 – 30 | C | Aprobado, estudia más |
| 31 – 40 | B | Aprobado |
| 41 – 50 | A | Aprobado |

Para que la escala fuera fácil de mantener se definió en una sola lista, `ESCALA_LITERAL`,
y una función `evaluar_nota()` que traduce cualquier calificación numérica a su letra, a
si aprueba o no, y a su comentario. Esa función es la única fuente de la equivalencia: la
usan el veredicto, las tarjetas de resultado, la lista ordenada de notas y el historial de
promedios. Si algún día cambian los cortes o las letras, basta con modificar esa lista y
todo lo demás se ajusta solo.

En pantalla, el panel izquierdo muestra la leyenda de la escala construida a partir de esa
misma lista; las tarjetas de promedio, nota mayor y nota menor muestran el número junto a
su letra; la lista de notas reemplazó la columna de diferencia por las columnas Letra y
Resultado; y el historial guarda la letra dentro de `notas.json`. Además, el ingreso de
notas pasó a validar el rango de 0 a 50. En esta misma etapa el subtítulo quedó como
«Sistema de Gestión PUCE».

---

## 5. Estado final del programa

| Aspecto | Versión inicial | Versión final |
|---------|-----------------|---------------|
| Nombre | Study Control | Sistema de Estudio |
| Módulos | 7 | 4 |
| Archivos JSON | 4 | 3 |
| Líneas de código | 4140 | 2925 |
| Paleta | Azul oscuro y morado | Gris 18 %, blanco y celeste |
| Escala de notas | 0 a 20 numérica | 0 a 50 con letras A, B, C, D |

El programa quedó organizado en 15 secciones comentadas, con 128 funciones y métodos, sin
funciones vacías ni partes sin terminar. Conserva las características que se fijaron desde
el principio: ventana fija de 1100 × 700 centrada, validaciones que impiden campos vacíos
o letras donde deben ir números, mensajes de error mediante cuadros de diálogo, protección
frente a errores inesperados para que la aplicación no se cierre sola, confirmación antes
de salir y guardado automático en archivos JSON que se cargan al iniciar.

Cada versión se comprobó ejecutando la aplicación y recorriendo sus módulos con una
batería de 68 comprobaciones automáticas que verifican el guardado y la recarga de los
archivos, las validaciones, los cálculos, los colores y el comportamiento de los botones.

Para ejecutarlo basta con abrir la carpeta en Visual Studio Code y escribir en la terminal:

```
python study_control.py
```

Los archivos `materias.json`, `horario.json` y `notas.json` se crean solos la primera vez
que se abre el programa.
