from tkinter import Label, Image
from PIL import Image, ImageTk, ImageSequence


class AnimatedGIF(Label):
    def __init__(self, parent, gif_path, bg_color="green"):
        super().__init__(parent, bg=bg_color)
        self.frames = []
        self.idx = 0

        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            self.frames.append(ImageTk.PhotoImage(frame.copy()))

        self.update_frame()

    def update_frame(self):
        self.configure(image=self.frames[self.idx])
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(100, self.update_frame)  # Delay in milliseconds