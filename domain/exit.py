from domain.tile import Tile

class Exit(Tile):
    _image_path = "./ressources/images/exit.png"

    def is_exit(self):
        return True
