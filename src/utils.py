#draw graphs/plots here
import matplotlib.pyplot as plt
import numpy as np

def histo_plot(tasks):
    task_durations = [i.duration for i in tasks]

    plt.hist(task_durations , color='blue', edgecolor='black')
    plt.title("Histogram of Task Durations")
    plt.show()


def plot_resource_requirements(tasks):
    x_cpu= [task.cpu for task in tasks]
    y_memory = [task.memory for task in tasks]

    plt.scatter(x_cpu, y_memory,c='blue')
    plt.title("Memory vs CPU")
    plt.xlabel("CPU Requirements")
    plt.ylabel("Memory Requirements")
    plt.show()


def plot_server_capacities(servers):
    cpu = [server.cpu for server in servers]
    memory = [server.memory for server in servers]
    storage = [server.storage for server in servers]
    indices = list(range(len(servers)))

    plt.scatter(indices, cpu)
    plt.scatter(indices, memory, marker='s')
    plt.scatter(indices, storage, marker='d')
    plt.xlabel("Server Index")
    plt.ylabel("Capacity")
    plt.legend(['CPU Capacity', 'Memory Capacity', 'Storage Capacity'])
    plt.show()


# def plot_gantt_chart(tasks, server_index):
#     fig, gnt = plt.subplots()
#
#     colors = plt.cm.tab10(np.linspace(0, 1, len(tasks)))
#     current_time = 0
#
#     for i, task in enumerate(tasks):
#         gnt.broken_barh([(current_time, task.duration)], (10, 9), facecolors=(colors[i]))
#         current_time += task.duration
#
#     gnt.set_xlabel("Time")
#     gnt.set_yticks([15])
#     gnt.set_yticklabels([f"Server {server_index}"])
#     plt.title("Gantt Chart: Task Parallelization on a Single Server")
#     plt.show()
#
#
def plot_decay_function(epochs, costs_aco, costs_random, title):
    plt.plot(epochs, costs_aco, label="ACO Scheduler", color="blue")
    plt.axhline(y=costs_random, color="red", linestyle="--", label="Random Scheduler")
    plt.xlabel("Epochs")
    plt.ylabel("Cost")
    plt.title(title)
    plt.legend()
    plt.show()
#
#
# def plot_load_imbalance_decay(epochs, load_imbalances, random_load):
#     plot_decay_function(epochs, load_imbalances, random_load, "Load Imbalance Decay")
#
#
# def plot_max_time_decay(epochs, times_aco, random_time):
#     plot_decay_function(epochs, times_aco, random_time, "Max Time/Time Taken Decay")
#
# # Example calls
# # servers = Server.initServers(m)
# # plot_server_capacities(servers)
#
# # tasks_for_server = [...]  # Assuming task list for a specific server
# # plot_gantt_chart(tasks_for_server, server_index=1)
#
# # epochs = list(range(150))  # Assuming epochs count
# # costs_aco = [cost1, cost2, ...]  # Fill with ACO costs per epoch
# # costs_random = total_random_cost  # Cost from random scheduler
# # plot_decay_function(epochs, costs_aco, costs_random, "Total Cost Decay")
