import math

from shapely import LineString


def segment_intersect(line1, line2):
    line = LineString(line1)
    other = LineString(line2)
    return line.intersects(other)


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i: i + chunk_size]


class PropagationModel:
    def __init__(self, frequency):
        self.frequency = frequency

    def plot_name(self):
        return f"{self.__class__.__name__}"

    def run(self, distance: float) -> float:
        # 2D distance between Tx and Rx (m)
        return 0.0


class ITUP1238IndoorPropagationModel(PropagationModel):
    def __init__(self, args):
        super().__init__(args)
        self.distance_power_loss_coefficient = 18.4
        self.floor_penetration_loss_factor = 0
        self.num_floors = 0

    def plot_name(self):
        return f"{super().plot_name()},N={self.distance_power_loss_coefficient},L_f={self.floor_penetration_loss_factor},f={self.num_floors} "

    def run(self, distance: float) -> float:
        distance += 0.0001

        alpha = 1.46
        beta = 34.62
        gamma = 2.03

        return (
                10 * alpha * math.log10(distance)
                + beta
                + 10 * gamma * math.log10(self.frequency)
        )
