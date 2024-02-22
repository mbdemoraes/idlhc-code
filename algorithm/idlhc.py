from algorithm.idlhc_utils import IDLHC_UTILS
import copy
import matplotlib.pyplot as plt

# IDLHC = Iteractive Discrete Latin Hypercube

class IDLHC:

    def __init__(self, problem, num_pdf, num_cut_pdf):
        self.idlhc_utils = IDLHC_UTILS(problem,num_pdf, num_cut_pdf)
        self.problem = problem
        self.population = None
        self.convergence_array = []
        self.best_individuals = []

    def plot_convergence(self):
        # cria a figura
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        # define o eixo x
        x_axis = [i for i in range(self.problem.num_of_generations)]

        # define o eixo y
        y_axis = self.convergence_array

        # formata o tamanho da fonte nos eixos
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.ylabel("Valor da função objetivo", fontsize=16)
        plt.xlabel("Gerações", fontsize=16)

        # plota o gráfico
        plt.plot(x_axis,y_axis, marker='o', color='blue', linestyle='None')
        plt.show()

    def do(self):
        # Cria população inicial
        self.population = self.problem.create_initial_population()

        print("Progresso:")
        for i in range(self.problem.num_of_generations):
            print(str(i)+"%",end="\r")

            # Conta as ocorrências das variáveis
            self.idlhc_utils.variable_count(self.population)
            # Atualiza o vetor de probabilidades
            self.idlhc_utils.update_probabilities(self.population)
            # Ajusta as probabilidades baseado no valor de corte
            self.idlhc_utils.adjust_cut_pdf(self.population)
            # Cria nova população
            new_population = copy.deepcopy(self.idlhc_utils.generate_new_population(self.population))
            self.population = new_population
            # Ordena a nova população
            if self.problem.direction == "MAX":
                # ordena a população de modo decrescente
                self.population.population.sort(key=lambda individual: individual.objective, reverse=True)
            else:
                # ordena a população de modo crescente
                self.population.population.sort(key=lambda individual: individual.objective)

            # Adiciona no vetor de convergência o melhor indivíduo encontrado até o momento
            self.convergence_array.append(self.population.population[0].objective)
            self.best_individuals.append(self.population.population[0].features)
            #if len(self.convergence_array) > 1 and self.convergence_array[-1] > self.convergence_array[-2]:
            #    self.best_individual = self.population.population[0]

        # Plota o gráfico de convergência
        #self.plot_convergence()

