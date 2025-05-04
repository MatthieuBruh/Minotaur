import time
from tkinter import Toplevel, Canvas, Label, Button

from domain.bush import Bush
from domain.exit import Exit
from domain.exitWithPlayer import ExitWithPlayer
from domain.floor import Floor
from domain.minotaur import Minotaur
from domain.player import Player
from service.pathfinder import find_path

TILE_SIZE = 32  # Taille d'une tuile en pixels


class GameWindow(Toplevel):
    """
    Classe de la fenêtre de jeu.
    Affiche différentes informations comme la carte (niveau) et le chronomètre.
    Gère de manière générale le déroulement du jeu.
    """

    def __init__(self, root, level_path, timer_limit):
        """
        Constructeur de la classe GameWindow
        :param root: fenêtre parent à laquelle on sera rattaché.
        :param level_path: Niveau choisit par l'utilisateur dans le menu.
        :param timer_limit: Temps maximal pour le timer choisit par l'utilisateur.
        """
        super().__init__(root)
        self.title("Minotaur - play")
        self.attributes("-fullscreen", True)
        self.configure(bg="green")
        self.start_time = None
        self.timer_limit = timer_limit
        # Canvas du jeu
        self.canvas = Canvas(self, bg="green")
        self.canvas.pack(fill="both", expand=True)
        # Permet de fermer la fenêtre de jeu quand le joueur appuie sur Escape
        self.bind("<Escape>", lambda e: self.destroy())

        # Gestion d'association classes de tuiles et caractères du fichier.
        ## Chargement des images et association des caractères aux classes de tuiles
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
        self.bind("<Return>", lambda event: self.start_game())
        self.canvas.focus_set()

    def load_level(self, level_path):
        """
        Méthode permettant de lire le fichier .txt du niveau et d'instancier les différentes tiles.
        :param level_path: Contient le chemin vers le fichier texte qui décrit la structure du niveau.
        :return: NONE
        """
        with open(level_path, "r") as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                tile_class = self.tile_classes.get(char, Floor)
                tile = tile_class()
                # Cas où la tile correspond au joueur ou au minotaur afin d'enregistrer leur position.
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
        Méthode permettant d'afficher les différentes tiles dans le canvas.
        :return: NONE
        """
        self.canvas.delete("all")
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tile.render(self.canvas, x * TILE_SIZE, y * TILE_SIZE)

    def start_game(self):
        """
        Méthode permettant de commencer la partie : active les touches et démarre le timer.
        :return: NONE
        """
        self.start_button.destroy()
        self.bind("<Up>", lambda e: self.move_player(0, -1))
        self.bind("<Down>", lambda e: self.move_player(0, 1))
        self.bind("<Left>", lambda e: self.move_player(-1, 0))
        self.bind("<Right>", lambda e: self.move_player(1, 0))
        self.focus_set()

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """
        Méthode permettant de mettre à jour le timer (dont l'affichage) toutes les 50 ms.
        Si le timer est écoulé, on termine la partie.
        :return: NONE
        """
        if not self.timer_label.winfo_exists():
            return

        elapsed = time.time() - self.start_time
        remaining = max(0, self.timer_limit.get() - elapsed)

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
        Méthode permettant de mettre fin à la partie et de fermer la fenêtre GameWindow. → retour écran d'accueil.
        Désactivation des touches et affichage d'un message de fin.
        :param is_lost: True : si le joueur est rattrapé par le minotaure.
        :param is_timeout: True : si le timer est écoulé.
        :return: NONE
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
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            milliseconds = int((elapsed - int(elapsed)) * 100)
            message = f"You won in {minutes:02}:{seconds:02}.{milliseconds:02}"
        end_label = Label(self, text=message, font=("Arial", 26), bg="green", fg="white")
        end_label.place(relx=0.5, rely=0.5, anchor="center")

        # Ferme la fenêtre GameWindow après 3 secondes
        self.after(3000, func=self.destroy)

    def move_player(self, dx, dy):
        """
        Méthode utilisée pour déplacer le joueur sur la carte.
        Comprend les vérifications :
            * Limites de la carte
            * Tile peut être marché par le joueur
                - Si oui, on déplace et vérifie que si la destination est la tile correspond à la sortie
                - Sinon, on déplace le minotaure
        :param dx: Déplacement en direction de l'axe des X
        :param dy: Déplacement en direction de l'axe des Y.
        :return: NONE
        """
        if not self.player:
            return

        old_x, old_y = self.player.x, self.player.y
        new_x = old_x + dx
        new_y = old_y + dy

        # Vérification que le joueur reste dans la carte.
        if not (0 <= new_y < len(self.tiles) and 0 <= new_x < len(self.tiles[0])):
            return

        target_tile = self.tiles[new_y][new_x]

        if target_tile.is_walkable():
            # Ancienne tile du joueur devient un Floor
            self.tiles[old_y][old_x] = Floor()

            # Cas où le joueur atteint la sortie
            if target_tile.is_exit():
                self.tiles[new_y][new_x] = ExitWithPlayer()
                self.end_game()
            # Simple déplacement
            else:
                self.player.move_to(new_x, new_y)
                self.tiles[new_y][new_x] = self.player
            self.render_level()
        # Si la tile n'est pas franchissable par le joueur
        else:
            self.move_minotaur(steps=5)

    def move_minotaur(self, steps=5):
        """
        Méthode permettant de déplacer le minotaure vers le joueur en utilisant du pathfinding.
        :param steps: Nombre de cases dont le minotaure va avancer par coup.
        :return: NONE
        """
        if not self.minotaur or not self.player: return

        start = (self.minotaur.x, self.minotaur.y)
        goal = (self.player.x, self.player.y)
        path = find_path(self.tiles, start, goal)

        if not path:
            print("Level ERROR : Minotaur cannot reach the player!!")
            return

        for (new_x, new_y) in path[:steps]:
            old_x, old_y = self.minotaur.x, self.minotaur.y

            self.tiles[old_y][old_x] = Floor()
            self.minotaur.move_to(new_x, new_y)
            self.tiles[new_y][new_x] = self.minotaur

            if (new_x, new_y) == (self.player.x, self.player.y):
                self.end_game(is_lost=True)
                break
        self.render_level()