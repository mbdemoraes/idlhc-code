
def gen_problem_vars():
    values = [random.randint(1, 100) for i in range(num_of_variables)]
    weights = [random.randint(1, 100) for i in range(num_of_variables)]

    ratios = [values[i] / weights[i] for i in range(num_of_variables)]

    sorted_ratio_indexes = sorted(range(len(values)), key=lambda i: ratios[i])
    return values, weights, ratios, sorted_ratio_indexes


    zero_list = ["" for i in range(num_of_problems)]

    problems_to_bench = pd.DataFrame(
    {
    "values": zero_list.copy(),
    "weights": zero_list.copy(),
    "sorted_ratio_indexes": zero_list.copy(),
    "ratios": zero_list.copy(),
    "capacity": capacity,
    }
    )


for i in range(num_of_problems):
    values, weights, ratios, sorted_ratio_indexes = gen_problem_vars()

    problems_to_bench.at[i, "values"] = values
    problems_to_bench.at[i, "weights"] = weights
    problems_to_bench.at[i, "ratios"] = ratios
    problems_to_bench.at[i, "sorted_ratio_indexes"] = sorted_ratio_indexes


    #filepath_1 = Path("problems/knapsack_problems.csv")

    filepath_1.parent.mkdir(parents=True, exist_ok=True)

    problems_to_bench.to_csv(filepath_1, mode="a", index=False, header=True)