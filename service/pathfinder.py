from collections import deque


def find_path(tiles_map, start, goal):
    """
    Fonction utilisée pour calculer le chemin entre une position de départ et une position d'arrivée.
    Basé sur l'algorithme : Breadth-first search (BFS)

    :param tiles_map: grille 2D grid (list of lists) contenant des Tiles
    :param start: Position de départ (x, y)
    :param goal: Position d'arrivée (x, y)
    :return: Une liste de positions pour atteindre le but sans comprendre le départ.
             Liste vide si pas de path trouvé.
    """

    # Set up BFS stuff
    queue = deque() # Tiles à explorer
    came_from = {}  # Utilisé pour reconstruire le chemin (key: position actuelle, value: d'où on vient)
    seen = set() # Tiles déjà explorée

    queue.append(start)
    seen.add(start)

    while queue:
        current = queue.popleft()

        # Si on atteint le but alors on s'arrête
        if current == goal:
            break

        cx, cy = current

        # Vérification des déplacements : haut, bas, gauche, droite.
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            neighbor = (nx, ny)

            # S'assurer qu'on est encore dans les clous.
            if ny < 0 or ny >= len(tiles_map):
                continue
            if nx < 0 or nx >= len(tiles_map[0]):
                continue

            tile = tiles_map[ny][nx]

            # Si on peut marcher sur la tile ou si c'est le but.
            if tile.is_walkable() or neighbor == goal:
                if neighbor not in seen:
                    queue.append(neighbor)
                    seen.add(neighbor)
                    came_from[neighbor] = current

    # Construire le chemin du retour à partir de l’objectif.
    path = []
    step = goal

    while step != start:
        prev = came_from.get(step)
        if prev is None:
            # Le but n'est pas atteignable.
            return []
        path.append(step)
        step = prev

    path.reverse()

    return path
