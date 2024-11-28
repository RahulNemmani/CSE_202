# CONSTANTS
# alpha, beta, rho, Q, E, tasks, servers, phermones
# E, phermones are matrices (len(tasks) * len(servers)) or it's transpose
# tasks and servers are instances of the task and server in models

# TODO : Shriniwas - instantiate all of the above constants and decide their values (which we will tweak)
# Shriniwas - write thr ACO scheduler

# TODO : Rahul - the main method where you will call the ACO scheduler and the random scheduler, call the plotting methods
# Rahul - write the random scheduler.

# TODO : Shinjini - write plotting methods in utils.py. The x coordinate will be num_epochs and y will be the cost components. Assume you will
# get the x and y from Rahul's code in the main method

# TODO : Anahita - Write the classes and constructors for models referring to the proposal. Also write a method that randomly initializes n
# models (tasks + servers) with their attributes given n. Rahul will use this method when he tests for different n. Set seed for reproducibility.

import random
random.seed(42) #set seed for reproducibility


# models class/constructor
class ResourceCapacities:
    """
    each task and server has a resource capacity tuple 
    (c_CPU,c_Memory,c_Storage)
    """
    
    def __init__(self, cpu, memory, storage):
        """Initialize the values of the resource capacity tuple."""
        # ?? not sure if need these later
        self.c_cpu = cpu
        self.c_memory = memory
        self.c_storage = storage
        # 
        
        self.capacities = (cpu, memory, storage)
      
        
        
# Randomly initialize n models (tasks + servers) with their attributes given n.
def initModels(num_models):
    """
    Input:  number of tasks and number of servers to initialize
    Output: (set of tasks T with capacity attributes, set of servers S with capacity attributes)
    
    to access the attributes (for x in Set: x.capacities)
    """
    T = set() #tasks
    S = set() #servers
    
    for i in range(num_models):
        
        # ?? is there a specific range for random numbers
        
        # task_i initialized and added to T set
        T.add(ResourceCapacities(random.random(), random.random(), random.random()))
        
        # server_i initialized and added to S set
        S.add(ResourceCapacities(random.random(), random.random(), random.random()))
        
    return S, T
