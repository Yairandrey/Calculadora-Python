import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re


# LÓGICA Y BACKEND


def verificar_parentesis(cadena):
    contador = 0

    for caracter in cadena:
        if caracter == "(":
            contador += 1
        elif caracter == ")":
            contador -= 1
            if contador < 0:
                return False

    return contador == 0


def newton_raphson():
    global x_next
    funcion_str = text_one.get()
    x = text_two.get()
    error = text_three.get()

    # Validación de la función

    if not funcion_str:
        messagebox.showerror("Error", "Ingresa una función.")
        return
    else:
        if not re.fullmatch(
            r"[\s*xXE*^+\-\/0-9()\.]+|(\b(sin|cos|tan|log|ln|exp|sqrt|E)\b[\s*()\d\.,xX^+\-\/]*)*",
            funcion_str,
        ):
            messagebox.showerror("Error", "La función solo debe contener la variable x")
            return

    if not verificar_parentesis(funcion_str):
        messagebox.showerror("Error", "Paréntesis incorrectos")
        return

    # Valido que solo se permitan numeros
    if not x:
        messagebox.showerror("Error", "Ingresa un valor para x.")

    else:
        try:
            x = float(x)
        except Exception as e:
            messagebox.showerror("Error", f"Error {e}")
            return

    if not error:
        messagebox.showerror("Error", "Ingresa un error relativo porcentual.")
        return
    else:
        try:
            error = float(error)
        except Exception as e:
            messagebox.showerror("Error", f"Error {e}")
            return

    # Defino variable a x
    variable_x = sp.Symbol("x")

    # Convierto a sympy la funcion ingresada
    funcion_sympy = sp.sympify(funcion_str)

    # Calculo la derivada de la función
    derivada = sp.diff(funcion_sympy, variable_x)
    print(derivada)

    # Paso a funciones lambda la funcion y su derivada

    funcion_lambda = sp.lambdify(variable_x, funcion_sympy)
    derivada_lambda = sp.lambdify(variable_x, derivada)

    # Inicializo el porcentaje de error relativo porcentual
    percent_error = 100.0000

    # matriz de la información
    data = []

    # Iterador
    i = 0

    # Parseo a float el error y la aproximación actual
    x_prev = round(x, 4)
    error = round(error, 4)

    # Ciclo para calcular el método
    while percent_error > error:
        # Caclulo la nueva aproximación
        try:
            if funcion_lambda(x_prev) == RuntimeWarning:
                messagebox.showerror(
                    "Error",
                    f"El valor {x_prev} en la funció real {funcion_str}  no existe",
                )
                data.append(
                    [
                        i,
                        round(x_prev, 4),
                        round(funcion_lambda(x_prev), 4),
                        round(derivada_lambda(x_prev), 4),
                        percent_error,
                    ]
                )
                break
            elif derivada_lambda(x_prev) == RuntimeWarning:
                messagebox.showerror(
                    "Error",
                    f"El valor {x_prev} en la derivada de {funcion_str}  no existe",
                )
                data.append(
                    [
                        i,
                        round(x_prev, 4),
                        round(funcion_lambda(x_prev), 4),
                        round(derivada_lambda(x_prev), 4),
                        percent_error,
                    ]
                )
                break
            x_next = round(
                x_prev - (funcion_lambda(x_prev) / derivada_lambda(x_prev)), 4
            )

            print(x_prev, funcion_lambda(x_prev), derivada_lambda(x_prev))
        except ZeroDivisionError:
            messagebox.showerror(
                "Error", f"La derivada {derivada} evaluadada en {x} da cero"
            )
            data.append(
                [
                    i,
                    round(x_prev, 4),
                    round(funcion_lambda(x_prev), 4),
                    round(derivada_lambda(x_prev), 4),
                    percent_error,
                ]
            )
            break
        except Exception as e:
            messagebox.showerror("Error", "Error")
            data.append(
                [
                    i,
                    round(x_prev, 4),
                    round(funcion_lambda(x_prev), 4),
                    round(derivada_lambda(x_prev), 4),
                    percent_error,
                ]
            )
            break
        if np.isnan(x_next):
            data.append([i, "", "", "", "", ""])
            messagebox.showinfo("aviso", "Intenta cambiar el valor inicial")
            break
        if x_next == 0.0000 and i == 0:
            messagebox.showerror("Error", f"No se puede dividir por cero")
            data.append(
                [
                    i,
                    round(x_prev, 4),
                    round(funcion_lambda(x_prev), 4),
                    round(derivada_lambda(x_prev), 4),
                    "------",
                ]
            )
            break
        elif x_next == 0.0000:
            messagebox.showerror("Error", f"No se puede dividir por cero")
            data.append(
                [
                    i,
                    round(x_prev, 4),
                    round(funcion_lambda(x_prev), 4),
                    round(derivada_lambda(x_prev), 4),
                    percent_error,
                ]
            )
            break
        # Calculo el error relativo porcentual
        if i != 0:
            try:
                percent_error = round(
                    ((x_prev - data[i - 1][1]) / x_prev) * 100.0000, 4
                )
            except ZeroDivisionError:
                messagebox.showerror(
                    "Error",
                    f"Intentando calcular error relativo porcentual"
                    f" y la división por por 0 es imposible",
                )
                data.append(
                    [
                        i,
                        round(x_prev, 4),
                        round(funcion_lambda(x_prev), 4),
                        round(derivada_lambda(x_prev), 4),
                        percent_error,
                    ]
                )
                break
            except Exception as e:
                messagebox.showerror("Error", "Error")

        if percent_error < 0:
            percent_error = round(percent_error * (-1), 4)

        if i == 0:
            data.append(
                [
                    i,
                    round(x_prev, 4),
                    round(funcion_lambda(x_prev), 4),
                    round(derivada_lambda(x_prev), 4),
                    "-----",
                ]
            )
        else:
            data.append(
                [
                    i,
                    round(x_prev, 4),
                    round(funcion_lambda(x_prev), 4),
                    round(derivada_lambda(x_prev), 4),
                    percent_error,
                ]
            )
        x_prev = x_next
        i += 1
    print(data)
    mostrar_matriz(data, ["Iteración", "x", "f(x)", "f'(x)", "Ea %"])


