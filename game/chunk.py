class Chunk:
    def __init__(self, players=None, cells=None):
        self.players = players or []
        self.cells = cells or []

    def add_player(self, player):
        self.players.append(player)

    def add_cell(self, cell):
        self.cells.append(cell)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def remove_cell(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
