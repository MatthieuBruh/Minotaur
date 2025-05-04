import glob
import os

from domain.level import Level

mandatory_elements = ["#", "-", ".", "@", "$"]
unique_elements = [".", "@", "$"]

def get_levels(levels_dir: str):
    """
    Fonction permettant de retourner une liste de niveaux par rapports aux fichiers .txt d'un répertoire.
    :param levels_dir: Répertoire dans lequel on va chercher les .txt des niveaux.
    :return: une liste des niveaux.
    """
    txt_files = glob.glob(os.path.join(levels_dir, '*.txt'))
    levels = []
    for txt_path in txt_files:
        # Vérification que le fichier .txt n'est pas vide.
        if os.stat(txt_path).st_size == 0:
            continue

        # Vérification qu'un PNG correspondant au niveau existe.
        modified_path = txt_path.replace('\\', '/')
        base_name = modified_path.split('/')[-1].split('.')[0]
        png_path = os.path.join(levels_dir, base_name + '.png')

        if not os.path.isfile(png_path):
            continue

        if not check_validity(txt_path):
            continue

        levels.append(Level(base_name, txt_path.split('.txt')[0]))
    return levels

def check_validity(path) -> bool:
    """
    Fonction utilisée pour vérifier la validité du niveau.
    Vérification que le fichier contienne bien les éléments obligatoires et un seul Minotaure, sortie et joueur.
    :param path: chemin du fichier à vérifier.
    :return: renvoie un booléen si le niveau est valide ou non
    """

    with open(path, "r") as file:
        content = file.read()

    # Vérification de la présence des éléments obligatoires
    for element in mandatory_elements:
        if element not in content:
            return False

    # Vérification d'unicité du Minotaure, joueur et de sortie
    for unique_el in unique_elements:
        if content.count(unique_el) != 1:
            print("Missing :", unique_el, "in file :", path)
            return False
    return True
