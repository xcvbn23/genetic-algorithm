from examples.wifi_coverage.plan import Plan, WALL_TYPE
from genetic_algorithm import GeneticAlgorithm, SelectionMethods, ReplacementMethod

# # # Scenario 1.1
# # Problem Parameters
# TARGETS = [(5, 2.5), (20, 2.5)]
# # Transceiver Configuration
# MAX_TRANSCEIVERS = 2
# MAX_TRANSCEIVER_POWER = 3  # dBm
# TRANSCEIVER_ANTENNA_GAIN = 3  # dBi
# USER_DEVICE_ANTENNA_GAIN = 1  # dBi
# DESIRED_RECEIVED_POWER = -50
# DIMENSIONS = 30, 5  # m
# OPERATING_FREQUENCY = 5.180  # GHz
# WALLS = []


# # # Scenario 1.2
# # Problem Parameters
# TARGETS = [(5, 2.5), (20, 2.5)]
# # Transceiver Configuration
# MAX_TRANSCEIVERS = 2
# MAX_TRANSCEIVER_POWER = 10  # dBm
# TRANSCEIVER_ANTENNA_GAIN = 3  # dBi
# USER_DEVICE_ANTENNA_GAIN = 1  # dBi
# DESIRED_RECEIVED_POWER = -50
# DIMENSIONS = 30, 5
# OPERATING_FREQUENCY = 5.180
# WALLS = []


# # # Scenario 1.3
# # Problem Parameters
# TARGETS = [(5, 2.5), (20, 2.5)]
# # Transceiver Configuration
# MAX_TRANSCEIVERS = 2
# MAX_TRANSCEIVER_POWER = 10  # dBm
# TRANSCEIVER_ANTENNA_GAIN = 3  # dBi
# USER_DEVICE_ANTENNA_GAIN = 1  # dBi
# DESIRED_RECEIVED_POWER = -50
# DIMENSIONS = 30, 5
# OPERATING_FREQUENCY = 5.180
# WALLS = [[(15, 4), (15, 1), WALL_TYPE.CONCRETE]]


# # # Scenario 2.1
# # Problem Parameters
# TARGETS = [(3, 6), (7, 1)]
# # Transceiver Configuration
# MAX_TRANSCEIVERS = 2
# MAX_TRANSCEIVER_POWER = 10  # dBm
# TRANSCEIVER_ANTENNA_GAIN = 3  # dBi
# USER_DEVICE_ANTENNA_GAIN = 1  # dBi
# DESIRED_RECEIVED_POWER = -50
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


# # # Scenario 2.2
# # Problem Parameters
# TARGETS = [(3, 6), (7, 1)]
# # Transceiver Configuration
# MAX_TRANSCEIVERS = 2
# MAX_TRANSCEIVER_POWER = 20  # dBm
# TRANSCEIVER_ANTENNA_GAIN = 3  # dBi
# USER_DEVICE_ANTENNA_GAIN = 1  # dBi
# DESIRED_RECEIVED_POWER = -50
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


# # Scenario 3
# Problem Parameters
TARGETS = [(3, 3), (16, 3), (3, 9), (6, 9), (11, 9), (13, 9), (18, 9)]
# Transceiver Configuration
MAX_TRANSCEIVERS = 2
MAX_TRANSCEIVER_POWER = 20  # dBm
TRANSCEIVER_ANTENNA_GAIN = 3  # dBi
USER_DEVICE_ANTENNA_GAIN = 1  # dBi
DESIRED_RECEIVED_POWER = -50
DIMENSIONS = 20, 10
OPERATING_FREQUENCY = 5.180
WALLS = [
    [(5, 1), (5, 6), WALL_TYPE.CHIP_BOARD],
    [(10, 1), (10, 6), WALL_TYPE.CHIP_BOARD],
    [(15, 1), (15, 6), WALL_TYPE.CHIP_BOARD],
    [(2, 8), (2, 10), WALL_TYPE.DRY_WALL],
    [(2, 8), (3, 8), WALL_TYPE.CHIP_BOARD],
    [(3, 8), (4, 8), WALL_TYPE.DRY_WALL],
    [(4, 8), (4, 10), WALL_TYPE.DRY_WALL],
    [(4, 8), (5, 8), WALL_TYPE.CHIP_BOARD],
    [(5, 8), (7, 8), WALL_TYPE.DRY_WALL],
    [(7, 8), (7, 10), WALL_TYPE.DRY_WALL],
    [(10, 8), (10, 10), WALL_TYPE.DRY_WALL],
    [(10, 8), (11, 8), WALL_TYPE.CHIP_BOARD],
    [(11, 8), (15, 8), WALL_TYPE.DRY_WALL],
    [(12, 8), (13, 8), WALL_TYPE.CHIP_BOARD],
    [(13, 8), (15, 8), WALL_TYPE.DRY_WALL],
    [(12, 8), (12, 10), WALL_TYPE.DRY_WALL],
    [(15, 8), (15, 10), WALL_TYPE.DRY_WALL],
    [(15, 8), (16, 8), WALL_TYPE.CHIP_BOARD],
    [(16, 8), (20, 8), WALL_TYPE.DRY_WALL],
    [(4, 4), (6, 4), WALL_TYPE.CHIP_BOARD],
    [(14, 4), (16, 4), WALL_TYPE.CHIP_BOARD],
]


def _gene_space() -> list:
    # router = range, x, y
    # gene = max_routers, [router]
    definition = [(int, 1, MAX_TRANSCEIVERS)]
    w, h = DIMENSIONS
    definition += MAX_TRANSCEIVERS * [
        (int, 1, MAX_TRANSCEIVER_POWER),
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
    num_of_parents = 40
    population_size = 100
    selection_method = SelectionMethods.tournament_selection
    replacement_method = ReplacementMethod.WEAK_INDIVIDUALS
    gene_space = _gene_space()

    def fitness_func(self, chromosome: list) -> float:
        plan = Plan(
            chromosome,
            TARGETS,
            DIMENSIONS,
            MAX_TRANSCEIVERS,
            OPERATING_FREQUENCY,
            TRANSCEIVER_ANTENNA_GAIN,
            USER_DEVICE_ANTENNA_GAIN,
            DESIRED_RECEIVED_POWER,
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
        MAX_TRANSCEIVERS,
        OPERATING_FREQUENCY,
        TRANSCEIVER_ANTENNA_GAIN,
        USER_DEVICE_ANTENNA_GAIN,
        DESIRED_RECEIVED_POWER,
        WALLS,
    )
    plan.plot()
