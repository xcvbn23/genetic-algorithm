import math

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from examples.wifi_coverage.utils import ITUP1238IndoorPropagationModel


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i: i + chunk_size]


class Plan:
    def __init__(self, chromosome: list, users: list, dimensions: tuple, max_sensors: int,
                 operating_frequency: float, router_antenna_gain: float, user_antenna_gain: float):
        self.max_sensors = max_sensors

        self.router_antenna_gain = router_antenna_gain
        self.user_antenna_gain = user_antenna_gain

        self.no_of_sensors = chromosome[0]

        sensors = chromosome[1:]
        sensors = list(split(sensors, 3))
        self.sensors = sensors[:self.no_of_sensors]

        self.targets = users

        self.w, self.h = dimensions

        self.propagation_model = ITUP1238IndoorPropagationModel(operating_frequency)

    def evaluate(self):
        connected = set()

        signal_qualities = []

        for target in self.targets:
            for sensor in self.sensors:
                sensor_range = sensor[0]
                sensor = sensor[1:]

                distance = math.dist(sensor, target)

                if distance <= sensor_range and target not in connected:
                    connected.add(target)
                    signal_qualities.append(distance)

        coverage = len(connected) / len(self.targets)
        signal_qualities = sum(signal_qualities) and 1 / sum(signal_qualities) or 0

        efficiency = self.max_sensors / self.no_of_sensors

        return 3 * coverage + 0.5 * signal_qualities + efficiency

    def plot(self, name: str = None):
        fig, ax = plt.subplots()
        ax.set_xlim([0, self.w])
        ax.set_ylim([0, self.h])
        ax.set_aspect('equal')

        label_scale = 3.5

        for target in self.targets:
            x, y = target
            ax.scatter(x, y, c="b")
            ax.annotate(
                f"user {(round(x, 2), round(y, 2))}",
                target,
                xytext=(x, y + 0.15 * label_scale),
                ha="center",
            )

        for sensor in self.sensors:
            range, x, y = sensor
            ax.scatter(x, y, c="r")
            circle = Circle((x, y), range, fill=False)
            ax.add_patch(circle)
            ax.annotate(
                f"router {(round(x, 2), round(y, 2))}",
                (x, y),
                xytext=(x, y + 1.15 * label_scale),
                ha="center",
            )

        plt.title("Plan")
        plt.xlabel("x coordinates in meters")
        plt.ylabel("y coordinates in meters")

        plt.savefig(name and name or "plan.png")


