from utils import *
import random
import numpy as np

CHROMOSOME_LENGHT = 4

MUTATION_RATE = 0.02
MUTATION_RANGE = 10

POPULATION_SIZE = 10
TOTAL_GENERATIONS = 100

GSM_VOICE_LIMITS = [0, 125]
GSM_DATA_LIMITS = [0, 30]

WCDMA_VOICE_LIMITS = [0, 150]
WCDMA_DATA_LIMITS = [0, 80]

VOICES_LIMIT = 275
DATA_LIMIT = 110

DESIRED_COST = 0.0

population = []
currentGeneration = 1

bestFitnessOfEachGeneration = []

class Individual:
  def __init__(self):
    self.chromosome = self.InitializeChromosome()
    self.fitness_score = self.fitness()

  def InitializeChromosome(self):
    GSMvoice = random.uniform(GSM_VOICE_LIMITS[0], GSM_VOICE_LIMITS[1])
    GSMdata = random.uniform(GSM_DATA_LIMITS[0], GSM_DATA_LIMITS[1])
    
    WCDMAvoice = random.uniform(WCDMA_VOICE_LIMITS[0], WCDMA_VOICE_LIMITS[1])
    WCDMAdata = random.uniform(WCDMA_DATA_LIMITS[0], WCDMA_DATA_LIMITS[1])

    return [GSMvoice, WCDMAvoice, GSMdata, WCDMAdata]

  def fitness(self):
    voices = self.chromosome[0:2]
    data = self.chromosome[2:4]

    userVoices = GetUserVoices(voices)
    userData = GetUserData(data)

    costGSM = GetGSMCost(voices[0], data[0])
    costWCDMA = GetWCDMACost(voices[1], data[1])

    cost = GetCost(userVoices, userData, costGSM, costWCDMA)

    return cost

  def IsValid(self):
    sumVoices = sum(self.chromosome[0:2])
    sumData = sum(self.chromosome[2:4])

    if sumVoices > VOICES_LIMIT:
      return False

    if sumData > DATA_LIMIT:
      return False

    return True

def Crossover(parent1, parent2):
  child = Individual()
  for i in range(0, CHROMOSOME_LENGHT):
    child.chromosome[i] = (parent1.chromosome[i] + parent2.chromosome[i]) / 2

  return child

def Mutation(individual):
  for i in range(0, CHROMOSOME_LENGHT):
    if random.random() < MUTATION_RATE:
      individual.chromosome[i] += random.gauss(-MUTATION_RANGE, MUTATION_RANGE)

  return individual

def GeneratePopulation():
  population = []

  while len(population) <= POPULATION_SIZE:
    individual = Individual()

    if individual.IsValid():
      population.append(individual)

  return population

def roulette_selection():
  global population

  total_fitness = sum(1/individual.fitness_score for individual in population)
  fitnesses = [1/individual.fitness_score for individual in population]
  probabilities = [fitness/total_fitness for fitness in fitnesses]

  return random.choices(population, probabilities, k=2)

# Evolutionary Algorithm
def Evolve():
  global population, currentGeneration, bestFitnessOfEachGeneration

  while population[0].fitness_score >= DESIRED_COST and currentGeneration < TOTAL_GENERATIONS:
    while len(population) < POPULATION_SIZE*2:
      parent1, parent2 = roulette_selection()

      child = Crossover(parent1, parent2)
      child = Mutation(child)

      child.fitness_score = child.fitness()

      if(child.IsValid()):
        population.append(child)

    population.sort(key=lambda x: x.fitness_score)
    population = population[:POPULATION_SIZE]

    bestFitnessOfEachGeneration.append(population[0].fitness_score)
    currentGeneration += 1

def PrintBestIndividual():
  global population, currentGeneration

  bestIndividual = population[0]
  print("Chromosome: ", bestIndividual.chromosome)
  print("Fitness: ", "%.8f" % bestIndividual.fitness_score)
  print("Current Generation: ", currentGeneration, "\n")

def AccessNetworkSelection():
  global population, currentGeneration, bestFitnessOfEachGeneration
  
  population = GeneratePopulation()
  population.sort(key=lambda x: x.fitness_score)

  bestFitnessOfEachGeneration.append(population[0].fitness_score)

  if(population[0].fitness_score < 0):
    print("Chromosome: ", population[0].chromosome)
    print("Fitness: ", "%.8f" % population[0].fitness_score)
    print("Current Generation: ", currentGeneration)
    return population[0], population[0].fitness_score, bestFitnessOfEachGeneration

  Evolve()
  PrintBestIndividual()

  return population[0], population[0].fitness_score, bestFitnessOfEachGeneration

    
if __name__ == '__main__':
  AccessNetworkSelection()
