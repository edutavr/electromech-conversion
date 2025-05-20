import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def desafio_2(core_lenght, core_area, n1, W1):

    # Carregar dados
    print("Diretório atual:", os.getcwd())
    df = pd.read_excel('../MagCurve.xlsx')
    MMF = df['MMF'].values
    Fluxo = df['Fluxo'].values

    # Parâmetros do núcleo (exemplo)
    l_c = core_lenght  # Comprimento do núcleo em metros
    A_nucleo = core_area  # Área do núcleo em m² (ajuste conforme Desafio 1)

    # Calcular H e B
    H = MMF / l_c  # A/m
    B = Fluxo / A_nucleo  # Tesla

    # Plotar curva B-H
    plt.plot(H, B, 'r-')
    plt.xlabel('Campo Magnético H (A/m)')
    plt.ylabel('Densidade de Fluxo B (T)')
    plt.title('Curva B-H do Material do Núcleo')
    plt.grid()
    plt.show()


    N_p = n1  # Valor de espiras do Desafio 1
    I_m = (H * l_c) / N_p  # Corrente de magnetização em A

    # Plotar I_m x tempo (assumindo excitação senoidal)
    t = np.linspace(0, 0.34, 1000)  # 340 ms com passo de 1/3000 s
    V_p = W1  # Tensão primária (Desafio 1)
    phi_max = max(B) * A_nucleo  # Fluxo máximo
    I_m_t = (phi_max / (N_p * A_nucleo)) * np.sin(2 * np.pi * 50 * t)  # Simplificado

    plt.plot(t, I_m_t)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Corrente de Magnetização (A)')
    plt.title('Curva I_m x Tempo')
    plt.grid()
    plt.show()