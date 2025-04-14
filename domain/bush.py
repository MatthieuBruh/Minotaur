from domain.tile import Tile

class Bush(Tile):
    def is_walkable(self):
        return False