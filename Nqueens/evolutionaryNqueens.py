import random

N = 8
TABLE = N * N
POPULATION = 100
MUTATION_RATE = 0.01
TOTAL_GENERATIONS = 100

population = []

class Individual:
    def __init__(self):
        chromosomeInit = [0] * TABLE
        for i in range(N):
            chromosomeInit[random.randint(0, N-1) * N + i] = 1

        self.chromosome = chromosomeInit
        self.fitness_score = self.fitness()

    def fitness(self):
        count_queens = sum(self.chromosome)
        conflicts = self.is_board_valid()
        fitness = 28 - conflicts if count_queens == N else 0
        return fitness

    def is_board_valid(self):
        board = [[self.chromosome[i * N + j] for j in range(N)] for i in range(N)]
        conflicts = 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == 1:
                    conflicts += self.check_diagonals(board, i, j)
                    conflicts += self.check_row(board, i, j)
                    conflicts += self.check_column(board, i, j)
        return conflicts

    @staticmethod
    def check_diagonals(board, row, col):
        conflicts = 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == 1 and j != col and i != row:
                    x = abs(i - row)
                    y = abs(j - col)
                    conflicts += 1 if x == y else 0
        return conflicts

    @staticmethod
    def check_row(board, row, col):
        conflicts = 0
        for i in range(N):
            if board[row][i] == 1 and i != col:
                conflicts += 1
        return conflicts

    @staticmethod
    def check_column(board, row, col):
        conflicts = 0
        for i in range(N):
            if board[i][col] == 1 and i != row:
                conflicts += 1
        return conflicts


def crossover(mother, father):
    new_individual = Individual()
    cut_point = random.randint(0, N-1) * N
    new_individual.chromosome[:cut_point] = mother.chromosome[:cut_point]
    new_individual.chromosome[cut_point:] = father.chromosome[cut_point:]
    return new_individual


def roulette_selection():
    total_fitness = sum(individual.fitness_score for individual in population)
    r = random.uniform(0, total_fitness)
    partial_sum = 0
    for individual in population:
        partial_sum += individual.fitness_score
        if partial_sum >= r:
            return individual
    return population[-1]


def mutation(individual):
    for i in range(TABLE):
        if random.randint(0, 100) < MUTATION_RATE*100:
            individual.chromosome[i] = 1 - individual.chromosome[i]

    return individual


def sort_population():
    population.sort(key=lambda individual: individual.fitness_score, reverse=True)


def print_population():
    for individual in population:
        board = [[individual.chromosome[i * N + j] for j in range(N)] for i in range(N)]
        for row in board:
            print(" ".join(map(str, row)))
        print("Fitness:", individual.fitness_score)
        print()


def print_best_individual():
    individual = population[0]
    board = [[individual.chromosome[i * N + j] for j in range(N)] for i in range(N)]
    print("Best individual:")
    for row in board:
        print(" ".join(map(str, row)))
    print("Fitness:", individual.fitness_score)
    print()


def evolve():
    global current_generation, population
    for i in range(POPULATION):
        mother = roulette_selection()
        father = roulette_selection()
        new_individual = crossover(mother, father)
        
        new_individual = mutation(new_individual)

        new_individual.fitness_score = new_individual.fitness()
        population.append(new_individual)
        
    sort_population()
    population = population[:POPULATION]
    current_generation += 1


def main():
    global current_generation, population
    population = [Individual() for _ in range(POPULATION)]
    current_generation = 1
    while population[0].fitness_score != 28 and current_generation <= TOTAL_GENERATIONS:
        evolve()

    print("Generation:", current_generation-1)
    print_best_individual()

main()