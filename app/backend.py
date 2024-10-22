import copy
import nevergrad as ng
import dimod
from dimod.reference.samplers import ExactSolver

def solve_classical(storage_main_data, budget_size):
    def cost(solution):
        data = copy.deepcopy(storage_main_data)
        satisfaction = 0.0
        for student_index, student_name in enumerate(sorted(data["students"].keys())):
            topic_name = solution[student_index]
            rating = data["topics"][topic_name]["students"][student_name]

            data["topics"][topic_name]["seats"] -= 1

            if data["topics"][topic_name]["seats"] < 0:
                satisfaction -= len(storage_main_data["topics"]) ** 4

            satisfaction += 2**rating

        return -satisfaction

    optim = ng.optimizers.NGOpt(
        parametrization=ng.p.Choice(
            storage_main_data["topics"].keys(),
            repetitions=len(storage_main_data["students"]),
        ),
        budget=budget_size,
    )
    result = optim.minimize(cost)

    return result


def solve_annealer(storage_main_data, budget_size):
    data = copy.deepcopy(storage_main_data)
    satisfaction = 0.0
    J = {}
    for student_index, student_name in enumerate(sorted(data["students"].keys())):
        topic_name = solution[student_index]
        rating = data["topics"][topic_name]["students"][student_name]

        data["topics"][topic_name]["seats"] -= 1

        if data["topics"][topic_name]["seats"] < 0:
            satisfaction -= len(storage_main_data["topics"]) ** 4

        satisfaction += 2**rating