def entrar_funcion(funcion):
    if text_one == ventana.focus_get():
        text_one.insert(tk.END, str(funcion))
    elif text_two == ventana.focus_get():
        text_two.insert(tk.END, str(funcion))
    elif text_three == ventana.focus_get():
        text_three.insert(tk.END, str(funcion))


def eliminar_entrada():
    if text_one == ventana.focus_get():
        # Obtiene el contenido actual del Entry
        contenido_actual = text_one.get()

        # Guardo funciones a eliminar
        funciones = ["cos", "sin", "tan", "log", "ln"]
        for funcion in funciones:
            if contenido_actual.endswith(funcion):
                # Borra la función completa
                nuevo_contenido = contenido_actual[: -len(funcion)]
                text_one.delete(0, tk.END)
                text_one.insert(0, nuevo_contenido)
                return  # Sale de la función después de eliminar la función

        # Si no hay ninguna función detectada, borra el último carácter
        nuevo_contenido = contenido_actual[:-1]
        text_one.delete(0, tk.END)
        text_one.insert(0, nuevo_contenido)

    elif text_two == ventana.focus_get():
        contenido_actual = text_two.get()

        funciones = ["cos", "sin", "tan", "log", "ln"]
        for funcion in funciones:
            if contenido_actual.endswith(funcion):
                # Borra la función completa
                nuevo_contenido = contenido_actual[: -len(funcion)]
                text_two.delete(0, tk.END)
                text_two.insert(0, nuevo_contenido)
                return

        nuevo_contenido = contenido_actual[:-1]
        text_two.delete(0, tk.END)
        text_two.insert(0, nuevo_contenido)

    elif text_three == ventana.focus_get():
        contenido_actual = text_three.get()

        funciones = ["cos", "sin", "tan", "log", "ln"]
        for funcion in funciones:
            if contenido_actual.endswith(funcion):
                nuevo_contenido = contenido_actual[: -len(funcion)]
                text_three.delete(0, tk.END)
                text_three.insert(0, nuevo_contenido)
                return

        nuevo_contenido = contenido_actual[:-1]
        text_three.delete(0, tk.END)
        text_three.insert(0, nuevo_contenido)


