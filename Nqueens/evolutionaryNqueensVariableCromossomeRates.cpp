// Solving n queens problem using evolutionary algorithm

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <vector>

using namespace std;

#define N 8
#define TABLE N*N
#define POPULATION 100
#define DIVERSITY_TARGET 0.1
#define TOTAL_GENERATIONS 10000

struct Individual {
    int cromossome[TABLE];
    float fitnessScore;
};

vector<Individual> population = vector<Individual>(POPULATION);
vector<Individual> newPopulation = vector<Individual>(POPULATION);
vector<Individual> mutatePopulation = vector<Individual>(POPULATION);

int currentNewPopulationCount = 0;
int currentMutatePopulationCount = 0;

int currentGeneration = 0;

double MUTATION_RATE = 0.01;
double CROSSOVER_RATE = 0.5;

int checkDiagonals(int board[N][N], int row, int col){
    int conflicts = 0;

    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            if(board[i][j] == 1 && j != col && i != row){
                int x = abs(i - row);
                int y = abs(j - col);

                conflicts += x == y ? 1 : 0;
            }
        }
    }

    return conflicts;
}

int checkRow(int board[N][N], int row, int col){
    int conflicts = 0;

    for(int i = 0; i < N; i++){
        if(board[row][i] == 1 && i != col){
            conflicts++;
        }
    }

    return conflicts;
}

int checkColumn(int board[N][N], int row, int col){
    int conflicts = 0;

    for(int i = 0; i < N; i++){
        if(board[i][col] == 1 && i != row){
            conflicts++;
        }
    }

    return conflicts;
}

int is_board_valid(vector<Individual> population, int individual) {
    int board[N][N];
    int conflicts = 0;

    //convert to 2D array
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            board[i][j] = population[individual].cromossome[i * N + j];
        }
    }
    
    //check diagonals
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            if(board[i][j] == 1){
                conflicts += checkDiagonals(board, i, j);
                conflicts += checkRow(board, i, j);
                conflicts += checkColumn(board, i, j);
            }
        }
    }
    
    return conflicts;
}

void printPopulation() {
    for(int i = 0; i < POPULATION; i++){
        for(int j = 0; j < TABLE; j++){
            cout << population[i].cromossome[j] << " ";
            if(j % N == N - 1){
                cout << endl;
            }
        }

        cout << endl;
        cout << "Fitness: " << population[i].fitnessScore << endl;
        cout << endl;
    }
}

void printBestIndividual() {

    cout << endl <<"Best individual:" << endl << endl;

    for(int i = 0; i < TABLE; i++){
        cout << population[0].cromossome[i] << " ";
        if(i % N == N - 1){
            cout << endl;
        }
    }

    cout << endl;
    cout << "Fitness: " << population[0].fitnessScore << endl;
    cout << endl;
}

void sortPopulation() {
    for (int i = 0; i < POPULATION; i++) {
        for (int j = i + 1; j < POPULATION; j++) {
            if (population[i].fitnessScore < population[j].fitnessScore) {
                Individual aux = population[i];
                population[i] = population[j];
                population[j] = aux;
            }
        }
    }
}

void sortNewPopulation() {
    for (int i = 0; i < POPULATION; i++) {
        for (int j = i + 1; j < POPULATION; j++) {
            if (newPopulation[i].fitnessScore < newPopulation[j].fitnessScore) {
                Individual aux = newPopulation[i];
                newPopulation[i] = newPopulation[j];
                newPopulation[j] = aux;
            }
        }
    }
}

void sortMutatePopulation() {
    for (int i = 0; i < POPULATION; i++) {
        for (int j = i + 1; j < POPULATION; j++) {
            if (mutatePopulation[i].fitnessScore < mutatePopulation[j].fitnessScore) {
                Individual aux = mutatePopulation[i];
                mutatePopulation[i] = mutatePopulation[j];
                mutatePopulation[j] = aux;
            }
        }
    }
}

double calculateDiversity(vector<Individual> population) {
    double soma = 0;

    for(int i = 0; i < TABLE; i++){
        int numZeros = 0;
        int numUns = 0;
        
        for(int j = 0; j < POPULATION; j++){
            population[j].cromossome[i] == 0 ? numZeros++ : numUns++;
        }

        double propZeros = double(numZeros) / POPULATION;
        double propOnes = double(numUns) / POPULATION;
        double diversity = 1 - pow(propZeros, 2) - pow(propOnes, 2);
        
        soma += diversity;
    }

    return soma / double(TABLE);
}

