from domain.tile import Tile

class Minotaur(Tile):
    _image_path = "./ressources/images/minotaur.png"

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def is_walkable(self):
        return False