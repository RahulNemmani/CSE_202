import random
random.seed(42) #set seed for reproducibility

class Server:
    """
    Each server has a resource capacity tuple (c_cpu,c_memory,c_storage).
    """
    
    def __init__(self, c_cpu, c_memory, c_storage):
        """Initialize the values of the resource capacity tuple.
           The random values are 3-4x of the tasks."""
        self.capacities = (c_cpu, c_memory, c_storage)
        
    
    # Randomly initialize n servers with their attributes given n.
    def initServers(num_models):
        """
        Input:  number of servers to initialize
        Output: set of servers S with capacity attributes
        
        to access the attributes (for x in S: x.capacities)
        """
        S = set() #servers
        
        for i in range(num_models):
            
            # randomize attributes: need to be 3-4x of the tasks
            c_cpu = random.randint(300, 400)
            c_memory = random.uniform(400, 512)  
            c_storage = random.uniform(24000, 32000) 
            
             # server_i initialized and added to S set
            S.add(Server(c_cpu, c_memory, c_storage))
            
        return S
