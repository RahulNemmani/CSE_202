import random
import math


def load_imbalance(solution, tasks, servers):
    loads = []
    for i in range(len(solution)):
        server_capacity_cpu = servers[i].cpu
        tasks_demand_cpu = 0
        for index in solution[i]:
            tasks_demand_cpu += tasks[index].cpu
        loads.append(tasks_demand_cpu / server_capacity_cpu)
    imbalance = 0
    mean_laod = sum(loads) / len(loads)
    for load in loads:
        imbalance += abs(load - mean_laod)
    return imbalance


def getCost(solution, tasks, servers):
    temp = [tasks[i].duration for i in range(len(tasks))]
    time_taken = -float('inf')

    for server_index in range(len(solution)):
        currServer = servers[server_index]
        currTasks = []
        startTimes = {}
        endTimes = {}

        for task_index in solution[server_index]:
            currTasks.append(tasks[task_index])

        for i in range(len(currTasks)):
            taskIndex = str(currTasks[i].index)
            startTimes[taskIndex] = 0
            endTimes[taskIndex] = 0

        time_taken = max(time_taken, makespan(currTasks, currServer, startTimes, endTimes))
    # print(solution)
    # print("time taken (Makespan) - ", time_taken)
    for i in range(len(tasks)):
        tasks[i].duration = temp[i]
    return 3 * time_taken + 2 * load_imbalance(solution, tasks, servers), startTimes, endTimes  # weighted sum


def heuristic(server, task):  # will be used in calculating server probability
    cpu_ratio = server.cpu / max(task.cpu, 1)
    memory_ratio = server.memory / max(task.memory, 1)
    storage_ratio = server.storage / max(task.storage, 1)

    # Weighted heuristic based on importance of resources, will make it more likely to assign tasks to larger servers
    return (0.4 * cpu_ratio + 0.4 * memory_ratio + 0.2 * storage_ratio) * 5


def server_probability_distribution(phermones, alpha, beta, servers, tasks,
                                    task_index):  # use the above heuristic and phermone matrix
    probabilities = []
    for i in range(len(servers)):
        h = heuristic(servers[i], tasks[task_index])
        phermone_level = phermones[task_index][i]
        probabilities.append(alpha * phermone_level + beta * h)
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    return probabilities


def assign(task, solution, probabilities):
    server_index = random.choices(range(len(probabilities)), weights=probabilities, k=1)[0]
    solution[server_index].append(task)
    return


def getParallelTasks(currTasks, parallelTasks, serverCPU, serverMemory, serverStorage, totalDuration, startTimes):
    minDuration = math.inf

    for i in range(
            len(currTasks)):  # Task 1 duration: 2 Task 2 duration 4: once task 1 is done even if task 2 is not done see if there is another task to add
        currTask = currTasks[i]
        if currTask.cpu < serverCPU and currTask.memory < serverMemory and currTask.storage < serverStorage:
            taskIndex = str(currTask.index)
            startTimes[taskIndex] = totalDuration
            parallelTasks.append(currTask)
            serverCPU -= currTask.cpu
            serverStorage -= currTask.storage
            serverMemory -= currTask.memory
            minDuration = min(minDuration, currTask.duration)

    # remove the tasks that will be processed
    tempTasks = []
    for task in currTasks:
        if task not in parallelTasks:
            tempTasks.append(task)

    currTasks = tempTasks

    return minDuration, parallelTasks, serverCPU, serverStorage, serverMemory, currTasks


def makespan(currTasks, currServer, startTimes, endTimes):
    totalDuration = 0

    while len(currTasks) > 0:
        firstTask = currTasks.pop(0)
        # current constraints remaining
        serverCPU = currServer.cpu - firstTask.cpu
        serverMemory = currServer.memory - firstTask.memory
        serverStorage = currServer.storage - firstTask.storage

        parallelTasks = []
        taskIndex = str(firstTask.index)
        startTimes[taskIndex] = totalDuration
        parallelTasks.append(firstTask)
        while not len(parallelTasks) == 0:
            minTimeTask, parallelTasks, serverCPU, serverStorage, serverMemory, currTasks = getParallelTasks(currTasks,
                                                                                                             parallelTasks,
                                                                                                             serverCPU,
                                                                                                             serverMemory,
                                                                                                             serverStorage,
                                                                                                             totalDuration,
                                                                                                             startTimes)

            for task in parallelTasks:
                minTimeTask = min(minTimeTask, task.duration)

            totalDuration += minTimeTask

            nonMinTasks = []

            # remove min tasks
            for task in parallelTasks:
                if task.duration == minTimeTask:
                    serverCPU += task.cpu
                    serverMemory += task.memory
                    serverStorage += task.storage
                    endIndex = str(task.index)
                    endTimes[endIndex] = totalDuration
                else:
                    nonMinTasks.append(task)

            parallelTasks = nonMinTasks
            for task in parallelTasks:
                task.duration -= minTimeTask

    return totalDuration


