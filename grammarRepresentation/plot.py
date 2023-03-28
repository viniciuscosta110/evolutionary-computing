from grammarEv import grammarEv
from grammarEvVariableRatesForPopulation import grammarEvPopulation
from grammarEvVariableRatesForIndividual import grammarEvIndividual

import matplotlib.pyplot as plt

def main():  
  best_individual, best_value, max_fitness = grammarEv()
  best_individual_adap_pop, best_value_adap_pop, max_fitness_adap_pop = grammarEvPopulation()
  best_individual_adap_crom, best_value_adap_crom, max_fitness_adap_crom = grammarEvIndividual()

  if(best_individual == None or best_individual_adap_pop == None or best_individual_adap_crom == None):
    return

  print(f'Best chromossome without adaptation: {(best_individual)} = {best_value}\n')
  print(f'Best chromossome with adaptation by population : {(best_individual_adap_pop)} = {best_value_adap_pop}\n')
  print(f'Best chromossome with adaptation in each chromosome: {(best_individual_adap_crom)} = {best_value_adap_crom}\n')
  
  fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

  ax1.plot(range(len(max_fitness)), max_fitness, color='blue', label='Without adaptation', marker='o')
  ax1.set_title('Without adaptation')
  ax1.set_ylabel('Fitness')

  ax2.plot(range(len(max_fitness_adap_pop)), max_fitness_adap_pop, color='red', label='With adaptation by population', marker='o')
  ax2.set_title('With adaptation by population')
  ax2.set_ylabel('Fitness')

  ax3.plot(range(len(max_fitness_adap_crom)), max_fitness_adap_crom, color='green', label='With adaptation in each chromosome', marker='o')
  ax3.set_title('With adaptation in each chromosome')
  ax3.set_ylabel('Fitness')
  ax3.set_xlabel('Generation')
  
  plt.tight_layout()
  plt.show()

main()