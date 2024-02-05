import random
import pandas as pd
from pathlib import Path
import math


def gen_problem_vars(num_of_variables=100, value_range=(1, 100), weight_range=(1, 100)):
    values = [random.randint(*value_range) for i in range(num_of_variables)]
    weights = [random.randint(*weight_range) for i in range(num_of_variables)]

    ratios = [values[i] / weights[i] for i in range(num_of_variables)]

    sorted_ratio_indexes = sorted(range(len(values)), key=lambda i: ratios[i])
    return (values, weights, ratios, sorted_ratio_indexes)


def save_knapsack_instances(num_of_steps):
    step_size = 100
    initial_size = 100
    
    row_df = pd.DataFrame({})

    #i = str(i)
    #problem_row = {
        #"values": values,
        #"weights": weights,
        #"ratios": ratios,
        #"sorted_ratio_indexes": sorted_ratio_indexes,
        ## "capacity":int((0.5 * max_weight_value) * current_size)
    #}
    
    for i in range(num_of_steps):
        current_size = initial_size + (i * step_size)

        min_item_value = 1
        max_item_value = int(math.ceil(1.6 * initial_size))
        min_weight_value = 1
        max_weight_value = int(math.ceil(1.6 * initial_size))
        num_of_variables = current_size

        test_values = gen_problem_vars(
            num_of_variables,
            value_range=(min_item_value, max_item_value),
            weight_range=(min_weight_value, max_weight_value),
        )

        values, weights, ratios, sorted_ratio_indexes = test_values

        problem_row = {
            ("values", i): values,
            ("weights",i): weights,
            ("ratios",i): ratios,
            ("sorted_ratio_indexes",i): sorted_ratio_indexes,
            #"capacity":int((0.5 * max_weight_value) * current_size)
        }

        filepath = Path("test_data/knapsack_new.csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        row_df = row_df.append(pd.DataFrame(problem_row))
        #row_df[i] = pd.DataFrame(problem_row)

    row_df.to_csv(filepath, mode="w", index=False)
save_knapsack_instances(num_of_steps=10)
