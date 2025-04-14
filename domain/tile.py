class Tile:
    def __init__(self, image):
        self.image = image

    def is_walkable(self):
        return True

    def is_exit(self):
        return False

    def render(self, canvas, x, y):
        canvas.create_image(x, y, image=self.image, anchor="nw")