import copy
f = open("input", "r")

inputArray = []
for line in f.readlines():
    line = line.strip()
    inputArray.append(line)

def createGrid():
    grid = dict()
    for path in inputArray:
        rocks = path.split(" -> ")
        lastX, lastY = rocks[0].split(",")
        lastX = int(lastX)
        lastY = int(lastY)
        for rock in rocks:
            x, y = rock.split(",")
            x = int(x)
            y = int(y)
            grid[(x,y)] = "#"

            if x != lastX:
                if x > lastX:
                    for diff in range(lastX, x):
                        grid[(diff, y)] = "#"
                else:
                    for diff in range(x, lastX):
                        grid[(diff, y)] = "#"

            if y != lastY:
                if y > lastY:
                    for diff in range(lastY, y):
                        grid[(x, diff)] = "#"
                else:
                    for diff in range(y, lastY):
                        grid[(x, diff)] = "#"

            lastX, lastY = x,y
    grid[(500, 0)] = "+"
    return grid

def printGrid(grid):
    # Get Lowest X value
    points = grid.keys()
    lowestX = float('inf')
    lowestY = float('inf')
    highestX = float('-inf')
    highestY = float('-inf')

    for point in points:
        if point[0] < lowestX:
            lowestX = point[0]
        elif point[0] > highestX:
            highestX = point[0]
        
        if point[1] < lowestY:
            lowestY = point[1]
        elif point[1] > highestY:
            highestY = point[1]
    for y in range(0, highestY + 2):
        for x in range(lowestX - 1, highestX + 2):
            print(grid.get((x,y), "."), end="")
        print()

def getHighestY(grid):
    highestY = float('-inf')
    for point in grid.keys():
        if point[1] > highestY and grid[point] == "#":
            highestY = point[1]
    return highestY

highestY = 0

def dropGrain(grid, source, highestY, part=1):
    canBeDropped = True
    x = source[0]
    y = source[1]
    while canBeDropped:
        if grid.get((x, y + 1), ".") == ".":
            y += 1
        else:
            if grid.get((x - 1, y + 1), ".") == ".":
                x -= 1
                y += 1
            elif grid.get((x + 1, y + 1), ".") == ".":
                x += 1
                y += 1
            else:
                canBeDropped = False
        if part == 1 and y > highestY:
            return(x,y)
        if part == 2 and y > highestY:
            grid[(x, y)] = "o"
            return (x, y)
                       
    grid[(x, y)] = "o"
    return (x, y)

def part1():
    grid = createGrid()
    grainsDropped = 0
    lastGrainY = 0
    highestY = getHighestY(grid)
    while lastGrainY < getHighestY(grid):
        lastGrainY = dropGrain(grid, (500, 0), highestY)[1]
        grainsDropped += 1
    return grainsDropped - 1

def part2():
    grid = createGrid()
    grainsDropped = 0
    lastGrain = (0,0)
    highestY = getHighestY(grid)
    while lastGrain != (500, 0):
        lastGrain = dropGrain(grid, (500, 0), highestY, part=2)
        grainsDropped += 1
    return grainsDropped
    
print("PART 1:", part1())
print("PART 2:", part2())
