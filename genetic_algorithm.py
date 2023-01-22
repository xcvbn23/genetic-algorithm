import random
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt


def single_point_crossover(gene_parent_1, gene_parent_2):
    crossover_point = random.randint(0, len(gene_parent_1))

    gene_child_1 = gene_parent_1[:crossover_point] + gene_parent_2[crossover_point:]
    gene_child_2 = gene_parent_2[:crossover_point] + gene_parent_1[crossover_point:]

    return gene_child_1, gene_child_2


def tournament_selection(population) -> tuple:
    winners = random.choices(population, k=5)

    winners = sorted(winners, key=lambda individual: individual[1], reverse=True)

    return winners[0], winners[1]


class GeneticAlgorithm(ABC):
    def __init__(self) -> list:
        self.individuals = []
        for _ in range(self.population_size()):
            gene = []
            for gene_type, min, max in self.gene_definition():
                if gene_type == int:
                    chromosome = random.randint(min, max)
                    gene.append(chromosome)
                elif gene_type == float:
                    chromosome = random.uniform(min, max)
                    gene.append(chromosome)
            fitness = 0
            self.individuals.append((gene, fitness))
            self.calculate_fitness()

    def calculate_fitness(self):
        for i, individual in enumerate(self.individuals):
            gene, fitness = individual
            fitness = self.fitness_func(gene)
            individual = gene, fitness
            self.individuals[i] = individual

    def run(self):
        total_fitness_per_generation = []
        for _ in range(1, self.generations() + 1):
            # Selection
            parents = self.perform_selection()
            # Crossover
            self.perform_crossover(parents)
            # Mutation
            self.perform_mutation()
            # Calculate fitness
            self.calculate_fitness()

            total_fitness = sum(map(lambda individual: individual[1], self.individuals))
            total_fitness_per_generation.append(total_fitness)

        x = range(1, self.generations() + 1)
        y = total_fitness_per_generation

        plt.plot(x, y)
        plt.title(
            f"Genetic Algorithm\nGenerations: {self.generations()},Population: {self.population_size()}"
        )
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.show()
        plt.savefig("plots/my_plot.png")
        plt.close()

    def perform_crossover(self, parents) -> None:
        for i in range(0, len(parents), 2):
            gene_parent_1 = self.individuals[i]
            gene_parent_1, _ = gene_parent_1

            gene_parent_2 = self.individuals[i + 1]
            gene_parent_2, _ = gene_parent_2

            gene_child_1, gene_child_2 = single_point_crossover(
                gene_parent_1, gene_parent_2
            )

            self.individuals[i] = gene_child_1, 0
            self.individuals[i] = gene_child_2, 0

    def perform_mutation(self):
        for i in range(0, self.population_size()):
            gene, _ = self.individuals[i]
            for i, chromosome in enumerate(gene):
                mutation_rate = 0.25
                mutation_chance = random.random()
                if mutation_chance > mutation_rate:
                    continue

                gene_type, _, _ = self.gene_definition()[i]
                if gene_type == int:
                    chromosome += random.randint(-1, 1)
                elif gene_type == float:
                    chromosome += random.uniform(-1, 1)

                gene[i] = chromosome
            self.individuals[i] = gene, 0

    def perform_selection(self):
        parents = []

        for _ in range(0, self.num_of_parents(), 2):
            parent_1, parent_2 = tournament_selection(self.individuals)
            parents.append(parent_1)
            parents.append(parent_2)

        return parents

    @property
    @abstractmethod
    def generations(self):
        pass

    @property
    @abstractmethod
    def gene_definition(self) -> list:
        pass

    @property
    @abstractmethod
    def fitness_func(self, individual: tuple) -> float:
        pass

    @property
    @abstractmethod
    def num_of_parents(self) -> int:
        pass

    @property
    @abstractmethod
    def population_size(self) -> int:
        pass
