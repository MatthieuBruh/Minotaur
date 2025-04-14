from collections import deque

def find_path(tiles, start, goal):
    queue = deque()
    visited = set()
    prev = {}

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if 0 <= nx < len(tiles[0]) and 0 <= ny < len(tiles):
                tile = tiles[ny][nx]
                if tile.is_walkable() or neighbor == goal:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        visited.add(neighbor)
                        prev[neighbor] = current

    # Reconstruire le chemin
    path = []
    current = goal
    while current != start:
        if current not in prev:
            return []  # Pas de chemin
        path.append(current)
        current = prev[current]
    path.reverse()
    return path
