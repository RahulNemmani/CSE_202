import random
random.seed(2) 

class Task:
    """Each task has cpu, memory, storage resource capacities AND duration."""
    
    def __init__(self, cpu, memory, storage, duration):
        """Initialize the values of the resource capacities and duration."""
        self.cpu = cpu
        self.memory = memory
        self.storage = storage
        self.duration = duration
        
    def initTasks(num_models):
        """
        Input:  number of tasks to initialize
        Output: list of tasks T with capacity and duration attributes each
        """
        T = []
        
        for i in range(num_models):
            
            # randomize attributes
            c_cpu = random.randint(150, 300)
            c_memory = random.uniform(128, 256)
            c_storage = random.uniform(16000, 24000)
            duration = random.uniform(1, 2000) 
            
             # task initialized and added to list of Tasks
            T.append(Task(c_cpu, c_memory, c_storage, duration))
            
        return T
    
    def __getitem__(self, index):
        """Access attributes with an index"""
        resCap = [self.cpu, self.memory, self.storage, self.duration]
        return resCap[index]
