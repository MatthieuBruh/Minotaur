import os
import glob

from domain.level import Level


def get_levels(levels_dir: str):
    txt_files = glob.glob(os.path.join(levels_dir, '*.txt'))
    levels = []

    for txt_path in txt_files:
        # Check that the txt_file is not empty
        if os.stat(txt_path).st_size == 0:
            continue

        # Check that the corresponding PNG exists
        modified_path = txt_path.replace('\\', '/')
        base_name = modified_path.split('/')[-1].split('.')[0]
        png_path = os.path.join(levels_dir, base_name + '.png')

        if not os.path.isfile(png_path):
            continue
        levels.append(Level(base_name, txt_path.split('.txt')[0]))
    return levels