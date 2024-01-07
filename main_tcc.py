from common.problem import Problem
from algorithm.idlhc import IDLHC
from bench_algorithms import Knapsack
import random
import pandas as pd
from pathlib import Path

generations = 100
num_of_individuals = 100
num_of_variables = 100
direction = "MAX"

num_pdf = 20
num_cut_pdf = 0.1

capacity = 2000
values = [random.randint(1, 100) for i in range(num_of_variables)]
weights = [random.randint(1, 100) for i in range(num_of_variables)]
ratios = [values[i] / weights[i] for i in range(num_of_variables)]

sorted_ratio_indexes = sorted(range(len(values)), key=lambda i: values[i])

knapsack = Knapsack(capacity, values, weights, sorted_ratio_indexes)

problem = Problem(
    num_of_variables=num_of_variables,
    num_of_individuals=num_of_individuals,
    num_of_generations=generations,
    objective=[knapsack.bench],
    repair=[knapsack.repair],
    mutation=(1 / num_of_variables),
    variables_range=[0, 1],
    direction=direction,
    initial_population_type=2,
)

iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
iteration.do()

num_iterations = 1

first_gens = []
best_values = []
population_gen_type = problem.initial_population_type
problem_type = "knapsack"
convergences = []

for i in range(num_iterations):
    iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
    iteration.do()
    best_value = max(iteration.convergence_array)
    best_values.append(best_value)
    convergences.append(iteration.convergence_array)

    for n in range(len(iteration.convergence_array)):
        if iteration.convergence_array[n] == best_values[i]:
            first_gens.append(n)
            break

df2 = pd.DataFrame(
    {
        "best_value": best_values,
        "firstgen_with_best_value": first_gens,
        "population_gen_type": population_gen_type,
        "problem_type": problem_type,
        "convergence_array": "",
    }
)

for i in range(len(best_values)):
    df2.at[i, "convergence_array"] = convergences[i]

filepath = Path("metrics/knapsack.csv")

filepath.parent.mkdir(parents=True, exist_ok=True)

df2.to_csv(filepath, mode="a", index=False, header=False)


final_dict = {}
num_of_problems = 100
capacity = 2000


def gen_problem_vars():
    values = [random.randint(1, 100) for i in range(num_of_variables)]
    weights = [random.randint(1, 100) for i in range(num_of_variables)]

    ratios = [values[i] / weights[i] for i in range(num_of_variables)]

    sorted_ratio_indexes = sorted(range(len(values)), key=lambda i: ratios[i])
    return values, weights, ratios, sorted_ratio_indexes


#zero_list = ["" for i in range(num_of_problems)]

#problems_to_bench = pd.DataFrame(
    #{
        #"values": zero_list.copy(),
        #"weights": zero_list.copy(),
        #"sorted_ratio_indexes": zero_list.copy(),
        #"ratios": zero_list.copy(),
        #"capacity": capacity,
    #}
#)


#for i in range(num_of_problems):
    #values, weights, ratios, sorted_ratio_indexes = gen_problem_vars()

    #problems_to_bench.at[i, "values"] = values
    #problems_to_bench.at[i, "weights"] = weights
    #problems_to_bench.at[i, "ratios"] = ratios
    #problems_to_bench.at[i, "sorted_ratio_indexes"] = sorted_ratio_indexes


#filepath_1 = Path("problems/knapsack_problems.csv")

#filepath_1.parent.mkdir(parents=True, exist_ok=True)

#problems_to_bench.to_csv(filepath_1, mode="a", index=False, header=True)
