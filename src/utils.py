#draw graphs/plots here
import matplotlib.pyplot as plt
import seaborn as sns

#Task Properties

def histo_plot_task_dur(tasks):
    task_durations = [i.duration for i in tasks]
    print("task_duration:",task_durations)

    plt.hist(task_durations , color='blue', edgecolor='black')
    plt.title("Histogram of Task Durations")
    plt.xlabel("Duration")
    plt.ylabel('Frequency')
    plt.show()


def plot_task_resource_requirements(tasks):
    task_cpu= [task.cpu for task in tasks]
    task_memory = [task.memory for task in tasks]

    plt.scatter(task_cpu, task_memory,c='blue')
    plt.title("Task Memory vs CPU")
    plt.xlabel("CPU Requirements")
    plt.ylabel("Memory Requirements")
    plt.show()

#Server Properties

def server_capacities(servers):
    cpu = [server.cpu for server in servers]
    memory = [server.memory for server in servers]
    storage = [server.storage for server in servers]

    server_indices = list(range(len(servers)))

    plt.scatter(server_indices, cpu,alpha=0.5)
    plt.scatter(server_indices, memory, marker='s')
    plt.scatter(server_indices, storage, marker='d',alpha=0.5)
    plt.xlabel("Server Index")
    plt.ylabel("Capacity")
    plt.legend(['CPU Capacity', 'Memory Capacity', 'Storage Capacity'])
    plt.show()

def server_capacities_two_feat(servers):
    cpu = [server.cpu for server in servers]
    memory = [server.memory for server in servers]
    storage = [server.storage for server in servers]

    # CPU vs Memory
    plt.figure(figsize=(8, 6))
    plt.scatter(cpu, memory)
    plt.title("Server Capacities: CPU vs Memory")
    plt.xlabel("CPU Capacity")
    plt.ylabel("Memory Capacity")
    plt.show()

    # CPU vs Storage
    plt.figure(figsize=(8, 6))
    plt.scatter(cpu, storage)
    plt.title("Server Capacities: CPU vs Storage")
    plt.xlabel("CPU Capacity")
    plt.ylabel("Storage Capacity")
    plt.show()

    # Memory vs Storage
    plt.figure(figsize=(8, 6))
    plt.scatter(memory, storage)
    plt.title("Server Capacities: Memory vs Storage")
    plt.xlabel("Memory Capacity")
    plt.ylabel("Storage Capacity")
    plt.show()


def plot_gantt_chart(server_index, tasks, startTimes, endTimes):
    fig, ax = plt.subplots()

    for task in tasks:
        task_id = str(task.index)
        if task_id in startTimes and task_id in endTimes:
            start = startTimes[task_id]
            end = endTimes[task_id]
            ax.broken_barh([(start, end - start)], (task.index * 10, 8), facecolors='skyblue', label=f"Task {task.index}")

    ax.set_xlabel("Time")
    ax.set_ylabel("Tasks")

    ax.set_yticks([task.index * 10  + 4 for task in tasks])
    ax.set_yticklabels([task.index for task in tasks])

    plt.show()

def plot_cost_decay(epoch, cost, random_cost):

    epoch_list = [i for i in range(epoch)]
    # Total Cost Decay
    plt.plot(epoch_list,cost, label="ACO Scheduler")
    plt.axhline(y=random_cost, color='r',label="Random Scheduler")
    plt.title("Total Cost Decay")
    plt.xlabel("Epochs")
    plt.ylabel("Cost")
    plt.legend()
    plt.show()

def plot_loadimb_decay_function(epoch,aco_load_imbalance_list,randomLoadImbalance):

    # Load Imbalance Decay
    epoch_list = [i for i in range(epoch)]
    plt.figure(figsize=(8, 6))
    plt.plot(epoch_list, aco_load_imbalance_list , label="ACO Scheduler")
    plt.axhline(y=randomLoadImbalance, color='r', linestyle='--', label="Random Scheduler")
    plt.title("Load Imbalance Decay")
    plt.xlabel("Epochs")
    plt.ylabel("Load Imbalance")
    plt.legend()
    plt.show()


def plot_pheromone_heatmaps(initial_pheromones, final_pheromones):
    plt.figure(figsize=(10, 8))
    sns.heatmap(initial_pheromones, cmap='coolwarm', annot=True, fmt=".2f")
    plt.title("Initial Pheromone Matrix")
    plt.xlabel("Servers")
    plt.ylabel("Tasks")
    plt.show()

    plt.figure(figsize=(10, 8))
    sns.heatmap(final_pheromones, cmap='coolwarm', annot=True, fmt=".2f")
    plt.title("Final Pheromone Matrix")
    plt.xlabel("Servers")
    plt.ylabel("Tasks")
    plt.show()



# def plot_param_effects(param_values, final_costs):
#     plt.plot(param_values, final_costs, marker='o')
#     plt.title("Effect of Parameters on Final Cost")
#     plt.xlabel("Parameter Value")
#     plt.ylabel("Final Cost")
#     plt.show()

def plot_solution_diversity(epochs, solution_diversity):
    plt.figure(figsize=(8, 6))
    epochs_list=[i for i in range(epochs-1)]
    plt.plot(epochs_list, solution_diversity, marker='o')
    plt.title("Solution Diversity Across Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Diversity Between Successive Solutions")
    plt.show()

