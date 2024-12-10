import random
import models
import sys
import os
import plotly.express as px
import pandas as pd

# Add the directory containing 'myclass.py' to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
from task_scheduler import *
# CONSTANTS
# alpha, beta, rho, Q, E, tasks, servers, phermones
# E, phermones are matrices (len(tasks) * len(servers)) or it's transpose
# tasks and servers are instances of the task and server in models
alpha = 0
beta = 1
rho = 0.0
Q = 10000
ants = 35
epochs = 150
n = 40 # num tasks
m = 5 # num servers
E = [[random.uniform(10, 100) for server in range(m)] for task in range(n)]
phermones = [[20 for server in range(m)] for task in range(n)]
# TODO : Shriniwas - instantiate all of the above constants and decide their values (which we will tweak)
# Shriniwas - write thr ACO scheduler

# TODO : Rahul - the main method where you will call the ACO scheduler and the random scheduler, call the plotting methods
# Rahul - write the random scheduler.

# TODO : Shinjini - write plotting methods in utils.py. The x coordinate will be num_epochs and y will be the cost components. Assume you will
# get the x and y from Rahul's code in the main method

# TODO : Anahita - Write the classes and constructors for models referring to the proposal. Also write a method that randomly initializes n
# models (tasks + servers) with their attributes given n. Rahul will use this method when he tests for different n. Set seed for reproducibility.
from models.server import Server
from models.task import Task
from task_scheduler import Random_Scheduler

def main ():
    allTasks = Task.initTasks(n)
    allServers = Server.initServers(m)

    randomScheduler, startTimes, endTimes = Random_Scheduler(allTasks, allServers)
    print("RUNNING THE RANDOM SCHEDULER - ")
    print("time taken by the random scheduler - ", randomScheduler)
    print("time taken by the random scheduler start times - ", startTimes)
    print("time taken by the random scheduler end times - ", endTimes)

    tasks = Task.initTasks(n)
    servers = Server.initServers(m)
    print("RUNNING THE ACO SCHEDULER")
    print("cost of the ACO scheduler - ", ACO_Scheduler(alpha, beta, rho, Q, E, epochs, ants, n, m, tasks, servers, phermones, randomScheduler))
    print("cost of the random scheduler - ", randomScheduler)
    print([task.duration for task in tasks])

    taskIds = list(startTimes.keys())
    
    taskIds.sort()

    sortedStartTimes = []
    sortedEndTimes = []
    for taskId in taskIds:
        sortedStartTimes.append(startTimes[taskId])
        sortedEndTimes.append(endTimes[taskId])

    df = pd.DataFrame({
        "Task": [f"Task {i}" for i in range(len(taskIds))],
        "Start": sortedStartTimes,
        "Finish": sortedEndTimes,
    })

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", title="Project Gantt Chart")   # will have to change the timeline here
    fig.update_yaxes(categoryorder="total ascending")  # Optional: Order tasks by start date
    #fig.show()


if __name__ == "__main__":
    main()