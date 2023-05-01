import math


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
