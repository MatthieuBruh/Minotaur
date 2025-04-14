from domain.tile import Tile

class Exit(Tile):
    def is_exit(self):
        return True