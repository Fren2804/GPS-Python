import pygame


import heapq

def neighbors(p, cols, rows):
	x, y = p
	if x > 0: yield (x - 1, y)
	if x < cols - 1: yield (x + 1, y)
	if y > 0: yield (x, y - 1)
	if y < rows - 1: yield (x, y + 1)

def reconstruct(came_from, start, goal):
	cur = goal
	path = [cur]
	while cur != start:
		cur = came_from.get(cur)
		if cur is None:
			return None
		path.append(cur)
	path.reverse()
	return path

def dijkstra(grid, start, goal, cols, rows):
	INF = 10**18
	dist = {start: 0}
	came_from = {}
	pq = [(0, start)]
	visited = set()

	while pq:
		d, u = heapq.heappop(pq)
		if u in visited:
			continue
		visited.add(u)

		if u == goal:
			return reconstruct(came_from, start, goal)

		for v in neighbors(u, cols, rows):
			x, y = v
			if grid[y][x] == 1:   # pared
				continue
			nd = d + 1
			if nd < dist.get(v, INF):
				dist[v] = nd
				came_from[v] = u
				heapq.heappush(pq, (nd, v))

	return None

def heuristic(a, b):
    # distancia Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal, cols, rows):
    INF = 10**18
    gscore = {start: 0}
    came_from = {}
    pq = [(heuristic(start, goal), 0, start)]
    visited = set()

    while pq:
        f, g, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        if u == goal:
            return reconstruct(came_from, start, goal)

        for v in neighbors(u, cols, rows):
            x, y = v
            if grid[y][x] == 1:
                continue

            ng = g + 1
            if ng < gscore.get(v, INF):
                gscore[v] = ng
                came_from[v] = u
                nf = ng + heuristic(v, goal)
                heapq.heappush(pq, (nf, ng, v))

    return None


pygame.init()

# --- Config ---
CELL = 25
COLS, ROWS = 32, 24  # 32*25=800, 24*25=600
W, H = COLS * CELL, ROWS * CELL

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Grid editor (click para paredes)")

clock = pygame.time.Clock()

# 0 = libre, 1 = pared
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (2, 2)
goal = (COLS - 3, ROWS - 3)

def cell_from_mouse(pos):
	mx, my = pos
	return mx // CELL, my // CELL

running = True
use_astar = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			x, y = cell_from_mouse(event.pos)
			if 0 <= x < COLS and 0 <= y < ROWS:
				# Click izquierdo: pared
				if event.button == 1:
					if (x, y) != start and (x, y) != goal:
						grid[y][x] = 1 - grid[y][x]
				# Click derecho: mover GOAL
				elif event.button == 3:
					if grid[y][x] == 0:
						goal = (x, y)
				# Click rueda: mover START
				elif event.button == 2:
					if grid[y][x] == 0:
						start = (x, y)


		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:  # limpiar todo
				grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
			elif event.key == pygame.K_1:
				use_astar = False
			elif event.key == pygame.K_2:
				use_astar = True

	if use_astar:
		path = astar(grid, start, goal, COLS, ROWS)
	else:
		path = dijkstra(grid, start, goal, COLS, ROWS)


	# --- Draw ---
	screen.fill((15, 15, 15))

	# celdas (paredes)
	for y in range(ROWS):
		for x in range(COLS):
			if grid[y][x] == 1:
				pygame.draw.rect(screen, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL))

	if path:
		for (x, y) in path:
			if (x, y) != start and (x, y) != goal:
				pygame.draw.rect(screen, (40, 90, 160), (x * CELL, y * CELL, CELL, CELL))

	# start / goal
	pygame.draw.rect(screen, (0, 140, 0), (start[0] * CELL, start[1] * CELL, CELL, CELL))
	pygame.draw.rect(screen, (140, 0, 0), (goal[0] * CELL, goal[1] * CELL, CELL, CELL))

	# líneas del grid
	for x in range(COLS + 1):
		pygame.draw.line(screen, (30, 30, 30), (x * CELL, 0), (x * CELL, H))
	for y in range(ROWS + 1):
		pygame.draw.line(screen, (30, 30, 30), (0, y * CELL), (W, y * CELL))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
