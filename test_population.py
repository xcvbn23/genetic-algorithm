import random
from population import BasePopulation

random.seed(42)


class Population(BasePopulation):
    def gene_definition(self):
        return [(int, 0, 1), (int, -5, 10), (float, 10.5, 75.5)]

    def fitness(self):
        return super().fitness()

    def size(self):
        return 3


class TestPopulation:
    def test_initialise_population(self):
        population = Population()
        assert len(population.population) == 3

        assert population.population == [
            [0, -5, 58.70078248438914],
            [0, 2, 19.569965354134354],
            [0, -3, 48.88201330918758],
        ]
