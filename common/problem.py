from common.individual import Individual
import random
import numpy as np
from common.population import Population
import copy

class Problem:

    def __init__(self,
                 objective,
                 num_of_variables,
                 variables_range,
                 num_of_individuals,
                 direction,
                 num_of_generations,
                 mutation,
                 expand=True):
        self.num_of_variables = num_of_variables
        self.num_of_individuals = num_of_individuals
        self.objective = objective
        self.expand = expand
        self.variables_range = variables_range
        self.direction = direction
        self.num_of_generations = num_of_generations
        self.variables = self.set_variables()
        self.mutation = mutation


    def set_variables(self):
        variables = [i for i in range(min(self.variables_range), max(self.variables_range) + 1)]
        return variables


    # Cria a população inicial de modo aleatório
    def create_initial_population(self):
        population = Population()
        for k in range(self.num_of_individuals):
            individual = self.generate_individual()
            individual.id = k
            self.calculate_objectives(individual)
            population.append(individual)
            population.last_id = k
        return population


    def generate_individual(self):
        individual = Individual(self.direction)
        individual.features = [random.randint(min(self.variables_range), max(self.variables_range)) for x in range(self.num_of_variables)]
        return individual


    def calculate_objectives(self, individual):
        individual.objective = [f(individual.features) for f in self.objective]
        individual.objective = individual.objective[0]