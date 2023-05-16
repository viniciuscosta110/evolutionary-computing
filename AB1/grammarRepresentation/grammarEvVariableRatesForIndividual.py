import random

# Define the problem space
OPERATORS = ['+', '-', '*', '/']
TARGET = 10
POP_SIZE = 100

MAX_MUTATION_RATE = 0.5
MIN_MUTATION_RATE = 0.01

MAX_CROSSOVER_RATE = 0.9
MIN_CROSSOVER_RATE = 0.4

CURRENT_MUTATION_RATE = 0.01
CURRENT_CROSSOVER_RATE = 0.5

TOTAL_GENERATIONS = 1000
CURRENT_GENERATION = 1
maxFitnessPerGeneration = []

# Define the chromosome as a syntax tree
class Node:
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right
        self.fitness = 0

    def evaluate(self):
      if self.op == '+':
          left = self.left.evaluate() if self.left is not None else 0
          right = self.right.evaluate() if self.right is not None else 0
          return left + right
      elif self.op == '-':
          left = self.left.evaluate() if self.left is not None else 0
          right = self.right.evaluate() if self.right is not None else 0
          return left - right
      elif self.op == '*':
          left = self.left.evaluate() if self.left is not None else 1
          right = self.right.evaluate() if self.right is not None else 1
          return left * right
      elif self.op == '/':
          left = self.left.evaluate() if self.left is not None else 1
          right = self.right.evaluate() if self.right is not None else 1
          if right == 0:
              return 0
          return left / right
      else:
          return self.op


    def __str__(self):
        if self.op in OPERATORS:
            return f'({str(self.left)} {self.op} {str(self.right)})'
        else:
            return str(self.op)

def diversity(population):
    return len(set([str(node) for node in population]))/1000

# Define the fitness function
def fitness(node):
    return abs(node.evaluate() - TARGET)

# Generate an initial population
def generate_population(size):
    population = []
    for i in range(size):
        root = Node(random.choice(OPERATORS))
        if root.op in OPERATORS:
            root.left = Node(random.randint(1, 100))
            root.right = Node(random.randint(1, 100))
        else:
            root.left = Node(random.randint(1, 100))
        population.append(root)
    return population

# Selection: select the fittest chromosomes
def select(population, n):
    population.sort(key=fitness)
    return population[:n]

def roulette_wheel_selection(population, n):
    fitnesses = [fitness(node) for node in population]
    total_fitness = sum(fitnesses)
    probabilities = [fitness/total_fitness for fitness in fitnesses]
    return random.choices(population, probabilities, k=n)

# Crossover: swap subtrees of selected chromosomes
def crossover(parent1, parent2, CROSSOVER_RATE=0.5):
    if random.random() > CROSSOVER_RATE:
        return [parent1, parent2]

    child1 = Node(parent1.op, parent2.left, parent1.right)
    child2 = Node(parent2.op, parent1.left, parent2.right)
    return [child1, child2]

    
# Mutation: randomly change a subtree in a chromosome
def mutate(node):
    CURRENT_MUTATION_RATE = random.uniform(MIN_MUTATION_RATE, MAX_MUTATION_RATE)
    if random.random() < CURRENT_MUTATION_RATE:
        if node.op not in OPERATORS:
            if node.left is not None and node.right is not None:
                if random.random() < 0.5:
                    node.left = Node(random.randint(1,10))
                else:
                    node.right = Node(random.randint(1,10))
        else:
            node.op = random.choice(OPERATORS)
    if node.left is not None:
        mutate(node.left)
    if node.right is not None:
        mutate(node.right)
    return node


def checkIfSolution(population):
    global maxFitnessPerGeneration

    for chromosome in population:
        # check if chromosome has a none string value at right and left
        if(str(chromosome.left.op) in OPERATORS or str(chromosome.right.op) in OPERATORS):
            continue
        if fitness(chromosome) == 0 and str(chromosome.left.op) :
            """     print("")
            print("Solution:", chromosome)
            print("Evaluation:", chromosome.evaluate())
            print("Diversity:", diversity(population)*100, "%")
            print("Generation:", CURRENT_GENERATION) """

            return population[0], population[0].evaluate(), maxFitnessPerGeneration

    return 0, 0, maxFitnessPerGeneration

def grammarEvIndividual():
    global CURRENT_MUTATION_RATE, CURRENT_CROSSOVER_RATE, CURRENT_GENERATION, TOTAL_GENERATIONS, POP_SIZE, TARGET, OPERATORS, maxFitnessPerGeneration
    # Run the genetic algorithm
    population = generate_population(POP_SIZE)

    # Evaluate the initial population
    checkIfSolution(population)

    for i in range(TOTAL_GENERATIONS):
        CURRENT_GENERATION += 1    

        selected = select(population, POP_SIZE // 2)
        population = []

        for j in range(POP_SIZE // 2):
            CURRENT_CROSSOVER_RATE = random.uniform(MIN_CROSSOVER_RATE, MAX_CROSSOVER_RATE)

            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            children = crossover(parent1, parent2, CURRENT_CROSSOVER_RATE)
            population.extend(children)
            
        population = [mutate(chromosome) for chromosome in population]
        for(chromosome) in population:
            chromosome.fitness = chromosome.evaluate()

        # sort populatiion by fitness close to target
        population.sort(key=lambda x: abs(x.fitness - TARGET))
        maxFitnessPerGeneration.append(population[0].fitness)

        # Check if the target has been reached
        solution, solutionFitness, maxFitnessPerGeneration = checkIfSolution(population)
        if solution:
            return solution, solutionFitness, maxFitnessPerGeneration

    print("Failed to find a solution")
    return population[0], population[0].evaluate(), maxFitnessPerGeneration


grammarEvIndividual()