def borrar_contenido():
    if text_one == ventana.focus_get():
        text_one.delete(0, tk.END)
    elif text_two == ventana.focus_get():
        text_two.delete(0, tk.END)
    elif text_three == ventana.focus_get():
        text_three.delete(0, tk.END)


# PARTE DEL FRONTEND:
# fUNCION PARA LAS RECOMENDACIONES
def mostrar_manual_usuario():
    root = Toplevel()
    root.geometry("1400x1000")
    root.title("Manual de Usuario")

    titulo = tk.Label(root, text="Recomendaciones", font=("Ivy 15 bold"), fg="red")
    titulo.place(x=100, y=30)

    (
        tk.Label(
            root,
            text="Al momento de navegar por la aplicación usted debe tener en cuenta:",
            font=("Ivy 15 bold"),
        ).place(x=100, y=70)
    )

    (
        tk.Label(
            root,
            text="☑La expresión que va dentro de funciones trigonométricas , logarítmicas y exponenciales va entre paréntesis.",
            font=("Ivy 14 bold"),
        ).place(x=99, y=140)
    )

    (
        tk.Label(
            root,
            text="☑La función log() por sí sola está definida sobre base del número Euler, y para indicar otra base se debe"
            "\n en el primer término la función, una coma y luego la base en que se desea calcular, es decir: log[f(x),base]."
            "\nLa base debe de estar entre 1 y 10",
            font=("Ivy 15 bold"),
        ).place(x=100, y=190)
    )

    (
        tk.Label(
            root,
            text="☑La función ln() tiene únicamente de base el número de Euler.",
            font=("Ivy 15 bold"),
        ).place(x=100, y=280)
    )
    (
        tk.Label(
            root,
            text="☑Cuando se use exp() entre los paréntesis va la potencia o función potencia a la que se quiere elevar Eluer(e).",
            font=("Ivy 15 bold"),
        ).place(x=100, y=320)
    )
    (
        tk.Label(
            root,
            text="☑Cuando presione el signo de raíz cuadrada saldará sqrt y la función deberá estar entre paréntesis.",
            font=("Ivy 15 bold"),
        ).place(x=100, y=370)
    )
    (
        tk.Label(
            root,
            text="☑eˣ se puede escribir como exp(x) ó E^x.",
            font=("Ivy 15 bold"),
        ).place(x=100, y=420)
    )
    (
        tk.Label(
            root,
            text="☑El botón EXP borra la última entrada del campo de entrada donde se encuentre.",
            font=("Ivy 15 bold"),
        ).place(x=100, y=470)
    )
    (
        tk.Label(
            root,
            text="☑El botón C borra la todo lo que hay  en el campo de entrada donde se encuentre.",
            font=("Ivy 15 bold"),
        ).place(x=100, y=510)
    )
    (
        tk.Label(
            root,
            text="☑Si al pinchar el botón de mostrar gráfica muestra una ventana con error, es porque debes de tener alguna de las 3 entradas "
            "\nincorrectas: para ello asegúrate de: escribir sólo en función de x, paréntesis cerrados, en valor inicial y error solo van números. ",
            font=("Ivy 15 bold"),
        ).place(x=100, y=570)
    )
    (
        tk.Label(
            root,
            text="☑Ten en cuenta que si la evaluación de la derivada da cero o el porcentaje de error esta dividido entre  0 el proceso finaliza. ",
            font=("Ivy 15 bold"),
        ).place(x=100, y=640)
    )
    (
        tk.Label(
            root,
            text="☑Ten en cuenta que si los valores no resultan es porque debes ajustar \nel valor inicial",
            font=("Ivy 15 bold"),
        ).place(x=100, y=690)
    )
    tk.Button(
        root,
        text="Salir",
        bg="red",
        fg="black",
        width=30,
        height=2,
        anchor="center",
        font=("Ivy 15 bold"),
        command=root.destroy,
    ).place(x=850, y=670)


color_1 = "#363434"
color_2 = "#feffff"
color_3 = "#37474F"
ventana = tk.Tk()
# Configuro el color de fuente
ventana.config(background="grey")
# Titulo de la ventana
ventana.title("Método Estándar de Newton Rapshon")
# Espacio de ventana
ventana.geometry("1400x1000")

