import math

# Valores calculados no Desafio 1:
P = 300  # VA
Vp = 120  # V (primário)
Vs = 220  # V (secundário)
Np = 330  # Espiras no primário (ajustado para o exemplo)
Ns = 605  # Espiras no secundário
Ip = P / Vp  # 2.5 A
Is = P / Vs  # 1.36 A
A_nucleo = 0.1732  # 0.1732 m²
V_ca = 220 # Tensão de alimentação: V_ca = 220 V (nominal do secundário).
I_ca = 0.5 # Corrente de excitação: I_ca = 0.5 A (típico para transformadores pequenos).
P_ca = 30 # Potência de entrada: P_ca = 30 W (perdas no núcleo + perdas ôhmicas desprezíveis).

# Perdas no núcleo (R_c)
R_c = (V_ca ** 2) / P_ca  # Resistência que modela as perdas por histerese e Foucault
print(f"Resistência de perdas no núcleo (R_c): {R_c:.2f} Ω")

# Potência aparente de magnetização
S_ca = V_ca * I_ca  # 220 * 0.5 = 110 VA
Q_ca = math.sqrt(S_ca ** 2 - P_ca ** 2)  # Potência reativa de magnetização

# Reatância de magnetização (X_m)
X_m = (V_ca ** 2) / Q_ca
print(f"Reatância de magnetização (X_m): {X_m:.2f} Ω")