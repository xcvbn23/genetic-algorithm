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

users = [(10, 50), (90, 50)]
walls = []

operating_frequency = 5.180  # GHz
transmitter_power = 23  # dBm
transmitter_gain = 3.5  # dBi
receiver_gain = 1  # dBi

propagation_model = ITUP1238IndoorPropagationModel(operating_frequency)


w, h = 30, 5
users = [(5, 2.5), (20, 2.5)]
walls = []
routers = []


class WifiOptimisationGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self) -> list:
        super().__init__()

    def crossover_strategy(self):
        return CrossoverStrategies.single_point

    def gene_definition(self):
        max_routers = 1
        definition = [(int, max_routers, max_routers)]
        definition += max_routers * [
            (float, 0, w),
            (float, 0, h),
        ]
        return definition

    def determine_received_power(self, router, user) -> float:
        distance = math.dist(user, router)
        path_loss = propagation_model.run(distance)
        for wall in walls:
            if segment_intersect(wall, [router, user]):
                path_loss += 3

        return transmitter_power + transmitter_gain - path_loss + receiver_gain

    def fitness_func(self, gene: list) -> float:
        received_powers = []
        router = gene[1:]

        for user in users:
            received_power = self.determine_received_power(router, user)
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
        [_, router_x, router_y] = best_gene
        for user in users:
            print(
                "user",
                user,
                "P_Rx",
                self.determine_received_power((router_x, router_y), user),
            )
        self.plot(users, walls, [(router_x, router_y)])

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
                xytext=(x, y + 0.15),
                ha="center",
            )

        for wall in walls:
            x, y = wall
            ax.plot(x, y, "r-")

        # for user in users:
        #     for wall in walls:
        #         for router in routers:
        #             x, y = router
        #             router_user = [(round(x), round(y)), user]
        #             pygame.draw.line(win, RED, *router_user)

        timestamp = now.strftime("%Y%m%d%H%M%S")

        plt.savefig(f"./examples/wifi_optimisation_screenshots/{timestamp}.png")


if __name__ == "__main__":
    genetic_algorithm = WifiOptimisationGeneticAlgorithm()
    options = sys.argv[1:]
    if len(options) > 0:
        genetic_algorithm.plot(users, walls, routers)
    else:
        genetic_algorithm.run()
