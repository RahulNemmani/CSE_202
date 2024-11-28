import random
random.seed(42) #set seed for reproducibility

class Task:
    """
    Each task has a resource capacity tuple (c_cpu,c_memory,c_storage) and duration.
    """
    
    def __init__(self, c_cpu, c_memory, c_storage, duration):
        """Initialize the values of the resource capacity tuple and duration."""
        self.capacities = (c_cpu, c_memory, c_storage)
        self.duration = duration
        
        
    # Randomly initialize n tasks with their attributes given n.
    def initTasks(num_models):
        """
        Input:  number of tasks to initialize
        Output: set of tasks T with capacity attributes
        
        to access the attributes (for x in T: x.capacities)
        """
        T = set() #tasks
        
        for i in range(num_models):
            
            # randomize attributes
            c_cpu = random.randint(1, 100)
            c_memory = random.uniform(8, 128) 
            c_storage = random.uniform(5, 8000) 
            duration = random.uniform(1, 2000) #not sure about these ranges
            
             # task_i initialized and added to T set
            T.add(Task(c_cpu, c_memory, c_storage, duration))
            
        return T
