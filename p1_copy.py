import heapq


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

def vecinos(point):
	vecinos_matriz = []
	x, y = point
	if (x + 1 >= 0 and x + 1 < 6):
		vecinos_matriz.append([x + 1, y])
	if (x - 1 >= 0 and x - 1 < 6):
		vecinos_matriz.append([x - 1, y])
	if (y + 1 >= 0 and y + 1 < 6):
		vecinos_matriz.append([x, y + 1])
	if (y - 1 >= 0 and y - 1 < 6):
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
		
	



"""matriz = [
    [-2, 3, 2, 9],
    [1, 7, 3, 8],
    [6, 5, 2, 1],
    [0, 3, 4, -1]
]"""

"""matriz = [
    [-2, 4, 1, 3, 9, 2, 8, 6, 3],
    [7, 8, 2, 1, 4, 3, 7, 2, 5],
    [6, 3, 5, 9, 2, 8, 1, 4, 7],
    [5, 7, 2, 6, 3, 4, 9, 1, 8],
    [9, 1, 8, 2, 7, 5, 3, 6, 4],
    [3, 6, 4, 8, 1, 9, 2, 7, 5],
    [8, 2, 7, 4, 6, 1, 5, 3, 9],
    [4, 9, 3, 5, 8, 7, 6, 2, 1],
    [2, 5, 6, 7, 3, 4, 1, 8, -1]
]"""

"""matriz = [
    [-2, 2, 5, 1],
    [4, 8, 2, 3],
    [1, 2, 4, 7],
    [6, 3, 1, -2]
]"""

matriz = [
    [-2, 3, 1, 8, 6, 4],
    [5,     9, 2, 1, 7, 3],
    [4,     6, 5, 2, 8, 1],
    [7,     2, 3, 9, 4, 6],
    [8,     5, 7, 3, 2, 9],
    [1,     4, 6, 5, 3, -2]
]

start = (0,0)
goal = (5,5)


dist = {(0,0): 0}
came_from = {}
pq = [(0, (0,0))]
visited = set()


while True:
	if not pq:
		break
	distance, point = heapq.heappop(pq)
	if point == goal:
		print(f"Win? {distance}")
		print(f"{came_from}")
		path = take_path(start, goal, came_from)
		print(path)
		break
	if point in visited:
		continue
	visited.add(point)
	vecinos_matriz = vecinos(point)
	for x, y in vecinos_matriz:
		if (x, y) in visited:
			continue
		if matriz[x][y] < 0:
			value = 0
		else:
			value = matriz[x][y]
		nuevo_valor = value + distance
		"""if nuevo_valor < dist.get((x, y), INF):
    came_from[(x, y)] = point
    dist[(x, y)] = nuevo_valor
    heapq.heappush(pq, (nuevo_valor, (x, y)))"""
		if dist.get((x, y)) is None:
			came_from[(x, y)] = (point)
			dist[(x, y)] = nuevo_valor
		elif nuevo_valor < dist[(x, y)]:
			came_from[(x, y)] = (point)
			dist[(x, y)] = nuevo_valor
		heapq.heappush(pq, (nuevo_valor, (x, y)))