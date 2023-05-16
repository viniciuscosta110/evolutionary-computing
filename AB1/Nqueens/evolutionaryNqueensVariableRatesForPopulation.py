import random
import copy

N = 8
TABLE = N * N
POPULATION = 1000
MIN_MUTATION_RATE = 0.01
MAX_MUTATION_RATE = 0.1
MIN_CROSSOVER_RATE = 0.5
MAX_CROSSOVER_RATE = 0.9
TOTAL_GENERATIONS = 100

currentMutationRate = MIN_MUTATION_RATE
currentCrossoverRate = MIN_CROSSOVER_RATE

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


def crossover(mother, father, CROSSOVER_RATE):
    new_individual = Individual()

    if(random.random() < CROSSOVER_RATE):
        cut_point = random.randint(0, N-1) * N
        new_individual.chromosome[:cut_point] = mother.chromosome[:cut_point]
        new_individual.chromosome[cut_point:] = father.chromosome[cut_point:]
    else:
        new_individual = copy.deepcopy(mother if random.random() < 0.5 else father) 
    return new_individual


def roulette_selection():
    total_fitness = sum(individual.fitness_score for individual in population)
    r = random.uniform(0, total_fitness)
    partial_sum = 0
    for individual in population:
        partial_sum += individual.fitness_score
        if partial_sum >= r:
            return individual
    return population[0]


def mutation(individual, mutationRate):
    for i in range(TABLE):
        if random.random() < mutationRate:
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
    global currentGeneration, population, currentMutationRate, currentCrossoverRate

    currentCrossoverRate = random.uniform(MIN_CROSSOVER_RATE, MAX_CROSSOVER_RATE)
    currentMutationRate = random.uniform(MIN_MUTATION_RATE, MAX_MUTATION_RATE)

    for i in range(POPULATION):
        mother = roulette_selection()
        father = roulette_selection()

        newIndividual = crossover(mother, father, currentCrossoverRate)
        newMutatedIndividual = mutation(copy.deepcopy(newIndividual), currentMutationRate) 

        newIndividual.fitness_score = newIndividual.fitness()
        newMutatedIndividual.fitness_score = newMutatedIndividual.fitness()
        
        population.append(newIndividual)
        population.append(newMutatedIndividual)
        
    sort_population()
    population = population[:POPULATION]
    currentGeneration += 1


def NqueensPopulation():
    global currentGeneration, population, currentMutationRate, currentCrossoverRate
    population = [Individual() for _ in range(POPULATION)]
    currentGeneration = 1
    maxFitnessPerGeneration = []

    # population[0].fitness_score != 28
    while currentGeneration <= TOTAL_GENERATIONS:
        evolve()
        maxFitnessPerGeneration.append(population[0].fitness_score)

    """ print_best_individual()
    print("Generation:", currentGeneration-1) """
    return population[0], population[0].fitness_score, maxFitnessPerGeneration

NqueensPopulation()