# Label de la funcion a calcular
label_one = tk.Label(
    ventana,
    text="Ingresa función",
    font=("Calibri 15"),
    anchor="center",
    bg="grey",
    fg="black",
)
label_one.place(x=50, y=20, width=200, height=50)

# Caja de texto donde obtengo la función
text_one = tk.Entry(ventana, font="Calibri 15", bg=color_1, fg=color_2)
text_one.place(x=380, y=20, width=300, height=50)


# Label para el valor inicial de la función
label_two = tk.Label(
    ventana,
    text="Ingresa valor inicial",
    font=("Calibri 15"),
    anchor="center",
    bg="grey",
    fg="black",
)
label_two.place(x=50, y=90, width=200, height=50)

# Caja de texto para obtener valor inicial
text_two = tk.Entry(ventana, font=("Calibri 15"), bg=color_1, fg=color_2)
text_two.place(x=380, y=90, width=300, height=50)


# Label para el valor relativo porcentual
label_three = tk.Label(
    ventana,
    text="Ingresa error relativo porcentual",
    font=("Calibri 15"),
    anchor="center",
    bg="grey",
    fg="black",
)
label_three.place(x=50, y=160, width=300, height=50)

# Caja de texto para obtener el valor relativo porcentual
text_three = tk.Entry(ventana, font=("Calibri 15"), bg=color_1, fg=color_2)
text_three.place(x=380, y=160, width=300, height=50)

# Botones de funciones trigonómetricas
# TANGENTE
btn_tan = tk.Button(
    ventana,
    text="tan",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("tan"),
)

btn_tan.place(x=50, y=230)

# COSENO
btn_cos = tk.Button(
    ventana,
    text="cos",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("cos"),
)
btn_cos.place(x=130, y=230)

# SENO
btn_sin = tk.Button(
    ventana,
    text="sin",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("sin"),
)
btn_sin.place(x=210, y=230)

# RAÍZ CUADRADA
btn_sqrt = tk.Button(
    ventana,
    text="√",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("sqrt"),
)
btn_sqrt.place(x=290, y=230)

# ln
btn_ln = tk.Button(
    ventana,
    text="ln",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("ln"),
)
btn_ln.place(x=50, y=267)

# log
btn_log = tk.Button(
    ventana,
    text="log",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("log"),
)
btn_log.place(x=130, y=267)

# e
btn_e = tk.Button(
    ventana,
    text="e",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("exp"),
)
btn_e.place(x=210, y=267)

# ^
btn_pow = tk.Button(
    ventana,
    text="^",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("^"),
)
btn_pow.place(x=290, y=267)

# ,
btn_comma = tk.Button(
    ventana,
    text=".",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("."),
)
btn_comma.place(x=50, y=304)

# pi
btn_pi = tk.Button(
    ventana,
    text=",",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(","),
)
btn_pi.place(x=130, y=304)

# (
btn_first = tk.Button(
    ventana,
    text="(",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("("),
)
btn_first.place(x=210, y=304)

# )
btn_end = tk.Button(
    ventana,
    text=")",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(")"),
)
btn_end.place(x=290, y=304)


# 1
btn_1 = tk.Button(
    ventana,
    text="1",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(1),
)
btn_1.place(x=50, y=341)

# 2
btn_2 = tk.Button(
    ventana,
    text="2",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(2),
)
btn_2.place(x=130, y=341)

# 3
btn_3 = tk.Button(
    ventana,
    text="3",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(3),
)
btn_3.place(x=210, y=341)

# 4
btn_4 = tk.Button(
    ventana,
    text="4",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(4),
)
btn_4.place(x=290, y=341)

# 5
btn_5 = tk.Button(
    ventana,
    text="5",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(5),
)
btn_5.place(x=50, y=378)

# 6
btn_6 = tk.Button(
    ventana,
    text="6",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(6),
)
btn_6.place(x=130, y=378)

# 7
btn_7 = tk.Button(
    ventana,
    text="7",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(7),
)
btn_7.place(x=210, y=378)

# 8
btn_8 = tk.Button(
    ventana,
    text="8",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(8),
)
btn_8.place(x=290, y=378)

# 9
btn_9 = tk.Button(
    ventana,
    text="9",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(9),
)
btn_9.place(x=50, y=415)

# 0
btn_0 = tk.Button(
    ventana,
    text="0",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion(0),
)
btn_0.place(x=130, y=415)

