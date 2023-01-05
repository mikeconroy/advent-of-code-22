import copy
f = open("input", "r")

inputArray = []
for line in f.readlines():
    line = line.strip()
    inputArray.append(line)

def createGrid():
    grid = dict()
    sensorSet = set()
    beaconSet = set()
    sensorToBeacon = dict()
    for line in inputArray:
        sensorPart, beaconPart = line.split(":")
        sensorY = int(sensorPart.split("y=")[1])
        sensorX = int(sensorPart.split(",")[0].split("x=")[1])
        sensor = (sensorX, sensorY)
        grid[sensor] = "S"
        sensorSet.add(sensor)

        beaconY = int(beaconPart.split("y=")[1])
        beaconX = int(beaconPart.split(",")[0].split("x=")[1])
        beacon = (beaconX, beaconY)
        grid[beacon] = "B"
        beaconSet.add(beacon)
        sensorToBeacon[sensor] = beacon
    return grid, sensorSet, beaconSet, sensorToBeacon

def getManhattanDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Updates all cells within (or equal to) the manhattan distance from the sensor to beacon
# It does this by looping through each cell within the square surrounding the sensor
# Square contains all cells within MHD including squares that aren't.
# This is too inefficient for the numbers in the puzzle.
# Search Area = 2_545_543_666_576 for the first sensor...
# Not Used
def updateNonBeaconCells(grid, sensor, beacon):
    print(sensor, beacon)
    distance = getManhattanDistance(sensor, beacon)
    searchArea = distance * distance
    print(distance)
    print(searchArea)
    for y in range(sensor[1] - searchArea, sensor[1] + searchArea):
        for x in range(sensor[0] - searchArea, sensor[0] + searchArea):
            cellToUpdate = (x, y)
            if getManhattanDistance(sensor, cellToUpdate) <= distance:
                if grid.get(cellToUpdate, ".") == ".":
                    grid[cellToUpdate] = "#"
    return grid

# Gives an answer in 22 Seconds by focusing on the row the question requests.
def part1(y=2_000_000):
    # Grid is a HashMap of coordinates where Sensors & Beacons are
    # Key Coordinate Tuple (x,y) -> Value is B for Beacon or S for Sensor
    # A potentially quicker option is to use 2 Sets.
    # 1 Set containing Sensor Coordinates
    # 1 Set containing Beacon Coordinates
    # This could be more efficient when checking if a coordinate is a Beacon
    grid, sensorSet, beaconSet, sensorToBeacon = createGrid()
    lowestX = float('inf')
    highestX = float('-inf')
    for sensor in sensorToBeacon:
        # grid = updateNonBeaconCells(grid, sensor, sensorToBeacon[sensor])
        distance = getManhattanDistance(sensor, sensorToBeacon[sensor])
        if (abs(sensor[1]) + distance) >= 10:
            for x in range(sensor[0] - distance, sensor[0] + distance):
                if getManhattanDistance(sensor, (x, y)) <= distance and grid.get((x, y), ".") == ".":
                    grid[(x, y)] = "#"
                    if x < lowestX:
                        lowestX = x
                    if x > highestX:
                        highestX = x

    noBeaconCount = 0
    for x in range(lowestX - 1, highestX + 2):
        value = grid.get((x, y), ".")
        # print(value, end="")
        if value == "#" or value == "S":
            noBeaconCount += 1

    return noBeaconCount

def part2():
    return 0
    
# print("PART 1:", part1(y=10))
print("PART 1:", part1())
print("PART 2:", part2())
