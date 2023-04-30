import math

import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i: i + chunk_size]


class Plan:
    def __init__(self, chromosome: list, targets: list, dimensions: tuple, max_sensors: int):
        self.max_sensors = max_sensors

        self.no_of_sensors = chromosome[0]

        sensors = chromosome[1:]
        sensors = list(split(sensors, 3))
        self.sensors = sensors[:self.no_of_sensors]

        self.targets = targets

        self.w, self.h = dimensions

    def evaluate(self):
        connected = set()

        signal_qualities = []

        for target in self.targets:
            for sensor in self.sensors:
                sensor_range = sensor[0]
                sensor = sensor[1:]

                signal_quality = math.dist(sensor, target)

                if signal_quality <= sensor_range and target not in connected:
                    connected.add(target)
                    signal_qualities.append(signal_quality)

        coverage = len(connected) / len(self.targets)
        signal_qualities = sum(signal_qualities) and 1 / sum(signal_qualities) or 0

        efficiency = self.max_sensors / self.no_of_sensors

        return 3 * coverage + 0.5 * signal_qualities + efficiency

    def plot(self, name: str = None):
        fig, ax = plt.subplots()
        ax.set_xlim([0, self.w])
        ax.set_ylim([0, self.h])
        ax.set_aspect('equal')

        for target in self.targets:
            x, y = target
            ax.scatter(x, y, c="b")
            ax.annotate(
                f"user {(round(x, 2), round(y, 2))}",
                target,
                xytext=(x, y + 0.15),
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
                xytext=(x, y + 1.15),
                ha="center",
            )

        plt.title("Plan")
        plt.xlabel("x coordinates in meters")
        plt.ylabel("y coordinates in meters")

        plt.savefig(name and name or "plan.png")


