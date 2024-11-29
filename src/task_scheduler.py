import random
import math
def makespan():
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

def randomSchedulerMakespan(currTasks, currServer):
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

def load_imbalance():
    return

def energy_usage():
    return

def cost():
    makespan() + load_imbalance() + energy_usage() # weighted sum
    return

def heuristic(): # will be used in calculating server probability
    return

def server_probability(): # use the above heuristic and phermone matrix
    return

def ACO_Scheduler(alpha, beta, rho, Q, E, tasks, servers, phermones):
    return

def Random_Scheduler(tasks, servers): # random task allottment for baseline comparsion
    numServers = len(servers)
    tasksInServers = []
    for i in range(numServers):
        tasksInServers.append([])
    
    #print("length initially ", len(tasksInServers))
    for task in tasks:
        randomServer = random.randint(0, numServers - 1)
        serverToAdd = tasksInServers[randomServer]
        serverToAdd.append(task)
    
    index = 0
    # for ts in tasksInServers:
    #     print ("Server ", index , "cpu ", servers[index].cpu, " memory ", servers[index].memory, " storage ", servers[index].storage)
    #     print("num of tasks ", len(ts))
    #     for s in ts:
    #         print("cpu of task ", s.cpu)
    #         print("memory of task ", s.memory)
    #         print("storage of task ", s.storage)
    #         print("duration of this task ", s.duration)
        # index += 1
    maxTime = 0
    for j in range(0,numServers):
        timeTaken = randomSchedulerMakespan(tasksInServers[j], servers[j])
        #print("timeTaken ", timeTaken)
        maxTime = max(maxTime, timeTaken)
    return maxTime