import math
import statistics

import matplotlib.pyplot as plt
from adjustText import adjust_text

from examples.wifi_coverage.utils import (
    ITUP1238IndoorPropagationModel,
    segment_intersect,
    split,
)


class WALL_TYPE:
    CONCRETE = 44.769
    DRY_WALL = 10.114
    LIME_BRICK = 7.799
    CHIP_BOARD = 0.838


class Plan:
    def __init__(
            self,
            chromosome: list,
            users: list,
            dimensions: tuple,
            max_sensors: int,
            operating_frequency: float,
            router_antenna_gain: float,
            user_antenna_gain: float,
            walls=None,
    ):
        self.max_routers = max_sensors

        self.router_antenna_gain = router_antenna_gain
        self.user_antenna_gain = user_antenna_gain

        self.no_of_sensors = chromosome[0]

        sensors = chromosome[1:]
        sensors = list(split(sensors, 3))
        self.routers = sensors[: self.no_of_sensors]

        self.users = users

        self.w, self.h = dimensions

        self.walls = walls or []

        self.propagation_model = ITUP1238IndoorPropagationModel(operating_frequency)

    def connect_users(self):
        connections = {}

        for user in self.users:
            for router in self.routers:
                rssi = self.determine_received_power(router, user)

                DESIRED_RSSI = -50
                if DESIRED_RSSI > rssi:
                    continue

                user_id = str(user)
                if user_id not in connections:
                    connections.update({user_id: [router, rssi]})
                else:
                    [_, preexisting_connection_rssi] = connections[user_id]
                    if rssi < preexisting_connection_rssi:
                        connections.update({user_id: [router, rssi]})

        return connections

    def evaluate(self):
        connections_registry = self.connect_users()

        coverage = len(connections_registry) / len(self.users)

        signal_qualities = []
        for [_, rssi] in connections_registry.values():
            signal_qualities.append(rssi)
        total_rssi = sum(signal_qualities) and 1 / sum(signal_qualities) or 0
        rssi_variance = (
            statistics.variance(signal_qualities) + 0.01
            if len(signal_qualities) >= 2
            else 1
        )
        effective_rssi = total_rssi / rssi_variance

        efficiency = self.max_routers / self.no_of_sensors

        return 3 * coverage - 0.5 * effective_rssi + efficiency

    def determine_received_power(self, router, user) -> float:
        transmit_power = router[0]
        router = router[1:]

        distance = math.dist(router, user)
        path_loss = self.propagation_model.run(distance)
        for wall in self.walls:
            point_1, point_2, wall_type = wall
            if segment_intersect([point_1, point_2], [router, user]):
                path_loss += wall_type
        received_power = (
                transmit_power
                + self.router_antenna_gain
                - path_loss
                + self.user_antenna_gain
        )
        return received_power

    def plot(self, name: str = None):
        fig, ax = plt.subplots()
        ax.set_xlim([0, self.w])
        ax.set_ylim([0, self.h])
        ax.set_aspect("equal")

        connected_registry = self.connect_users()

        texts = []
        for user_id, connections in connected_registry.items():
            router, rssi = connections
            user = user_id.strip("()")
            user = user.split(",")
            x, y = map(float, user)
            ax.scatter(x, y, c="b")
            texts.append(
                plt.text(
                    x,
                    y,
                    f"user {(round(x, 2), round(y, 2), round(rssi, 2))}",
                    ha="center",
                    va="center",
                )
            )

        for router in self.routers:
            range, x, y = router
            ax.scatter(x, y, c="r")
            texts.append(
                plt.text(
                    x,
                    y,
                    f"router {(round(x, 2), round(y, 2))}",
                    ha="center",
                )
            )

        adjust_text(texts)

        for wall in self.walls:
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

        plt.title("Plan", loc="left")
        plt.title(f"MAX_ROUTERS {self.max_routers}", loc="right")
        plt.xlabel("x coordinates in meters")
        plt.ylabel("y coordinates in meters")

        plt.savefig(name and name or "plan.png")


if __name__ == "__main__":
    plan = Plan(
        [
            1,
            10,
            12.500111390936478,
            2.5044413549436424,
            10,
            7.802416841537527,
            4.517764690467797,
        ],
        [(5, 2.5), (20, 2.5)],
        (30, 5),
        2,
        5.180,
        3,
        1,
        [[(15, 4), (15, 1), WALL_TYPE.CONCRETE]],
    )
    plan.evaluate()
    plan.plot("plot-analysis-1")
