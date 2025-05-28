import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

from desafio_1 import initialize_parameters, first_and_second_current, \
    conductor_section, bitola,magnectic_section,core_geometric_section_1, \
    calculate_a_and_b_geometric_section, core_geometric_section, \
    core_magnetic_section, calculate_turns_number_1, \
    dimensions_core, blades_qtd, blade_type

if __name__ == '__main__': 

    print('Selecione o desafio. Exemplo: \n Desafio 1 --> D1 \n Desafio 2 --> D2 \n ...')
    desafio = input("Desafio: ")

    try:
        if desafio == 'D1':
            print('Escreva os parâmetros do transformador:')
            acesita_blade_espessura= 0.035
            W2 = input('A potência de saída é: ')
            V2 = input('Tensão de saída é: ')
            V1 = input('Tensão de entrada é: ')
            frequency = input('Frequência: ')
            if initialize_parameters(W2,V2,V1) != None:
                W2 = int(W2)
                V2 = int(V2)
                V1 = int(V1)
                frequency = int(frequency)
                first_current, second_current = first_and_second_current(W2,V2,V1)
            else:
                print("Valores não inicializados de forma correta, assinalando valor default para zero")
                first_current, second_current = 0,0
            W1 = 1.1 * W2 
            
            section_1 = conductor_section(first_current, W2)
            section_2 = conductor_section(second_current, W2)

            section_1_bitola = bitola(section_1)
            section_2_bitola = bitola(section_2)

            magnetic_section = magnectic_section(W1,frequency,False)
            geometric_section = core_geometric_section_1(magnetic_section)

            if(W2>800):
                print("Uso das laminas Compridas pois a potencia é maior que 800VA")
            else:
                print("Uso das laminas padronizadas pois a potencia é menor que 800VA")

            a = round(math.sqrt(geometric_section))
            blade = blade_type(a)
            b = round(calculate_a_and_b_geometric_section(geometric_section,a),1)
            
            
            core_gs = core_geometric_section(a, b)
            core_ms =round(core_magnetic_section(a, b),1)
            n1 = calculate_turns_number_1(frequency, W1, core_ms)
            n2 = calculate_turns_number_1(frequency,  W2, core_ms)*1.1

            dimensions= dimensions_core(a,b,W2)
            qtd_blades= blades_qtd(b,acesita_blade_espessura)


            print("Número de Espiras do Enrolamento Primário: ", n1)
            print("Número de Espiras do Enrolamento Secundário: ", n2)
            print("Bitola do cabo primário: ", section_1_bitola)
            print("Bitola do cabo secundário: ", section_2_bitola)
            print("Tipo de lâmina: ", blade)
            print("Quantidade de lâminas: ", qtd_blades)
            print("Dimensões: ",dimensions)

    
    except ValueError:
        print('Valor do desafio não é uma string')
