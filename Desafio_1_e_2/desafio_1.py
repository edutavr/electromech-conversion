import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Inicializando os parâmetros de entrada, no caso 
# W2 --> Potência de saída 
# V2 -->  Tensão Secundária
# V1 --> Tensão Primária 
def initialize_parameters(W2, V2, V1):
    
    if W2.isdigit() & V2.isdigit() & V1.isdigit():
        if W2 > 800:
            print('Potência de saída do transformador é maior do que 800 VA. Não é possível usar lâminas padronizadas')   
            laminas_padrozinadas = False
        else:
            print('A potência de saída do transformador é menor do que 800 VA. É possível utilizar as lâminas padronizadas')
            laminas_padrozinadas = True
        return laminas_padrozinadas    
    else:
        print('Os valores inseridos não são dígitos...')
        return 

def first_and_second_current(W2,V2,V1):
    Is = (W2/V2) 
    
    #A Pontência primária é calculada a partir do aumento em 10% da potência secundária
    W1 = 1.1 * W2
    Ip = (W1/V1)

    return Is,Ip

def conductor_section(current,W2):
    if W2 == 500:
        return current/3
    elif W2 > 500 & W2 <= 1000:
        return  current/2.5
    elif W2 > 1000 & W2 <= 3000:
        return current/2
    else:
        return "Potência fora do range limite recomendado"

def bitola(condutor_section): 
    conductor_section = {
    "upper_limit": [53.476, 42.409, 33.362, 26.271, 21.152, 16.774, 13.303, 10.549, 8.366, 6.635, 5.262, 4.173, 3.309, 2.624, 2.081, 1.650, 1.309, 1.038, 0.823, 0.653, 0.518],
    "lower_limit": [42.409, 33.362, 26.271, 21.152, 16.774, 13.303, 10.549, 8.366, 6.635, 5.262, 4.173, 3.309, 2.624, 2.081, 1.650, 1.309, 1.038, 0.823, 0.653, 0.518, 0.411],
    "description": ["fio 0", "fio 1", "fio 2", "fio 3", "fio 4", "fio 5", "fio 6", "fio 7", "fio 8", "fio 9", "fio 10", "fio 11", "fio 12", "fio 13", "fio 14", "fio 15", "fio 16", "fio 17", "fio 18", "fio 19", "fio 20"]
    }
    df = pd.DataFrame(conductor_section)
    row = df[(df['lower_limit'] < condutor_section) & (df['upper_limit'] >= condutor_section)]
    if not row.empty:
        upper_limit = row.iloc[0]['upper_limit']
        description = row.iloc[0]['description']
        return [upper_limit, description]
    else:
        return []


def magnectic_section(potency, frequency,is_long_cable,
                      is_two_primary_circuits=False,is_two_secondary_circuits=False):
    standard_cables = 7.5*(math.sqrt(potency/frequency))
    long_cables = 6.5*(math.sqrt(potency/frequency))
    if is_two_primary_circuits is False and is_two_secondary_circuits is False:
        if is_long_cable:
            return long_cables
        return standard_cables

    if is_two_primary_circuits is True and is_two_secondary_circuits is False:
        standard_cables = 7.5*(math.sqrt(1.25*potency/frequency))
        long_cables = 6*(math.sqrt(1.25*potency/frequency))

        if is_long_cable:
            return long_cables
        return standard_cables

    if is_two_primary_circuits is True and is_two_secondary_circuits is True:
        standard_cables = 7.5*(math.sqrt(1.5*potency/frequency))
        long_cables = 6*(math.sqrt(1.5*potency/frequency))

        if is_long_cable:
            return long_cables
        return standard_cables

    print('Inválido')
    return [0, 0]


def core_geometric_section_1(magnetic_section):
    return magnetic_section*1.1


def calculate_a_and_b_geometric_section(geometric_section):
    if geometric_section > 25:
        a = 5
    else:
        a = 4
    b = geometric_section/a
    return b

def core_geometric_section(length, width):
    return length*width

def core_magnetic_section(length, width):
    return core_geometric_section(length, width)/1.1

def calculate_turns_number_1(frequency, tension, core_ms):
    if(frequency == 50):
        return tension*(40/core_ms)
    return tension*(33.5/core_ms)


def iron_core_weight(geometric_section):
    b = calculate_a_and_b_geometric_section(geometric_section)

    if(geometric_section>25):
        return 1.580*b
    return 1.000*b


def cooper_section(n1,s1,n2,s2):
    return n1*s1 + n2*s2


def calculate_lm(core_gs):
    b = calculate_a_and_b_geometric_section(core_gs)

    if(core_gs>25):
        return (2*5 + 2*b + 0.5*3.14*5)
    return (2*4 + 2*b + 0.5*3.14*4)

def cooper_weight(section_cooper, lm):
    return ((section_cooper/100)*lm*9)*0.001


def dimensions_core(a,b,second_potency):
    if(second_potency>800):
        largura=3*a
        altura=4*a
        comprimento=b
        seção_janela=(0.5*a*1.5*a)*100  ## mm²
        volume= ((largura*altura) - (0.5*a*3*a*2))*b*0.9 ## cm³


        return ("\nA Largura é: "+str(largura)+"cm\n" +
                "A Altura é: "+str(altura)+"cm\n" +
                "O Comprimento é: "+str(comprimento)+"cm\n" +
                "A Seção da janela é: "+str(seção_janela)+"mm²\n"+
                "O Volume é: "+str(volume)+"cm³")

    else:
     print("mero")