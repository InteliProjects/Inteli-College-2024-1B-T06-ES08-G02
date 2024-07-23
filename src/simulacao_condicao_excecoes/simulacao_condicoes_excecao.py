# -*- coding: utf-8 -*-
"""Simulacao_Condicoes_Excecao.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10RcA354RA7djk9YC6unb6cQXC2zRh3Ol

# Simulação das Condições de Exceção do Sistema com Melhorias

Bibliotecas Nescessarias
"""

!pip install simpy
import simpy
import random
import matplotlib.pyplot as plt

"""## Definindo o processo de atendimento bancário com exceções"""

def processo_banco(env, nome, tempo_servico, tempo_quebra, tempo_reparo, clientes_atendidos):
    while True:
        try:

            yield env.timeout(tempo_servico)
            clientes_atendidos.append(env.now)
            #Aqui vamos simular uma quebra de serviço
            if random.random() < 0.1:  #Colocamos 10% na chance de tal falha
                yield env.timeout(tempo_quebra)
                yield env.timeout(tempo_reparo)
        except simpy.Interrupt:
            print(f'{nome} interrompido em {env.now}')

"""## Cenário de Quebra de Serviço"""

def simulacao_quebra_servico(num_clientes, tempo_servico, tempo_quebra, tempo_reparo):
    env = simpy.Environment()
    clientes_atendidos = []
    for i in range(num_clientes):
        env.process(processo_banco(env, f'Caixa {i+1}', tempo_servico, tempo_quebra, tempo_reparo, clientes_atendidos))
    env.run(until=100) #Numero de simulaçoes
    return clientes_atendidos

"""## Cenário de Queda de Serviços Internos"""

def simulacao_queda_servicos(tempo_servico, tempo_falha):
    env = simpy.Environment()
    clientes_atendidos = []
    caixas = [env.process(processo_banco(env, f'Caixa {i+1}', tempo_servico, 0, 0, clientes_atendidos)) for i in range(10)]
    env.run(until=50)
    for caixa in caixas:
        caixa.interrupt('Falha completa')
    env.run(until=50 + tempo_falha)
    return clientes_atendidos

"""## Cenário Adicional: Metade dos Caixas Falhando"""

def simulacao_metade_falhando(num_clientes, tempo_servico, tempo_quebra, tempo_reparo):
    env = simpy.Environment()
    clientes_atendidos = []
    for i in range(num_clientes):
        if i % 2 == 0:
            env.process(processo_banco(env, f'Caixa {i+1}', tempo_servico, tempo_quebra, tempo_reparo, clientes_atendidos))
        else:
            env.process(processo_banco(env, f'Caixa {i+1}', tempo_servico, 0, 0, clientes_atendidos))
    env.run(until=100)
    return clientes_atendidos

"""## Configurações da Simulação e Execução dos Cenários de Exceção"""

tempo_servico = 5  # Tempo de serviço normal
tempo_quebra = 3  # Tempo da quebra do serviço
tempo_reparo = 5  # Tempo que demoraria para reparar
tempo_falha_completa = 10  # Tempo que demoraria para reparar uma falha total


resultados_quebra_servico = simulacao_quebra_servico(num_clientes=10, tempo_servico=tempo_servico, tempo_quebra=tempo_quebra, tempo_reparo=tempo_reparo)
resultados_queda_servicos = simulacao_queda_servicos(tempo_servico=tempo_servico, tempo_falha=tempo_falha_completa)
resultados_metade_falhando = simulacao_metade_falhando(num_clientes=10, tempo_servico=tempo_servico, tempo_quebra=tempo_quebra, tempo_reparo=tempo_reparo)

"""## Visualização dos Resultados"""

plt.figure(figsize=(12, 6))
plt.hist(resultados_quebra_servico, bins=50, alpha=0.7, label='Quebra de Serviço')
plt.hist(resultados_metade_falhando, bins=50, alpha=0.7, label='Metade dos Caixas Falhando')
plt.title('Distribuição dos Tempos de Atendimento')
plt.xlabel('Tempo')
plt.ylabel('Número de Clientes Atendidos')
plt.legend()
plt.show()