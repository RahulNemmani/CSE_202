def makespan():
    return

def load_imbalance():
    return

def energy_usage():
    return

def cost():
    makespan() + load_imbalance() + energy_usage() # weighted sum
    return

def heuristic(): # will be used in calculating server probability
    return

def server_probability_distribution(): # use the above heuristic and phermone matrix
    return

def assign(task, solution, probabilities):
    return

def ACO_Scheduler(alpha, beta, rho, Q, E, epochs, ants, n, m, tasks, servers, phermones):

    global_best_solution = []
    global_best_cost = float('inf')

    for e in range(epochs):
        solutions = []
        local_best_solution = []
        local_best_cost = float('inf')

        for a in range(ants):
            solution = [[] for _ in range(m)]

            for task in tasks:
                probabilities = server_probability_distribution(alpha, beta)
                assign(task, solution, probabilities)
            cost = cost(solution, servers, tasks, E)

            if cost < local_best_cost:
                local_best_cost = cost
                local_best_solution = solution
            phermones = phermones * (1 - rho) # need to write a loop / numpy

            for s in range(len(solution)):
                phermones[solution[s]][s] += Q / cost
            solutions.append([cost, solution])

        for s in range(len(solution)):
            phermones[local_best_solution[s]][s] += Q / local_best_cost
        
        if local_best_cost < global_best_cost:
            global_best_cost = local_best_cost
            global_best_solution = local_best_solution
    return global_best_solution
    

def Random_Scheduler(tasks, servers): # random task allottment for baseline comparsion
    return