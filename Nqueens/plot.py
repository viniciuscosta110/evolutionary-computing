from evolutionaryNqueens import Nqueens
from evolutionaryNqueensVariableRatesForPopulation import NqueensPopulation
from evolutionaryNqueensVariableRatesForIndividual import NqueensIndividual

import matplotlib.pyplot as plt

def main():  
  best_individual, best_value, max_fitness = Nqueens()
  best_individual_adap_pop, best_value_adap_pop, max_fitness_adap_pop = NqueensPopulation()
  best_individual_adap_crom, best_value_adap_crom, max_fitness_adap_crom = NqueensIndividual()
  
  print(f'Melhor expressão sem adaptação: {best_individual.chromosome} = {best_value}\n')
  print(f'Melhor expressão com adaptação: {best_individual_adap_pop.chromosome} = {best_value_adap_pop}\n')
  print(f'Melhor expressão com taxas em cada cromossomo: {best_individual_adap_crom.chromosome} = {best_value_adap_crom}\n')
  
  (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

  ax1.plot(range(len(max_fitness)), max_fitness, color='blue', label='Sem adaptação')
  ax1.set_title('Sem adaptação')
  ax1.set_ylabel('Fitness')

  ax2.plot(range(len(max_fitness_adap_pop)), max_fitness_adap_pop, color='red', label='Com adaptação')
  ax2.set_title('Com adaptação por população')
  ax2.set_ylabel('Fitness')

  ax3.plot(range(len(max_fitness_adap_crom)), max_fitness_adap_crom, color='green', label='Com taxas em cada cromossomo')
  ax3.set_title('Com adaptação em cada cromossomo')
  ax3.set_ylabel('Fitness')
  ax3.set_xlabel('Gerações')
  
  plt.show()

main()