# Borrar de uno por uno
btn_del = tk.Button(
    ventana,
    text="DEL",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_1,
    fg="red",
    command=lambda: eliminar_entrada(),
)
btn_del.place(x=210, y=415)

# Borrar todo
btn_c = tk.Button(
    ventana,
    text="C",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_1,
    fg="red",
    command=lambda: borrar_contenido(),
)
btn_c.place(x=290, y=415)

# *
btn_mult = tk.Button(
    ventana,
    text="*",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("*"),
)
btn_mult.place(x=50, y=452)

# /
btn_divi = tk.Button(
    ventana,
    text="/",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("/"),
)
btn_divi.place(x=130, y=452)

# +
btn_sum = tk.Button(
    ventana,
    text="+",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("+"),
)
btn_sum.place(x=210, y=452)

# -
btn_rest = tk.Button(
    ventana,
    text="-",
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    bd=0,
    font=("Ivy 14 bold"),
    bg=color_3,
    fg=color_2,
    command=lambda: entrar_funcion("-"),
)
btn_rest.place(x=290, y=452)

btn_x = tk.Button(
    ventana,
    text="x",
    bg=color_3,
    width=6,
    height=1,
    relief="raised",
    overrelief="ridge",
    anchor="center",
    font=("Ivy 14 bold"),
    fg=color_2,
    bd=0,
    command=lambda: entrar_funcion("x"),
)
btn_x.place(x=50, y=489)


# Botón para calcular método
boton = tk.Button(
    ventana,
    text="Calcular",
    bg="black",
    width=19,
    height=1,
    font=("Ivy 14 bold"),
    fg="white",
    command=newton_raphson,
)
boton.place(x=130, y=489)


# Botón para ir al Manual de Usuario
btn_manual_usuario = tk.Button(
    ventana,
    text="Manual de Usuario",
    bg="blue",
    relief="raised",
    overrelief="ridge",
    anchor="center",
    width=30,
    height=1,
    font=("Ivy 20 bold"),
    fg="white",
    command=mostrar_manual_usuario,
)
btn_manual_usuario.place(x=50, y=650)


def mostrar_matriz(matriz, cabeceras):

    # Crear el Treeview con cabeceras
    tree = ttk.Treeview(
        ventana,
        columns=list(range(5)),
        show="headings",
    )
    tree.place(
        x=400,
        y=500,
        width=800,
        height=110,
    )
    # Eliminar la matriz anterior
    for child in tree.get_children():
        tree.delete(child)

    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background=color_3,  # Color de fondo del Treeview
        fieldbackground="lightblue",  # Color de fondo para las celdas
        foreground="black",
    )  # Color del texto

    # Determinar el número de columnas basado en la longitud de las cabeceras
    num_cols = len(cabeceras)

    # Configurar las columnas y las cabeceras
    for i, cabecera in enumerate(cabeceras):
        tree.column(i, anchor="center", width=150)
        tree.heading(i, text=cabecera)

    # Añadir los datos de la matriz al Treeview
    for row in matriz:
        tree.insert("", tk.END, values=row)

    # Agregar Scrollbar
    scrollbar = tk.Scrollbar(ventana, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(x=1200, y=500, height=100)


def graficar_funcion():
    try:
        funcion_str = text_one.get()

        x = sp.symbols("x")
        expresion = sp.sympify(funcion_str)

        x_vals = np.linspace(0.1, float(text_two.get()) + 2, 400)
        y_vals = [expresion.subs(x, val).evalf() for val in x_vals]

        # Limpiar figura anterior si existe
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(x_vals, y_vals, label=f"f(x) = {funcion_str}")
        ax.set_title(f"Gráfica de la función f(x) = {funcion_str}")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        canvas.draw()
    except:
        messagebox.showerror("Error", message="Error")
        return


# Botón para graficar la función
btn_graficar = tk.Button(
    ventana,
    text="Graficar Función",
    bg=color_3,
    fg=color_2,
    command=lambda: graficar_funcion(),
)
btn_graficar.place(x=1000, y=20)

# Configurar el espacio para la figura de Matplotlib
fig = Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(
    fig, master=ventana
)  # Crear área de dibujo de Matplotlib en Tkinter
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=750, y=60)


ventana.mainloop()
