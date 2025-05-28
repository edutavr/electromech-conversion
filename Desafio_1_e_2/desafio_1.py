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
        if int(W2) > 800:
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
    if W2 <= 500:
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


def magnectic_section(potency, frequency,is_long_cable,is_two_primary_circuits=False,is_two_secondary_circuits=False):
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


def calculate_a_and_b_geometric_section(geometric_section,a):
    b = geometric_section/a
    return b

def core_geometric_section(length, width):
    return length*width

def core_magnetic_section(length, width):
    return core_geometric_section(length, width)/1.1

def calculate_turns_number_1(frequency, tension, core_ms):
    if(frequency == 50):
        return tension*(40/core_ms)
    #Frequency = 60Hz
    return tension*(33.5/core_ms)


def blades_qtd(b:float,acesita:float):
  return round((b*0.9)/acesita)

def blade_type(a): 
    if a == 1.5: 
        return "Lãmina tipo 0"
    elif a == 2:
        return "Lãmina tipo 1"
    elif a == 2.5: 
        return "Lãmina tipo 2"
    elif a == 3: 
        return "Lãmina tipo 3"
    elif a == 3.5: 
        return "Lãmina tipo 4"
    elif a == 4: 
        return "Lãmina tipo 5"
    elif a == 5:
        return "Lâmina tipo 6"
    else: 
        return "Lãmina não encontrada"
    

def dimensions_core(a,b,second_potency):
    if(second_potency>800):
        largura=3*a
        altura=4*a
        comprimento=b
        seção_janela=(0.5*a*1.5*a)*100  ## mm²
        volume= ((largura*altura) - (0.5*a*3*a*2))*b*0.9 ## cm³
        peso = 5.4*(a**2)*7.8


        return ("\nA Largura é: "+str(largura)+"cm\n" +
                "A Altura é: "+str(altura)+"cm\n" +
                "O Comprimento é: "+str(comprimento)+"cm\n" +
                "A Seção da janela é: "+str(seção_janela)+"mm²\n"+
                "O Volume é: "+str(volume)+"cm³\n"
                "Peso é:" + str(peso)+ 'g')
    else:
        largura=3*a
        altura=2.5*a
        print("a", a)
        print("largura ", largura)
        print("altura ", altura)
        comprimento=b
        seção_janela=(0.5*a*1.5*a)*100  ## mm²
        volume= ((float(largura)*float(altura)) - (0.5*a*3*a*2))*b*0.9 ## cm
        peso = 5.4*(a**2)*7.8


        return ("\nA Largura é: "+str(largura)+"cm\n" +
                "A Altura é: "+str(altura)+"cm\n" +
                "O Comprimento é: "+str(comprimento)+"cm\n" +
                "A Seção da janela é: "+str(seção_janela)+"mm²\n"+
                "O Volume é: "+str(volume)+"cm³\n"
                "Peso é:" + str(peso)+ 'g')


def create_transformer_sections(x, y, z, dx, dy, dz):
    return np.array([[x, y, z],
                     [x + dx, y, z],
                     [x + dx, y + dy, z],
                     [x, y + dy, z],
                     [x, y, z + dz],
                     [x + dx, y, z + dz],
                     [x + dx, y + dy, z + dz],
                     [x, y + dy, z + dz]])


def rotate_transformer(vertices, angle):
    rotation_matrix = np.array([
        [ np.cos(angle), 1,0],
        [0,-np.cos(angle),1],
        [ np.sin(angle), np.cos(angle),0]
    ])
    return np.dot(vertices, rotation_matrix.T)


def plot_transformer(ax, vertices, c):
    faces = [[vertices[j] for j in [0, 1, 5, 4]],
             [vertices[j] for j in [7, 6, 2, 3]],
             [vertices[j] for j in [0, 3, 7, 4]],
             [vertices[j] for j in [1, 2, 6, 5]],
             [vertices[j] for j in [0, 1, 2, 3]],
             [vertices[j] for j in [4, 5, 6, 7]]]

    poly3d = Poly3DCollection(faces, linewidths=1, alpha=.35, color=c)
    ax.add_collection3d(poly3d)


def generate_transformer(ax, angle:float, a:float, b:float, first_tension:float, second_tension:float):

    parts = [                     # X, Y, Z, H, W, T
        create_transformer_sections(0, 0, 0, 0.5*a, 3*a, b),  # base da lamina "E"
        create_transformer_sections(0, a+1.5*a, 0, 2*a, a*0.5, b),  # seção do secundario
        create_transformer_sections(0, a, 0, 2*a, a, b),  # tronco central do transformador
        create_transformer_sections(0, 0, 0, 2*a, a*0.5, b),  # seção do primario
        create_transformer_sections(2*a, 0, 0, 0.5*a, 3*a, b)   # Seção que compõe a lamina tipo "I" (topo do transformador)
    ]
   #cont = 0
    for part in parts:
        c = 'gray'
        #if cont == 1 or cont == 3:
        #    c = "C" + str(cont) #C1 = Laranja, C2 = Vermelho
        #cont += 1
        rotated_part = rotate_transformer(part, angle)
        plot_transformer(ax, rotated_part, c) # plotar transformador rotacionado

    n1 = first_tension*1.1
    n2 = second_tension*1.1

    if(n1>n2):
        #primeiro enrolamento
        zline = np.linspace(0.6*a, a*1.2, 100)+a*(0.75)
        xline = np.cos(zline*3*b)
        yline = np.sin(zline*3*b)
        ax.plot3D((b/1.5)*xline-(a*(-1.52)), yline*(b/1.5)+(b/2), zline, color='brown')

        #segundo enrolamento
        zline = np.linspace(a, 0.5*a, 50)-a*(0.01)
        xline = np.cos(zline*2*b)-2.5
        yline = np.sin(zline*2*b)
        ax.plot3D((b/1.5)*xline+(b*2.79), yline*(b/1.5)+(b/2), zline, color='brown')

    elif(n2>n1): #se n2>n1
        #primeiro enrolamento
        zline = np.linspace(0.6*a, a*1.2, 100)-a*(0.01)
        xline = np.cos(zline*3*b)
        yline = np.sin(zline*3*b)
        ax.plot3D((b/1.5)*xline-(a*(-1.52)), yline*(b/1.5)+(b/2), zline, color='brown')

        #segundo enrolamento
        zline = np.linspace(a, 0.5*a, 50)+a*(1.01)
        xline = np.cos(zline*2*a)-2.5
        yline = np.sin(zline*2*a)
        ax.plot3D((b/1.5)*xline+(b*2.79), yline*(b/1.5)+(b/2), zline, color='brown')

    else:
        #primeiro enrolamento
        zline = np.linspace(a, 0.5*a, 50)+a*(1.01)
        xline = np.cos(zline*2*a)
        yline = np.sin(zline*2*a)
        ax.plot3D((b/1.5)*xline-(a*(-1.52)), yline*(b/1.5)+(b/2), zline, color='brown')

        #segundo enrolamento
        zline = np.linspace(a, 0.5*a, 50)+a*(1.01)
        xline = np.cos(zline*2*a)
        yline = np.sin(zline*2*a)
        ax.plot3D((b/1.5)*xline-(a*(-1.52)), yline*(b/1.5)+(b/2), zline-a, color='brown')