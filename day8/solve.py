f = open("input", "r")

# grid[y][x]
grid = []
for index, line in enumerate(f.readlines()):
    line = line.strip()
    grid.append([])
    for tree in line:
        grid[index].append(tree)

# Digit = Tree Height
# 0 is shortest
# 9 is tallest
# A tree is visible if all of the other trees between it
# and an edge of the grid are shorter than it.
# All of the trees around the edge of the grid are visible.

# Count the number of visible trees
# Up, Down, Left, Right

# Quick and dirty approach
def part1():
    # Set will hold (x, y) tuple
    treesSeen = set()

    # Look across each row
    for y, row in enumerate(grid):
        # Look Right
        currentTallest = row[0]
        treesSeen.add((0, y))
        # print("RIGHT")
        for x, tree in enumerate(row):
            # print("X", x, "Y", y, "Height", grid[y][x], "Tallest", currentTallest)
            if tree > currentTallest:
                currentTallest = tree
                treesSeen.add((x, y))

        # Look Left
        row.reverse()
        # print("LEFT")
        currentTallest = row[0]
        treesSeen.add((len(row) - 1, y))
        for x, tree in enumerate(row):
            # print("X", x, "Y", y, "Height", tree, "Tallest", currentTallest)
            if tree > currentTallest:
                currentTallest = tree
                # print("Adding", (len(row) - 1 - x,y))
                treesSeen.add((len(row) - 1 - x, y))
            
        row.reverse()

    # Look Up/Down
    rowCount = len(grid)
    for x in range(0, len(grid[0])):
        currentTallest = grid[0][x]
        treesSeen.add((x, 0))
        # print("DOWN")
        for y in range(0, rowCount):
            # print("X", x, "Y", y, "Height", grid[y][x], "Tallest", currentTallest)
            if grid[y][x] > currentTallest:
                currentTallest = grid[y][x]
                # print("Adding", (x,y))
                treesSeen.add((x, y))

        # print("UP")
        currentTallest = grid[rowCount - 1][x]
        treesSeen.add((x, rowCount - 1, ))
        # print("Adding", (x, rowCount - 1, ))
        for y in range(rowCount - 1, -1, -1):
            # print("X", x, "Y", y, "Height", grid[y][x], "Tallest", currentTallest)
            if grid[y][x] > currentTallest:
                currentTallest = grid[y][x]
                # print("Adding", (x,y))
                treesSeen.add((x, y))
    #     print(len(treesSeen))


    # print(treesSeen)
    # print(len(treesSeen))
    return len(treesSeen)

def lookRightScore(x, y, height):
    score = 0
    for index in range(x + 1, len(grid[y])):
        # print("Index", index, "Height", grid[y][index])
        if (grid[y][index] >= height):
            score += 1
            break
        else:
            score += 1
    # print("RIGHT", score)
    return score

def lookLeftScore(x, y, height):
    score = 0
    for index in range(x, 0, -1):
        index = index - 1
        # print("Index", index, "Height", grid[y][index])
        if grid[y][index] >= height:
            score += 1
            break
        else:
            score += 1
    # print("LEFT", score)
    return score

def lookDownScore(x, y, height):
    score = 0
    # Increase Y by 1 until we reach the end of the grid
    for index in range(y + 1, len(grid)):
        # print("Index", index, "Height", grid[index][x])
        if grid[index][x] >= height:
            score += 1
            break
        else:
            score += 1
    # print("DOWN", score)
    return score

def lookUpScore(x, y, height):
    score = 0
    # Decrease Y by 1 until we reach 0
    for index in range(y, 0, -1):
        index = index - 1
        if grid[index][x] >= height:
            score += 1
            break
        else:
            score += 1
    # print("UP", score)
    return score

def part2():
    highestScenicScore = 0

    for y, row in enumerate(grid):
        for x, height in enumerate(grid[y]):
            # print("X", x, "Y", y, "Height", height)
            currentScenicScore = lookRightScore(x, y, height)
            currentScenicScore *= lookLeftScore(x, y, height)
            currentScenicScore *= lookDownScore(x, y, height)
            currentScenicScore *= lookUpScore(x, y, height)
            
            if currentScenicScore > highestScenicScore:
                highestScenicScore = currentScenicScore

    return highestScenicScore

print("PART 1:", part1())
print("PART 2:", part2())