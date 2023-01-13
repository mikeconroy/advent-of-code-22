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

def getManhattanDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Gives an answer in 20 Seconds by focusing on the row the question requests.
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
        # This check will be important for part 2 (scanning row by row)
        # Confirms whether the sensor distance is in range of the row being scanned
        if (abs(sensor[1]) + distance) >= y:
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

def calculateSensorDistances(sensorToBeacon):
    sensorToBeaconDistance = dict()
    for sensor in sensorToBeacon:
        sensorToBeaconDistance[sensor] = getManhattanDistance(sensor, sensorToBeacon[sensor])
    return sensorToBeaconDistance

def isInRange(cell, sensor, distance):
    if getManhattanDistance(cell, sensor) <= distance:
        return True
    else:
        return False

# Calculates the new Column/X that the search can skip to in that row.
def skipTo(currentCell, sensor, distance):
    return sensor[0] + (distance - abs(sensor[1] - currentCell[1]))

def findDistressBeacon(distressBeaconSearchSpace, sensorSet, beaconSet, sensorToBeaconDistance):
    # Loop around each cell in the search space
    for y in range(distressBeaconSearchSpace[0], distressBeaconSearchSpace[1] + 1):
        # We need to loop through x 'manually' as we need to skip values at certain points.
        x = 0
        while x < distressBeaconSearchSpace[1]:
            currentCell = (x,y)
            # Skip cells which are already sensors or beacons.
            if currentCell not in sensorSet and currentCell not in beaconSet:
                # Check each sensor for any in range of the current cell
                sensorInRangeFound = False
                for sensor in sensorToBeaconDistance:
                    if isInRange(currentCell, sensor, sensorToBeaconDistance[sensor]):
                        sensorInRangeFound = True
                        x = skipTo(currentCell, sensor, sensorToBeaconDistance[sensor])
                if sensorInRangeFound == False:
                    return currentCell
            x += 1
    return None

# Distress Beacon is between (0, 0) (0, 4_000_000) (4_000_000, 0) (4_000_000, 4_000_000)
# Tuning Frequecy = (x * 4_000_000) + y
# Brute Force with an optimization of skipping X Values when a sensor in range is found.
# We are able to skip based on the symmetry of the manhattan distance.
# Finds an answer in: 180 Seconds
def part2(distressBeaconSearchSpace=(0, 4_000_000)):
    grid, sensorSet, beaconSet, sensorToBeacon = createGrid()

    sensorToBeaconDistance = calculateSensorDistances(sensorToBeacon)

    distressBeacon = findDistressBeacon(distressBeaconSearchSpace,
                                        sensorSet,
                                        beaconSet,
                                        sensorToBeaconDistance)
    return (distressBeacon[0] * 4_000_000) + distressBeacon[1]
    
# print("PART 1:", part1(y=10))
# print("PART 2:", part2((0, 20)))
print("PART 1:", part1())
print("PART 2:", part2())

# More efficient ways for Part 2:
# Search around the perimeters of Sensors: https://www.reddit.com/r/adventofcode/comments/zmfwg1/2022_day_15_part_2_seekin_for_the_beacon/
# Use Line Intersections (borders) to locate the distress beacon: https://www.reddit.com/r/adventofcode/comments/zmw9d8/comment/j0dhu1w/?utm_source=share&utm_medium=web2x&context=3
# Merge ranges of sensors for each row: https://www.reddit.com/r/adventofcode/comments/zmtpwz/comment/j0dcmtc/?utm_source=share&utm_medium=web2x&context=3