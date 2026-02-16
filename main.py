import heapq
import sys
import time
import pygame
import random

from collections import deque

def set_speed(grid, cols, rows):
	for y in range(rows):
		for x in range(cols):
			if (grid[y][x] == 1):
				grid[y][x] = random.randint(1, 9)
	return grid

def walls(start, goal, cols, rows, wall_probability = 0.35):
	grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
	for y in range(rows):
		for x in range(cols):
			if (x,y) != start and (x,y) != goal:
				if random.random() < wall_probability:
					grid[y][x] = 0

	grid[start[1]][start[0]] = -1
	grid[goal[1]][goal[0]] = -2	

	return grid

def mark_path(grid, start, goal, cols, rows):
	next_cells = deque()
	visited_cells = set()
	next_cells.append(start)
	while next_cells:
		x, y = next_cells.popleft()
		if (x, y) in visited_cells:
			continue
		visited_cells.add((x, y))
		if (x, y) == goal:
			return grid
		if (x + 1 >= 0 and x + 1 < cols and grid[y][x + 1] != 0):
			next_cells.append((x + 1, y))
			grid[y][x + 1] = 200
		if (x - 1 >= 0 and x - 1 < cols and grid[y][x - 1] != 0):
			next_cells.append((x - 1, y))
			grid[y][x - 1] = 200
		if (y + 1 >= 0 and y + 1 < rows and grid[y + 1][x] != 0):
			next_cells.append((x, y + 1))
			grid[y + 1][x] = 200
		if (y - 1 >= 0 and y - 1 < rows and grid[y - 1][x] != 0):
			next_cells.append((x, y - 1))
			grid[y - 1][x] = 200

def mark_path_see(grid, start, goal, cols, rows, screen, cell, width, height):
	next_cells = deque()
	visited_cells = set()
	next_cells.append(start)
	while next_cells:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return None
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return None
		x, y = next_cells.popleft()
		if (x, y) in visited_cells:
			continue
		visited_cells.add((x, y))
		if (x, y) == goal:
			return grid
		if (x + 1 >= 0 and x + 1 < cols and grid[y][x + 1] != 0):
			next_cells.append((x + 1, y))
			pygame.draw.rect(screen, (0, 0, 140), ((x + 1) * cell, y * cell, cell, cell))
			pygame.display.flip()
			pygame.time.delay(2)
		if (x - 1 >= 0 and x - 1 < cols and grid[y][x - 1] != 0):
			next_cells.append((x - 1, y))
			pygame.draw.rect(screen, (0, 0, 140), ((x - 1) * cell, y * cell, cell, cell))
			pygame.display.flip()
			pygame.time.delay(2)
		if (y + 1 >= 0 and y + 1 < rows and grid[y + 1][x] != 0):
			next_cells.append((x, y + 1))
			pygame.draw.rect(screen, (0, 0, 140), (x * cell, (y + 1) * cell, cell, cell))
			pygame.display.flip()
			pygame.time.delay(2)
		if (y - 1 >= 0 and y - 1 < rows and grid[y - 1][x] != 0):
			next_cells.append((x, y - 1))
			pygame.draw.rect(screen, (0, 0, 140), (x * cell, (y - 1) * cell, cell, cell))
			pygame.display.flip()
			pygame.time.delay(2)
		for x in range(COLS + 1):
			pygame.draw.line(screen, (30, 30, 30), (x * cell, 0), (x * cell, height))
		for y in range(ROWS + 1):
			pygame.draw.line(screen, (30, 30, 30), (0, y * cell), (width, y * cell))

def has_path(grid, start, goal, cols, rows):
	next_cells = deque()
	visited_cells = set()
	next_cells.append(start)
	while next_cells:
		x, y = next_cells.popleft()
		if (x, y) in visited_cells:
			continue
		visited_cells.add((x, y))
		if (x, y) == goal:
			return grid
		if (x + 1 >= 0 and x + 1 < cols and grid[y][x + 1] != 0):
			next_cells.append((x + 1, y))
		if (x - 1 >= 0 and x - 1 < cols and grid[y][x - 1] != 0):
			next_cells.append((x - 1, y))
		if (y + 1 >= 0 and y + 1 < rows and grid[y + 1][x] != 0):
			next_cells.append((x, y + 1))
		if (y - 1 >= 0 and y - 1 < rows and grid[y - 1][x] != 0):
			next_cells.append((x, y - 1))

	return None


