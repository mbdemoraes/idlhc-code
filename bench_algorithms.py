class Knapsack:
    def __init__(self, capacity, values, weights, sorted_ratio_indexes):
        self.capacity = capacity
        self.values = values
        self.weights = weights
        self.sorted_ratio_indexes = sorted_ratio_indexes

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
                index = self.sorted_ratio_indexes[i]
                if individual.features[index] == 1:
                    individual.features[index] = 0
                    individual.total_weight -= self.weights[index]
                    individual.objective -= self.values[index]
            else:
                break
        return individual
