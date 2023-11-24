import math
import matplotlib.pyplot as plt
from tabulate import tabulate
import tkinter as tk
from tkinter import Label, Entry, Button, Text, scrolledtext

# Coeficientes para el cálculo de Tsat
n1 = 0.116_705_214_527_67E4
n2 = -0.724_213_167_032_06E6
n3 = -0.170_738_469_400_92E2
n4 = 0.120_208_247_024_70E5
n5 = -0.323_255_503_223_33E7
n6 = 0.149_151_086_135_30E2
n7 = -0.482_326_573_615_91E4
n8 = 0.405_113_405_420_57E6
n9 = -0.238_555_575_678_49
n10 = 0.650_175_348_447_98E3

C_ea = 4186  # [J/(kg°C)]

# Funciones de cálculo
def calculo_Tsat(p):
    beta = pow(p, 0.25)
    E = (pow(beta, 2)) + (n3 * beta) + n6
    F = (n1 * pow(beta, 2)) + (n4 * beta) + n7
    G = (n2 * pow(beta, 2)) + (n5 * beta) + n8
    D = (2 * G) / (-F - math.sqrt(pow(F, 2) - 4 * E * G))
    T_sat = ((n10 + D - math.sqrt(pow((n10 + D), 2) - 4 * (n9 + n10 * D))) / 2.0) - 273.15
    return T_sat  # [°C]

def calculo_entalpia_vap(T_sat):
    h_fg = 2256.4 * (pow(((1 - ((T_sat + 273.15) / 647.096)) / (1 - 0.57665623)), 0.375))
    return h_fg  # [kJ/kg]

def calculo_calidad(Valor, Valor_l, Valor_v):
    return ((Valor - Valor_l) / (Valor_v - Valor_l))

def calculo_masa_temperatura(C_ea, T_i, M_i, P, T_sat, t_sat, t_vap, t):
    if t_sat >= t:
        M_t = M_i
        Q_t = P * t
        T_t = (Q_t * 1 / (M_t * C_ea)) + T_i
    elif t_vap >= t:
        x = calculo_calidad(t, t_vap + t_sat, t_sat)
        M_t = M_i * x
        Q_t = P * t
        T_t = T_sat
    else:
        return -1
    return [M_t, T_t]

# Función para manejar el botón "Calcular"
def calcular():
    T_i = float(entry_temp_inicial.get())
    M_i = float(entry_masa_inicial.get())
    t = float(entry_intervalo_tiempo.get())
    P = float(entry_potencia_parrilla.get())
    P_atm = float(entry_presion_atmosferica.get())

    T_sat = calculo_Tsat(P_atm)  # [°C]

    if T_sat > T_i:
        text_resultado.delete(1.0, tk.END)
    else:
        text_resultado.delete(1.0, tk.END)
        text_resultado.insert(tk.END, "No se inicia en fase líquida, saliendo...\n")
        return

    Q_a = M_i * C_ea * (T_sat - T_i)  # [J]
    t_sat = (1 / P) * Q_a  # [s]

    h_fg = calculo_entalpia_vap(T_sat)  # [kJ/kg]
    h_fg = h_fg * (1000)  # [J/kg]
    Q_e = h_fg * M_i  # [J]
    t_vap = (1 / P) * Q_e  # [s]

    incremento = 0
    dt = 1
    M_ot = []
    T_ot = []

    flag = True
    while flag:
        Data = calculo_masa_temperatura(C_ea, T_i, M_i, P, T_sat, t_sat, t_vap, incremento)
        if Data == -1:
            flag = False
        else:
            incremento = incremento + dt
            M_ot.append(Data[0])
            T_ot.append(Data[1])

    Data_ut = calculo_masa_temperatura(C_ea, T_i, M_i, P, T_sat, t_sat, t_vap, t)

    # Crear tabla
    tabla_data = [["Masa de líquido", "Temperatura"], Data_ut]
    tabla_resultado = tabulate(tabla_data, headers="firstrow", tablefmt="grid")

    # Mostrar tabla
    text_resultado.delete(1.0, tk.END)
    text_resultado.insert(tk.END, "Tabla de valores a los {t}[s] de inicio\n".format(t=t))
    text_resultado.insert(tk.END, tabla_resultado)

    # Graficar M_ot
    plt.figure(1)
    plt.plot(M_ot, label='Masa [kg]')
    plt.xlabel('Segundos [s]')
    plt.ylabel('Masa [kg]')
    plt.title('Gráfica de masa líquida en función del tiempo')
    plt.legend()

    # Graficar T_ot
    plt.figure(2)
    plt.plot(T_ot, label='Temperatura')
    plt.xlabel('Segundos [s]')
    plt.ylabel('Temperatura [ºC]')
    plt.title('Gráfica de temperatura en función del tiempo')
    plt.legend()

    plt.show()

# Crear la interfaz gráfica
window = tk.Tk()
window.title("Cálculo de Masa y Temperatura")

# Etiquetas y campos de entrada
Label(window, text="Temperatura Inicial (°C):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_temp_inicial = Entry(window)
entry_temp_inicial.grid(row=0, column=1, padx=10, pady=5)

Label(window, text="Masa Inicial (kg):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_masa_inicial = Entry(window)
entry_masa_inicial.grid(row=1, column=1, padx=10, pady=5)

Label(window, text="Intervalo de Tiempo (s):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_intervalo_tiempo = Entry(window)
entry_intervalo_tiempo.grid(row=2, column=1, padx=10, pady=5)

Label(window, text="Potencia de la Parrilla (W):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_potencia_parrilla = Entry(window)
entry_potencia_parrilla.grid(row=3, column=1, padx=10, pady=5)

Label(window, text="Presión Atmosférica (MPa):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_presion_atmosferica = Entry(window)
entry_presion_atmosferica.grid(row=4, column=1, padx=10, pady=5)

# Botón de cálculo
btn_calcular = Button(window, text="Calcular", command=calcular)
btn_calcular.grid(row=5, column=0, columnspan=2, pady=10)

# Resultado
Label(window, text="Resultado:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
text_resultado = scrolledtext.ScrolledText(window, width=40, height=10, wrap=tk.WORD)
text_resultado.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

window.mainloop()