def vecinos(point, cols, rows):
	vecinos_matriz = []
	x, y = point
	if (x + 1 >= 0 and x + 1 < cols):
		vecinos_matriz.append([x + 1, y])
	if (x - 1 >= 0 and x - 1 < cols):
		vecinos_matriz.append([x - 1, y])
	if (y + 1 >= 0 and y + 1 < rows):
		vecinos_matriz.append([x, y + 1])
	if (y - 1 >= 0 and y - 1 < rows):
		vecinos_matriz.append([x, y - 1])
	return vecinos_matriz

def vecinos_dijkstra(point, cols, rows):
	vecinos_matriz = []
	x, y = point
	if (x + 1 >= 0 and x + 1 < cols):
		vecinos_matriz.append([x + 1, y])
	if (x - 1 >= 0 and x - 1 < cols):
		vecinos_matriz.append([x - 1, y])
	if (y + 1 >= 0 and y + 1 < rows):
		vecinos_matriz.append([x, y + 1])
	if (y - 1 >= 0 and y - 1 < rows):
		vecinos_matriz.append([x, y - 1])
	return vecinos_matriz

def take_path(start, goal, came_from):
	path = []
	point = goal
	while point != start:
		point = came_from[point]
		path.append(point)
	path.reverse()
	return path

def dijkstra(grid, start, goal, cols, rows):
	
	dist = {(start): 0}
	came_from = {}
	pq = [(0, (start))]
	visited = set()


	while True:
		if not pq:
			break
		distance, point = heapq.heappop(pq)
		if point == goal:
			#print(f"Win? {distance}")
			#print(f"{came_from}")
			path = take_path(start, goal, came_from)
			#print(path)
			return path
		if point in visited:
			continue
		visited.add(point)
		vecinos_matriz = vecinos_dijkstra(point, cols, rows)
		for x, y in vecinos_matriz:
			if (x, y) in visited:
				continue
			if grid[y][x] == 0:
				continue
			if grid[y][x] < 0:
				value = 0
			else:
				value = grid[y][x]
			nuevo_valor = value + distance
			if dist.get((x, y)) is None:
				came_from[(x, y)] = (point)
				dist[(x, y)] = nuevo_valor
			elif nuevo_valor < dist[(x, y)]:
				came_from[(x, y)] = (point)
				dist[(x, y)] = nuevo_valor
			heapq.heappush(pq, (nuevo_valor, (x, y)))

def mark_path_dijkstra(grid, path):
	for x, y in path:
		grid[y][x] = 300
	return grid

def mark_dijkstra_see(grid, goal, start, cols, rows, screen, cell, width, height):
	dist = {(start): 0}
	pq = [(0, (start))]
	visited = set()


	while True:
		if not pq:
			break
		distance, point = heapq.heappop(pq)
		if point == goal:
			break
		if point in visited:
			continue
		pygame.draw.rect(screen, (0, 0, 140), (point[0] * cell, point[1] * cell, cell, cell))
		pygame.display.flip()
		pygame.time.delay(2)
		for x in range(COLS + 1):
			pygame.draw.line(screen, (30, 30, 30), (x * cell, 0), (x * cell, height))
		for y in range(ROWS + 1):
			pygame.draw.line(screen, (30, 30, 30), (0, y * cell), (width, y * cell))
		visited.add(point)
		vecinos_matriz = vecinos_dijkstra(point, cols, rows)
		for x, y in vecinos_matriz:
			if (x, y) in visited:
				continue
			if grid[y][x] == 0:
				continue
			if grid[y][x] < 0:
				value = 0
			else:
				value = grid[y][x]
			nuevo_valor = value + distance
			if dist.get((x, y)) is None:
				dist[(x, y)] = nuevo_valor
			elif nuevo_valor < dist[(x, y)]:
				dist[(x, y)] = nuevo_valor
			heapq.heappush(pq, (nuevo_valor, (x, y)))

