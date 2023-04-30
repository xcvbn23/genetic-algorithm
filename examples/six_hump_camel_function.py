from genetic_algorithm import GeneticAlgorithm, SelectionMethods, ReplacementMethod


class SixHumpCamelGeneticAlgorithm(GeneticAlgorithm):
    """
    Minimise z within the boundaries of x and y
    https://www.sfu.ca/~ssurjano/camel6.html
    """
    generations = 100
    # x, y
    gene_space = [(float, -3, 3), (float, -2, 2)]
    mutation_rate = 0.05
    num_of_parents = 10
    population_size = 100
    selection_method = SelectionMethods.tournament_selection
    replacement_method = ReplacementMethod.BOTH_PARENTS

    def fitness_func(self, chromosome: list) -> float:
        x = chromosome
        return - (
                (4 - 2.1 * x[0] ** 2 + x[0] ** 4 / 3.0) * x[0] ** 2
                + x[0] * x[1]
                + (-4 + 4 * x[1] ** 2) * x[1] ** 2
        )


if __name__ == '__main__':
    ga = SixHumpCamelGeneticAlgorithm()
    ga.run()
