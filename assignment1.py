#!/usr/bin/env python
# coding: utf-8

# In[382]:


import random
import pygad
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp


# TASK 1

# In[383]:


def generate_random_graph_txt(filename, num_nodes=10, edge_prob=0.2, max_dist=10):
    with open(filename, "w") as f:
        f.write(f"{num_nodes}\n")

        for u in range(1, num_nodes + 1):
            for v in range(1, num_nodes + 1):
                if u == v:
                    continue  # brez samopovezav

                if random.random() < edge_prob:
                    distance = random.randint(1, max_dist)
                    f.write(f"{u} {v} {distance}\n")

    print(f"Graph saved to {filename}")


# In[384]:


# generate_random_graph_txt('graph5.txt', 50)


# In[385]:


def read_graph(file_path):
    graph = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_nodes = int(lines[0].strip())
    for node in range (1, num_nodes + 1):
        graph[node] = []

    for line in lines[1:]:
        parts = line.strip().split()
        if(len(parts) != 3):
            continue

        start = int(parts[0])
        finish = int(parts[1])
        distance = int(parts[2])

        graph[start].append((finish, distance))
    return graph


# In[386]:


graph3 = read_graph("graph3.txt")
graph3

graph = read_graph("graph5.txt")


# In[387]:


def graph_visualization(graph):
    G = nx.DiGraph()
    for node, value in graph.items():
        for nxt, distance in value:
            G.add_edge(node, nxt, weight=distance)

    pos = nx.spring_layout(G, k=5, iterations=100)
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1, arrowstyle='-|>', arrowsize=7)


    nx.draw_networkx_labels(G, pos, font_size=6, font_color='black')


    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)

    plt.axis('off')
    plt.show()


# In[388]:


graph_visualization(graph3)


# In[389]:


def path_distance(path, graph):
    result = 0

    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i+1]
        neighbors = graph[current_node]

        distance = None
        for(f, d) in neighbors:
            if f == next_node:
                distance = d
                break

        if distance is None:
            return None

        result += distance

    return result


# In[390]:


path1 = [1, 3, 4, 5]
path2 = [1, 4, 5]

print("path1:", path_distance(path1, graph3))
print("path2:", path_distance(path2, graph3))


# In[391]:


def generate_path(start, end, graph, max_steps = 100):
    current = start
    path = [current]

    for _ in range(max_steps):
        if current == end:
            return path

        neighbors = graph[current]
        if not neighbors:
            return None

        next_node, _ = random.choice(neighbors)
        path.append(next_node)
        current = next_node

    if current == end:
        return path
    else:
        return None


# In[392]:


for i in range(10):
    p = generate_path(1, 20, graph3)
    print(p, " -> distance:", path_distance(p, graph3) if p is not None else None)


# In[393]:


def generate_initial_population(start, end , graph, population_size = 50):
    population = []
    attempts = 0

    while (len(population) < population_size and attempts < population_size * 10):
        path = generate_path(start, end, graph)

        if path is not None:
            population.append(path)

        attempts += 1
    return population


# In[394]:


population = generate_initial_population(1, 20, graph3, population_size=15)
population


# In[395]:


def fitness(path, graph, start, end):
    if path is None:
        return 1e9

    if path[0] != start or path[-1] != end:
        return 1e9

    dist = path_distance(path, graph)

    if dist is None:
        return 1e9

    return dist


# In[396]:


start = 1
end = 20

pop = generate_initial_population(start, end, graph3, population_size=5)

for p in pop:
    print(p, "fitness:", fitness(p, graph3, start, end))


# In[397]:


def tournament_selection(population, fitnesses, tournament_size = 3):
    indices = random.sample(range(len(population)), tournament_size)
    best_idx = min(indices, key=lambda i: fitnesses[i])

    return population[best_idx]


# In[398]:


starts = 1
end = 20
population = generate_initial_population(starts, end, graph, population_size=10)
fitnesses = [fitness(p, graph, starts, end) for p in population]

print("POPULACIJA:")
for p, f in zip(population, fitnesses):
    print(p, "fitness:", f)

