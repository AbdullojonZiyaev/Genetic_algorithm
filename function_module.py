import random

### Generating random population for the AI to work further
def generate_random_program(length):
    """
    Generate a random Brainfuck program of the specified length.
    """
    valid_characters = ['>', '<', '+', '-', '[', ']', '.', ',']
    program = ''.join(random.choice(valid_characters) for _ in range(length))
    return program

def generate_random_population(population_size, program_length = 100):
    """
    Generate a population of ra3ndom Brainfuck programs of the specified length.
    """
    population = [generate_random_program(program_length) for _ in range(population_size)]
    return population

#population_size = 100
#program_length = 50  # Adjust the length as needed
#initial_population = generate_random_population(population_size, program_length)

#########################################################################################################################

### Imitating the brainfuck to work further
def execute_brainfuck(program):
    """
    Execute a Brainfuck program and capture its output.
    """
    memory = [0] * 30000  # Initialize a memory tape with 30,000 cells
    ptr = 0  # Memory pointer
    output = []  # List to capture the program's output
    program_length = len(program)
    program_counter = 0

    while program_counter < program_length:
        command = program[program_counter]

        if command == '>':
            ptr += 1
        elif command == '<':
            ptr -= 1
        elif command == '+':
            memory[ptr] = (memory[ptr] + 1) % 256
        elif command == '-':
            memory[ptr] = (memory[ptr] - 1) % 256
        elif command == '.':
            output.append(chr(memory[ptr]))
        elif command == ',':
            # Implement input handling if needed
            pass
        elif command == '[':
            if memory[ptr] == 0:
                # Jump forward to the matching ']'
                level = 1
                while level > 0:
                    program_counter += 1
                    if program[program_counter] == '[':
                        level += 1
                    elif program[program_counter] == ']':
                        level -= 1
            else:
                pass
        elif command == ']':
            if memory[ptr] != 0:
                # Jump back to the matching '['
                level = 1
                while level > 0:
                    program_counter -= 1
                    if program[program_counter] == ']':
                        level += 1
                    elif program[program_counter] == '[':
                        level -= 1
            else:
                pass

        program_counter += 1
        print(program_counter)

    return ''.join(output)

example_program = "[++[.-,>+<++-<.[+<-<-<.[]<][+.>,.,>[<].>.>+>][<[[,.,<[--<],-]-]<[.>]+.>->-+.]++><>++-.<,,>[].[]]]"
output = execute_brainfuck(example_program)
print(output)

#########################################################################################################################

###Calculate the fitness function
def calculate_fitness(program_output, target_output):
    """
    Calculate the fitness of a Brainfuck program by comparing its output to the target output.
    returns A fitness score, where 1.0 represents a perfect match and lower values represent deviations.
    """
    # Calculate the Levenshtein distance (edit distance) between the program output and target output
    # Smaller distance indicates a closer match
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    # Calculate fitness as a normalized similarity score (1 - normalized distance)
    distance = levenshtein_distance(program_output, target_output)
    max_distance = max(len(program_output), len(target_output))
    fitness = 1.0 - (distance / max_distance)
    return max(0.0, fitness)  # Ensure fitness is non-negative

#target_output = "Hello, World!"
#example_output = "JX"
#fitness_score = calculate_fitness(example_output, target_output)

#########################################################################################################################

def tournament_selection(population, fitness_scores, tournament_size = 2):
    """
    Perform tournament selection to select individuals from the population.

    :param population: The list of Brainfuck programs.
    :param fitness_scores: A list of (program, fitness) tuples for each program.
    :param tournament_size: The number of individuals to participate in each tournament.
    :return: A list of selected programs.
    """
    selected_programs = []
    while len(selected_programs) < len(population):
        tournament = random.sample(fitness_scores, tournament_size)
        winner = max(tournament, key=lambda x: x[1])  # Select the program with the highest fitness
        selected_programs.append(winner[0])
    return selected_programs

#population = ["Program1", "Program2", "Program3", "Program4"]
#fitness_scores = [("Program1", 0.8), ("Program2", 0.7), ("Program3", 0.6), ("Program4", 0.9)]
#tournament_size = 2
#selected_programs = tournament_selection(population, fitness_scores, tournament_size)

#########################################################################################################################

### The random selection is better for diversity and exploration giving us more place to work, we can also use the roulette choose
###choosing the parents with higher fitness score that will boost the time, but random is more flexible

def select_parents(selected_population):
    """
    Randomly select two parents from the selected population.

    :param selected_population: A list of programs selected for the next generation.
    :return: A tuple containing two selected parents.
    """
    parent1, parent2 = random.sample(selected_population, 2)
    return parent1, parent2

#selected_population = ["Program1", "Program2", "Program3", "Program4", "Program5"]
#parent1, parent2 = select_parents(selected_population)

#########################################################################################################################

###Randomly crossing the segments
def crossover(parent1, parent2):
    """
    Perform single-point crossover to create offspring from two parents.

    :param parent1: The first parent program as a string.
    :param parent2: The second parent program as a string.
    :return: Offspring program created by combining genetic information from parents.
    """
    # Choose a random crossover point
    crossover_point = random.randint(0, min(len(parent1), len(parent2)))

    # Create the offspring by combining segments of the parents
    offspring = parent1[:crossover_point] + parent2[crossover_point:]

    return offspring
#parent1 = "++++++++[>++++++>++++++++>+++<<<-]>."
#parent2 = "++++++++[>++++++++++>+++++++<<-]>."
#offspring = crossover(parent1, parent2)

#########################################################################################################################

def mutate(program, mutation_rate, valid_characters):
    """
    Mutate a Brainfuck program by changing one character at a random position.

    :param program: The input Brainfuck program as a string.
    :param mutation_rate: The probability of a mutation occurring (e.g., 0.1 for 10% mutation rate).
    :param valid_characters: A list of valid Brainfuck characters (e.g., ['>', '<', '+', '-', '[', ']', '.', ',']).
    :return: The mutated program as a string.
    """
    if random.random() < mutation_rate:
        # Choose a random position for mutation
        mutation_position = random.randint(0, len(program) - 1)
        
        # Choose a random valid Brainfuck character to replace the current character
        new_character = random.choice(valid_characters)
        
        # Mutate the program by replacing the character at the chosen position
        program = program[:mutation_position] + new_character + program[mutation_position + 1:]
    
    return program

# Example usage
#original_program = "++++++++[>++++++>++++++++>+++<<<-]>."
#mutation_rate = 0.2  # 10% mutation rate
#valid_characters = ['>', '<', '+', '-', '[', ']', '.', ',']
#mutated_program = mutate(original_program, mutation_rate, valid_characters)

#########################################################################################################################

def get_best_program(fitness_scores):
    """
    Get the program with the highest fitness score from a list of (program, fitness) tuples.

    :param fitness_scores: A list of (program, fitness) tuples for each program.
    :return: A tuple containing the best program and its fitness score.
    """
    best_program, best_fitness = max(fitness_scores, key=lambda x: x[1])
    return best_program, best_fitness

# Example usage
#fitness_scores = [("Program1", 0.8), ("Program2", 0.7), ("Program3", 0.6), ("Program4", 0.9)]
#best_program, best_fitness = get_best_program(fitness_scores)


