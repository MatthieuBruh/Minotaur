import os

class Level:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self):
        return f"Level: {self.name}"

    def get_name(self):
        return f"Level: {self.name}"

    def get_txt_path(self) -> str:
        return os.path.join(self.path + ".txt")

    def get_png_path(self) -> str:
        return os.path.join(self.path + ".png")