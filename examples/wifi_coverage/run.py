from examples.wifi_coverage.plan import Plan
from genetic_algorithm import GeneticAlgorithm, SelectionMethods, ReplacementMethod

# # Scenario 1.1
# Problem Parameters
TARGETS = [(5, 2.5), (20, 2.5)]
# Router Configuration
MAX_ROUTERS = 2
MAX_ROUTER_POWER = 3  # dBm
ROUTER_ANTENNA_GAIN = 3  # dBi
USER_ANTENNA_GAIN = 1  # dBi
DIMENSIONS = 30, 5
OPERATING_FREQUENCY = 5.180


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i: i + chunk_size]


def _gene_space() -> list:
    # router = range, x, y
    # gene = max_routers, [router]
    definition = [(int, 1, MAX_ROUTERS)]
    w, h = DIMENSIONS
    definition += MAX_ROUTERS * [
        (int, 1, MAX_ROUTER_POWER),
        (float, 0, w),
        (float, 0, h),
    ]
    return definition


class WiFiCoverageGeneticAlgorithm(GeneticAlgorithm):
    """
    Maximise target coverage
    Maximise quality of connections
    Minimise amount of cells
    """

    generations = 100
    mutation_rate = 0.25
    num_of_parents = 100
    population_size = 1000
    selection_method = SelectionMethods.tournament_selection
    replacement_method = ReplacementMethod.NO_REPLACEMENT
    gene_space = _gene_space()

    def fitness_func(self, chromosome: list) -> float:
        plan = Plan(
            chromosome,
            TARGETS,
            DIMENSIONS,
            MAX_ROUTERS,
            OPERATING_FREQUENCY,
            ROUTER_ANTENNA_GAIN,
            USER_ANTENNA_GAIN,
        )
        return plan.evaluate()


if __name__ == "__main__":
    ga = WiFiCoverageGeneticAlgorithm()
    ga.run()

    best_individual = ga.population[0]

    _, chromosome, _ = best_individual
    plan = Plan(
        chromosome,
        TARGETS,
        DIMENSIONS,
        MAX_ROUTERS,
        OPERATING_FREQUENCY,
        ROUTER_ANTENNA_GAIN,
        USER_ANTENNA_GAIN,
    )
    plan.plot()
