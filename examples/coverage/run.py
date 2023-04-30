from examples.coverage.plan import Plan
from genetic_algorithm import GeneticAlgorithm, SelectionMethods, ReplacementMethod

# Problem Parameters
TARGETS = [(25, 25), (75, 75)]
MAX_SENSORS = 2
SENSOR_RANGE = 30
DIMENSIONS = 100, 100


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i: i + chunk_size]


def _gene_space() -> list:
    # sensor = range, x, y
    # gene = max_sensors, [sensor]
    definition = [(int, 1, MAX_SENSORS)]
    w, h = DIMENSIONS
    definition += MAX_SENSORS * [
        (int, 1, SENSOR_RANGE),
        (int, 0, w),
        (int, 0, h),
    ]
    return definition


class CoverageGeneticAlgorithm(GeneticAlgorithm):
    """
    Maximise target coverage
    Maximise quality of connections
    Minimise amount of cells
    """
    generations = 500
    mutation_rate = 0.25
    num_of_parents = 100
    population_size = 1000
    selection_method = SelectionMethods.tournament_selection
    replacement_method = ReplacementMethod.WEAK_PARENT
    gene_space = _gene_space()

    def fitness_func(self, chromosome: list) -> float:
        plan = Plan(chromosome, TARGETS, DIMENSIONS, MAX_SENSORS)
        return plan.evaluate()


if __name__ == '__main__':
    ga = CoverageGeneticAlgorithm()
    ga.run()

    best_individual = ga.population[0]

    _, chromosome, _ = best_individual
    plan = Plan(chromosome, TARGETS, DIMENSIONS, MAX_SENSORS)
    plan.plot()
