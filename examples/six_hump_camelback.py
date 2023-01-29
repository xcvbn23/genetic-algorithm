from genetic_algorithm import (
    REPLACEMENT_METHOD,
    CrossoverStrategies,
    GeneticAlgorithm,
)


class SixHumpCamelbackAlgorithm(GeneticAlgorithm):
    def crossover_strategy(self):
        return CrossoverStrategies.single_point

    def gene_definition(self):
        return [(float, -3, 3), (float, -2, 2)]

    def fitness_func(self, gene: list) -> float:
        x = gene
        return -(
            (4 - 2.1 * x[0] ** 2 + x[0] ** 4 / 3.0) * x[0] ** 2
            + x[0] * x[1]
            + (-4 + 4 * x[1] ** 2) * x[1] ** 2
        )

    def generations(self):
        return 500

    def mutation_rate(self) -> float:
        return 0.05

    def num_of_parents(self):
        return 10

    def population_size(self):
        return 100

    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.WEAK_PARENT


if __name__ == "__main__":
    genetic_algorithm = SixHumpCamelbackAlgorithm()
    genetic_algorithm.run()