def heuristica_a(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_func(grid, start, goal, cols, rows):
	
	dist = {(start): 0}
	came_from = {}
	pq = [(0, (start))]
	visited = set()


	while True:
		if not pq:
			break
		distance, point = heapq.heappop(pq)
		if point == goal:
			#print(f"Win? {distance}")
			#print(f"{came_from}")
			path = take_path(start, goal, came_from)
			#print(path)
			return path
		if point in visited:
			continue
		visited.add(point)
		vecinos_matriz = vecinos_dijkstra(point, cols, rows)
		for x, y in vecinos_matriz:
			if (x, y) in visited:
				continue
			if grid[y][x] == 0:
				continue
			if grid[y][x] < 0:
				value = 0
			else:
				value = grid[y][x]
			nuevo_valor = value + distance
			if dist.get((x, y)) is None:
				came_from[(x, y)] = (point)
				dist[(x, y)] = nuevo_valor
			elif nuevo_valor < dist[(x, y)]:
				came_from[(x, y)] = (point)
				dist[(x, y)] = nuevo_valor
			heuristica = heuristica_a((x, y), goal)
			heapq.heappush(pq, (nuevo_valor + heuristica, (x, y)))

def mark_path_a(grid, path):
	for x, y in path:
		grid[y][x] = 300
	return grid

def mark_a_see(grid, goal, start, cols, rows, screen, cell, width, height):
	dist = {(start): 0}
	pq = [(0, (start))]
	visited = set()


	while True:
		if not pq:
			break
		distance, point = heapq.heappop(pq)
		if point == goal:
			break
		if point in visited:
			continue
		pygame.draw.rect(screen, (0, 0, 140), (point[0] * cell, point[1] * cell, cell, cell))
		pygame.display.flip()
		pygame.time.delay(2)
		for x in range(COLS + 1):
			pygame.draw.line(screen, (30, 30, 30), (x * cell, 0), (x * cell, height))
		for y in range(ROWS + 1):
			pygame.draw.line(screen, (30, 30, 30), (0, y * cell), (width, y * cell))
		visited.add(point)
		vecinos_matriz = vecinos_dijkstra(point, cols, rows)
		for x, y in vecinos_matriz:
			if (x, y) in visited:
				continue
			if grid[y][x] == 0:
				continue
			if grid[y][x] < 0:
				value = 0
			else:
				value = grid[y][x]
			nuevo_valor = value + distance
			if dist.get((x, y)) is None:
				dist[(x, y)] = nuevo_valor
			elif nuevo_valor < dist[(x, y)]:
				dist[(x, y)] = nuevo_valor
			heuristica = heuristica_a((x, y), goal)
			heapq.heappush(pq, (nuevo_valor + heuristica, (x, y)))
		
	


pygame.init()

CELL = 10
COLS, ROWS = 190, 100
#CELL = 20
#COLS, ROWS = 20, 20
W, H = COLS * CELL, ROWS * CELL

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Grid editor (click para paredes)")

clock = pygame.time.Clock()

while True:
	while True:

		start_x = random.randrange(COLS)
		start_y = random.randrange(ROWS)
		goal_x = random.randrange(COLS)
		goal_y = random.randrange(ROWS)
		if (abs(start_x - goal_x) > 3 and abs(start_y - goal_y) > 3):
			break


	start = (start_x, start_y)
	goal = (goal_x, goal_y)

	grid_original = walls(start, goal, COLS, ROWS)
	grid_original = has_path(grid_original, start, goal, COLS, ROWS)
	if grid_original is not None:
		break
grid = grid_original
grid_auxiliar_path = [row[:] for row in grid_original]
grid_auxiliar_path = mark_path(grid_auxiliar_path, start, goal, COLS, ROWS)
grid_auxiliar_speed = [row[:] for row in grid_original]
grid_auxiliar_speed = set_speed(grid_auxiliar_speed, COLS, ROWS)
grid_auxiliar_dijkstra = [row[:] for row in grid_original]
grid_dijkstra = [row[:] for row in grid_original]
path_dijkstra = dijkstra(grid_dijkstra, start, goal, COLS, ROWS)
grid_dijkstra = mark_path_dijkstra(grid_dijkstra, path_dijkstra)
grid_auxiliar_a = [row[:] for row in grid_original]
grid_a = [row[:] for row in grid_original]
path_a = a_func(grid_a, start, goal, COLS, ROWS)
grid_a = mark_path_a(grid_a, path_a)

grid_path_color = False
grid_speed= False
grid_color = False
running = True
grid_path_dijkstra = False
grid_path_a = False

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:  # salir
				running = False
			if event.key == pygame.K_z:  # marca el path
				grid_path_color = not grid_path_color
				if grid_path_color:
					grid = grid_auxiliar_path
				else:
					grid = grid_original
			if event.key == pygame.K_x:  # limpiar todo
				mark_path_see(grid_original, start, goal, COLS, ROWS, screen, CELL, W, H)
			if event.key == pygame.K_c:
				grid_color = not grid_color
			if event.key == pygame.K_v:
				grid_path_dijkstra = False
				grid_path_a = False
				grid_speed = not grid_speed
				if grid_speed:
					grid = grid_auxiliar_speed
				else:
					grid = grid_original
				grid_auxiliar_dijkstra = [row[:] for row in grid]
				grid_dijkstra = [row[:] for row in grid]
				path_dijkstra = dijkstra(grid_dijkstra, start, goal, COLS, ROWS)
				grid_dijkstra = mark_path_dijkstra(grid_dijkstra, path_dijkstra)
				grid_auxiliar_a = [row[:] for row in grid]
				grid_a = [row[:] for row in grid]
				path_a = a_func(grid_a, start, goal, COLS, ROWS)
				grid_a = mark_path_a(grid_a, path_a)
			if event.key == pygame.K_b:
				mark_dijkstra_see(grid_auxiliar_dijkstra, goal, start, COLS, ROWS, screen, CELL, W, H)
			if event.key == pygame.K_g:
				grid_path_a = False
				grid_path_dijkstra = not grid_path_dijkstra
				if grid_path_dijkstra:
					grid = grid_dijkstra
				else:
					if grid_speed:
						grid = grid_auxiliar_speed
					else:
						grid = grid_original
			if event.key == pygame.K_n:
				mark_a_see(grid_auxiliar_a, goal, start, COLS, ROWS, screen, CELL, W, H)
			if event.key == pygame.K_a:
				grid_path_dijkstra = False
				grid_path_a = not grid_path_a
				if grid_path_a:
					grid = grid_a
				else:
					if grid_speed:
						grid = grid_auxiliar_speed
					else:
						grid = grid_original

	# --- Draw ---
	screen.fill((15, 15, 15))

	# celdas (paredes)
	for y in range(ROWS):
		for x in range(COLS):
			if grid[y][x] == 0:
				pygame.draw.rect(screen, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL))

	for y in range(ROWS):
			for x in range(COLS):
				if grid[y][x] == 300:
					pygame.draw.rect(screen, (0, 0, 140), (x * CELL, y * CELL, CELL, CELL))
	if grid_color:
		for y in range(ROWS):
			for x in range(COLS):
				if grid[y][x] == 200:
					pygame.draw.rect(screen, (0, 0, 140), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 100:
					pygame.draw.rect(screen, (40, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 1:
					pygame.draw.rect(screen, (0, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 2:
					pygame.draw.rect(screen, (40, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 3:
					pygame.draw.rect(screen, (80, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 4:
					pygame.draw.rect(screen, (120, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 5:
					pygame.draw.rect(screen, (160, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 6:
					pygame.draw.rect(screen, (200, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 7:
					pygame.draw.rect(screen, (240, 140, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 8:
					pygame.draw.rect(screen, (240, 180, 0), (x * CELL, y * CELL, CELL, CELL))
				elif grid[y][x] == 9:
					pygame.draw.rect(screen, (240, 220, 0), (x * CELL, y * CELL, CELL, CELL))




	# start / goal
	pygame.draw.rect(screen, (0, 255, 255), (start[0] * CELL, start[1] * CELL, CELL, CELL))
	pygame.draw.rect(screen, (255, 0, 0), (goal[0] * CELL, goal[1] * CELL, CELL, CELL))

	# líneas del grid
	for x in range(COLS + 1):
		pygame.draw.line(screen, (30, 30, 30), (x * CELL, 0), (x * CELL, H))
	for y in range(ROWS + 1):
		pygame.draw.line(screen, (30, 30, 30), (0, y * CELL), (W, y * CELL))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
