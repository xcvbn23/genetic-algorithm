import math
from shapely.geometry import LineString


def segment_intersect(line1, line2):
    line = LineString(line1)
    other = LineString(line2)
    return line.intersects(other)


def freespace_propagation_loss(distance: float, frequency: float):
    # frequency is frequency(Hz)
    # distance is meters(m)
    light_speed = 300000000.0  # m/s
    return 20 * math.log10((4.0 * math.pi * distance) / (light_speed / frequency))
