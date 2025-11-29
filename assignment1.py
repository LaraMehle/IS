#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random


# TASK 1

# In[3]:


def generate_random_graph_txt(filename, num_nodes=10, edge_prob=0.2, max_dist=10):

    with open(filename, "w") as f:
        # Zapiši število vozlišč
        f.write(f"{num_nodes}\n")

        # Generiraj robove
        for u in range(1, num_nodes + 1):
            for v in range(1, num_nodes + 1):
                if u == v:
                    continue  # brez samopovezav

                if random.random() < edge_prob:
                    distance = random.randint(1, max_dist)
                    f.write(f"{u} {v} {distance}\n")

    print(f"Graph saved to {filename}")


# In[4]:


# generate_random_graph_txt('graph5.txt', 50)


# In[5]:


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


# In[6]:


graph = read_graph("graph5.txt")
graph


# In[7]:


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


# In[8]:


path1 = [1, 3, 4, 5]
path2 = [1, 4, 5]

print("path1:", path_distance(path1, graph))
print("path2:", path_distance(path2, graph))


# In[9]:


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


# In[10]:


for i in range(10):
    p = generate_path(1, 20, graph)
    print(p, " -> distance:", path_distance(p, graph) if p is not None else None)


# In[11]:


def generate_initial_population(start, end , graph, population_size = 50):
    population = []
    attempts = 0

    while (len(population) < population_size and attempts < population_size * 10):
        path = generate_path(start, end, graph)

        if path is not None:
            population.append(path)

        attempts += 1
    return population


# In[12]:


population = generate_initial_population(1, 20, graph, population_size=15)
population


# In[13]:


def fitness(path, graph, start, end):
    if path is None:
        return 1e9

    if path[0] != start or path[-1] != end:
        return 1e9

    dist = path_distance(path, graph)

    if dist is None:
        return 1e9

    return dist


# In[14]:


start = 1
end = 20

pop = generate_initial_population(start, end, graph, population_size=5)

for p in pop:
    print(p, "fitness:", fitness(p, graph, start, end))


# In[15]:


def tournament_selection(population, fitnesses, tournament_size = 3):
    indices = random.sample(range(len(population)), tournament_size)
    best_idx = min(indices, key=lambda i: fitnesses[i])

    return population[best_idx]


# In[16]:


start = 1
end = 20
population = generate_initial_population(start, end, graph, population_size=10)
fitnesses = [fitness(p, graph, start, end) for p in population]

print("POPULACIJA:")
for p, f in zip(population, fitnesses):
    print(p, "fitness:", f)

print("\nIZBRAN STARŠ:")
parent = tournament_selection(population, fitnesses, tournament_size=3)
print(parent, "fitness:", fitness(parent, graph, start, end))


# In[17]:


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


# In[18]:


p = population[0]
print("Original:", p)

mutated = mutate(p, graph, mutation_probability=0.5)
print("Mutated: ", mutated)

print("Fitness original:", fitness(p, graph, start, end))
print("Fitness mutated: ", fitness(mutated, graph, start, end))


# In[19]:


def single_point_crossover(parent1, parent2):
    if len(parent1) < 3 or len(parent2) < 3:
        return parent1[:], parent2[:]

    cut1 = random.randint(1, len(parent1) - 2)
    cut2 = random.randint(1, len(parent2) - 2)

    child1 = parent1[:cut1] + parent2[cut2:]
    child2 = parent2[:cut2] + parent1[cut1:]

    return child1, child2


# In[20]:


start = 1
end = 20

population = generate_initial_population(start, end, graph, population_size=4)
fitnesses = [fitness(p, graph, start, end) for p in population]

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


# In[21]:


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


# In[22]:


start = 1
end = 20

best_path, best_fit = genetic_algorithm(start, end, graph, population_size=50, generations=100, mutation_probability=0.1, tournament_size=3)

print("Najdena pot:", best_path)
print("Dolžina poti:", best_fit)


# TASK 2

# In[23]:


def follows_targets(path, targets):
    # Vrne True, če pot sledi target node-om v zaporedju.
    t_index = 0

    for node in path:
        if t_index < len(targets) and node == targets[t_index]:
            t_index += 1

    return t_index == len(targets)


# In[24]:


targets = [3,7,12]
path1 = [1, 3, 6, 7, 11, 12, 15]
path2 = [1, 7, 3, 12]
path3 = [1, 3, 6, 11, 15]
print(follows_targets(path1, targets))
print(follows_targets(path2, targets))
print(follows_targets(path3, targets))


# In[25]:


def fitness2(path, graph, start, end, targets):
    if path is None:
        return 1e9

    if path[0] != start or path[-1] != end:
        return 1e9

    dist = path_distance(path, graph)

    if dist is None:
        return 1e9

    if not follows_targets(path, targets):
        return 1e9

    return dist


# In[26]:


start = 1
end = 20
targets = [1, 6, 11, 20]

p1 = [1, 3, 6, 11, 14, 16, 17, 18, 19, 20]
p2 = [1, 3, 7, 11, 15, 16, 17, 18, 19, 20, 6]
p3 = [1, 3, 11, 6, 14, 16, 17, 18, 19, 20]

print(fitness2(p1, graph, start, end, targets))
print(fitness2(p2, graph, start, end, targets))
print(fitness2(p3, graph, start, end, targets))


# In[27]:


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


# In[28]:


start = 1
end = 20
targets = [6, 11, 14]

for i in range(10):
    p = generate_path_with_targets(start, end, targets, graph)
    if p is None:
        print("p = None (slepa ulica)")
        continue
    print(p, "  follows:", follows_targets(p, targets), "  dist:", path_distance(p, graph))


# In[29]:


def genetic_algorithm2(start, end, targets, graph, population_size=50, generations=100, mutation_probability=0.1, tournament_size=3):
    population = generate_initial_population(start, end, graph, population_size)
    best_path = None
    best_fitness = float("inf")

    for gen in range(generations):
        fitnesses = [fitness2(p, graph, start, end, targets) for p in population]

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


# In[30]:


start = 1
end = 20
targets = [5, 10, 14]

best_path, best_fit = genetic_algorithm2(start, end, targets, graph, population_size=50, generations=50)

print("Najboljša pot:", best_path)
print("Dolžina:", best_fit)

# preveriva še ročno
print("Sledi targetom? ", follows_targets(best_path, targets))


# In[31]:


start = 1
end = 50
targets = [7, 11, 14]

best_path, best_fit = genetic_algorithm2(
    start, end, targets, graph,
    population_size=50,
    generations=150,
    mutation_probability=0.1,
    tournament_size=3
)

print("Najdena pot:", best_path)
print("Dolžina:", best_fit)
print("Sledi targetom:", follows_targets(best_path, targets))


# TASK 3

# In[ ]:




