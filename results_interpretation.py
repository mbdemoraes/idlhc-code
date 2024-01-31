import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_convergence(arr1,arr2,arr3):
    # cria a figura
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    # define o eixo x
    x_axis = [i for i in range(len(arr1))]

    # formata o tamanho da fonte nos eixos
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylabel("Valor da função objetivo", fontsize=16)
    plt.xlabel("Gerações", fontsize=16)

    # plota o gráfico
    plt.plot(x_axis,arr1, marker='o', color='blue', linestyle='None')
    plt.plot(x_axis,arr2, marker='o', color='blue', linestyle='None')
    plt.plot(x_axis,arr3, marker='o', color='blue', linestyle='None')
    plt.show()

def get_data():
    filepath = Path("algorithm_metrics/knapsack_problem_p.csv")

    filepath.parent.mkdir(parents=True, exist_ok=True)

    results = pd.read_csv(filepath)

    best_value_list = results["best_value"]
    firstgen_with_best_value_list = results["firstgen_with_best_value"]
    population_gen_type_list = results["population_gen_type"]
    convergence_array_list = [i.replace("[","").replace("]", "").split(",") for i in results["convergence_array"]]
    for element in convergence_array_list:
        for count,value in enumerate(element):
           element[count] = int(value) 
    problem_number_list = results["problem_number"]

    return best_value_list,firstgen_with_best_value_list,population_gen_type_list,convergence_array_list,problem_number_list

def analyse_results():
    best_value_list,firstgen_with_best_value_list,population_gen_type_list,convergence_array_list,problem_number_list = get_data()
    data = {
        "total_best_values_per_p_type": [0,0,0],
        "total_final_values_per_p_type": [0,0,0],
        "average_b": [0,0,0],
        "average_f": [0,0,0],
        "firstgens_per_p_type": [0,0,0],
        "num_variables": [0,0,0]
    }
    
    problem_data = [data.copy() for i in range(100)]
    
    for count,element in enumerate(population_gen_type_list):
        selected_problem = problem_data[problem_number_list[count]]
        selected_problem["num_variables"][element] += 1
        selected_problem["total_best_values_per_p_type"][element] += best_value_list[count]
        selected_problem["total_final_values_per_p_type"][element] += convergence_array_list[count][-1]
        selected_problem["firstgens_per_p_type"][element] += firstgen_with_best_value_list[count]

    for dic_entry in problem_data:
        dic_entry["average_b"][0] = dic_entry["total_best_values_per_p_type"][0]/dic_entry["num_variables"][0]  
        dic_entry["average_b"][1] = dic_entry["total_best_values_per_p_type"][1]/dic_entry["num_variables"][1]  
        dic_entry["average_b"][2] = dic_entry["total_best_values_per_p_type"][2]/dic_entry["num_variables"][2]  

    arr1,arr2,arr3 = [],[],[]
    for dic_entry in problem_data:
        arr1.append(dic_entry["average_b"][0])
        arr2.append(dic_entry["average_b"][1])
        arr3.append(dic_entry["average_b"][2])
    return arr1,arr2,arr3, problem_data

arr1,arr2,arr3,problem_data = analyse_results()
print(problem_data[0])
#plot_convergence(arr1,arr2,arr3)