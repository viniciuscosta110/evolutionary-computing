import random

# Define the problem space
OPERATORS = ['+', '-', '*', '/']
TARGET = 10
POP_SIZE = 10000
MUTATION_RATE = 0.5

# Define the chromosome as a syntax tree
class Node:
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

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

# Define the fitness function
def fitness(node):
    return abs(node.evaluate() - TARGET)

# Generate an initial population
def generate_population(size):
    population = []
    for i in range(size):
        root = Node(random.choice(OPERATORS))
        if root.op in OPERATORS:
            root.left = Node(random.randint(1, 10))
            root.right = Node(random.randint(1, 10))
        else:
            root.left = Node(random.randint(1, 10))
        population.append(root)
    return population

# Selection: select the fittest chromosomes
def select(population, n):
    population.sort(key=fitness)
    return population[:n]

# Crossover: swap subtrees of selected chromosomes
def crossover(parent1, parent2):
    child1 = Node(parent1.op, parent2.left, parent1.right)
    child2 = Node(parent2.op, parent1.left, parent2.right)
    return [child1, child2]

    
# Mutation: randomly change a subtree in a chromosome
def mutate(node):
    if random.random() < MUTATION_RATE:
        if node.op not in OPERATORS:
            if node.left is not None and node.right is not None:
                if random.random() < 0.5:
                    node.left = Node(random.choice(OPERATORS))
                else:
                    node.right = Node(random.choice(OPERATORS))
        else:
            node.op = random.choice(OPERATORS)
    if node.left is not None:
        mutate(node.left)
    if node.right is not None:
        mutate(node.right)
    return node


# Run the genetic algorithm
population = generate_population(POP_SIZE)
for i in range(100):
    selected = select(population, POP_SIZE // 2)
    population = []
    for j in range(POP_SIZE // 2):
        parent1 = random.choice(selected)
        parent2 = random.choice(selected)
        children = crossover(parent1, parent2)
        population.extend(children)
    population = [mutate(chromosome) for chromosome in population]
    
    # Check if the target has been reached
    for chromosome in population:
        """ check if chromosome has a none string value at right and left """
        if(str(chromosome.left.op) in OPERATORS or str(chromosome.right.op) in OPERATORS):
          continue
        if fitness(chromosome) == 0 and str(chromosome.left.op) :
            print(chromosome)
            exit(0)

print("Failed to find a solution")
