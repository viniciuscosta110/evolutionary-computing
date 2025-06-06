import random

GERACAO = 100
N_POPULACAO = 500
TAXA_MUTACAO = 0.05
TAMANHO_DO_TORNEIO = 30
TAMANHO_SEM_MELHORA = 20

DNAs = ['ATCGAGCTAGCTAGC--',
'CTAGCTAGCT--CTCCCAA',
'GCTAG-TAGCTAGCTAG']

populacao = []
geracao_atual = 1

class individuo:
    def __init__(self):
        self.sequencias = self.gerar_sequencias()
        self.fitness = self.calcular_fitness()

    def recalcular(self,nova_sequencia):
        self.sequencias = nova_sequencia
        self.fitness = self.calcular_fitness()

    def gerar_sequencias(self):
        sequencia = []
        # Essa função coloca todas as sequências de entrada no mesmo tamanho da maior e aumenta em 50% para colocar Gaps
        maio_tam = max([len(seq) for seq in DNAs])
        maio_tam += maio_tam//2
        
        for seq in DNAs:
            seq = list(seq)
            while(len(seq) != maio_tam):
                seq.insert(random.randint(0, len(seq)), '-')
            sequencia.append(seq)

        return sequencia

    def calcular_fitness(self):
        fitness = 0
        tamanho = max([len(seq) for seq in self.sequencias])

        for j in range(tamanho): #esse for loopa entre todas as colunas
            for i in range(len(DNAs)): #os proximos fors loopam entre todas as sequencias de DNA
                for k in range(i + 1,len(DNAs)):
                    if(self.sequencias[i][j] == '-' or self.sequencias[k][j] == '-'):
                        continue
                    elif(self.sequencias[i][j] == self.sequencias[k][j]):
                        fitness += 1
                    else:
                        fitness -= 1
        return fitness

def sort_populacao():
    populacao.sort(key=lambda individual: individual.fitness, reverse=True)

def crossover(pai,mae):
    filho = individuo()
    sequencia_gerada = []

    for i in range(len(pai.sequencias)):
        if random.random() < 0.5:
            sequencia_gerada.append(pai.sequencias[i])
        else:
            sequencia_gerada.append(mae.sequencias[i])
    
    filho.recalcular(sequencia_gerada)

    return filho

def mutacao(novo):
    nova_sequencias = []

    for seq in novo.sequencias:
        seq = list(seq) #pega cada sequencia do individuo e verifica se vai ser mutada
        if(random.random() < TAXA_MUTACAO):
            contador = 0

            while('-' in seq): #remove todos os gaps
                seq.remove('-')
                contador += 1

            for i  in range(contador): #distribui todos de forma aleatoria
                seq.insert(random.randint(0, len(seq)), '-')
        
        nova_sequencias.append(seq)

    novo.recalcular(nova_sequencias)
    return novo

def gerar_populacao():
    populacao = []
    while(len(populacao) < N_POPULACAO):
        novo = individuo()
        populacao.append(novo)

    sort_populacao()
    return populacao

def selection(populacao):
    torneio = random.sample(populacao, TAMANHO_DO_TORNEIO)
    torneio.sort(key=lambda individual: individual.fitness, reverse=True)

    return torneio[0]

def evoluir(populacao):
    global geracao_atual

    for i in range(N_POPULACAO):
        mae = selection(populacao)
        pai = selection(populacao)

        novo = crossover(pai,mae)
        novo = mutacao(novo)

        populacao.append(novo)
        
    sort_populacao()
 
    populacao = populacao[:N_POPULACAO]
    geracao_atual += 1

def checarSeFitnessMelhorou(cacheMelhorFitness):
    # Caso a fitness não tenha melhorado em TAMANHO_SEM_MELHORA gerações, reinicia a população
    if len(cacheMelhorFitness) <= TAMANHO_SEM_MELHORA: return
    
    if cacheMelhorFitness[-1] == cacheMelhorFitness[-TAMANHO_SEM_MELHORA]:
        for i in range(1, len(populacao)):
            populacao[i] = individuo()
        sort_populacao()
        cacheMelhorFitness.clear()
        cacheMelhorFitness.append(populacao[0].fitness)
        print("Reiniciando população")

def main():
    global populacao
    global geracao_atual
    populacao = gerar_populacao()

    cacheMelhorFitness = []
    cacheMelhorFitness.append(populacao[0].fitness)

    while(geracao_atual <= GERACAO):
        evoluir(populacao)
        cacheMelhorFitness.append(populacao[0].fitness)
        checarSeFitnessMelhorou(cacheMelhorFitness)
        print("Geração:", geracao_atual)
        print("Fitness:", populacao[0].fitness, '\n')
        
    for seq in populacao[0].sequencias:
        print(seq)
    print(populacao[0].calcular_fitness())

main()