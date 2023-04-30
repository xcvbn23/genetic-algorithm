import logging
import random
import uuid
from abc import abstractmethod, ABC
from enum import Enum, auto
from typing import Callable

import enlighten
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReplacementMethod(Enum):
    BOTH_PARENTS = auto()
    RANDOM = auto()
    WEAK_PARENT = auto()
    NO_REPLACEMENT = auto()


class CrossoverMethod:
    @staticmethod
    def single_point_crossover(parents: list, gene_space: list):
        children = []
        crossover_point = random.randint(0, len(gene_space) - 1)
        for i in range(0, len(parents), 2):
            _, parent1, _ = parents[i]
            _, parent2, _ = parents[i + 1]
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            children.append(child1)
            children.append(child2)
        return children


class SelectionMethods:
    @staticmethod
    def tournament_selection(cls, population: list, num_of_parents: int, **kwargs) -> list:
        parents = []
        for _ in range(0, num_of_parents, 2):
            # tournament_size is 20% of the population
            winners = random.choices(population, k=int(0.2 * len(population)))
            winners = sorted(
                winners, key=lambda individual: individual[2], reverse=True
            )
            parents.append(winners[0])
            parents.append(winners[1])

        return parents


class GeneticAlgorithm(ABC):
    population = []

    def __init__(self, *args, **kwargs):
        pass

    def _calculate_fitness(self):
        for i in range(len(self.population)):
            id, gene, fitness = self.population[i]
            fitness = self.fitness_func(gene)
            individual = id, gene, fitness
            self.population[i] = individual

    @abstractmethod
    def fitness_func(self, chromosome: list):
        pass

    @property
    @abstractmethod
    def gene_space(self) -> list:
        pass

    @abstractmethod
    def generations(self) -> int:
        pass

    def _initialise_population(self):
        logger.info("Initialising population of %d individuals", self.population_size)
        for idx in range(self.population_size):
            chromosome = []
            for gene_type, min, max in self.gene_space:
                if gene_type == int:
                    gene = random.randint(min, max)
                elif gene_type == float:
                    gene = random.uniform(min, max)
                chromosome.append(gene)
            self.population.append((str(uuid.uuid4()), chromosome, self.fitness_func(chromosome)))

    def perform_crossover(self, parents: list):
        children = CrossoverMethod.single_point_crossover(parents, self.gene_space)
        children = [(str(uuid.uuid4()), child, self.fitness_func(child)) for child in children]
        return children

    def perform_mutation(self, children) -> list:
        for i, child in enumerate(children):
            id, individual, fitness = children[i]
            for j, gene in enumerate(individual):
                if random.random() < self.mutation_rate:
                    continue

                gene_type, min, max = self.gene_space[j]
                if gene_type == int:
                    mutated_chromosome = gene + random.randint(-1, 1)
                    while mutated_chromosome < min or mutated_chromosome > max:
                        mutated_chromosome = gene + random.randint(-1, 1)
                    gene = mutated_chromosome
                elif gene_type == float:
                    mutated_chromosome = gene + random.uniform(-1, 1)
                    while mutated_chromosome < min or mutated_chromosome > max:
                        mutated_chromosome = gene + random.uniform(-1, 1)
                    gene = mutated_chromosome

                individual[j] = gene
            children[i] = (id, individual, self.fitness_func(individual))

        return children

    def perform_replacement(self, parents: list, children: list) -> None:
        # TODO O(n) use hash table to make it 0(1)?
        if ReplacementMethod.NO_REPLACEMENT:
            for child in children:
                self.population.append(child)
        elif ReplacementMethod.RANDOM:
            for child in children:
                random_position = random.randint(0, len(self.population) - 1)
                self.population[random_position] = child
        elif ReplacementMethod.BOTH_PARENTS:
            for parent in parents:
                parent_idx = self.population.index(parent)
                self.population[parent_idx] = children[parent_idx]
        elif ReplacementMethod.WEAK_PARENT:
            for child in children:
                for parent in parents:
                    _, child_fitness, _ = child
                    _, parent_fitness, _ = parent
                    if child_fitness >= parent_fitness:
                        parent_idx = self.population.index(parent)
                        self.population[parent_idx] = children[parent_idx]
                        continue

    def perform_selection(self) -> list:
        return self.selection_method(self.population, self.num_of_parents)

    @property
    @abstractmethod
    def mutation_rate(self) -> float:
        pass

    @property
    @abstractmethod
    def num_of_parents(self):
        pass

    @property
    @abstractmethod
    def population_size(self):
        pass

    @property
    @abstractmethod
    def replacement_method(self) -> ReplacementMethod:
        pass

    def run(self):
        fitness_graph = []

        self._initialise_population()

        pbar = enlighten.Counter(total=self.generations, desc='Basic', unit='ticks')
        for generation in range(self.generations):
            pbar.update()

            parents = self.perform_selection()
            children = self.perform_crossover(parents)
            children = self.perform_mutation(children)

            self.perform_replacement(parents, children)

            self._calculate_fitness()

            best_gene = sorted(
                self.population,
                key=lambda gene: gene[2],
                reverse=True,
            )[0]
            best_fitness = best_gene[2]
            fitness_graph.append([generation, best_fitness])

        self.population.sort(key=lambda d: d[2], reverse=True)

        for individual in self.population[:3]:
            logger.info("Best individual %s", individual)

        x_values = [row[0] for row in fitness_graph]
        y_values = [row[1] for row in fitness_graph]

        plt.plot(x_values, y_values)
        plt.xlabel("Generation")
        plt.ylabel("Fitness Value")

        plt.title("foo")
        plt.suptitle("f")

        plt.savefig('fitness-graph.png')

    @property
    @abstractmethod
    def selection_method(self) -> Callable:
        pass
