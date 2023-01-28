from genetic_algorithm import (
    REPLACEMENT_METHOD,
    CrossoverStrategies,
    GeneticAlgorithm,
)


class MaximiseSumGeneticAlgorithm(GeneticAlgorithm):
    def crossover_strategy(self):
        return CrossoverStrategies.single_point

    def gene_definition(self):
        return [(int, 0, 1), (int, -5, 10), (float, 10.5, 75.5)]

    def fitness_func(self, gene: list) -> float:
        return sum(gene)

    def generations(self):
        return 500

    def mutation_rate(self) -> float:
        return 0.05

    def num_of_parents(self):
        return 2

    def population_size(self):
        return 10

    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.WEAK_PARENT


if __name__ == "__main__":
    genetic_algorithm = MaximiseSumGeneticAlgorithm()
    genetic_algorithm.run()
