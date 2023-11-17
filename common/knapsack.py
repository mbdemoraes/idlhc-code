class Knapsack(object):

    def __init__(self, capacity, values, weights, ratios, sorted_ratio_indexes):
        self.capacity = capacity
        self.values = values
        self.weights = weights 
        self.ratios = ratios
        self.sorted_ratio_indexes = sorted_ratio_indexes