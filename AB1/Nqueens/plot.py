from evolutionaryNqueens import Nqueens
from evolutionaryNqueensVariableRatesForPopulation import NqueensPopulation
from evolutionaryNqueensVariableRatesForIndividual import NqueensIndividual

import matplotlib.pyplot as plt

def print_best_individual(individual):
    board = [[individual.chromosome[i * 8 + j] for j in range(8)] for i in range(8)]
    for row in board:
        print(" ".join(map(str, row)))
    print()

def main():  
  best_individual, best_value, max_fitness = Nqueens()
  best_individual_adap_pop, best_value_adap_pop, max_fitness_adap_pop = NqueensPopulation()
  best_individual_adap_crom, best_value_adap_crom, max_fitness_adap_crom = NqueensIndividual()
  
  print(f'Best chromossome without adaptation: {print_best_individual(best_individual)} = {best_value}\n')
  print(f'Best chromossome with adaptation by population : {print_best_individual(best_individual_adap_pop)} = {best_value_adap_pop}\n')
  print(f'Best chromossome with adaptation in each chromosome: {print_best_individual(best_individual_adap_crom)} = {best_value_adap_crom}\n')
  
  fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

  ax1.plot(range(len(max_fitness)), max_fitness, color='blue', label='Without adaptation')
  ax1.set_title('Without adaptation')
  ax1.set_ylabel('Fitness')

  ax2.plot(range(len(max_fitness_adap_pop)), max_fitness_adap_pop, color='red', label='With adaptation by population')
  ax2.set_title('With adaptation by population')
  ax2.set_ylabel('Fitness')

  ax3.plot(range(len(max_fitness_adap_crom)), max_fitness_adap_crom, color='green', label='With adaptation in each chromosome')
  ax3.set_title('With adaptation in each chromosome')
  ax3.set_ylabel('Fitness')
  ax3.set_xlabel('Generations')
  
  plt.tight_layout()
  plt.show()

main()