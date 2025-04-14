from domain.tile import Tile

class ExitWithPlayer(Tile):
    def is_exit(self):
        return True