import random
from abc import ABC, abstractmethod


class BasePopulation(ABC):
    def __init__(self) -> list:
        self.population = []
        for _ in range(self.size()):
            individual = []
            for gene_type, min, max in self.gene_definition():
                if gene_type == int:
                    gene = random.randint(min, max)
                    individual.append(gene)
                elif gene_type == float:
                    gene = random.uniform(min, max)
                    individual.append(gene)
            self.population.append(individual)

    @property
    @abstractmethod
    def gene_definition(self) -> list:
        pass

    @abstractmethod
    def fitness(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass
