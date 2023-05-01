import math
import statistics

import matplotlib.pyplot as plt

from examples.wifi_coverage.utils import ITUP1238IndoorPropagationModel


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i: i + chunk_size]


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

        label_scale = 3.5

        connected_registry = self.connect_users()
        for user_id, connections in connected_registry.items():
            router, rssi = connections
            user = user_id.strip('()')
            user = user.split(',')
            x, y = map(float, user)
            ax.scatter(x, y, c="b")
            ax.annotate(
                f"user {(round(x, 2), round(y, 2), round(rssi, 2))}",
                (x, y),
                xytext=(x, y + 0.15 * label_scale),
                ha="center",
            )

        for router in self.routers:
            range, x, y = router
            ax.scatter(x, y, c="r")
            ax.annotate(
                f"router {(round(x, 2), round(y, 2))}",
                (x, y),
                xytext=(x, y + - 0.5 * label_scale),
                ha="center",
            )

        plt.title("Plan", loc="left")
        plt.title(f"MAX_ROUTERS {self.max_routers}", loc="right")
        plt.xlabel("x coordinates in meters")
        plt.ylabel("y coordinates in meters")

        plt.savefig(name and name or "plan.png")