print("\nIZBRAN STARŠ:")
parent = tournament_selection(population, fitnesses, tournament_size=3)
print(parent, "fitness:", fitness(parent, graph, start, end))


# In[399]:


def mutate(path, graph, mutation_probability = 0.1):
    new_path = path[:]

    for i in range(len(new_path) - 1):
        if random.random() < mutation_probability:
            current = new_path[i]
            neighbors = graph[current]

            if not neighbors:
                continue

            next_node, _ = random.choice(neighbors)
            new_path[i + 1] = next_node

    return new_path


# In[400]:


p = population[0]
print("Original:", p)

mutated = mutate(p, graph, mutation_probability=0.5)
print("Mutated: ", mutated)

print("Fitness original:", fitness(p, graph, start, end))
print("Fitness mutated: ", fitness(mutated, graph, start, end))


# In[401]:


def single_point_crossover(parent1, parent2):
    if len(parent1) < 3 or len(parent2) < 3:
        return parent1[:], parent2[:]

    cut1 = random.randint(1, len(parent1) - 2)
    cut2 = random.randint(1, len(parent2) - 2)

    child1 = parent1[:cut1] + parent2[cut2:]
    child2 = parent2[:cut2] + parent1[cut1:]

    return child1, child2


# In[402]:


starts = 1
end = 20

population = generate_initial_population(starts, end, graph, population_size=4)
fitnesses = [fitness(p, graph, starts, end) for p in population]

print("STARŠI:")
for p, f in zip(population, fitnesses):
    print(p, "fitness:", f)

# izberemo 2 starša
parent1 = tournament_selection(population, fitnesses, tournament_size=3)
parent2 = tournament_selection(population, fitnesses, tournament_size=3)

print("\nIZBRAN STARŠ 1:", parent1)
print("IZBRAN STARŠ 2:", parent2)

child1, child2 = single_point_crossover(parent1, parent2)

print("\nOTROCI:")
print("child1:", child1, "fitness:", fitness(child1, graph, start, end))
print("child2:", child2, "fitness:", fitness(child2, graph, start, end))


# In[403]:


def genetic_algorithm(start, end, graph, population_size=50, generations=100, mutation_probability=0.1, tournament_size=3):
    population = generate_initial_population(start, end, graph, population_size)
    best_path = None
    best_fitness = float("inf")

    for gen in range(generations):
        fitnesses = [fitness(p, graph, start, end) for p in population]

        gen_best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        gen_best_path = population[gen_best_idx]
        gen_best_fitness = fitnesses[gen_best_idx]

        if gen_best_fitness < best_fitness:
            best_fitness = gen_best_fitness
            best_path = gen_best_path

        new_population = []
        new_population.append(best_path)

        while len(new_population) < population_size:
            # izberi starše
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)

            # crossover
            child1, child2 = single_point_crossover(parent1, parent2)

            # mutacija
            child1 = mutate(child1, graph, mutation_probability)
            child2 = mutate(child2, graph, mutation_probability)
            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    return best_path, best_fitness


# In[404]:


start = 1
end = 20

best_path, best_fit = genetic_algorithm(start, end, graph, population_size=50, generations=100, mutation_probability=0.1, tournament_size=3)

print("Najdena pot:", best_path)
print("Dolžina poti:", best_fit)


# TASK 2

# In[405]:


def generate_path2(targets, graph):



    current = targets[0]
    path = [current]


    success = True


    for i in range(len(targets)-1):
        current = targets[i]
        nxt = targets[i+1]
        segment = [current]

        future_targets = set(targets[i+2:])



        while (segment[-1]!= nxt):

            possible_nodes =  [node for node, _ in graph.get(segment[-1], []) if node not in segment and node not in future_targets]




            if not possible_nodes:
                success = False
                break

            n = random.choice(possible_nodes)
            segment.append(n)

        if not success:
            break


        path.extend(segment[1:])

    if success:
        return path 

    return []  




# In[406]:


for i in range(10):
    p = generate_path2([1, 14, 20], graph3)
    print(p, " -> distance:", path_distance(p, graph3))


# In[407]:


