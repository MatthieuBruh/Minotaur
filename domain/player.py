from domain.tile import Tile

class Player(Tile):
    def __init__(self, image):
        super().__init__(image)
        self.x = 0
        self.y = 0

    def move_to(self, x, y):
        self.x = x
        self.y = y