import os
import glob

from domain.level import Level


def get_levels(levels_dir: str):
    """
    Procédure permettant de retourner une liste de niveaux par rapports aux fichiers .txt d'un répertoire.
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
        levels.append(Level(base_name, txt_path.split('.txt')[0]))
    return levels