from common.problem import Problem
from algorithm.idlhc import IDLHC


# Função objetivo que soma a quantidade de 1 dentro do vetor de decisão
def f1(individual):
    return sum(individual)


# CONFIGURAÇÕES
generations = 50  # quantidade de gerações (ou iterações)
num_of_individuals = 100  # controla quantos indivíduos existem na população
num_of_variables = 100  # controla o tamanho do vetor de decisão
direction = "MAX"  # se o problema é de maximização (MAX) ou de minimização (MIN)

# Parâmetros do IDLHC

num_pdf = 20 # quantos indivíduos são considerados para a construção da função de distribuição de probabilidade
num_cut_pdf = 0.1 # porcentagem utilizada para cortar opções

# define a classe de problema
problem = Problem(
    num_of_variables=num_of_variables,
    num_of_individuals=num_of_individuals,
    num_of_generations=generations,
    objective=[f1],  # ATENÇÃO: aqui ele passa uma função
    mutation=(1 / num_of_variables),
    variables_range=[0, 1],
    direction=direction,
)

# cria o objeto da classe IDLHC
iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)

# executa o algoritmo
iteration.do()


def knapsack_bench(individual, knapsack_vars):
    if len(individual.features) != len(knapsack_vars.values) or len(
        individual.features
    ) != len(knapsack_vars.weights):
        return False

    total_value = 0
    individual.total_weight = 0

    for i in range(len(individual.features)):
        if individual.features[i] != 0 and individual.features[i] != 1:
            return False
        elif individual.features[i] == 1:
            individual.total_weight += knapsack_vars.weights[i]
            total_value += knapsack_vars.values[i]

    return total_value


def knapsack_repair(individual, knapsack_vars):
    if individual.total_weight <= knapsack_vars.capacity:
        return individual
    for i in range(len(knapsack_vars.values)):
        if individual.total_weight > knapsack_vars.capacity:
            index = knapsack_vars.sorted_ratio_indexes[i]
            if individual.features[index] == 1:
                individual.features[index] = 0
                individual.total_weight -= knapsack_vars.weights[index]
                individual.objective -= knapsack_vars.values[index]
        else:
            break
    return individual


# define a classe de problema
problem = Problem(
    num_of_variables=num_of_variables,
    num_of_individuals=num_of_individuals,
    num_of_generations=generations,
    objective=[knapsack_bench],  # ATENÇÃO: aqui ele passa uma função
    repair=[knapsack_repair],
    objective_vars=knapsack_vars,
    mutation=(1 / num_of_variables),
    variables_range=[0, 1],
    direction=direction,
    initial_population_type=2,
)
