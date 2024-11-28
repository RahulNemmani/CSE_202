import random
random.seed(42)

class Server:
    """Each server has cpu, memory, and storage resource capacities."""
    
    def __init__(self, cpu, memory, storage):
        """Initialize the values of the resource capacities per server."""
        self.cpu = cpu
        self.memory = memory
        self.storage = storage
        
    def initServers(num_models):
        """
        Input:  number of servers to initialize
        Output: list of servers S with capacity attributes each
        """
        S = []
        
        for i in range(num_models):
            
            # randomize attributes: 3-4 times greater than the tasks
            c_cpu = random.randint(300, 400)
            c_memory = random.uniform(400, 512)  
            c_storage = random.uniform(24000, 32000) 
            
             # server initialized and added to list of Servers
            S.append(Server(c_cpu, c_memory, c_storage))
            
        return S
    
    def __getitem__(self, index):
        """Access attributes with an index"""
        resCap = [self.cpu, self.memory, self.storage]
        return resCap[index]
