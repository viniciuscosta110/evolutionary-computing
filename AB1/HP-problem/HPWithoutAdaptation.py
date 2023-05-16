import random
import math
import copy

GERACAO = 100
N_POPULACAO = 1000
TAXA_MUTACAO = 0.01
VARIACOES = ['C','B','D','E']
CADEIA = "HPHPHPHPHHPHHPPH"

populacao = []
maxFitnessPerGeneration = []
geracao_atual = 1

class individuo:
    def __init__(self):
        self.orientacao = self.gerar_orientacao()
        self.pontos = self.calcular_pontos()
        self.monstro = self.verificar_monstro()
        self.fitness = self.calcular_fitness()

    def recalcular(self):
        self.pontos = self.calcular_pontos()
        self.monstro = self.verificar_monstro()
        self.fitness = self.calcular_fitness()

    def gerar_orientacao(self):
        ordem = []

        for i in range(0,len(CADEIA)):
            ordem.append(VARIACOES[random.randint(0,3)])
        
        return ordem
    
    def calcular_pontos(self):
        pontos = [(0,0)]
        for i in range(1,len(self.orientacao)):
            pontox = pontos[i-1][0]
            pontoy = pontos[i-1][1]

            if(self.orientacao[i-1] == 'C'):
                pontoy += 1
            elif(self.orientacao[i-1] == 'B'):
                pontoy -= 1
            if(self.orientacao[i-1] == 'D'):
                pontox += 1
            elif(self.orientacao[i-1] == 'E'):
                pontox -= 1
            
            pontos.append((pontox,pontoy))

        return pontos
    
    def verificar_monstro(self):
        for i in range(0,len(self.pontos)):
            for j in range(0,len(self.pontos)):
                if(i != j):
                    if(self.pontos[i] == self.pontos[j]):
                        return True
        return False

    def calcular_fitness(self):
        energia = 0

        for i in range(0,len(self.pontos)):
            if(CADEIA[i] == 'H'):
                for j in range(0,len(self.pontos)):
                    if(i != j and CADEIA[j] == 'H'):
                        ponto1x = self.pontos[i][0]
                        ponto1y = self.pontos[i][1]
                        ponto2x = self.pontos[j][0]
                        ponto2y = self.pontos[j][1]

                        if(ponto1x == ponto2x or ponto1y == ponto2y):
                            dist = math.sqrt(math.pow((ponto2x - ponto1x),2) + math.pow((ponto2y - ponto1y),2))
                            if(dist == 1):
                                energia += 1
        return energia
    

def sort_populacao():
    populacao.sort(key=lambda individual: individual.fitness, reverse=True)

def crosoover(pai,mae):
    novo = individuo()
    ponto_corte = random.randint(0,len(CADEIA))
    novo.orientacao[:ponto_corte] = mae.orientacao[:ponto_corte]
    novo.orientacao[ponto_corte:] = pai.orientacao[ponto_corte:]

    novo.recalcular()

    return novo

def mutacao(novo):
    for i in range(0,len(CADEIA)):
        if random.random() < TAXA_MUTACAO:
            novo.orientacao[i] = VARIACOES[random.randint(0,3)]
    
    novo.recalcular()

    return novo

def gerar_populacao():
    populacao = []
    while(len(populacao) < N_POPULACAO):
        novo = individuo()
        if novo.monstro == False:
            populacao.append(novo)

    sort_populacao()
    return populacao


def roulette_selection(populacao):
    fitness_total = sum(indiv.fitness for indiv in populacao)
    r = random.uniform(0, fitness_total)
    soma_partial = 0

    for individual in populacao:
        soma_partial += individual.fitness
        if soma_partial >= r:
            return copy.deepcopy(individual)
        
    return copy.deepcopy(populacao[0])

def evoluir(populacao):
    global geracao_atual
    global maxFitnessPerGeneration
    
    for i in range(len(populacao)):
        mae = roulette_selection(populacao)
        pai = roulette_selection(populacao)

        novo = crosoover(pai,mae)
        novo = mutacao(novo)

        if(novo.monstro):
            populacao.append(mae)
        else:
            populacao.append(novo)

        sort_populacao()
        populacao = populacao[:N_POPULACAO]
        
    maxFitnessPerGeneration.append(populacao[0].fitness)
    geracao_atual += 1


def main():
    global populacao
    global geracao_atual
    global maxFitnessPerGeneration

    populacao = gerar_populacao()
    while(geracao_atual <= GERACAO):
        evoluir(populacao)

    """ print("É AGORA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") """
    return populacao[0], populacao[0].fitness, maxFitnessPerGeneration
   # for rapaz in populacao:
    #    print(rapaz.fitness,rapaz.pontos)
    """ print(populacao[0].fitness,populacao[0].pontos) """
main()