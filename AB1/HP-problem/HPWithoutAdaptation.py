import random
import math
import copy

GERACAO = 100
N_POPULACAO = 20
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
                pontoy -= 1
            elif(self.orientacao[i-1] == 'B'):
                pontoy += 1
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
                    if(self.pontos[i][0] == self.pontos[j][0] and self.pontos[i][1] == self.pontos[j][1]):
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

def crossover(pai,mae):
    novo = individuo()
    ponto_corte = random.randint(0,len(CADEIA))
    ponto_corte2 = random.randint(0,len(CADEIA))

    while ponto_corte2 == ponto_corte:
        ponto_corte2 = random.randint(0,len(CADEIA))

    if ponto_corte > ponto_corte2:
        ponto_corte, ponto_corte2 = ponto_corte2, ponto_corte
    
    novo.orientacao = (mae.orientacao[:ponto_corte] + 
                      pai.orientacao[ponto_corte:ponto_corte2] + 
                      mae.orientacao[ponto_corte2:])

    novo.recalcular()

    return novo

def mutacao(novo):
    for i in range(0,len(CADEIA)):
        if random.randint(0, 100) < TAXA_MUTACAO*100:
            orientacao = novo.orientacao[i]
            novo.orientacao[i] = VARIACOES[random.randint(0,3)]

            while orientacao == novo.orientacao[i]:
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

        novo = crossover(pai,mae)
        novo = mutacao(novo)

        while(novo.monstro):
            novo = crossover(pai,mae)
            novo = mutacao(novo)
            
        populacao.append(novo)
        populacao = populacao[:N_POPULACAO]
        
    maxFitnessPerGeneration.append(populacao[0].fitness)
    geracao_atual += 1

def para_por_igualdade(cacheMelhorEnergia):
    # Caso os últimos 50 sejam o mesmo, parar
    tamanho = len(cacheMelhorEnergia)
    if(tamanho < 5): return False

    for i in range(tamanho-1, tamanho-50, -1):
        if(cacheMelhorEnergia[i] != cacheMelhorEnergia[i-1]):
            return False
    
    return True
        
    
def HP():
    global populacao
    global geracao_atual
    global maxFitnessPerGeneration

    populacao = gerar_populacao()
    pararPorFaltaDeMelhoria = False
    cacheMelhorEnergia = [0]

    while(geracao_atual <= GERACAO and not pararPorFaltaDeMelhoria):
        evoluir(populacao)
        cacheMelhorEnergia.append(populacao[0].fitness)
        pararPorFaltaDeMelhoria = para_por_igualdade(cacheMelhorEnergia)
    
    sort_populacao()
    print("Melhor individuo encontrado: ")
    print("Orientacao: ", populacao[0].orientacao)
    print("Energia: ", populacao[0].fitness)
    print("Geracao: ", geracao_atual)

    
    
    # Visualize the protein in 2D grid if needed
    min_x = min(p[0] for p in populacao[0].pontos)
    max_x = max(p[0] for p in populacao[0].pontos)
    min_y = min(p[1] for p in populacao[0].pontos)
    max_y = max(p[1] for p in populacao[0].pontos)
    
    grid_width = max_x - min_x + 1
    grid_height = max_y - min_y + 1
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
    
    for i, (x, y) in enumerate(populacao[0].pontos):
        grid[y - min_y][x - min_x] = CADEIA[i]
    
    print("\nVisualização 2D:")
    for row in grid:
        print(''.join(row))

def main():
    global populacao
    global geracao_atual
    global maxFitnessPerGeneration

    populacao = gerar_populacao()
    while populacao[0].fitness != 16:
        HP()

main()