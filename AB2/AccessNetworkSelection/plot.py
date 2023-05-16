from AccessNetworkSelection import AccessNetworkSelection

import matplotlib.pyplot as plt

def main():  
  best_individual, best_value, max_fitness = AccessNetworkSelection()

  max_fitness_length = len(max_fitness)

  fig, ax1 = plt.subplots(1, sharex=True, sharey=True)

  if max_fitness_length > 1:
    ax1.plot(range(1, len(max_fitness)+1), max_fitness, color='blue', label='Without adaptation')
  else:
    ax1.scatter(1, max_fitness[0], color='blue', label='Without adaptation')
  
  # x axis will be integers
  ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

  ax1.set_ylabel('Fitness')
  ax1.set_xlabel('Generations')
  plt.subplots_adjust(bottom=0.3)
  ax1.text(0.5, -0.3, f'Best chromossome: [{best_individual.chromosome[0]}], [{best_individual.chromosome[1]}],\n [{best_individual.chromosome[2]}], [{best_individual.chromosome[3]}]\n Fitness = {"%.8f" % best_value} \n Last Generation = {max_fitness_length} ', horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
  
  plt.show()



main()