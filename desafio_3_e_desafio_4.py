import numpy as np
import matplotlib.pyplot as plt
import cmath
from matplotlib.patches import Arc

class AnaliseCarregamentoTransformador:
    """
    Realiza análise de desempenho do transformador sob diferentes condições de carga,
    incluindo cálculo de regulação de tensão e eficiência.
    """
    
    def __init__(self, parametros_transformador, fator_potencia=0.92, tipo_fator_potencia='atrasado', potencia_carga_kVA=None):
        """
        Inicializa o transformador monofásico com base nos parâmetros calculados
        
        Parâmetros:
        parametros_transformador: Dicionário com parâmetros do transformador
        fator_potencia: Fator de potência da carga (0 a 1)
        tipo_fator_potencia: 'atrasado' (indutivo) ou 'adiantado' (capacitivo)
        potencia_carga_kVA: Potência da carga (kVA). Se None, usa potência nominal.
        """
        self.parametros = parametros_transformador
        self.potencia_nominal = self.parametros['potencia_nominal']
        self.tensao_primaria_nominal = self.parametros['tensao_alta']
        self.tensao_secundaria_nominal = self.parametros['tensao_baixa']
        self.impedancia_equivalente = complex(
            self.parametros['resistencia_equivalente_alta'],
            self.parametros['reatancia_equivalente_alta']
        )
        self.fator_potencia = fator_potencia
        self.tipo_fator_potencia = tipo_fator_potencia.lower()
        
        # Determina potência de carga considerando valor nominal se não especificado
        self.potencia_carga = potencia_carga_kVA * 1e3 if potencia_carga_kVA is not None else self.potencia_nominal
        
        # Relação de transformação entre enrolamentos
        self.relacao_transformacao = self.parametros['relacao_transformacao']
        
        # Valida tipo de fator de potência
        if self.tipo_fator_potencia not in ['atrasado', 'adiantado']:
            raise ValueError("tipo_fator_potencia deve ser 'atrasado' ou 'adiantado'")
    
    def calcular_corrente_secundaria(self):
        """
        Calcula a corrente no secundário considerando fator de potência
        
        Retorna:
        Fasor complexo da corrente secundária (A)
        """
        # --- AJUSTE ADICIONADO ---
        # Garante que o fator de potência esteja no intervalo matemático válido para evitar erros.
        if not -1.0 <= self.fator_potencia <= 1.0:
            raise ValueError(f"Fator de Potência Inválido: {self.fator_potencia}. O valor deve estar entre -1.0 e 1.0.")

        modulo_corrente = self.potencia_carga / self.tensao_secundaria_nominal
        angulo = np.arccos(self.fator_potencia)
        
        # Define ângulo conforme tipo de carga (indutiva ou capacitiva)
        if self.tipo_fator_potencia == 'atrasado':
            angulo = -angulo  # Corrente atrasada em relação à tensão
            
        return cmath.rect(modulo_corrente, angulo)
    
    def calcular_tensao_sem_carga(self):
        """
        Calcula a tensão secundária em vazio usando modelo equivalente
        
        Retorna:
        Fasor complexo da tensão em vazio (V)
        """
        # Os parâmetros já estão referidos ao lado de alta, mas os cálculos são feitos
        # como se estivessem no lado de baixa para a análise de regulação.
        # Por isso, vamos referir a impedância para o lado de baixa.
        impedancia_eq_baixa = self.impedancia_equivalente / (self.relacao_transformacao**2)
        
        corrente_secundaria = self.calcular_corrente_secundaria()
        tensao_plena_carga = self.tensao_secundaria_nominal
        
        # Calcula tensão em vazio referida ao secundário
        return tensao_plena_carga + impedancia_eq_baixa * corrente_secundaria
    
    def calcular_regulacao_tensao(self):
        """
        Calcula a regulação percentual de tensão
        
        Retorna:
        Regulação percentual (|V_vazio| - |V_carga|)/|V_carga| * 100
        """
        tensao_sem_carga = self.calcular_tensao_sem_carga()
        tensao_plena_carga = self.tensao_secundaria_nominal
        
        return (abs(tensao_sem_carga) - tensao_plena_carga) / tensao_plena_carga * 100
    
    def calcular_eficiencia(self):
        """
        Calcula a eficiência do transformador sob carga
        
        Retorna:
        Eficiência percentual (P_saída/P_entrada * 100)
        """
        # Potência ativa entregue à carga
        potencia_saida = self.potencia_carga * self.fator_potencia
        
        # Perdas no Cobre (Pcu)
        corrente_secundaria_modulo = self.potencia_carga / self.tensao_secundaria_nominal
        resistencia_eq_baixa = self.impedancia_equivalente.real / (self.relacao_transformacao**2)
        perdas_cobre = resistencia_eq_baixa * (corrente_secundaria_modulo ** 2)

        # Perdas no Núcleo (Pfe) - obtidas do ensaio de circuito aberto
        resistencia_nucleo_baixa = self.parametros['resistencia_nucleo_baixa']
        perdas_nucleo = (self.tensao_secundaria_nominal ** 2) / resistencia_nucleo_baixa
        
        potencia_entrada = potencia_saida + perdas_cobre + perdas_nucleo
        
        if potencia_entrada == 0:
            return 0

        return (potencia_saida / potencia_entrada) * 100
    
    def plotar_diagrama_fasorial(self):
        """
        Gera diagrama fasorial mostrando relações entre tensões e correntes
        sob condição de carga.
        """
        tensao_sec_vazio = self.calcular_tensao_sem_carga()
        corrente_sec = self.calcular_corrente_secundaria()
        tensao_sec_carga = complex(self.tensao_secundaria_nominal, 0)
        
        impedancia_eq_baixa = self.impedancia_equivalente / (self.relacao_transformacao**2)
        
        queda_resistiva = impedancia_eq_baixa.real * corrente_sec
        queda_indutiva = 1j * impedancia_eq_baixa.imag * corrente_sec

        # Prepara componentes vetoriais
        origem = np.array([0, 0]) # --- CORREÇÃO APLICADA ---
        v_carga_xy = np.array([tensao_sec_carga.real, tensao_sec_carga.imag])
        i_sec_xy = np.array([corrente_sec.real, corrente_sec.imag])
        queda_r_xy = np.array([queda_resistiva.real, queda_resistiva.imag])
        queda_x_xy = np.array([queda_indutiva.real, queda_indutiva.imag])
        v_vazio_xy = np.array([tensao_sec_vazio.real, tensao_sec_vazio.imag])
        
        # Configura figura
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        
        # Plota fasores principais
        plt.quiver(*origem, *v_carga_xy, angles='xy', scale_units='xy', scale=1, color='blue', width=0.005, label=f'$V_2$ (carga) = {abs(tensao_sec_carga):.1f} V')
        plt.quiver(*origem, *i_sec_xy, angles='xy', scale_units='xy', scale=1, color='orange', width=0.005, label=f'$I_2$ = {abs(corrente_sec):.1f} A')
        plt.quiver(*origem, *v_vazio_xy, angles='xy', scale_units='xy', scale=1, color='green', width=0.005, label=f'$V_2$ (vazio) = {abs(tensao_sec_vazio):.1f} V')
        
        # Plota componentes da queda de tensão
        plt.quiver(*v_carga_xy, *queda_r_xy, angles='xy', scale_units='xy', scale=1, color='red', width=0.003, label='$R_{eq} \cdot I_2$')
        plt.quiver(*(v_carga_xy + queda_r_xy), *queda_x_xy, angles='xy', scale_units='xy', scale=1, color='purple', width=0.003, label='$jX_{eq} \cdot I_2$')
        
        # Adiciona ângulo do fator de potência
        if abs(corrente_sec) > 0:
            angulo_fp_rad = cmath.phase(corrente_sec)
            angulo_fp_deg = np.degrees(angulo_fp_rad)
            raio = abs(tensao_sec_carga) * 0.3
            
            theta1, theta2 = (angulo_fp_deg, 0) if angulo_fp_deg < 0 else (0, angulo_fp_deg)
            arco = Arc(origem, 2*raio, 2*raio, angle=0, theta1=theta1, theta2=theta2, color='k', linestyle='--')
            ax.add_patch(arco)
            
            angulo_texto_rad = angulo_fp_rad / 2
            plt.text(raio * np.cos(angulo_texto_rad), raio * np.sin(angulo_texto_rad), f'$\\phi = {abs(angulo_fp_deg):.1f}^\\circ$', fontsize=12)
        
        # Configurações finais do gráfico
        limite_max = abs(tensao_sec_vazio) * 1.2
        plt.xlim(-limite_max, limite_max)
        plt.ylim(-limite_max, limite_max)
        plt.axhline(0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(0, color='k', linestyle='--', alpha=0.3)
        plt.grid(True, linestyle='--', alpha=0.5)
        
        angulo_graus_carga = np.degrees(np.arccos(self.fator_potencia))
        tipo_carga_str = "Indutiva" if self.tipo_fator_potencia == 'atrasado' else "Capacitiva"
        plt.title(f'Diagrama Fasorial - Carga {tipo_carga_str} (FP={self.fator_potencia}, $\\phi={angulo_graus_carga:.1f}^\\circ$)')
        plt.xlabel('Componente Real (V ou A)')
        plt.ylabel('Componente Imaginária (V ou A)')
        plt.legend(loc='best')
        plt.gca().set_aspect('equal', adjustable='box')
        
        return plt

class AnaliseTransformadorMonofasico:
    """
    Determina parâmetros do transformador a partir de ensaios
    de circuito aberto e curto-circuito.
    """
    
    def __init__(self, tensao_ca, corrente_ca, potencia_ca, tensao_cc, corrente_cc, potencia_cc, 
                 tensao_baixa, tensao_alta, frequencia=60):
        """
        Inicializa com dados de ensaios e características nominais
        """
        self.tensao_ca = tensao_ca
        self.corrente_ca = corrente_ca
        self.potencia_ca = potencia_ca
        self.tensao_cc = tensao_cc
        self.corrente_cc = corrente_cc
        self.potencia_cc = potencia_cc
        self.tensao_baixa = tensao_baixa
        self.tensao_alta = tensao_alta
        self.frequencia = frequencia
        self.relacao_transformacao = tensao_alta / tensao_baixa
        
        self.parametros = {}
        self.calcular_parametros()
    
    def calcular_parametros(self):
        """Calcula parâmetros do circuito equivalente"""
        # 1. Parâmetros do ensaio em vazio (lado BT)
        resistencia_nucleo_baixa = (self.tensao_ca ** 2) / self.potencia_ca
        admitancia_ca = self.corrente_ca / self.tensao_ca
        condutancia_nucleo_baixa = 1 / resistencia_nucleo_baixa
        # Y = sqrt(G^2 + B^2) => B = sqrt(Y^2 - G^2)
        suscetancia_mag_baixa = np.sqrt(admitancia_ca**2 - condutancia_nucleo_baixa**2)
        reatancia_magnetizacao_baixa = 1 / suscetancia_mag_baixa

        # 2. Parâmetros do ensaio em curto (lado AT)
        resistencia_equivalente_alta = self.potencia_cc / (self.corrente_cc ** 2)
        impedancia_cc = self.tensao_cc / self.corrente_cc
        reatancia_equivalente_alta = np.sqrt(impedancia_cc**2 - resistencia_equivalente_alta**2)
        
        # Armazena os parâmetros no dicionário
        self.parametros = {
            'resistencia_nucleo_baixa': resistencia_nucleo_baixa,
            'reatancia_magnetizacao_baixa': reatancia_magnetizacao_baixa,
            'resistencia_equivalente_alta': resistencia_equivalente_alta,
            'reatancia_equivalente_alta': reatancia_equivalente_alta,
            'relacao_transformacao': self.relacao_transformacao,
            'tensao_baixa': self.tensao_baixa,
            'tensao_alta': self.tensao_alta,
            'potencia_nominal': self.tensao_alta * self.corrente_cc
        }

    def obter_parametros(self):
        """Retorna dicionário com todos os parâmetros calculados"""
        return self.parametros
    
    def imprimir_parametros(self):
        """Apresenta parâmetros calculados formatados"""
        params = self.obter_parametros()
        a = params['relacao_transformacao']
        
        print("\n" + "="*60)
        print("PARÂMETROS DO TRANSFORMADOR MONOFÁSICO")
        print("="*60)
        
        print("\n--- Parâmetros do Ramo de Excitação (Referidos ao Lado de Baixa) ---")
        print(f"Resistência de perdas no núcleo (Rc_BT): {params['resistencia_nucleo_baixa']:.2f} Ω")
        print(f"Reatância de magnetização (Xm_BT): {params['reatancia_magnetizacao_baixa']:.2f} Ω")
        
        print("\n--- Parâmetros Série Equivalentes (Referidos ao Lado de Alta) ---")
        print(f"Resistência equivalente série (Req_AT): {params['resistencia_equivalente_alta']:.2f} Ω")
        print(f"Reatância equivalente série (Xeq_AT): {params['reatancia_equivalente_alta']:.2f} Ω")
        
        res_nucleo_alta = params['resistencia_nucleo_baixa'] * a**2
        reat_mag_alta = params['reatancia_magnetizacao_baixa'] * a**2
        print(f"\n--- Parâmetros do Ramo de Excitação (Referidos ao Lado de Alta) ---")
        print(f"Resistência de perdas no núcleo (Rc_AT): {res_nucleo_alta/1000:.2f} kΩ")
        print(f"Reatância de magnetização (Xm_AT): {reat_mag_alta/1000:.2f} kΩ")

        print("\n--- Características Nominais ---")
        print(f"Relação de transformação (a): {params['relacao_transformacao']:.2f}")
        print(f"Potência nominal aparente (Sn): {params['potencia_nominal']/1000:.2f} kVA")

def main():
    """Função principal para execução dos desafios 3 e 4"""
    
    # ======================================================================================
    # DESAFIO 3: Determinação dos parâmetros do transformador a partir dos ensaios
    # Os valores foram alterados para simular um transformador de 10 kVA, 13200/240 V.
    # ======================================================================================
    print("\n=== DESAFIO 3: Determinação de Parâmetros ===")
    transformador = AnaliseTransformadorMonofasico(
        tensao_ca=240,      # Tensão ensaio vazio Vca (V) - Lado BT
        corrente_ca=0.2,    # Corrente ensaio vazio Ica (A)
        potencia_ca=35,     # Potência ensaio vazio Pca (W)
        tensao_cc=528,      # Tensão ensaio curto Vcc (V) - Lado AT
        corrente_cc=0.757,  # Corrente ensaio curto Icc (A) - Nominal AT
        potencia_cc=120,    # Potência ensaio curto Pcc (W)
        tensao_baixa=240,   # Tensão nominal V_baixa (V)
        tensao_alta=13200   # Tensão nominal V_alta (V)
    )
    transformador.imprimir_parametros()
    
    # Prepara parâmetros para a próxima etapa
    parametros_calculados = transformador.obter_parametros()
    
    # ======================================================================================
    # DESAFIO 4: Cálculo da Regulação e Eficiência, e plotagem do diagrama fasorial
    # Os valores foram alterados para uma carga de 8 kVA com fator de potência 0.7 indutivo.
    # ======================================================================================
    print("\n\n=== DESAFIO 4: Análise de Desempenho Sob Carga ===")
    transformador_carregado = AnaliseCarregamentoTransformador(
        parametros_transformador=parametros_calculados,
        fator_potencia=0.7,
        tipo_fator_potencia='atrasado',  # 'atrasado' para indutivo, 'adiantado' para capacitivo
        potencia_carga_kVA=8             # Potência da carga (8 kVA = 80% da nominal)
    )
    
    # Resultados operacionais
    print("\n--- Resultados Operacionais ---")
    print(f"Regulação de tensão: {transformador_carregado.calcular_regulacao_tensao():.2f}%")
    print(f"Eficiência em carga: {transformador_carregado.calcular_eficiencia():.2f}%")
    
    # Gera diagrama fasorial
    print("\nGerando diagrama fasorial de operação sob carga...")
    plot_diagrama = transformador_carregado.plotar_diagrama_fasorial()
    plot_diagrama.show()

if __name__ == "__main__":
    main()