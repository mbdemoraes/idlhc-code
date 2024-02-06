import math

class Knapsack:
    minimum_size = 100
    min_item_value = 1
    max_item_value = int(math.ceil(1.6 * minimum_size))
    min_weight_value = 1
    max_weight_value = int(math.ceil(1.6 * minimum_size))

    def __init__(self, values, weights):
        self.values = values
        self.weights = weights
        self.capacity = int((0.5 * self.max_weight_value) * len(self.values))

    def get_sorted_ratio_indexes(self):
        ratios = [self.values[i] / self.weights[i] for i in range(len(self.values))]
        sorted_ratio_indexes = sorted(range(len(self.values)), key=lambda i: ratios[i])
        return sorted_ratio_indexes

    def bench(self, individual):
        if len(individual.features) != len(self.values) or len(
            individual.features
        ) != len(self.weights):
            return False

        total_value = 0
        individual.total_weight = 0

        for i in range(len(individual.features)):
            if individual.features[i] != 0 and individual.features[i] != 1:
                return False
            elif individual.features[i] == 1:
                individual.total_weight += self.weights[i]
                total_value += self.values[i]

        return total_value

    def repair(self, individual):
        if individual.total_weight <= self.capacity:
            return individual
        for i in range(len(self.values)):
            if individual.total_weight > self.capacity:
                sorted_ratio_indexes = self.get_sorted_ratio_indexes()
                index = sorted_ratio_indexes[i]
                if individual.features[index] == 1:
                    individual.features[index] = 0
                    individual.total_weight -= self.weights[index]
                    individual.objective -= self.values[index]
            else:
                break
        return individual
