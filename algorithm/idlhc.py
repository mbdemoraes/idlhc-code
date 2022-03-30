from algorithm.idlhc_utils import IDLHC_UTILS
import copy
import itertools
import numpy as np
import matplotlib.pyplot as plt

class IDLHC:

    def __init__(self, problem, num_pdf, num_cut_pdf):
        self.idlhc_utils = IDLHC_UTILS(problem,num_pdf, num_cut_pdf)
        self.problem = problem
        self.population = None
        self.convergence_array = []

    def plot_convergence(self):
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        x_axis = [i for i in range(self.problem.num_of_generations)]
        y_axis = self.convergence_array

        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.ylabel("Valor da função objetivo", fontsize=16)
        plt.xlabel("Gerações", fontsize=16)

        plt.plot(x_axis,y_axis, marker='o', color='blue', linestyle='None')
        plt.show()

    def do(self):
        self.population = self.problem.create_initial_population()

        for i in range(self.problem.num_of_generations):
            print("Generation: " + str(i))
            #print("Generating variable counts...")
            self.idlhc_utils.variable_count(self.population)
            #print("Updating probabilities...")
            self.idlhc_utils.update_probabilities(self.population)
            #print("Adjusting probabilities based on parameter cut...")
            self.idlhc_utils.adjust_cut_pdf(self.population)
            #print("Generate new population based on probabilities...")
            new_population = copy.deepcopy(self.idlhc_utils.generate_new_population(self.population))
            self.population = new_population
            self.population.population.sort(key=lambda individual: individual.objective, reverse=True)

            self.convergence_array.append(self.population.population[0].objective)

        self.plot_convergence()
        #print(self.population.population[0].objective)
