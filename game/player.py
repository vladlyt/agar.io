import random
import uuid

from game.utils import is_dot_in_radius, get_random_from_bounds


class Player:
    INITIAL_RADIUS = 10
    PLAYER_COLORS = (
        (64, 128, 255),
        (11, 88, 200),
        (100, 20, 100),
        (0, 200, 64),
        (225, 225, 0),
        (225, 0, 0),
        (230, 50, 230),
    )

    def __init__(self, name, x, y, color, radius=INITIAL_RADIUS):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def can_eat_food(self, cell):
        return is_dot_in_radius(cell.x, cell.y, self.x, self.y, self.radius)

    def can_eat_player(self, player):
        return self.radius > player.radius and is_dot_in_radius(player.x, player.y, self.x, self.y, self.radius)

    def eat_food(self, cell):
        self.radius += cell.radius

    def eat_player(self, other_player: 'Player'):
        self.radius += other_player.radius // 3

    def reset_radius(self):
        self.radius = self.INITIAL_RADIUS

    def move(self, xv, yv):
        self.x += xv
        self.y += yv

    @classmethod
    def random_player(cls, name, bounds):
        return cls(
            name,
            *get_random_from_bounds(bounds),
            random.choice(cls.PLAYER_COLORS),
        )

    def __repr__(self):
        return f'Player: {self.name}'
