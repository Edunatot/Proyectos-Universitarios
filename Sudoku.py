import tkinter as tk
import random
import copy

casillas = []
solucion = []

def es_valido(tablero, fila, columna, numero):
    for c in range(9):
        if tablero[fila][c] == numero:
            return False

    for f in range(9):
        if tablero[f][columna] == numero:
            return False

    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3

    for f in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_columna, inicio_columna + 3):
            if tablero[f][c] == numero:
                return False

    return True


def buscar_vacio(tablero):
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:
                return fila, columna

    return None


def resolver(tablero):
    vacio = buscar_vacio(tablero)

    if vacio is None:
        return True

    fila, columna = vacio
    numeros = list(range(1, 10))
    random.shuffle(numeros)

    for numero in numeros:
        if es_valido(tablero, fila, columna, numero):
            tablero[fila][columna] = numero

            if resolver(tablero):
                return True
            
            tablero[fila][columna] = 0

    return False


def generar_sudoku():
    tablero = [[0] * 9 for _ in range(9)]

    resolver(tablero)
    solucion_local = copy.deepcopy(tablero)

    for _ in range(40):
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)
        tablero[fila][columna] = 0
    return tablero, solucion_local


def ui():
    ventana.withdraw()

    ventanaR = tk.Toplevel()
    ventanaR.title("Sudoku")
    ventanaR.geometry("250x200")

    enc = tk.Frame(ventanaR, bg="darkred", padx=10, pady=10)
    enc.pack(fill="x")
    tk.Label(enc, text="SUDOKU", font=("Arial", 20), fg="white", bg="darkred").pack()

    iniciar = tk.Button(ventanaR, text="Iniciar Juego", command=lambda: inplay(ventanaR))
    iniciar.pack(pady=55)


def inplay(ventanaAnterior):
    global solucion

    ventanaAnterior.destroy()
    casillas.clear()
    tablero_juego, solucion = generar_sudoku()

    ventanaA = tk.Toplevel()
    global ventana_juego
    ventana_juego = ventanaA
    ventanaA.title("Sudoku")
    ventanaA.geometry("750x500")
    enc = tk.Frame(ventanaA, bg="darkgreen", padx=10, pady=10)
    enc.pack(fill="x")
    tk.Label(enc, text="SUDOKU", font=("Arial", 20), fg="white", bg="darkgreen").pack()

    tablero = tk.Frame(ventanaA)
    tablero.pack(pady=20)

    for fila in range(9):
        fila_actual = []

        for columna in range(9):
            padx = (1, 3) if columna % 3 == 2 else 1
            pady = (1, 3) if fila % 3 == 2 else 1

            entrada = tk.Entry(tablero, width=2, font=("Arial", 18), justify="center")

            if tablero_juego[fila][columna] != 0:
                entrada.insert(0, str(tablero_juego[fila][columna]))
                entrada.config(state="readonly")

            entrada.grid(row=fila, column=columna, padx=padx, pady=pady)
            fila_actual.append(entrada)

        casillas.append(fila_actual)

    enviar = tk.Button(ventanaA, text="Enviar", command=respuesta)
    enviar.pack(pady=20)

    limpiar = tk.Button(ventanaA, text="Limpiar", command=limpiarTab)
    limpiar.pack()


def respuesta():
    global ventana_juego
    jugador = []

    for fila in casillas:
        fila_actual = []

        for entrada in fila:
            texto = entrada.get()

            if texto == "":
                fila_actual.append(0)
            else:
                try:
                    fila_actual.append(int(texto))
                except:
                    fila_actual.append(0)

        jugador.append(fila_actual)

    print("JUGADOR")
    for fila in jugador:
         print(fila)

    print("\nSOLUCION")
    for fila in solucion:
        print(fila)

    print(type(jugador[0][0]))
    print(type(solucion[0][0]))

    if jugador == solucion:
        resultado = tk.Toplevel()
        resultado.title("Victoria")

        tk.Label(resultado, text="Ganaste :D", font=("Arial", 18)).pack(padx=20, pady=10)
        tk.Button(resultado, text="Jugar otra vez", command=lambda: nueva_partida(resultado)).pack(pady=10)
    else:
        resultado = tk.Toplevel()
        resultado.title("Resultado")

        tk.Label(resultado, text="Incorrecto", font=("Arial", 18)).pack(padx=20, pady=20)


def limpiarTab():
    for fila in casillas:
        for entrada in fila:
            if str(entrada["state"]) != "readonly":
                entrada.delete(0, tk.END)


def nueva_partida(ventanaResultado):
    global ventana_juego

    ventanaResultado.destroy()
    ventana_juego.destroy()

    inplayF()

def inplayF():
    inF = tk.Toplevel()
    inplay(inF)


ventana = tk.Tk()
ventana.geometry("512x300")

ui()

ventana.mainloop()