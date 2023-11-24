import math # Para las raíces
import matplotlib.pyplot as plt # Para los gráficos
from tabulate import tabulate # Para las tablas

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

C_ea = 4186 # [J/(kg°C)]

def Cálculo_Tsat(p): # p: Presión en [MPa]
    beta = pow(p, 0.25)
    E = (pow(beta, 2)) + (n3*beta) + n6
    F = (n1*pow(beta, 2)) + (n4*beta) + n7
    G = (n2*pow(beta, 2)) + (n5*beta) + n8
    D = (2*G)/(-F-math.sqrt(pow(F, 2)-4*E*G))
    T_sat = ((n10 + D - math.sqrt(pow((n10 + D), 2)-4*(n9 + n10*D)))/2.0) - 273.15

    return T_sat # [°C]

def Cálculo_EntalpíaVap(T_sat): # Tsat: Temperatura de saturación en [°C]
    h_fg = 2256.4*(pow(((1-((T_sat+273.15)/(647.096)))/(1-0.57665623)), 0.375))
    
    return h_fg # [kJ/kg]



T_i = float(input("Introduzca la temperatura inicial del agua\n\t[°C]> "))
M_i = float(input("Introduzca la masa inicial del agua\n\t[kg]> "))
t = float(input("Introduzca el intervalo de tiempo para obtener la temperatura y la masa líquida del sistema\n\t[s]> "))
P = float(input("Introduzca la potencia de la parrilla\n\t[W]> "))
P_atm = float(input("Introduzca la presión atmosférica\n\t[MPa]> "))

# Verificar que la temperatura inicial corresponde a la fase líquida
T_sat = Cálculo_Tsat(P_atm) # [°C]
if(T_sat > T_i):
    print("Se inicia en fase líquida\n")
else:
    print("No se inicia en fase líquida, saliendo...\n")
    exit()

# Calcular el tiempo necesario para llegar a la temperatura de saturación
Q_a = M_i*C_ea*(T_sat-T_i) # [J]
t_sat = (1/P)*Q_a # [s]

# Calcular el tiempo necesario para evaporar toda la masa
h_fg = Cálculo_EntalpíaVap(T_sat) # [kJ/kg]
h_fg = h_fg*(1000) # [J/kg]
Q_e = h_fg*M_i # [J]
t_vap = (1/P)*Q_e # [s]

# Calcular la temperatura y la masa líquida en el tiempo dado
def Cáculo_MasaTemperatura(C_ea, T_i, M_i, P, T_sat, t_sat, t_vap, t):
    if(t_sat >= t):
        M_t = M_i
        Q_t = P*t
        T_t = (Q_t*1/(M_t*C_ea)) + T_i
    elif(t_vap >= t):
        x = (t-(t_vap+t_sat))/(t_sat-(t_vap+t_sat))
        M_t = M_i*x
        Q_t = P*t
        T_t = T_sat
    else:
        return -1;
    
    return [M_t, T_t]

flag = True
i = 0
M_ot = []
T_ot = []

while(flag):
    Data = Cáculo_MasaTemperatura(C_ea, T_i, M_i, P, T_sat, t_sat, t_vap, i)
    if(Data == -1):
        flag = False
    else:
        i = i + 1
        M_ot.append(Data[0])
        T_ot.append(Data[1])

Data_ut = Cáculo_MasaTemperatura(C_ea, T_i, M_i, P, T_sat, t_sat, t_vap, t)

tabla_data = [
    ["Masa de líquido", "Temperatura"],
    Data_ut
]

# Crear la tabla utilizando tabulate
tabla = tabulate(tabla_data, headers="firstrow", tablefmt="grid")

# Imprimir la tabla
print(tabla)

# Graficar la lista M_ot
plt.figure(1)
plt.plot(M_ot, label='Masa [kg]')
plt.xlabel('Segundos [s]')
plt.ylabel('Masa [kg]')
plt.title('Gráfica de masa líquida en función del tiempo')
plt.legend()

# Graficar la lista T_ot
plt.figure(2)
plt.plot(T_ot, label='Temperatura')
plt.xlabel('Segundos [s]')
plt.ylabel('Temperatura [ºC]')
plt.title('Gráfica de temperatura en función del tiempo')
plt.legend()

plt.show()
