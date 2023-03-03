import math
import random
from shapely.geometry import LineString


def segment_intersect(line1, line2):
    line = LineString(line1)
    other = LineString(line2)
    return line.intersects(other)


def pseudo_norm(a, b):
    """Generate a value between [a, b] in a normal distribution with the Central Limit Theorem"""
    count = 10
    values = sum([random.randint(a, b) for x in range(count)])
    return round(values / count)


class PropagationModel:
    def __init__(self, frequency):
        self.frequency = frequency

    def plot_name(self):
        return f"{self.__class__.__name__}"

    def run(self, distance: float) -> float:
        # 2D distance between Tx and Rx (m)
        return 0.0


class FreeSpacePathLossModel(PropagationModel):
    def __init__(self, args):
        super().__init__(args)

    def run(self, distance: float) -> float:
        distance += 0.0001
        return (
            (20 * math.log10(distance))
            + (20 * math.log10(self.frequency * math.pow(10, 9)))
            - 147.55
        )  # (dB)


class LogDistancePathLossModel(FreeSpacePathLossModel):
    def __init__(self, args):
        super().__init__(args)
        self.path_loss_exponent = 2.03  # Path Loss Exponent
        self.mu = 0.00
        self.sigma = 2.00

    def plot_name(self):
        return f"{super().plot_name()},\u03B3={self.path_loss_exponent},\u03BC={self.mu},\u03C3={self.sigma}"

    def run(self, distance: float) -> float:
        distance += 0.0001
        reference_distance = 1  # (m)
        reference_distance_path_loss = super().run(reference_distance)
        path_loss = (
            reference_distance_path_loss
            + 10 * self.path_loss_exponent * math.log10(distance / reference_distance)
        )  # dB
        shadowing_effect = pseudo_norm(self.mu, self.sigma)  # dB
        path_loss += shadowing_effect
        return path_loss  # dB


class ITUP1238IndoorPropagationModel(FreeSpacePathLossModel):
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
