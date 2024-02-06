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
    direction="MAX",
    num_pdf=20,
    num_cut_pdf=0.1,
):
    knapsack_tests_data = pd.read_csv("test_data/knapsack_new.csv",header=[0,1])
    total_knapsack_instances = list(knapsack_tests_data)[-1][1]
    
    #for current_instance in range(int(total_knapsack_instances)+1):      
    kkkk = [9]
    for current_instance in kkkk:      
        values = list(knapsack_tests_data["values"][str(current_instance)].dropna())
        weights = list(knapsack_tests_data["weights"][str(current_instance)].dropna())
        
        knapsack = Knapsack(values, weights)

        num_of_variables = len(values)
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

        print(threading.current_thread().name, "Test Num: ", current_instance)
        iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
        iteration.do()
        capture_test_data(iteration,problem, current_instance)
        
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