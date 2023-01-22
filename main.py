from genetic_algorithm import GeneticAlgorithm


class MyGeneticAlgorithm(GeneticAlgorithm):
    def gene_definition(self):
        return [(int, 0, 1), (int, -5, 10), (float, 10.5, 75.5)]

    def fitness_func(self, gene: tuple) -> float:
        return sum(gene)

    def generations(self):
        return 100

    def num_of_parents(self):
        return 2

    def population_size(self):
        return 10


if __name__ == "__main__":
    genetic_algorithm = MyGeneticAlgorithm()
    genetic_algorithm.run()
