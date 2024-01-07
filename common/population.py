class Population:

    def __init__(self):
        self.population = []
        self.last_id = 0
        self.var_count = []
        self.probs = []
        self.global_best = 0

    # Função que adiciona um conjunto de indivíduos à população
    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    # Função que adiciona um único indivíduo à população
    def append(self, new_individual):
        self.population.append(new_individual)