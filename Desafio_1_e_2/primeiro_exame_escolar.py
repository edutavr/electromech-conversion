import pandas as pd
import numpy as np
from desafio_1 import initialize_parameters, first_and_second_current, \
    conductor_section, bitola,magnectic_section,core_geometric_section_1, \
    calculate_a_and_b_geometric_section, core_geometric_section, \
    core_magnetic_section, calculate_turns_number_1, iron_core_weight, \
    cooper_section, calculate_lm, cooper_weight, dimensions_core

if __name__ == '__main__': 

    print('Selecione o desafio. Exemplo: \n Desafio 1 --> D1 \n Desafio 2 --> D2 \n ...')
    desafio = input("Desafio: ")

    try:
        if desafio == 'D1':
            print('Escreva os parâmetros do transformador:')
            W2 = input('A potência de saída é: ')
            V2 = input('Tensão de saída é: ')
            V1 = input('Tensão de entrada é: ')
            frequency = input('Frequência: ')
            if initialize_parameters(W2,V2,V1) != None:
                first_current, second_current = first_and_second_current(W2,V2,V1)
            else:
                print("Valores não inicializados de forma correta, assinalando valor default para zero")
                first_current, second_current = 0,0
            W1 = 1.1 * W2 
            
            section_1 = conductor_section(first_current, W2)
            section_2 = conductor_section(second_current, W2)

            section_1_bitola = bitola(section_1)
            section_2_bitola = bitola(section_2)

            magnetic_section = magnectic_section(W1,frequency,True)
            geometric_section = core_geometric_section_1(magnetic_section)

            if geometric_section > 25: 
                a = 5
            else: 
                a = 4
            
            b = round(calculate_a_and_b_geometric_section(geometric_section),1)
            core_gs = core_geometric_section(a, b)
            core_ms =round(core_magnetic_section(a, b),1)
            n1 = calculate_turns_number_1(frequency, W1, core_ms)
            n2 = calculate_turns_number_1(frequency,  W2, core_ms)*1.1

            iron_weight = iron_core_weight(core_gs)
            section_cooper= cooper_section(n1,section_1,n2,section_2)
            comprimento_medio_espiras_cobre = calculate_lm(core_gs)
            weight_cooper = cooper_weight(section_cooper,comprimento_medio_espiras_cobre)

            dimensions= dimensions_core(a,b,W2)
            qtd_blades= blades_qtd(b,acesita_blade_espessura)

    
    except ValueError:
        print('Valor do desafio não é uma string')
