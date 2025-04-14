from domain.tile import Tile

class Bush(Tile):
    _image_path = "./ressources/images/bush.png"

    def is_walkable(self):
        return False