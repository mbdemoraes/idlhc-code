import copy
from common.individual import Individual
import numpy as np
from common.population import Population
import random
from operator import attrgetter
from sklearn.cluster import KMeans
from sklearn import datasets, mixture



class IDLHC_UTILS:

    def __init__(self, problem,
                 AMOSTRAS_PDF=20,
                 CORTE_PDF=0.2):

        self.num_pdf = AMOSTRAS_PDF
        self.num_cut_pdf = CORTE_PDF
        self.problem = problem


    def variable_count(self, population):
        count_var = [[] for i in range(self.problem.num_of_variables)]
        best_features = []

        if self.problem.direction=="MAX":
            # ordena a população de modo decrescente
            population.population.sort(key=lambda individual: individual.objective, reverse=True)
        else:
            # ordena a população de modo crescente
            population.population.sort(key=lambda individual: individual.objective)

        # Seleciona os NUM_PDF melhores indivíduos e adiciona
        # seus vetores de decisão em uma lista
        for i in range(len(population.population)):
            if i < self.num_pdf:
                best_features.append(population.population[i].features)
            else:
                break

        # Busca a lista com os melhores vetores de decisão
        # e conta quantas vezes cada possível variável apareceu nesses vetores
        for best in best_features:
            counter = 0
            for variable in best:
                if counter < self.problem.num_of_variables:
                    count_var[counter].append(variable)
                    counter += 1
                else:
                    break
        # Adiciona o vetor com a quantidade de aparições na população
        population.var_count = copy.deepcopy(count_var)



    def update_probabilities(self, population):
        # A partir do vetor com a quantidade de vezes que cada possível variável apareceu nos melhores
        # cria um vetor de probabilidades de ocorrência para cada possibilidade
        new_probabilities = [[] for i in range(self.problem.num_of_variables)]
        for i in range(self.problem.num_of_variables):
            for candidate in self.problem.variables_range:
                freq_norm = round(population.var_count[i].count(candidate) / self.num_pdf, 2)
                new_probabilities[i].append(freq_norm)
        population.probs = copy.deepcopy(new_probabilities)


    def individual_cut_pdf(self, prob):
        # Função que identifica probabilidades que estejam abaixo do valor de corte
        # Zera essas probabilidades e redistribui as probabilidades que sobraram
        # para as demais opções, para que a soma seja sempre 1

        lista_probabilidades_atualizada = copy.deepcopy(prob)
        np_probabilidades = np.array(prob)
        # Máscara que identifica as probabilidades que estejam abaixo de um valor de corte
        mask_corte_inferior = np_probabilidades <= self.num_cut_pdf
        if not all(mask_corte_inferior):
            if any(mask_corte_inferior):
                np_probabilidades[~mask_corte_inferior] = np_probabilidades[~mask_corte_inferior] + sum(
                    np_probabilidades[mask_corte_inferior]) / len(np_probabilidades[~mask_corte_inferior])
                np_probabilidades[mask_corte_inferior] = 0
                lista_probabilidades_atualizada = [float(probability) for probability in list(np_probabilidades)]

        return copy.deepcopy(lista_probabilidades_atualizada)

    def adjust_cut_pdf(self, population):
        for i in range (len(population.probs)):
            population.probs[i] = self.individual_cut_pdf(population.probs[i])


    def generate_new_population(self, population):
        new_population = Population()
        new_population.probs = copy.deepcopy(population.probs)
        features = []
        for i in range(self.problem.num_of_variables):
            prob = population.probs[i]
            new_feature = self.generate_samples(prob, self.problem.variables, self.problem.num_of_individuals)
            features.append(new_feature)

        features = np.array(features).T
        features = self.check_duplicity(features)

        for i in range(len(features)):
            individual = Individual(direction=self.problem.direction)
            individual.features = features[i].tolist()
            self.problem.calculate_objectives(individual)
            new_population.append(individual)
        return new_population

    def check_duplicity(self, sampled: np.array) -> np.array:
        """
        Chega duplicidade nos sorteios e retona solucoes sem repeticao
        :param sampled: vetor com as variaveis amostradas para cada amostra
        :return sampled_clean: amostragem sem repeticao
        """
        sampled_clean, c = np.unique(sampled, return_counts=True, axis=0)
        return sampled_clean

    # Função que utiliza as probabilidades e cria indivíduos com base nessa probabilidade
    def generate_samples(self, probs: list, values: list, samples: int) -> list:
        """
        gera amostragem para uma variavel
        :param probs: probabilidade dos niveis das variaveis
        :param values: valor de cada nivel das variaveis
        :param samples: numero de amostras esperado
        :return sampled values: vetor com a amostragem das variaveis
        """
        sampled_values = []
        for prob, value in zip(probs, values):
            sampled_values += round(samples * prob) * [value]

        if len(sampled_values) > 0:
            while len(sampled_values) != samples:
                unicos, n_repeticoes = np.unique(sampled_values, return_counts=True, axis=0)
                c = list(zip(unicos, n_repeticoes))
                random.shuffle(c)
                unicos, n_repeticoes = zip(*c)
                if len(sampled_values) > samples:
                    sampled_values.remove(unicos[np.argmax(n_repeticoes)])
                elif len(sampled_values) < samples:
                    sampled_values += [unicos[np.argmin(n_repeticoes)]]
            random.shuffle(sampled_values)
        return sampled_values