RULES = """
Règles du jeu :
Le jeu du Minotaure est initialement un jeu de plateau. 
Le joueur doit sortir du labyrinthe aussi vite que possible mais aussi lentement que nécessaire. 
Pour cela, il doit trouver la sortie en moins de 20 secondes et faire un minimum d'erreurs.
Est considéré comme erreur, lorsque le joueur essaie de marcher en direction d'un buisson.
A chaque erreur, le Minotaure avance de 5 cases en direction du joueur.
Si ce dernier rattrape le joueur, alors il a perdu.

Conditions de victoire :
    - Le joueur a trouvé la sortie en moins de 20 secondes sans se faire rattraper par le Minotaure.

Conditions de défaite :
    - Le joueur n'est pas sorti du labyrinthe dans les 20 secondes.
    - Le joueur a fait un trop grand nombre d'erreurs et le Minotaure l'a rattrapé.
"""