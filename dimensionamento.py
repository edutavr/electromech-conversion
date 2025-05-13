import math

# Entrada
P = 300  #Potencia aparente do transformador em VA
Vp = 120  # Tensao do enrolamento primario em V
Vs = 220  # Tensao do enrolamento secundario V
f = 50  # Hz
B = 1.2  # Densidade de fluxo magnetico maximo admissivel no nucleo em T (típico para núcleo silício)
J = 2.5  # A/mm² (densidade de corrente)

# 1. Área da seccao transversal do núcleo
A = math.sqrt(P)  # cm²
A_m2 = A * 1e-4  # para cálculo com B em T e f em Hz

# 2. Espiras por volt (e)
e = 1e4 / (4.44 * f * B * A)  # fórmula Martignoni

# 3. Número de espiras
Np = round(e * Vp) # no enrolamento primario
Ns = round(e * Vs) # no enrolamento secundario

# 4. Correntes
Ip = P / Vp # no enrolamento primario
Is = P / Vs # no enrolamento secundario

# 5. Bitolas dos fios
Sp = Ip / J # no enrolamento primario
Ss = Is / J # no enrolamento secundario

# Resultados
print("----- RESULTADOS -----")
print(f"Área do núcleo (A): {A:.2f} cm²")
print(f"Espiras por volt (e): {e:.2f}")
print(f"Espiras no primário (Np): {Np}")
print(f"Espiras no secundário (Ns): {Ns}")
print(f"Corrente no primário: {Ip:.2f} A → Bitola: {Sp:.2f} mm²")
print(f"Corrente no secundário: {Is:.2f} A → Bitola: {Ss:.2f} mm²")
