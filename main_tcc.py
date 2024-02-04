from common.problem import Problem
from algorithm.idlhc import IDLHC
from bench_algorithms import Knapsack
import random
import pandas as pd
from pathlib import Path
import threading
#import concurrent.futures

def gen_test_cases(
    initial_population_type = 0,
    generations=100,
    num_of_individuals=100,
    num_of_variables=100,
    direction="MAX",
    num_pdf=20,
    num_cut_pdf=0.1,
):
    knapsack_tests_data = pd.read_csv("test_data/knapsack_new.csv")
    
    for count,data_row in enumerate(knapsack_tests_data.iloc):
        #data_row = knapsack_tests_data.iloc[0]
        capacity = int(data_row["capacity"])
        values = [int(i) for i in data_row["values"].replace("[","").replace("]", "").split(",")]
        weights = [int(i) for i in data_row["weights"].replace("[","").replace("]", "").split(",")]
        sorted_ratio_indexes = [
            int(i) for i in data_row["sorted_ratio_indexes"].replace("[","").replace("]", "").split(",")
        ]

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
            initial_population_type=initial_population_type,
        )

        print(threading.current_thread().name, "Test Num: ", count)
        iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
        iteration.do()
        capture_test_data(iteration,problem, count)
        
def capture_test_data(iteration : IDLHC, problem: Problem, problem_number : int):
    best_value = max(iteration.convergence_array)
    convergence_array = iteration.convergence_array
    first_gen_with_best_value = 0
    population_gen_type = problem.initial_population_type
    problem_type = "knapsack"

    for count,value in enumerate(convergence_array):
        if value == best_value:
            first_gen_with_best_value = count
            break

            
    problem_row = {
    "best_value": best_value,
    "firstgen_with_best_value": first_gen_with_best_value,
    "population_gen_type": population_gen_type,
    "problem_type": problem_type,
    "convergence_array": "",
    "problem_number": problem_number 
    }

    row_df = pd.DataFrame([problem_row])
    row_df.at[0, "convergence_array"] = convergence_array

    filepath = Path("algorithm_metrics/knapsack_problem_updated.csv")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    csv_output_lock = threading.Lock()
    with csv_output_lock:
        row_df.to_csv(filepath, mode="a", index=False, header=False)

for i in range(5):
    t1 = threading.Thread(target=gen_test_cases, args=(0,) )
    t2 = threading.Thread(target=gen_test_cases, args=(1,) )
    t3 = threading.Thread(target=gen_test_cases, args=(2,) )
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

print("done")