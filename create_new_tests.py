import random
import pandas as pd
from pathlib import Path
import math
from bench_algorithms import Knapsack

def gen_problem_vars(num_of_variables=100, value_range=(1, 100), weight_range=(1, 100)):
    values = [random.randint(*value_range) for i in range(num_of_variables)]
    weights = [random.randint(*weight_range) for i in range(num_of_variables)]

    return (values, weights)


def save_knapsack_instances(num_of_steps):
    step_size = 100
    initial_size = Knapsack.minimum_size
    
    row_df = pd.DataFrame({})
    
    for i in range(num_of_steps):
        current_size = initial_size + (i * step_size)

        test_values = gen_problem_vars(
            current_size,
            value_range=(Knapsack.min_item_value, Knapsack.max_item_value),
            weight_range=(min_weight_value, max_weight_value),
        )

        values, weights = test_values

        problem_row = {
            ("values", i): values,
            ("weights",i): weights,
        }

        filepath = Path("test_data/knapsack_new.csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        row_df = pd.concat([row_df,pd.DataFrame(problem_row)],axis=1)

    row_df.to_csv(filepath, mode="w", index=False)

save_knapsack_instances(num_of_steps=10)
