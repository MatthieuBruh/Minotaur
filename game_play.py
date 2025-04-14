from tkinter import Toplevel, Canvas, Label, Button
from PIL import ImageTk, Image
from domain.exit import Exit
from domain.exitWithPlayer import ExitWithPlayer
from domain.floor import Floor
from domain.minotaur import Minotaur
from domain.player import Player
from domain.bush import Bush
from service.pathfinder import find_path
import time

TILE_SIZE = 32  # Taille d'une tuile en pixels


class GameWindow(Toplevel):
    """
    Classe de la fenêtre de jeu.
    Affiche différentes informations comme la carte (niveau) et le chronomètre.
    Gère de manière générale le déroulement du jeu.
    """


    def __init__(self, root, level_path):
        """
        Constructeur de la classe GameWindow
        :param root: fenêtre parent à laquelle on sera rattaché.
        :param level_path: Niveau choisit par l'utilisateur dans le menu.
        """
        super().__init__(root)
        self.title("Minotaur - play")
        self.attributes("-fullscreen", True)
        self.configure(bg="green")
        # Canvas du jeu
        self.canvas = Canvas(self, bg="green")
        self.canvas.pack(fill="both", expand=True)
        # Permet de fermer la fenêtre de jeu quand le joueur appuie sur Escape
        self.bind("<Escape>", lambda e: self.destroy())

        # Gestion d'association classes de tuiles et caractères du fichier.
        ##  Chargement des images et association des caractères aux classes de tuiles
        self.images = self.load_images()
        self.tile_classes = {
            "#": Bush,
            "-": Floor,
            "$": Minotaur,
            "@": Player,
            ".": Exit
        }

        self.tiles = []     # Grille des tuiles du niveau
        self.player = None  # Référence au joueur
        self.minotaur = None  # Référence au minotaure

        # Chargement du niveau depuis le fichier
        self.load_level(level_path)
        self.render_level()

        # Interface : Chronomètre et bouton de démarrage
        self.timer_label = Label(self, text=f"00:00:00", font=("Arial", 40), bg="green", fg="red")
        self.timer_label.place(relx=1.0, y=10, anchor="ne")

        self.start_button = Button(self, text="Start", font=("Arial", 40), bg="green", fg="red", command=self.start_game)
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

    def load_images(self):
        """
        Charge les images des différentes entités du jeu et les redimensionne.

        Returns:
            dict: Association caractère -> image Tkinter.
        """
        def load(path):
            pil_image = Image.open(path).resize((TILE_SIZE, TILE_SIZE))
            return ImageTk.PhotoImage(pil_image)

        return {
            "#": load("./ressources/images/bush.png"),
            "-": load("./ressources/images/floor.png"),
            "$": load("./ressources/images/minotaur.png"),
            "@": load("./ressources/images/player.png"),
            ".": load("./ressources/images/exit.png"),
            "|": load("./ressources/images/exitWithPlayer.png")
        }

    def load_level(self, level_path):
        """
        Lit le fichier du niveau et crée les tuiles correspondantes.

        Args:
            level_path (str): Chemin vers le fichier du niveau.
        """
        with open(level_path, "r") as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                tile_class = self.tile_classes.get(char, Floor)
                tile = tile_class(self.images.get(char))

                # Initialisation des entités mobiles
                if isinstance(tile, Player):
                    tile.move_to(x, y)
                    self.player = tile
                elif isinstance(tile, Minotaur):
                    tile.move_to(x, y)
                    self.minotaur = tile

                row.append(tile)
            self.tiles.append(row)

    def render_level(self):
        """
        Dessine les tuiles sur le canvas en fonction de leur position.
        """
        self.canvas.delete("all")
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tile.render(self.canvas, x * TILE_SIZE, y * TILE_SIZE)

    def start_game(self):
        """
        Démarre la partie :
        - Active les touches de déplacement
        - Lance le chronomètre
        """
        self.start_button.destroy()
        self.bind("<Up>", lambda e: self.move_player(0, -1))
        self.bind("<Down>", lambda e: self.move_player(0, 1))
        self.bind("<Left>", lambda e: self.move_player(-1, 0))
        self.bind("<Right>", lambda e: self.move_player(1, 0))
        self.focus_set()

        self.time_limit = 20  # Temps limite en secondes
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """
        Met à jour le chronomètre à intervalle régulier (toutes les 50 ms).
        Termine la partie si le temps est écoulé.
        """
        if not self.timer_label.winfo_exists():
            return

        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        milliseconds = int((remaining - int(remaining)) * 100)

        self.timer_label.config(text=f"{minutes:02}:{seconds:02}.{milliseconds:02}")

        if remaining <= 0:
            self.end_game(is_timeout=True)
        else:
            self.after(50, self.update_timer)

    def end_game(self, is_lost=False, is_timeout=False):
        """
        Termine la partie, affiche un message selon le résultat.

        Args:
            is_lost (bool): Vrai si le joueur est attrapé par le minotaure.
            is_timeout (bool): Vrai si le temps est écoulé.
        """
        self.timer_label.destroy()
        self.unbind("<Up>")
        self.unbind("<Down>")
        self.unbind("<Left>")
        self.unbind("<Right>")

        if is_lost:
            message = "You lost, the Minotaur caught you..."
        elif is_timeout:
            message = "You lost, time's up..."
        else:
            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time - int(elapsed_time)) * 100)
            message = f"You won in {minutes:02}:{seconds:02}.{milliseconds:02}"

        end_label = Label(self, text=message, font=("Arial", 26), bg="green", fg="white")
        end_label.place(relx=0.5, rely=0.5, anchor="center")

        # Fermeture automatique après 3 secondes
        self.after(3000, func=self.destroy)

    def move_player(self, dx, dy):
        """
        Déplace le joueur si possible, puis met à jour l'affichage.

        Args:
            dx (int): Déplacement horizontal.
            dy (int): Déplacement vertical.
        """
        if not self.player:
            return

        old_x, old_y = self.player.x, self.player.y
        new_x = old_x + dx
        new_y = old_y + dy

        if not (0 <= new_y < len(self.tiles) and 0 <= new_x < len(self.tiles[0])):
            return

        target_tile = self.tiles[new_y][new_x]

        if target_tile.is_walkable():
            self.tiles[old_y][old_x] = Floor(self.images["-"])

            if target_tile.is_exit():
                # Le joueur a gagné
                self.tiles[new_y][new_x] = ExitWithPlayer(self.images["|"])
                self.end_game()
            else:
                # Déplacement normal
                self.player.move_to(new_x, new_y)
                self.tiles[new_y][new_x] = self.player

            self.render_level()
        else:
            # Le joueur a échoué à se déplacer, le minotaure avance
            self.move_minotaur(steps=5)

    def move_minotaur(self, steps=5):
        """
        Déplace le minotaure vers le joueur en suivant le chemin trouvé.

        Args:
            steps (int): Nombre de pas maximum que le minotaure peut faire.
        """
        if not self.minotaur or not self.player:
            return

        start = (self.minotaur.x, self.minotaur.y)
        goal = (self.player.x, self.player.y)
        path = find_path(self.tiles, start, goal)

        if not path:
            print("Level ERROR : Minotaur cannot reach the player!!")
            return

        moves = path[:steps]

        for (new_x, new_y) in moves:
            old_x, old_y = self.minotaur.x, self.minotaur.y

            if (new_x, new_y) == (self.player.x, self.player.y):
                # Le minotaure a attrapé le joueur
                self.end_game(is_lost=True)
                return

            self.tiles[old_y][old_x] = Floor(self.images["-"])
            self.minotaur.move_to(new_x, new_y)
            self.tiles[new_y][new_x] = self.minotaur

        self.render_level()
