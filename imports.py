import function_module as fc_m
import random
# Define constants and parameters
target_program = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
population_size = 100
mutation_rate = 0.1
crossover_rate = 0.7
max_generations = 1000
program_length = 100

# Generate an initial population of Brainfuck programs
population = fc_m.generate_random_population(population_size, program_length)

for generation in range(max_generations):
    # Evaluate the fitness of each program in the population
    print(generation,"generation")
    fitness_scores = []
    for program in population:
        print(program,"member of",generation,"generation")
        output = fc_m.execute_brainfuck(program)
        fitness = fc_m.calculate_fitness(output, target_program)
        fitness_scores.append((program, fitness))
    
    # Select programs for the next generation using tournament selection
    selected_population = fc_m.tournament_selection(population, fitness_scores)
    
    # Create the next generation through crossover and mutation
    next_generation = []
    while len(next_generation) < population_size:
        if random.random() < crossover_rate:
            parent1, parent2 = fc_m.select_parents(selected_population)
            child = fc_m.crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = fc_m.mutate(child)
            next_generation.append(child)
    
    # Replace the current population with the new generation
    population = next_generation

    # Check for convergence or success
    best_program, best_fitness = fc_m.get_best_program(fitness_scores)
    if best_fitness == 1.0:
        print("Found a program that prints 'Hello, World!':", best_program)
        break

print("No solution found after", max_generations, "generations.")
