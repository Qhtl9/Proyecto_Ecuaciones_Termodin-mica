---
tags:
  - UNAM/3°Semestre
  - UNAM/3°Semestre/Termodinámica
  - Termodinámica
---
# Ecuación 1 (Temperatura de saturación)
$p = \text{Entrada del usuario } [MPa]$
$\beta = p^{0.25}$
$E = \beta^2 + n_3\times\beta + n_6$
$F = n_1\times\beta^2+n_4\times\beta+n_7$
$G = n_2\times\beta^2+n_5\times\beta+n_8$
$D=\frac{2\times G}{-F-\sqrt{F^2-4\times E\times G}}$
$T_{sat}=\frac{n_{10}+D-\sqrt{(n_{10}+D)^2 - 4(n_9+n_{10}\times D)}}{2.0}-273.15$

# Ecuación 2 (Entalpía de vaporización)
$h_{fg}\left[\frac{kJ}{kg}\right] = 2256.4\times\left[ \frac{1-\frac{T_{sat}}{647.096}}{1-0.57665623} \right]^{0.375}$


# Código
## Fuente (No en vivo)
```python
import math # Para las raíces

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

p = float(input("Introduzca la presión en [MPa]\n\t> "))

# Cáclulo de la temperatrua de saturación
beta = pow(p, 0.25)
E = (pow(beta, 2)) + (n3*beta) + n6
F = (n1*pow(beta, 2)) + (n4*beta) + n7
G = (n2*pow(beta, 2)) + (n5*beta) + n8
D = (2*G)/(-F-math.sqrt(pow(F, 2)-4*E*G))
Tsat = ((n10 + D - math.sqrt(pow((n10 + D), 2)-4*(n9 + n10*D)))/2.0) - 273.15

print("Temperatura de saturación calculada: " + str(Tsat) + "[°C]")


# Cáclulo de la entalpía de vaporización
hfg = 2256.4*pow(((1-((Tsat+273.15)/(647.096)))/(1-0.57665623)), 0.375)

print("Entalpía de vaporización calculada: " + str(hfg) + "[kJ/kg]")
```
## Editar
![[Ecuaciones.py]]