def calculate_solution_diversity(solution1, solution2):
    """
    Calculates the Hamming distance between two solutions.
    """
    diversity = 0
    for server in range(len(solution1)):
        set1 = set(solution1[server])
        set2 = set(solution2[server])
        diversity += len(set1.symmetric_difference(set2))
    return diversity


def ACO_Scheduler(alpha, beta, rho, Q, E, epochs, ants, n, m, tasks, servers, phermones, reference_cost):
    initialCostPrinted = False

    global_best_solution = []
    global_best_cost = float('inf')

    epoch_list = []
    aco_costs = []
    aco_load_imbalance_list = []
    aco_makespan_list = []
    solution_diversity_list = []

    previous_solution = None

    initial_pheromones = [row[:] for row in phermones]

    for e in range(epochs):
        solutions = []
        local_best_solution = []
        local_best_cost = float('inf')

        for a in range(ants):
            alpha += 0.05
            solution = [[] for _ in range(m)]

            for task_index in range(len(tasks)):
                probabilities = server_probability_distribution(phermones, alpha, beta, servers, tasks, task_index)
                assign(task_index, solution, probabilities)

            cost, aco_startTimes, aco_endTimes = getCost(solution, tasks, servers)
            if not initialCostPrinted:
                print(cost)
                initialCostPrinted = True

            load_imb = load_imbalance(solution, tasks, servers)
            makespan_value = max(
                makespan([tasks[i] for i in sublist], servers[idx], {}, {}) for idx, sublist in enumerate(solution)
            )

            if cost < local_best_cost:
                local_best_cost = cost
                local_best_solution = solution
                local_best_load_imbalance = load_imb
                local_best_makespan = makespan_value

            solutions.append([cost, solution])

            phermones = [[phermone * (1 - rho) for phermone in row] for row in phermones]

            for s in range(len(solution)):
                for t in solution[s]:
                    if cost > reference_cost:
                        phermones[t][s] *= 1
                    else:
                        phermones[t][s] += Q / cost

        aco_load_imbalance_list.append(local_best_load_imbalance)

        for s in range(len(solution)):
            for t in local_best_solution[s]:
                phermones[t][s] += Q / local_best_cost

        if local_best_cost < global_best_cost:
            global_best_cost = local_best_cost
            global_best_solution = local_best_solution

        if previous_solution is not None:
            diversity = calculate_solution_diversity(global_best_solution, previous_solution)
            solution_diversity_list.append(diversity)
        else:
            solution_diversity_list.append(0)
        previous_solution = global_best_solution

        epoch_list.append(e)
        aco_costs.append(local_best_cost)
        aco_makespan_list.append(local_best_makespan)

        final_pheromones = [row[:] for row in phermones]

    print("aco_load_imbalance_list:", aco_load_imbalance_list)
    print("aco_cost:", aco_costs)

    return global_best_cost, final_pheromones, initial_pheromones, solution_diversity_list, aco_costs, aco_load_imbalance_list, aco_startTimes, aco_endTimes


def Random_Scheduler(tasks, servers):  # random task allottment for baseline comparsion
    numServers = len(servers)
    tasksInServers = [[] for s in servers]

    solution = [[] for s in servers]
    for i in range(len(tasks)):
        randomServer = random.randint(0, numServers - 1)
        serverToAdd = tasksInServers[randomServer]
        serverToAdd.append(tasks[i])
        solution[randomServer].append(i)

    '''
    index = 0
    for ts in tasksInServers:
        print ("Server ", index , "cpu ", servers[index].cpu, " memory ", servers[index].memory, " storage ", servers[index].storage)
        print("num of tasks ", len(ts))
        for s in ts:
            print("cpu of task ", s.cpu)
            print("memory of task ", s.memory)
            print("storage of task ", s.storage)
            print("duration of this task ", s.duration)
        index += 1
    '''
    totalCost, startTimes, endTimes = getCost(solution, tasks, servers)
    randomLoadImbalance = load_imbalance(solution, tasks, servers)
    print("random total cost:", totalCost)
    print("random load imb", randomLoadImbalance)
    return totalCost, randomLoadImbalance, startTimes, endTimes
