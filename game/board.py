import itertools
import time

from game.cell import Cell
from game.chunk import Chunk


class Board:
    ROUND_DURATION = 60 * 2

    def __init__(self, players=None, cells=None, bounds=(1000, 1000), chunk_size=1000):
        players = players or []
        cells = cells or []
        self.bounds = bounds
        self.chunk_size = chunk_size
        self.chunks = []

        for i in range((self.bounds[0] * 2) // chunk_size + 1):
            self.chunks.append([Chunk() for _ in range((self.bounds[1] * 2) // chunk_size + 1)])

        for player in players:
            self.add_player(player)
        for cell in cells:
            self.add_cell(cell)

        self.start_round_time = time.time()

    def add_player(self, player):
        chunk = self.get_chunk(player.x, player.y)
        chunk.add_player(player)

    def add_cell(self, cell):
        chunk = self.get_chunk(cell.x, cell.y)
        chunk.add_cell(cell)

    def remove_player(self, player):
        chunk = self.get_chunk(player.x, player.y)
        chunk.remove_player(player)

    def remove_cell(self, cell):
        chunk = self.get_chunk(cell.x, cell.y)
        chunk.remove_cell(cell)

    @property
    def cells(self):
        cells = []
        for chunks in self.chunks:
            for chunk in chunks:
                cells += chunk.cells
        return cells

    @property
    def players(self):
        players = []
        for chunks in self.chunks:
            for chunk in chunks:
                players += chunk.players
        return players

    def fill_cells(self, cell_count):
        for i in range(cell_count):
            self.add_cell(Cell.random_cell(self.bounds))

    def get_chunk(self, x, y) -> Chunk:
        chunk_x, chunk_y = self.get_chunk_coords(x, y)
        return self.chunks[chunk_x][chunk_y]

    def get_chunk_coords(self, x, y):
        return (x + self.bounds[0]) // self.chunk_size, (y + self.bounds[1]) // self.chunk_size

    def reset_all_players(self):
        for player in self.players:
            player.reset_radius()

    def get_nearest_chunks(self, x, y):
        chunks = []
        chunk_x, chunk_y = self.get_chunk_coords(x, y)

        for i in itertools.product((-1, 0, 1), repeat=2):
            new_x, new_y = chunk_x + i[0], chunk_y + i[1]
            if new_x >= 0 and new_x < len(self.chunks) and new_y >= 0 and new_y < len(self.chunks[0]):
                chunks.append(self.chunks[new_x][new_y])

        return chunks

    def get_data_from_chunks(self, chunks):
        cells = []
        players = []
        for chunk in chunks:
            cells += chunk.cells
            players += chunk.players
        return cells, players

    def update(self):
        if time.time() - self.start_round_time >= self.ROUND_DURATION:
            self.reset_all_players()
            self.fill_cells(((self.bounds[0] + self.bounds[1]) // 4) - len(self.cells))
            self.start_round_time = time.time()

        seen_players = self.players
        for player in seen_players:

            seen_chunks = self.get_nearest_chunks(player.x, player.y)
            cells, players = self.get_data_from_chunks(seen_chunks)

            for cell in cells:
                if player.can_eat_food(cell):
                    player.eat_food(cell)
                    self.remove_cell(cell)

            for other_player in players:
                if player == other_player:
                    continue
                if player.can_eat_player(other_player):
                    player.eat_player(other_player)
                    self.remove_player(other_player)
                    seen_players.remove(other_player)

    def get_player_info(self, x, y):
        chunks = self.get_nearest_chunks(x, y)
        cells, players = self.get_data_from_chunks(chunks)
        board = Board(players, cells, self.bounds, self.chunk_size)
        board.start_round_time = self.start_round_time
        return board

    def move_player(self, player, xv, yv):
        self.remove_player(player)
        player.move(xv, yv)
        self.add_player(player)
