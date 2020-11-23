import math
import random


def is_dot_in_radius(x: int, y: int, circle_x: int, circle_y: int, radius: int) -> bool:
    return math.sqrt((x - circle_x) ** 2 + (y - circle_y) ** 2) < radius


def get_random_from_bounds(bounds):
    return random.randint(-bounds[0] + 1, bounds[1] - 1), random.randint(-bounds[0] + 1, bounds[1] - 1)