def generate_initial_population2(targets, graph, population_size = 50):
    population = []
    attempts = 0

    while (len(population) < population_size and attempts < population_size * 10):
        path = generate_path2(targets, graph)

        if path :
            population.append(path)

        attempts += 1
    return population


# In[408]:


population2 = generate_initial_population2([1, 3, 19], graph3, population_size=15)
population2


# In[409]:


def make_fitness2(path, graph, targets):
    def fitness2(ga_instance, solution, solution_idx):



        if path is None:
            return 1e-9

        it = iter(path)
        if not (all(target in it for target in targets)):
            return 1e-9

        dist = path_distance(path, graph)

        if dist is None:
            return 1e-9

        return 1.0/ (1.0+dist)

    return fitness2


# In[410]:


for p in population2:
    print(p, "fitness:", make_fitness2(p, graph3, [1, 3, 19]))


# In[411]:


def mutate2(path, graph, targets, mutation_probability = 0.1):
    new_path = path[:]

    for i in range(len(new_path) - 1):
        if path[i+1] in targets:
            continue
        if random.random() < mutation_probability:
            current = new_path[i]
            neighbors = [n for n, _ in graph[current] if n not in targets]


            if not neighbors:
                continue

            next_node = random.choice(neighbors)
            new_path[i + 1] = next_node

    return new_path


# In[412]:


# p2 = population2[0]
# print("Original:", p2)

# mutated2 = mutate2(p2, graph3,[1, 3, 19], mutation_probability=0.5)
# print("Mutated: ", mutated2)

# print("Fitness original:", fitness2(p2, graph3, [1, 3, 19]))
# print("Fitness mutated: ", fitness2(mutated2, graph3, [1, 3, 19]))


# TASK 3

# In[413]:


def follows_targets(path, targets):
    # Vrne True, če pot sledi target node-om v zaporedju.
    t_index = 0

    for node in path:
        if t_index < len(targets) and node == targets[t_index]:
            t_index += 1

    return t_index == len(targets)


# In[414]:


def generate_path_with_targets(start, end, targets, graph):
    full_path = []
    current = start

    for target in targets + [end]:
        segment = generate_path(current, target, graph)
        if segment is None:
            return None

        if full_path:
            full_path += segment[1:]
        else:
            full_path = segment[:]

        current = target

    return full_path


# In[415]:


def generate_multi_agents_path(start_positions, end, graph, targets):
    paths = []
    num_agents = len(start_positions)
    for i in range(num_agents):
        path = generate_path_with_targets(start_positions[i], end, targets, graph)
        if path is None:
            return None
        paths.append(path)   

    return paths


# In[416]:


def generate_multi_agents_population(start_positions, end, graph, targets, population_size = 50):
    population = []
    attempts = 0

    while (len(population) < population_size and attempts < population_size * 50):
        path = generate_multi_agents_path(start_positions, end, graph, targets)
        if path is not None:
            population.append(path)   
        attempts += 1
    return population


# In[417]:


def move_with_time(path, graph):
    start = path[0]
    path_time = []
    path_time.append(("node", start))

    for i in range(len(path) - 1):
        for (neighbor, distance) in graph[path[i]]:
            if neighbor == path[i + 1]:
                for t in range(distance):
                    path_time.append(("edge", (path[i], path[i + 1])))
                path_time.append(("node", path[i + 1]))
                if i + 1 != len(path) - 1:
                    for t in range (9):
                        path_time.append(("node", path[i + 1]))
                break

    return path_time


# In[418]:


graph = read_graph("graph1.txt")
path = [1, 3, 4, 5]
print(move_with_time(path, graph))


# In[419]:


def expand_agents(paths, graph):
    expanded_paths = []
    max_length = 0
    for path in paths:
        expanded_path = move_with_time(path, graph)
        expanded_paths.append(expanded_path)
        if len(expanded_path) > max_length:
            max_length = len(expanded_path)

    for i in range(len(expanded_paths)):
        while len(expanded_paths[i]) < max_length:
            state, value = expanded_paths[i][-1]
            if state == "edge":
                final_node = value[1]
            else:
                final_node = value
            expanded_paths[i].append(("done", final_node))

    return expanded_paths


