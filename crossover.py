import random
from typing import Tuple, overload


@overload
def single_point_crossover(parent_1: float, parent_2: float) -> Tuple[float, float]:
    """
    Selects a random crossover point from within the parents' value range.
    Two children are spawned from the value of said crossover point.

    Args:
        parent_1 (float): _description_
        parent_2 (float): _description_

    Returns:
        Tuple[float, float]: _description_
    """
    # Select a crossover point
    point = random.uniform(min(parent_1, parent_2), max(parent_1, parent_2))
    # Generate children
    child1 = point
    child2 = point
    return child1, child2


def two_point_crossover(parent_1: float, parent_2: float) -> Tuple[float, float]:
    """
    Selects two random crossover points from within the parents' value range.
    Then creates the children by averaging the values of the parents between those two points.
    This function is written with the assumption that the parents are represented as a single continuous variable.

    Args:
        parent_1 (float): _description_
        parent_2 (float): _description_

    Returns:
        _type_: _description_
    """
    # Select two crossover points
    point1 = random.uniform(min(parent_1, parent_2), max(parent_1, parent_2))
    point2 = random.uniform(point1, max(parent_1, parent_2))

    # Generate children
    child1 = (parent_1 + point2) / 2
    child2 = (parent_2 + point1) / 2
    return child1, child2
