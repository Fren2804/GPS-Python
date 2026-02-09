import pygame
import random

from collections import deque


def set_speed(grid, cols, rows):
	for y in range(rows):
		for x in range(cols):
			if (grid[y][x] == 1):
				grid[y][x] = random.randint(2, 9)
	return grid


def mark_path(grid, start, goal, cols, rows):
	sx, sy = start
	gx, gy = goal

	q = deque([(sx, sy)])
	visited = set([(sx, sy)])

	while q:
		actual_x, actual_y = q.popleft()
		if (actual_x, actual_y) == (gx, gy):
			break

		for (d_x, d_y) in ((1,0), (-1,0), (0,1), (0,-1)):
			new_x = actual_x + d_x
			new_y = actual_y + d_y
			if (new_x >= 0 and new_x < cols) and (new_y >= 0 and new_y < rows):
				if (new_x, new_y) not in visited and grid[new_y][new_x] != 0:
					q.append((new_x, new_y))
					visited.add((new_x, new_y))
					grid[new_y][new_x] = 200

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
	
	#grid = mark_path(grid, start, goal, cols, rows)
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

	start_x = random.randrange(COLS)
	start_y = random.randrange(ROWS)
	goal_x = random.randrange(COLS)
	goal_y = random.randrange(ROWS)
	if (abs(start_x - goal_x) > 3 and abs(start_y - goal_y) > 3):
		break


start = (start_x, start_y)
goal = (goal_x, goal_y)

grid = walls(start, goal, COLS, ROWS)
grid = set_speed(grid, start, goal, COLS, ROWS)

def cell_from_mouse(pos):
	mx, my = pos
	return mx // CELL, my // CELL

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
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
				grid = mark_path(grid, start, goal, COLS, ROWS)

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
			"""elif grid[y][x] == 2:
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
				pygame.draw.rect(screen, (240, 220, 0), (x * CELL, y * CELL, CELL, CELL))"""



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
