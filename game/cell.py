import random

from game.utils import get_random_from_bounds


class Cell:
    CELL_COLORS = (
        (64, 128, 255),
        (11, 88, 200),
        (100, 20, 100),
        (0, 200, 64),
        (225, 225, 0),
        (225, 0, 0),
        (230, 50, 230),
    )
    CELL_RANGE = (1, 5)

    def __init__(self, x: int, y: int, color, radius: int):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    @staticmethod
    def get_random_color():
        return random.sample((20, 255, random.randint(0, 255)), 3)

    @classmethod
    def random_cell(cls, bounds):
        return cls(
            *get_random_from_bounds(bounds),
            cls.get_random_color(),
            random.randrange(*cls.CELL_RANGE),
        )
