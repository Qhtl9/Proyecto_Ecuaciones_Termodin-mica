# Ecuación 1 (Temperatura de saturación)
$p = \text{Entrada del usuario } [MPa]$ 

$\beta = p^{0.25}$

$E = \beta^2 + n_3\times\beta + n_6$

$F = n_1\times\beta^2+n_4\times\beta+n_7$

$G = n_2\times\beta^2+n_5\times\beta+n_8$

$D=\frac{2\times G}{-F-\sqrt{F^2-4\times E\times G}}$

$T_{sat}=\frac{n_{10}+D-\sqrt{(n_{10}+D)^2 - 4(n_9+n_{10}\times D)}}{2.0}-273.15$
P
# Ecuación 2 (Entalpía de vaporización)
$h_{fg} = 2256.4\times\left[ \frac{1-\frac{T_{sat} + 273.15}{647.096}}{1-0.57665623} \right]^{0.375}$