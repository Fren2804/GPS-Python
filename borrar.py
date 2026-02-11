def neighbors(p, cols, rows):
    x, y = p
    result = []

    if x > 0:
        result.append((x - 1, y))
    if x < cols - 1:
        result.append((x + 1, y))
    if y > 0:
        result.append((x, y - 1))
    if y < rows - 1:
        result.append((x, y + 1))

    return result

def reconstruct(came_from, start, goal):
    path = []
    cur = goal

    while cur != start:
        path.append(cur)
        cur = came_from[cur]

    path.append(start)
    path.reverse()
    return path

def pathfinding(grid, start, goal, cols, rows):

    queue = [start]          # nodos a visitar
    visited = set([start])   # ya visitados
    came_from = {}

    while queue:
        current = queue.pop(0)   # saca el primero

        if current == goal:
            return reconstruct(came_from, start, goal)

        for n in neighbors(current, cols, rows):
            x, y = n

            if grid[y][x] == 1:
                continue

            if n not in visited:
                visited.add(n)
                queue.append(n)
                came_from[n] = current

    return None