# In[420]:


def detect_collision(expanded_paths):
    num_agents = len(expanded_paths)

    for t in range(len(expanded_paths[0])):
        states_at_t = [expanded_paths[i][t] for i in range(num_agents)]
        for i in range(num_agents):
            for j in range(i+1, num_agents):
                state1 = states_at_t[i]
                state2 = states_at_t[j]
                if(state1[0] == "node" and state2[0] == "node" and state1[1] == state2[1]):
                    return True

                if(state1[0] == "edge" and state2[0] == "edge"):
                    (u1, v1) = state1[1]
                    (u2, v2) = state2[1]
                    if u1 == u2 and v1 == v2:
                        return True
                    if u1 == v2 and v1 == u2:
                        return True

    return False


# In[421]:


def fitness3(paths, graph, start_positions, end, targets):
    for i, path in enumerate(paths):
        if path[0] != start_positions[i]:
            return 1e9
        if path[-1] != end:
            return 1e9
        if not follows_targets(path, targets):
            return 1e9

        for j in range(len(path)-1):
                u, v = path[j], path[j+1]
                valid_next = [n for n,_ in graph[u]]
                if v not in valid_next:
                    return 1e9    # punish invalid edge


    expanded = expand_agents(paths, graph)

    if detect_collision(expanded):
        return 1e9

    return len(expanded[0])


# In[422]:


def genetic_algorithm3(starts, end, targets, graph, population_size=50, generations=100, mutation_probability=0.1, tournament_size=3):
    population = generate_multi_agents_population(starts, end, graph, targets, population_size)
    best_path = None
    best_fitness = float("inf")

    for gen in range(generations):
        fitnesses = [fitness3(p, graph, starts, end, targets) for p in population]


        gen_best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        gen_best_path = population[gen_best_idx]
        gen_best_fitness = fitnesses[gen_best_idx]

        if gen_best_fitness < best_fitness:
            best_fitness = gen_best_fitness
            best_path = gen_best_path

        new_population = []
        new_population.append(best_path)

        while len(new_population) < population_size:
            # izberi starše
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)

            num_agents = len(parent1)
            # crossover
            child1 = []
            child2 = []
            for i in range(num_agents):
                c1_i, c2_i = single_point_crossover(parent1[i], parent2[i])
                child1.append(c1_i)
                child2.append(c2_i)

            # mutacija
            for i in range(num_agents):
                child1[i] = mutate(child1[i], graph, mutation_probability)
                child2[i] = mutate(child2[i], graph, mutation_probability)

            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    return best_path, best_fitness


# In[ ]:





# In[423]:


starts = [1, 3]
end = 20
targets = [4]

best, fit = genetic_algorithm3(starts, end, targets, graph3, population_size=20, generations=30)

print("Best solution:", best)
print("Fitness:", fit)

expanded = expand_agents(best, graph)
print("Collision:", detect_collision(expanded))


# In[ ]:


pop = generate_multi_agents_population(starts, end, graph3, targets, population_size=20)
print("POP:", pop)


# In[ ]:


def print_multi_agent_paths(paths):
    for i, p in enumerate(paths):
        print(f"Agent {i+1}: {' -> '.join(map(str, p))}")


# In[ ]:


print_multi_agent_paths(best)


# In[ ]:


def draw_paths_on_graph(graph, paths):
    G = nx.DiGraph()

    for u, neighbors in graph.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10)

    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=15)

    colors = ["red", "green", "blue", "purple", "orange"]

    for i, path in enumerate(paths):
        edges = [(path[j], path[j+1]) for j in range(len(path)-1)]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=edges,
            width=3,
            edge_color=colors[i % len(colors)],
            arrowstyle='-|>',
            arrowsize=20
        )

    plt.axis("off")
    plt.show()


# In[ ]:


paths = [[1,4,5], [3,4,5]]
graph_visualization(graph3)
print_multi_agent_paths(best)
draw_paths_on_graph(graph, best)


# In[ ]:




