import random

import pytest

from genetic_algorithm import GeneticAlgorithm


@pytest.fixture
def genetic_algorithm(random_seed):
    class MyGeneticAlgorithm(GeneticAlgorithm):
        def gene_definition(self):
            return [(int, 0, 1), (int, -5, 10), (float, 10.5, 75.5)]

        def fitness_func(self, gene: tuple) -> float:
            return sum(gene)

        def generations(self):
            return 10

        def num_of_parents(self):
            return 2

        def population_size(self):
            return 10

    genetic_algorithm = MyGeneticAlgorithm()
    yield genetic_algorithm


class TestGeneticAlgorithm:
    def test_initialise_population(self, genetic_algorithm):
        assert len(genetic_algorithm.individuals) == 10
        assert genetic_algorithm.individuals == [
            ([0, -5, 58.70078248438914], 53.70078248438914),
            ([0, 2, 19.569965354134354], 21.569965354134354),
            ([0, -3, 48.88201330918758], 45.88201330918758),
            ([0, -5, 16.59019059100351], 11.590190591003509),
            ([0, -5, 46.98092909100984], 41.98092909100984),
            ([1, 2, 39.698588008450486], 42.698588008450486),
            ([1, -5, 59.822478863434874], 55.822478863434874),
            ([0, 8, 32.61628357366947], 40.61628357366947),
            ([0, 1, 72.71884969344077], 73.71884969344077),
            ([1, -2, 16.528479819709613], 15.528479819709613),
        ]

    def test_run(self, genetic_algorithm):
        genetic_algorithm.run()
        assert genetic_algorithm.individuals[0] == (
            [1, -4, 58.17889313665809],
            55.17889313665809,
        )
