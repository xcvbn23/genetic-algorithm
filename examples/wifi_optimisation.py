import math
import statistics
import sys
from datetime import datetime

import matplotlib.pyplot as plt

from examples.wifi_optimisation_utils import (
    ITUP1238IndoorPropagationModel,
    segment_intersect,
)
from genetic_algorithm import REPLACEMENT_METHOD, CrossoverStrategies, GeneticAlgorithm


operating_frequency = 5.180  # GHz
transmitter_power = 23  # dBm
transmitter_gain = 2  # dBi
receiver_gain = 1  # dBi

propagation_model = ITUP1238IndoorPropagationModel(operating_frequency)


class WALL_TYPE:
    CONCRETE = 44.769
    LIME_BRICK = 7.799
    DRY_WALL = 10.114
    CHIP_BOARD = 0.838


w, h = 20, 10
users = [(3, 3), (16, 3), (3, 9), (6, 9), (11, 9), (13, 9), (18, 9)]
walls = [
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
# routers = [(3.07, 4.65), (17.3, 6.47)]
routers = []
max_routers = 2


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i : i + chunk_size]


class WifiOptimisationGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self) -> list:
        super().__init__()

    def crossover_strategy(self):
        return CrossoverStrategies.single_point

    def gene_definition(self):
        definition = [(int, 1, max_routers)]
        definition += max_routers * [
            (float, 0, w),
            (float, 0, h),
        ]
        return definition

    def determine_received_power(self, router, user) -> float:
        distance = math.dist(user, router)
        path_loss = propagation_model.run(distance)
        for wall in walls:
            point_1, point_2, wall_type = wall
            if segment_intersect([point_1, point_2], [router, user]):
                path_loss += wall_type

        return transmitter_power + transmitter_gain - path_loss + receiver_gain

    def fitness_func(self, gene: list) -> float:
        received_powers = []
        no_of_routers = gene[0]
        routers = gene[1:]
        routers = list(split(routers, 2))
        routers = routers[: 2 * no_of_routers]
        for router in routers:
            for user in users:
                received_power = self.determine_received_power(router, user)
                if received_power < -65:
                    return -999
                received_powers.append(received_power)

        total_received_power = sum(received_powers)
        received_power_variance = statistics.variance(received_powers)

        return -received_power_variance + total_received_power

    def generations(self):
        return 300

    def mutation_rate(self) -> float:
        return 0.05

    def num_of_parents(self):
        return 10

    def on_complete(self, best_individuals: list) -> None:
        super().on_complete(best_individuals)
        _, best_gene, _ = best_individuals[0]
        no_of_routers = best_gene[0]
        routers = best_gene[1:]
        routers = list(split(routers, 2))
        routers = routers[: 2 * no_of_routers]
        for router in routers:
            for user in users:
                print(
                    "router",
                    router,
                    "user",
                    user,
                    "P_Rx",
                    self.determine_received_power(router, user),
                )
        self.plot(users, walls, routers)

    def population_size(self):
        return 100

    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.WEAK_PARENT

    def plot(self, users: list, walls: list, routers: list):
        now = datetime.now()

        fig, ax = plt.subplots()
        ax.set_xlim([0, w])
        ax.set_ylim([0, h])

        for user_location in users:
            x, y = user_location
            ax.scatter(x, y, c="b")
            ax.annotate(
                f"user {(round(x, 2), round(y, 2))}",
                user_location,
                xytext=(x, y + 0.15),
                ha="center",
            )

        for router_location in routers:
            x, y = router_location
            ax.scatter(*router_location, c="r")
            ax.annotate(
                f"router {(round(x, 2), round(y, 2))}",
                router_location,
                xytext=(x, y + 1.15),
                ha="center",
            )

        for wall in walls:
            point1, point2, wall_type = wall

            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]

            if wall_type == WALL_TYPE.CONCRETE:
                wall_type = "r-"
            elif wall_type == WALL_TYPE.DRY_WALL:
                wall_type = "b-"
            elif wall_type == WALL_TYPE.CHIP_BOARD:
                wall_type = "g-"
            else:
                wall_type = "o-"
            ax.plot(x_values, y_values, wall_type)

        timestamp = now.strftime("%Y%m%d%H%M%S")

        plt.savefig(f"./examples/wifi_optimisation_screenshots/{timestamp}.png")


if __name__ == "__main__":
    genetic_algorithm = WifiOptimisationGeneticAlgorithm()
    options = sys.argv[1:]
    if len(options) > 0:
        genetic_algorithm.plot(users, walls, routers)
    else:
        genetic_algorithm.run()
