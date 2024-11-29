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
    return makespan() + load_imbalance(solution, tasks, servers) # weighted sum
    

def heuristic(server, task): # will be used in calculating server probability
    cpu_ratio = server.cpu / max(task.cpu, 1)
    memory_ratio = server.memory / max(task.memory, 1)
    storage_ratio = server.storage / max(task.storage, 1)
    
    # Weighted heuristic based on importance of resources, will make it more likely to assign tasks to larger servers
    return 0.4 * cpu_ratio + 0.4 * memory_ratio + 0.2 * storage_ratio

def server_probability_distribution(phermones, alpha, beta, servers, tasks, task_index): # use the above heuristic and phermone matrix
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

def getParallelTasks(currTasks, parallelTasks, serverCPU, serverMemory, serverStorage):
    minDuration = math.inf

    for i in range(len(currTasks)):         # Task 1 duration: 2 Task 2 duration 4: once task 1 is done even if task 2 is not done see if there is another task to add
        currTask = currTasks[i]
        if currTask.cpu < serverCPU and currTask.memory < serverMemory and currTask.storage < serverStorage:
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

def makespan (currTasks, currServer):
    totalDuration = 0

    while len(currTasks) > 0:
        firstTask = currTasks.pop(0)
        # current constraints remaining
        serverCPU = currServer.cpu - firstTask.cpu
        serverMemory = currServer.memory - firstTask.memory
        serverStorage = currServer.storage - firstTask.storage

        parallelTasks = []
        parallelTasks.append(firstTask)
        while not len(parallelTasks) == 0:
            minTimeTask, parallelTasks, serverCPU, serverStorage, serverMemory, currTasks = getParallelTasks(currTasks, parallelTasks, 
                                                                                                  serverCPU, serverMemory, serverStorage)
            
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
                else:
                    nonMinTasks.append(task)
            
            parallelTasks = nonMinTasks
            for task in parallelTasks:
                task.duration -= minTimeTask

    return totalDuration

def ACO_Scheduler(alpha, beta, rho, Q, E, epochs, ants, n, m, tasks, servers, phermones):

    global_best_solution = []
    global_best_cost = float('inf')

    for e in range(epochs):
        solutions = []
        local_best_solution = []
        local_best_cost = float('inf')

        for a in range(ants):
            solution = [[] for _ in range(m)]

            for task_index in range(len(tasks)):
                probabilities = server_probability_distribution(phermones, alpha, beta, servers, tasks, task_index)
                assign(task_index, solution, probabilities)
            cost = getCost(solution, tasks, servers)

            if cost < local_best_cost:
                local_best_cost = cost
                local_best_solution = solution
            phermones = [[phermone * (1 - rho) for phermone in row] for row in phermones]

            for s in range(len(solution)):
                for t in solution[s]:
                    phermones[t][s] += Q / cost
            solutions.append([cost, solution])

        for s in range(len(solution)):
            for t in local_best_solution[s]:
                phermones[t][s] += Q / local_best_cost
        
        if local_best_cost < global_best_cost:
            global_best_cost = local_best_cost
            global_best_solution = local_best_solution
        print(global_best_cost)
    return global_best_solution
    

def Random_Scheduler(tasks, servers): # random task allottment for baseline comparsion
    numServers = len(servers)
    tasksInServers = []
    for i in range(numServers):
        tasksInServers.append([])

    for task in tasks:
        randomServer = random.randint(0, numServers - 1)
        serverToAdd = tasksInServers[randomServer]
        serverToAdd.append(task)
    
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
    maxTime = 0
    for j in range(0, numServers):
        timeTaken = makespan(tasksInServers[j], servers[j])
        #print("timeTaken ", timeTaken)
        maxTime = max(maxTime, timeTaken)
    return maxTime