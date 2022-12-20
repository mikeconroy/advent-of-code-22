from queue import PriorityQueue
import math
import sys
f = open("input", "r")

heightMap = []
for y, line in enumerate(f.readlines()):
    line = line.strip()
    row = []
    for x, char in enumerate(line):
        if char == "S":
            start = (x,y)
            value = 0
        elif char == "E":
            end = (x, y)
            value = 26
        else:
            value = ord(char) - 97
        row.append(value)
    heightMap.append(row)


# def findShortestPath(start, target, distances, processing):
#     currentHeight = heightMap[start[1]][start[0]]

#     processing[start] = True
#     if start == target:
#         distances[target] = 0
#         return 0
#     if start in distances:
#         return distances[start]
#     up = (start[0], start[1] + 1)
#     down = (start[0], start[1] - 1)
#     right = (start[0] + 1, start[1])
#     left = (start[0] - 1, start[1])

#     surroundingCells = []
#     for cell in [up, down, right, left]:
#         if cell[0] < 0 or cell[0] >= len(heightMap[0]):
#             continue
#         if cell[1] < 0 or cell[1] >= len(heightMap):
#             continue
#         if cell in processing and cell not in distances:
#             continue
#         cellHeight = heightMap[cell[1]][cell[0]]
#         if currentHeight == cellHeight or currentHeight == cellHeight - 1:
#             findShortestPath(cell, target, distances, processing)
#             if cell in distances:
#                 surroundingCells.append(distances[cell])
#     else:
#         distance = min(surroundingCells) + 1
#     distances[start] = distance
#     return distance

# Not the best approach by a long shot.
# AStar / Dijkstra implemented afterwards.
def findShortestDistance(start, target, distances):
    sys.setrecursionlimit(5000)

    if start == target:
        distances[target] = distances[start] + 1
        return

    up = (start[0], start[1] + 1)
    down = (start[0], start[1] - 1)
    right = (start[0] + 1, start[1])
    left = (start[0] - 1, start[1])

    for cell in [up, down, right, left]:
        if cell[0] < 0 or cell[0] >= len(heightMap[0]):
            continue
        if cell[1] < 0 or cell[1] >= len(heightMap):
            continue
        cellHeight = heightMap[cell[1]][cell[0]]
        currentHeight = heightMap[start[1]][start[0]]
        # This line caused several hours of debugging due to misunderstanding requirements...
        # if currentHeight == cellHeight or currentHeight == cellHeight - 1:
        if cellHeight <= currentHeight + 1:
            if cell in distances:
                if distances[cell] > distances[start] + 1:
                    distances[cell] = distances[start] + 1
                    findShortestDistance(cell, target, distances)
            else:
                distances[cell] = distances[start] + 1
                findShortestDistance(cell, target, distances)

def reconstructPath(cameFrom, current):
    totalPath = set()
    totalPath.add(current)
    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.add(current)
    return totalPath

def getNeighbours(start, upwards=True):
    validNeighbours = []
    up = (start[0], start[1] + 1)
    down = (start[0], start[1] - 1)
    right = (start[0] + 1, start[1])
    left = (start[0] - 1, start[1])
    for cell in [up, down, right, left]:
        if cell[0] < 0 or cell[0] >= len(heightMap[0]):
            continue
        if cell[1] < 0 or cell[1] >= len(heightMap):
            continue
        cellHeight = heightMap[cell[1]][cell[0]]
        currentHeight = heightMap[start[1]][start[0]]
        if upwards:
            if cellHeight <= currentHeight + 1:
                validNeighbours.append(cell)
        else:
            if cellHeight >= currentHeight - 1:
                validNeighbours.append(cell)
    return validNeighbours

def aStar(start, target, upwards=True):
    openSetQ = PriorityQueue()
    openSetQ.put((0, start))
    openSet = set()
    openSet.add(start)
    cameFrom = dict()
    gScore = dict()
    gScore[start] = 0
    while not openSetQ.empty():
        current = openSetQ.get()[1]
        openSet.remove(current)
        if current in target:
            return reconstructPath(cameFrom, current)
        
        for neighbour in getNeighbours(current, upwards):
            tentativeGScore = gScore[current] + 1
            if tentativeGScore < gScore.get(neighbour, float('inf')):
                cameFrom[neighbour] = current
                gScore[neighbour] = tentativeGScore
                if neighbour not in openSet:
                    openSet.add(neighbour)
                    openSetQ.put((gScore[neighbour], neighbour))
    return "ERROR"

def part1():
    distances = dict()
    distances[start] = 0
    # Too Slow
    # findShortestDistance(start, end, distances)
    # return distances[end] - 1
    path = aStar(start, {end})
    return len(path) - 1

def part2():
    target = set()
    for y, row in enumerate(heightMap):
        for x, height in enumerate(row):
            if height == 0:
                target.add((x, y))
    path = aStar(end, target, upwards=False)
    return len(path) - 1
    
print("PART 1:", part1())
print("PART 2:", part2())
