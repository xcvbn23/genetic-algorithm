from enum import Enum
import math
import random
from abc import ABC, abstractmethod
import time

import matplotlib.pyplot as plt


class REPLACEMENT_METHOD(Enum):
    RANDOM = 0
    WEAK_PARENT = 1
    BOTH_PARENTS = 2


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
        for idx in range(self.population_size()):
            gene = []
            for gene_type, min, max in self.gene_definition():
                if gene_type == int:
                    chromosome = random.randint(min, max)
                elif gene_type == float:
                    chromosome = random.uniform(min, max)
                gene.append(chromosome)
            fitness = 0
            self.individuals.append((idx, gene, fitness))
            self.calculate_fitness()

    def calculate_penalty(self, gene) -> int:
        for i, (_, min, max) in enumerate(self.gene_definition()):
            if gene[i] < min or gene[i] > max:
                return -math.inf

        return 0

    def calculate_fitness(self):
        for individual in self.individuals:
            idx, gene, fitness = individual
            fitness = self.fitness_func(gene)
            penalty = self.calculate_penalty(gene)
            individual = idx, gene, (fitness + penalty)
            self.individuals[idx] = individual

    def run(self):
        best_fitness_per_generation = []
        for n in range(1, self.generations() + 1):
            print("Generation", n)
            # Selection
            parents = self.perform_selection()
            # Crossover
            children = self.perform_crossover(parents)
            # Mutation
            children = self.perform_mutation(children)
            # Replacement
            self.perform_replacement(children, self.replacement_method())
            # Calculate fitness
            self.calculate_fitness()

            best_individual = sorted(
                self.individuals,
                key=lambda individual: individual[2],
                reverse=True,
            )[0]
            best_fitness = best_individual[2]
            best_fitness_per_generation.append(best_fitness)

        x = range(1, self.generations() + 1)
        y = best_fitness_per_generation

        plt.plot(x, y)
        plt.title(f"Genetic Algorithm")
        plt.xlabel("Generation")
        plt.ylabel("f(x)")
        plt.gcf().text(
            0.333,
            0.01,
            f"generations: {self.generations()}, population: {self.population_size()}, parents: {self.num_of_parents()}",
            fontsize=9,
        )
        plt.tight_layout()
        # plt.show()
        plt.savefig(f"plots/{int(time.time())}.png")
        plt.close()

        self.individuals.sort(key=lambda d: d[2], reverse=True)

        self.on_complete(self.individuals)

    def perform_crossover(self, parents: list) -> list:
        children = []
        for i in range(0, len(parents), 2):
            gene_parent_1 = self.individuals[i]
            idx_1, gene_parent_1, _ = gene_parent_1

            gene_parent_2 = self.individuals[i + 1]
            idx_2, gene_parent_2, _ = gene_parent_2

            gene_child_1, gene_child_2 = single_point_crossover(
                gene_parent_1, gene_parent_2
            )

            children.append((idx_1, gene_child_1, 0))
            children.append((idx_2, gene_child_2, 0))

        return children

    def perform_mutation(self, children: list) -> list:
        mutated_children = []
        for child in children:
            idx, gene, _ = child
            for i, chromosome in enumerate(gene):
                mutation_rate = 0.25
                mutation_chance = random.random()
                if mutation_chance > mutation_rate:
                    continue

                gene_type, min, max = self.gene_definition()[i]
                if gene_type == int:
                    mutated_chromosome = chromosome + random.randint(-1, 1)
                    while mutated_chromosome < min or mutated_chromosome > max:
                        mutated_chromosome = chromosome + random.randint(-1, 1)
                    chromosome = mutated_chromosome
                elif gene_type == float:
                    mutated_chromosome = chromosome + random.uniform(-1, 1)
                    while mutated_chromosome < min or mutated_chromosome > max:
                        mutated_chromosome = chromosome + random.uniform(-1, 1)
                    chromosome = mutated_chromosome

                gene[i] = chromosome
            mutated_children.append((idx, gene, 0))

        return mutated_children

    def perform_replacement(
        self, children: list, replacement: REPLACEMENT_METHOD
    ) -> None:
        if replacement == replacement.BOTH_PARENTS:
            for child in children:
                idx, _, _ = child
                self.individuals[idx] = child
        elif replacement == replacement.RANDOM:
            for child in children:
                random_position = random.randint(0, self.population_size() - 1)
                self.individuals[random_position] = child
        elif replacement == replacement.WEAK_PARENT:
            for child in children:
                idx, child_gene, _ = child
                _, _, parent_fitness = self.individuals[idx]

                child_fitness = self.fitness_func(child_gene) + self.calculate_penalty(
                    child_gene
                )
                if child_fitness > parent_fitness:
                    self.individuals[idx] = child

    def perform_selection(self) -> list:
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
    def mutation_rate(self) -> float:
        pass

    def on_complete(self, best_individuals: list) -> None:
        for individual in self.individuals[:10]:
            print(individual)
        print("Best individual", best_individuals[0])

    @property
    @abstractmethod
    def population_size(self) -> int:
        pass

    @property
    @abstractmethod
    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.RANDOM
