import pygame
import random

from collections import deque


def mark_path(grid, start, goal, cols, rows):
	sx, sy = start
	gx, gy = goal

	q = deque([(sx, sy)])
	visited = set([(sx, sy)])

	while q:
		x, y = q.popleft()
		if (x, y) == (gx, gy):
			break

		for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
			nx, ny = x + dx, y + dy
			if 0 <= nx < cols and 0 <= ny < rows:
				if (nx, ny) not in visited and grid[ny][nx] != 0:  # 1 = pared
					visited.add((nx, ny))
					grid[ny][nx] = 200
					q.append((nx, ny))

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
	
	grid = has_path(grid, start, goal, cols, rows)
	return grid


pygame.init()

# --- Config ---
CELL = 10
COLS, ROWS = 190, 100  # 32*25=800, 24*25=600
"""CELL = 20
COLS, ROWS = 20, 20"""
W, H = COLS * CELL, ROWS * CELL

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Grid editor (click para paredes)")

clock = pygame.time.Clock()


while True:

	xstart = random.randrange(COLS)
	ystart = random.randrange(ROWS)
	xgoal = random.randrange(COLS)
	ygoal = random.randrange(ROWS)
	if (abs(xstart - xgoal) > 3 and abs(ystart - ygoal) > 3):
		break


start = (xstart, ystart)
goal = (xgoal, ygoal)

grid = walls(start, goal, COLS, ROWS)

def cell_from_mouse(pos):
	mx, my = pos
	return mx // CELL, my // CELL

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		"""elif event.type == pygame.MOUSEBUTTONDOWN:
			x, y = cell_from_mouse(event.pos)
			if 0 <= x < COLS and 0 <= y < ROWS:
				if event.button == 1:  # click izq: alterna pared
					if (x, y) != start and (x, y) != goal:
						grid[y][x] = 1 - grid[y][x]
				elif event.button == 3:  # click dcho: limpia
					if (x, y) != start and (x, y) != goal:
						grid[y][x] = 1

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:  # limpiar todo
				grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]"""

	# --- Draw ---
	screen.fill((15, 15, 15))

	# celdas (paredes)
	for y in range(ROWS):
		for x in range(COLS):
			if grid[y][x] == 0:
				pygame.draw.rect(screen, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL))

	for y in range(ROWS):
		for x in range(COLS):
			if grid[y][x] == 200:
				pygame.draw.rect(screen, (0, 0, 140), (x * CELL, y * CELL, CELL, CELL))

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
