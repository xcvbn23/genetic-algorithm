import random
from typing import Tuple

from crossover import single_point_crossover, two_point_crossover
from population import BasePopulation


class MyIndividual(BasePopulation):
    def __init__(self, gene):
        self._gene = gene

    @property
    def gene_definition(self):
        return ["int", "int", "int"]

    def fitness(self):
        return sum(self._gene)


# Fitness function to optimize
def fitness(x):
    return x**2


# Selection function
def selection(population, fitnesses):
    # Select parents using roulette wheel selection
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, individual in enumerate(population):
        current += fitnesses[i]
        if current > pick:
            return individual


# Genetic algorithm
def genetic_algorithm(
    population_size: int,
    mutation_rate: float,
    crossover_strategy: str,
    selection_strategy: str,
):
    """_summary_

    Args:
        population_size (_type_): _description_
        mutation_rate (_type_): _description_
        crossover_strategy (_type_): _description_
        selection_strategy (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    # Initialize population
    population = [random.uniform(-10, 10) for _ in range(population_size)]

    for generation in range(100):
        # Evaluate fitness
        fitnesses = [fitness(individual) for individual in population]
        # Select parents
        parents = [selection(population, fitnesses) for _ in range(population_size)]
        # Perform crossover
        children = []
        if crossover_strategy == "single_point":
            # Single point crossover
            for i in range(0, population_size, 2):
                child1, child2 = single_point_crossover(parents[i], parents[i + 1])
                children.append(child1)
                children.append(child2)
        elif crossover_strategy == "two_point":
            # Two point crossover
            for i in range(0, population_size, 2):
                child1, child2 = two_point_crossover(parents[i], parents[i + 1])
                children.append(child1)
                children.append(child2)
        else:
            raise ValueError("Invalid crossover strategy")
        # Perform mutation
        for i in range(len(children)):
            if random.uniform(0, 1) < mutation_rate:
                children[i] += random.gauss(0, 0.1)
        # Select survivors
        if selection_strategy == "elitist":
            # Elitist selection
            population = sorted(population + children, key=fitness, reverse=True)[
                :population_size
            ]
        elif selection_strategy == "roulette_wheel":
            # Roulette wheel selection
            population = [
                selection(population + children, fitnesses)
                for _ in range(population_size)
            ]
        else:
            raise ValueError("Invalid selection strategy")
    best_individual = population[0]
    best_fitness = fitness(best_individual)
    return best_individual, best_fitness


# Example usage:
if __name__ == "__main__":
    best_individual, best_fitness = genetic_algorithm(
        100, 0.1, "single_point", "elitist"
    )
    print(best_individual, best_fitness)
