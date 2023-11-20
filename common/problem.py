from common.individual import Individual
import random
from common.population import Population
from math import cos

class Problem:

    def __init__(self,
                 objective,
                 repair,
                 num_of_variables,
                 variables_range,
                 num_of_individuals,
                 direction,
                 num_of_generations,
                 mutation,
                 expand=True,
                 initial_population_type = 0,
                 objective_vars = 0
                 ):
        self.num_of_variables = num_of_variables
        self.num_of_individuals = num_of_individuals
        self.objective = objective
        self.repair = repair
        self.expand = expand
        self.variables_range = variables_range
        self.direction = direction
        self.num_of_generations = num_of_generations
        self.variables = self.set_variables()
        self.mutation = mutation
        self.initial_population_type = initial_population_type
        self.objective_vars = objective_vars

        self.current_value = None

    # Define quais possíveis variáveis do problema
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


    # Gera um indivíduo
    def generate_individual(self):
        salt = random.random() * (10 ** -6)
        # print(salt)
        if self.initial_population_type == 0:
            def simpe_generation(self):
                individual = Individual(self.direction)
                individual.features = [random.randint(min(self.variables_range), max(self.variables_range)) for x in range(self.num_of_variables)]
                return individual
            return simpe_generation(self)
        
        elif self.initial_population_type == 1:
            def logistic_map_generation(self):
                individual = Individual(self.direction)
                individual.features = [0.254561 if self.current_value == None else self.current_value]
                r = 3.999999301 + salt
                for n in range(self.num_of_variables-1):
                    individual.features.append( r*individual.features[n]*(1-individual.features[n]) )
                self.current_value = individual.features[-1]
                individual.features = [0 if i < 0.5 else 1 for i in individual.features]
                return individual
            return logistic_map_generation(self)
        
        elif self.initial_population_type == 2:
            def cosin_map_generation(self):
                individual = Individual(self.direction)
                individual.features = [0.1 if self.current_value == None else self.current_value]
                r = 6 + salt
                for n in range(self.num_of_variables-1):
                    individual.features.append( cos(r*individual.features[n]) )
                self.current_value = individual.features[-1]
                individual.features = [0 if i <= 0 else 1 for i in individual.features]
                return individual
            return cosin_map_generation(self)


    # Calcula o valor da função objetivo
    def calculate_objectives(self, individual):
        individual.objective = [f(individual, self.objective_vars) for f in self.objective]
        individual.objective = individual.objective[0]
        self.repair_objective(individual)

    def repair_objective(self, individual):
        temp = [f(individual,self.objective_vars) for f in self.repair]
        individual = temp[0] 