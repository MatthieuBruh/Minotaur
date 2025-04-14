from tkinter import Button
from PIL import Image, ImageTk, ImageDraw, ImageFont


# Source : https://python-forum.io/thread-34264.html & ChatGPT
class ImageButton(Button):
    """
    Classe ImageButton qui permet d'avoir des images comme bouton sur Tkinter.
    """
    def __init__(self, parent, image_path, label_text, command):
        """
        Constructeur de la classe ImageBouton afin d'initialiser le bouton.
        :param parent: Parent qui va contenir le bouton.
        :param image_path: Chemin d'accès à l'image.
        :param label_text: Texte qui sera contenu au centre du bouton-image.
        :param command: Commande exécutée par le bouton lorsqu'il est pressé.
        """
        self.parent = parent
        self.original_image = Image.open(image_path)
        self.label_text = label_text
        self.tk_image = None
        self.command = command
        super().__init__(parent, command=command)
        self.configure(compound="top", bd=0)
        self.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        """
        Méthode permettant de redimensionner l'image pour l'affichage.
        :param event:
        :return: NONE
        """
        new_width = event.width
        new_height = event.height

        if new_width > 0 and new_height > 0:
            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            draw = ImageDraw.Draw(resized_image)
            try:
                font_size = new_width // 8
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            # Permet de connaitre la taille de la bounding box
            bbox = draw.textbbox((0, 0), self.label_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Compute coordinates to center the text on the image
            text_x = (new_width - text_width) // 2
            text_y = (new_height - text_height) // 2

            # Ecrire le texte sur l'image
            draw.text((text_x, text_y), self.label_text, font=font, fill="red")

            # Conversion de l'image compatible avec Tkinter
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.configure(image=self.tk_image)
            self.image = self.tk_image

