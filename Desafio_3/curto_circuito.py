import cmath

# Valores calculados no Desafio 1:
P = 300  # VA
Vp = 120  # V (primário)
Vs = 220  # V (secundário)
Np = 330  # Espiras no primário (ajustado para o exemplo)
Ns = 605  # Espiras no secundário
Ip = P / Vp  # 2.5 A
Is = P / Vs  # 1.36 A
A_nucleo = 0.1732  # 0.1732 m²
V_cc = 15 # Tensão de alimentação: V_cc = 15 V (ajustada para circular corrente nominal)
I_cc = 2.5 # Corrente de curto: I_cc = 2.5 A (igual à corrente nominal do primário)
P_cc = 40 # Potência de entrada: P_cc = 40 W (perdas no cobre)

# Resistência equivalente (R_eq)
R_eq = P_cc / (I_cc ** 2)  # 40 / (2.5²) = 6.4 Ω
print(f"Resistência equivalente (R_eq): {R_eq:.2f} Ω")

# Impedância equivalente (Z_eq)
Z_eq = V_cc / I_cc  # 15 / 2.5 = 6 Ω

# Reatância equivalente (X_eq)
X_eq = cmath.sqrt(Z_eq ** 2 - R_eq ** 2)
print(f"Reatância equivalente (X_eq): {X_eq:.2f} Ω")