class Camera:

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def set_to_center(self, x, y):
        self.x = x - self.width / 2
        self.y = y + self.height / 2

    def adjust(self, x, y):
        return x - self.x, self.y - y
