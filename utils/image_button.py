from tkinter import Button
from PIL import Image, ImageTk, ImageDraw, ImageFont


# Source : https://python-forum.io/thread-34264.html
# Custom button that displays a resizable image with centered text overlaid
class ImageButton(Button):
    def __init__(self, parent, image_path, label_text, command=None):
        # Store parameters and load the original image
        self.parent = parent
        self.original_image = Image.open(image_path)
        self.label_text = label_text
        self.tk_image = None
        self.command = command

        # Initialize the base Button with the parent and command
        super().__init__(parent, command=command)

        # Configure appearance (no border, image on top if text is also set)
        self.configure(compound="top", bd=0)

        # Bind the resize event to update the image dynamically
        self.bind("<Configure>", self._resize_image)

        # Store the image path (optional, useful for debugging or future features)
        self.image_path = image_path

    def _resize_image(self, event):
        # Get the current width and height of the widget
        new_width = event.width
        new_height = event.height

        # Only proceed if dimensions are valid
        if new_width > 0 and new_height > 0:
            # Resize the original image to the new dimensions
            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)

            # Create a drawable image surface
            draw = ImageDraw.Draw(resized_image)

            # Try to use a TTF font for better rendering; fallback to default if unavailable
            try:
                font_size = new_width // 12  # Set font size relative to width
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            # Calculate the size of the text bounding box
            bbox = draw.textbbox((0, 0), self.label_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Compute coordinates to center the text on the image
            text_x = (new_width - text_width) // 2
            text_y = (new_height - text_height) // 2

            # Draw the text onto the image
            draw.text((text_x, text_y), self.label_text, font=font, fill="red")

            # Convert the image to a Tkinter-compatible PhotoImage
            self.tk_image = ImageTk.PhotoImage(resized_image)

            # Update the button to display the new image
            self.configure(image=self.tk_image)

            # Keep a reference to prevent the image from being garbage collected
            self.image = self.tk_image

