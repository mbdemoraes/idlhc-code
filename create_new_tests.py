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


def save_knapsack_instances():
    step_size = 100
    num_of_problems = 10
    for i in range(num_of_problems):
        test_values = gen_problem_vars(
            num_of_variables=100 + (i * step_size),
            value_range=(1, math.ceil(1.6 * (100 + (i * step_size)))),
            weight_range=(1, math.ceil(1.4 * (100 + (i * step_size)))),
        )
        values, weights, ratios, sorted_ratio_indexes = test_values

        problem_row = {
            "values": "",
            "weights": "",
            "ratios": "",
            "sorted_ratio_indexes": "",
            "capacity": int((100 + (i * step_size)) * 20 )
        }

        row_df = pd.DataFrame([problem_row])
        row_df.at[0, "values"] = values
        row_df.at[0, "weights"] = weights
        row_df.at[0, "ratios"] = ratios
        row_df.at[0, "sorted_ratio_indexes"] = sorted_ratio_indexes

        filepath = Path("test_data/knapsack_new.csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)

        row_df.to_csv(filepath, mode="a", index=False, header=False)


save_knapsack_instances()
