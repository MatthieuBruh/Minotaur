from PIL import Image, ImageTk

TILE_SIZE = 32

class Tile:
    _image_path = None
    _image = None

    def __init__(self):
        if not self.__class__._image:
            img = Image.open(self.__class__._image_path).resize((TILE_SIZE, TILE_SIZE))
            self.__class__._image = ImageTk.PhotoImage(img)
        self.image = self.__class__._image

    def is_walkable(self):
        return True

    def is_exit(self):
        return False

    def render(self, canvas, x, y):
        canvas.create_image(x, y, image=self.image, anchor="nw")
