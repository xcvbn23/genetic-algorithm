from examples.wifi_coverage.plan import Plan, WALL_TYPE
from genetic_algorithm import GeneticAlgorithm, SelectionMethods, ReplacementMethod

# # # Scenario 1.1
# # Problem Parameters
# TARGETS = [(5, 2.5), (20, 2.5)]
# # Router Configuration
# MAX_ROUTERS = 2
# MAX_ROUTER_POWER = 3  # dBm
# ROUTER_ANTENNA_GAIN = 3  # dBi
# USER_ANTENNA_GAIN = 1  # dBi
# DIMENSIONS = 30, 5
# OPERATING_FREQUENCY = 5.180

# # # Scenario 1.2
# # Problem Parameters
# TARGETS = [(5, 2.5), (20, 2.5)]
# # Router Configuration
# MAX_ROUTERS = 2
# MAX_ROUTER_POWER = 10  # dBm
# ROUTER_ANTENNA_GAIN = 3  # dBi
# USER_ANTENNA_GAIN = 1  # dBi
# DIMENSIONS = 30, 5
# OPERATING_FREQUENCY = 5.180

# # # Scenario 1.3
# # Problem Parameters
# TARGETS = [(5, 2.5), (20, 2.5)]
# # Router Configuration
# MAX_ROUTERS = 2
# MAX_ROUTER_POWER = 10  # dBm
# ROUTER_ANTENNA_GAIN = 3  # dBi
# USER_ANTENNA_GAIN = 1  # dBi
# DIMENSIONS = 30, 5
# OPERATING_FREQUENCY = 5.180
# WALLS = [[(15, 4), (15, 1), WALL_TYPE.CONCRETE]]

# # # Scenario 2.1
# # Problem Parameters
# TARGETS = [(3, 6), (7, 1)]
# # Router Configuration
# MAX_ROUTERS = 2
# MAX_ROUTER_POWER = 10  # dBm
# ROUTER_ANTENNA_GAIN = 3  # dBi
# USER_ANTENNA_GAIN = 1  # dBi
# DIMENSIONS = 8, 7
# OPERATING_FREQUENCY = 5.180
# WALLS = [
#     [(1, 5), (2, 5), WALL_TYPE.CHIP_BOARD],
#     [(0, 5), (1, 5), WALL_TYPE.CONCRETE],
#     #
#     [(3, 4), (6, 4), WALL_TYPE.CONCRETE],
#     [(2, 4), (3, 4), WALL_TYPE.CHIP_BOARD],
#     #
#     [(3, 4), (6, 4), WALL_TYPE.CONCRETE],
#     [(6, 4), (6, 7), WALL_TYPE.CONCRETE],
#     [(2, 4), (2, 7), WALL_TYPE.CONCRETE],
#     #
#     [(5, 0), (5, 3), WALL_TYPE.DRY_WALL],
#     [(2, 0), (2, 3), WALL_TYPE.DRY_WALL],
# ]


# # Scenario 2.2
# Problem Parameters
TARGETS = [(3, 6), (7, 1)]
# Router Configuration
MAX_ROUTERS = 2
MAX_ROUTER_POWER = 20  # dBm
ROUTER_ANTENNA_GAIN = 3  # dBi
USER_ANTENNA_GAIN = 1  # dBi
DIMENSIONS = 8, 7
OPERATING_FREQUENCY = 5.180
WALLS = [
    [(1, 5), (2, 5), WALL_TYPE.CHIP_BOARD],
    [(0, 5), (1, 5), WALL_TYPE.CONCRETE],
    #
    [(3, 4), (6, 4), WALL_TYPE.CONCRETE],
    [(2, 4), (3, 4), WALL_TYPE.CHIP_BOARD],
    #
    [(3, 4), (6, 4), WALL_TYPE.CONCRETE],
    [(6, 4), (6, 7), WALL_TYPE.CONCRETE],
    [(2, 4), (2, 7), WALL_TYPE.CONCRETE],
    #
    [(5, 0), (5, 3), WALL_TYPE.DRY_WALL],
    [(2, 0), (2, 3), WALL_TYPE.DRY_WALL],
]


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

    generations = 250
    mutation_rate = 0.25
    num_of_parents = 20
    population_size = 100
    selection_method = SelectionMethods.tournament_selection
    replacement_method = ReplacementMethod.WEAK_PARENT
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
            WALLS,
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
        WALLS,
    )
    plan.plot()
