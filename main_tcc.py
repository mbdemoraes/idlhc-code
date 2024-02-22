from common.problem import Problem
from algorithm.idlhc import IDLHC
from bench_algorithms import Knapsack
import random
import pandas as pd
from pathlib import Path
from os import listdir
import threading
from common.helper import file_name_parser
import sys


def save_df_to_path(path,df,prefix = None):
    try:
        file = pd.read_csv(path)
    except:
        file = pd.DataFrame()
    
    final_df = pd.concat(
        [file, df], axis=1, ignore_index=True
    )
    if prefix is None:
        prefix = "run_"
    else:
        prefix = prefix + "_"
    final_df.add_prefix(prefix).to_csv(path, mode="w", index=False)
    return final_df

def create_directories_from_str(dir_as_str):
    path = Path(dir_as_str)
    path.parent.mkdir(parents=True, exist_ok=True) 

def capture_test_data(iteration: IDLHC, problem: Problem, instance_num: int):
    convergence_array = iteration.convergence_array
    population_gen_type = problem.initial_population_type
    best_individuals = iteration.best_individuals

    folder_path = "knapsack/tests/population-gen-type_{population_gen_type}/".format(
        population_gen_type=population_gen_type,
    )

    file_path = "knapsack-instance_{instance_num}.csv".format(
        instance_num=instance_num, population_gen_type=population_gen_type
    )
    file_path = folder_path + file_path
    
    create_directories_from_str(file_path)
    
    final_test_df = save_df_to_path(path=file_path,df = pd.DataFrame(convergence_array))

    best_individual_path = "best-individuals-instance_{instance_num}/run_{run}.csv".format(
        instance_num = instance_num,
        run=final_test_df.columns[-1]
    )
    best_individual_path = folder_path + best_individual_path
    create_directories_from_str(best_individual_path)
    
    best_individual_df = pd.DataFrame()
    for individual in best_individuals:
        best_individual_df = pd.concat([best_individual_df,pd.DataFrame(individual)],axis=1,ignore_index=True)
    save_df_to_path(path=best_individual_path, df= best_individual_df,prefix="gen")

def gen_test_cases(
    initial_population_type=0,
    generations=100,
    num_of_individuals=100,
    direction="MAX",
    num_pdf=20,
    num_cut_pdf=0.1,
):
    instances_path = "knapsack/instances/"
    tests_path = "knapsack/tests"
    knapsack_instances = ["num_1|size_200.csv"]

    for current_instance in knapsack_instances:
        knapsack_instances_data = pd.read_csv(Path(instances_path + current_instance))

        current_instance_info = file_name_parser(current_instance)

        values = list(knapsack_instances_data["values"])
        weights = list(knapsack_instances_data["weights"])

        knapsack = Knapsack(values, weights)

        num_of_variables = current_instance_info["size"]

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

        iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
        iteration.do()
        
        capture_test_data(iteration, problem, current_instance_info["num"])

num_runs = int(sys.argv[1])
gen_type = int(sys.argv[2])
for i in range(num_runs):
    gen_test_cases(initial_population_type=gen_type)
print("done")