int fitness(int individual, vector<Individual> population) {
    int countQueens = 0;

    for (int i = 0; i < TABLE; i++) {
        if (population[individual].cromossome[i] == 1) {
            countQueens++;
        }
    }

    int conflicts = is_board_valid(population, individual);
    int fitness = countQueens < 8 || countQueens > 8 ? 0 : 28 - conflicts;

    return fitness;
}

void crossover(int mother, int father) {
    int cutPoint = rand() % N;

    Individual newIndividual = population[mother];

    for (int i = cutPoint; i < TABLE; i++) {
        if(CROSSOVER_RATE > rand() % 100){
            newIndividual.cromossome[i] = population[father].cromossome[i];
        }
    }

    newPopulation[currentNewPopulationCount] = newIndividual;
    newPopulation[currentNewPopulationCount].fitnessScore = fitness(currentNewPopulationCount, newPopulation);
    currentNewPopulationCount++;
}

void mutate(int individual) {
    Individual newIndividual = newPopulation[individual];

    for(int i = 0; i < TABLE; i++){
        if(rand() % 100 < 5){
            newIndividual.cromossome[i] = newIndividual.cromossome[i] == 1 ? 0 : 1;
        }
    }

    mutatePopulation[individual] = newIndividual;
    newPopulation[currentMutatePopulationCount].fitnessScore = fitness(individual, mutatePopulation);
    currentMutatePopulationCount++;
}

int rouletteSelecion() {
    int sum = 0;

    for(int i = 0; i < POPULATION; i++){
        sum += population[i].fitnessScore;
    }

    int random = rand() % sum;

    for(int i = 0; i < POPULATION; i++){
        if(random < population[i].fitnessScore){
            return i;
        }
        random -= population[i].fitnessScore;
    }

    return rand() % POPULATION;
}

void init() {
    for (int i = 0; i < POPULATION; i++) {
        for (int j = 0; j < N; j++) {
            int random = rand() % N;
            int index = j * N + random;
            population[i].cromossome[index] = 1;
        }
    }

    for (int i = 0; i < POPULATION; i++) {
        population[i].fitnessScore = fitness(i, population);
    }
}

int main() {
    srand(time(NULL));
    init();

    while(TOTAL_GENERATIONS > currentGeneration) {
        sortPopulation();
        if(population[0].fitnessScore == 28){
            break;
        }

        for(int i = 0; i < POPULATION; i++){
            crossover(rouletteSelecion(), rouletteSelecion());
        }

        for(int i = 0; i < POPULATION; i++){
            if(rand() % 100 < MUTATION_RATE * 100){
                mutate(i);
            } else {
                mutatePopulation[i] = newPopulation[i];
            }
        }

        currentMutatePopulationCount = 0;
        currentNewPopulationCount = 0;

        for(int i = 0; i < POPULATION; i++){
            newPopulation[i].fitnessScore = fitness(i, newPopulation);
            mutatePopulation[i].fitnessScore = fitness(i, mutatePopulation);
        }

        sortNewPopulation();
        sortPopulation();
        sortMutatePopulation();

        for(int i = 0; i < POPULATION; i++){
            if(i > 10 && i < 20) {
                population[i] = newPopulation[i-10];
            } else if(i >=20) {
                population[i] = mutatePopulation[i-20];
            }
        }
        
        double diversity = calculateDiversity(population);
        // Set mutation rate and crossover rate based on diversity target
         if(diversity < DIVERSITY_TARGET) {
            MUTATION_RATE += rand() % 10 * 0.01;
            CROSSOVER_RATE += rand() % 10 * 0.01;
        } else if(diversity > DIVERSITY_TARGET) {
            MUTATION_RATE -= rand() % 10 * 0.01;
            CROSSOVER_RATE -= rand() % 10 * 0.01;
        }

        // Get absolute value with abs
        MUTATION_RATE = fmod(abs(MUTATION_RATE), 1.0);
        CROSSOVER_RATE = fmod(abs(CROSSOVER_RATE), 1.0);

        currentGeneration++;
    }
    
    for(int i = 0; i < POPULATION; i++){
        population[i].fitnessScore = fitness(i, population);
    }

    sortPopulation();
    // printPopulation();
    printBestIndividual();

    cout << "Generation: " << currentGeneration << endl;
    cout << "Diversity: " << calculateDiversity(population) << endl;
    cout << "Mutation Rate: " << MUTATION_RATE << endl;
    cout << "Crossover Rate: " << CROSSOVER_RATE << endl;

    return 0;
}