from tkinter import Tk, Frame, PhotoImage, PanedWindow, Label
from tkinter.constants import HORIZONTAL

from game_play import GameWindow
from service.load_level import get_levels
from utils.GifClass import AnimatedGIF
from utils.image_button import ImageButton


def play_level(root_window, level):
    """
    Fonction utilisée lorsque le joueur clic sur une image-bouton représentant un niveau.
    → Ouvre la fenêtre du niveau pour que le joueur puisse commencer la partie.
    :param root_window: Fenêtre mère
    :param level: niveau sélectionné par le joueur
    :return: NONE
    """
    GameWindow(root=root_window, level_path=level.get_txt_path())


class GameMenu(Frame):
    """
    Classe de la fenêtre qui affiche le menu principal du jeu.
    """

    def __init__(self, root: Tk = None):
        """
        Constructeur de la classe GameMenu.
        → Permet l'initialisation de l'interface et des différents attributs
        :param root: Fenêtre principale de l'application.
        """
        Frame.__init__(self, root)
        self._root = root
        self._root.title("Game Menu")
        self.manage_window_size()
        self.manage_window_info()
        self.manage_paned()

    def manage_window_info(self):
        """
        Méthode utilisée pour configurer les informations générales de la fenêtre, comme le titre et l'icône.
        :return: NONE
        """
        self._root.title("Minotaur game")
        self._root.iconphoto(False, PhotoImage(file="./ressources/images/game_menu/minotaur.png"))

    def manage_window_size(self):
        """
        Méthode utilisée pour configurer la taille de la fenêtre par rapport à la taille de l'écran.
        La fenêtre prend le 2/3 de l'écran et est positionné au centre de l'écran
        :return: NONE
        """
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        self._root.window_width = (screen_width * 2) // 3
        self._root.window_height = (screen_height * 2) // 3
        position_top = (screen_height - self._root.window_height) // 2
        position_left = (screen_width - self._root.window_width) // 2
        self._root.geometry(f"{self._root.window_width}x{self._root.window_height}+{position_left}+{position_top}")
        self._root.resizable(False, False)

    def manage_paned(self):
        """
        Méthode utilisée pour créer et organiser la fenêtre en deux sections principales.
        1 section : titre et GIF d'un minotaure animé (1/3 de la hauteur)
        2 section : liste des niveaux (2/3 de la hauteur)
        :return: NONE
        """
        one_third_height = self._root.window_height // 4
        two_third_height = self._root.window_height - one_third_height

        # 1 section - titre + GIF
        self._root.paned_title = PanedWindow(self._root, orient=HORIZONTAL, height=one_third_height, bd=0)
        self._root.paned_title.pack(fill="x")
        # Conteneur centré pour le titre et le GIF
        title_frame = Frame(self._root.paned_title, bg="green")
        title_frame.grid_rowconfigure(0, weight=1)
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=1)
        # Label du titre du jeu
        p1_label = Label(title_frame, text="The Minotaur", bg="green", fg="black", font=("Arial", 40))
        p1_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")
        # Animation GIF du minotaure
        gif_widget = AnimatedGIF(title_frame, "./ressources/images/game_menu/minotaur.gif")
        gif_widget.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        # Ajout du cadre complet au PanedWindow
        self._root.paned_title.add(title_frame)

        # 2 section - liste des niveaux
        self._root.paned_levels = PanedWindow(self._root, orient=HORIZONTAL, height=two_third_height, bd=0)
        self._root.paned_levels.pack(fill="both", expand=True)
        self.display_levels(self._root.paned_levels)

    def display_levels(self, paned_levels: PanedWindow):
        """
        Méthode permettant d'afficher les niveaux sous forme d'image-bouton et de les organiser proprement.
        :param paned_levels: PanedWindows qui va contenir la liste des niveaux
        :return: NONE
        """
        levels = get_levels("./ressources/levels")
        columns = 3  # Nombre de colonnes pour la grille de boutons
        grid_frame = Frame(paned_levels, bg="green", padx=30, pady=30)
        paned_levels.add(grid_frame)

        for idx, level in enumerate(levels):
            row = idx // columns
            col = idx % columns
            # Création du bouton image avec action au clic
            img_button = ImageButton(
                grid_frame,
                image_path=level.get_png_path(),
                label_text=level.get_name(),
                command=lambda lvl=level: play_level(self._root, lvl)
            )
            img_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            grid_frame.grid_columnconfigure(col, weight=1)
            grid_frame.grid_rowconfigure(row, weight=1)

        # Permet d'équilibrer la largeur des colonnes
        for i in range(columns):
            grid_frame.grid_columnconfigure(i, weight=1)


if __name__ == "__main__":
    # Lancement de l'application
    game_window = Tk()
    game = GameMenu(game_window)
    game.mainloop()
