import heapq
import time
from typing import List, Tuple, Dict, Optional, Set

Pos = Tuple[int, int]

def neighbors(p: Pos, w: int, h: int) -> List[Pos]:
    x, y = p
    out = []
    if x > 0: out.append((x - 1, y))
    if x < w - 1: out.append((x + 1, y))
    if y > 0: out.append((x, y - 1))
    if y < h - 1: out.append((x, y + 1))
    return out

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct(came_from: Dict[Pos, Pos], start: Pos, goal: Pos) -> List[Pos]:
    cur = goal
    path = [cur]
    while cur != start:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    return path

def dijkstra(grid: List[List[int]], start: Pos, goal: Pos):
    h = len(grid)
    w = len(grid[0])
    INF = 10**18
    dist = {start: 0}
    came_from: Dict[Pos, Pos] = {}
    visited: Set[Pos] = set()
    pq = [(0, start)]
    pops = 0

    while pq:
        d, u = heapq.heappop(pq)
        pops += 1
        if u in visited:
            continue
        visited.add(u)

        if u == goal:
            return reconstruct(came_from, start, goal), pops, len(visited)

        for v in neighbors(u, w, h):
            if grid[v[1]][v[0]] == 1:
                continue
            nd = d + 1
            if nd < dist.get(v, INF):
                dist[v] = nd
                came_from[v] = u
                heapq.heappush(pq, (nd, v))

    return None, pops, len(visited)

def astar(grid: List[List[int]], start: Pos, goal: Pos):
    h = len(grid)
    w = len(grid[0])
    INF = 10**18
    g = {start: 0}
    came_from: Dict[Pos, Pos] = {}
    visited: Set[Pos] = set()
    pq = [(manhattan(start, goal), 0, start)]  # (f, g, node)
    pops = 0

    while pq:
        f, gu, u = heapq.heappop(pq)
        pops += 1
        if u in visited:
            continue
        visited.add(u)

        if u == goal:
            return reconstruct(came_from, start, goal), pops, len(visited)

        for v in neighbors(u, w, h):
            if grid[v[1]][v[0]] == 1:
                continue
            ng = gu + 1
            if ng < g.get(v, INF):
                g[v] = ng
                came_from[v] = u
                nv_f = ng + manhattan(v, goal)
                heapq.heappush(pq, (nv_f, ng, v))

    return None, pops, len(visited)

def print_grid(grid: List[List[int]], path: Optional[List[Pos]], start: Pos, goal: Pos):
    path_set = set(path) if path else set()
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            p = (x, y)
            if p == start:
                row.append("S")
            elif p == goal:
                row.append("G")
            elif grid[y][x] == 1:
                row.append("#")
            elif p in path_set:
                row.append(".")
            else:
                row.append(" ")
        print("".join(row))

def run_case(name: str, grid: List[List[int]], start: Pos, goal: Pos):
    print(f"\n=== {name} ===")
    print(f"Start={start} Goal={goal} Size={len(grid[0])}x{len(grid)}")

    t0 = time.perf_counter()
    path_d, pops_d, vis_d = dijkstra(grid, start, goal)
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    path_a, pops_a, vis_a = astar(grid, start, goal)
    t3 = time.perf_counter()

    def stats(label, path, pops, vis, dt):
        if path is None:
            print(f"{label}: NO PATH | popped={pops} visited={vis} time={dt*1000:.2f}ms")
        else:
            print(f"{label}: len={len(path)-1} | popped={pops} visited={vis} time={dt*1000:.2f}ms")

    stats("Dijkstra", path_d, pops_d, vis_d, t1 - t0)
    stats("A*",      path_a, pops_a, vis_a, t3 - t2)

    # Muestra el camino de A* (normalmente es igual de corto) para visualizar
    print("\nGrid (path='.'  wall='#'):")
    print_grid(grid, path_a if path_a else None, start, goal)

def make_grid_case_open(w=40, h=20):
    # Caso 1: casi vacío (A* arrasa a Dijkstra en nodos explorados)
    grid = [[0]*w for _ in range(h)]
    return grid, (1, 1), (w-2, h-2)

def make_grid_case_maze(w=40, h=20):
    # Caso 2: tipo laberinto con pasillos (A* mejora menos, a veces similar)
    grid = [[0]*w for _ in range(h)]
    # bordes
    for x in range(w):
        grid[0][x] = 1
        grid[h-1][x] = 1
    for y in range(h):
        grid[y][0] = 1
        grid[y][w-1] = 1

    # paredes verticales con huecos
    for x in range(4, w-4, 4):
        for y in range(1, h-1):
            grid[y][x] = 1
        gap = 2 + (x // 4) % (h-4)
        grid[gap][x] = 0
        grid[gap+1][x] = 0

    start = (1, 1)
    goal = (w-2, h-2)
    grid[start[1]][start[0]] = 0
    grid[goal[1]][goal[0]] = 0
    return grid, start, goal

if __name__ == "__main__":
    grid1, s1, g1 = make_grid_case_open()
    run_case("CASE 1: OPEN FIELD", grid1, s1, g1)

    grid2, s2, g2 = make_grid_case_maze()
    run_case("CASE 2: MAZE-LIKE", grid2, s2, g2)
