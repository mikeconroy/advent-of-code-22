f = open("input", "r")

directoryMap = dict()
directoryMap["/"] = {"name": "/", "size": 0, "subItems": [], "isDirectory": True}
currentDirectory = directoryMap["/"]
currentDirectory["parent"] = currentDirectory
input = []
for line in f.readlines():
    line = line.strip()
    if "$ " in line:
        if " cd " in line:
            if ".." in line:
                currentDirectory = currentDirectory["parent"]
                parentDirectory = currentDirectory["parent"]
            else: 
                parentDirectory = currentDirectory
                newDirectoryName = line.split("cd ")[1]
                for dir in currentDirectory["subItems"]:
                    if dir["name"] == newDirectoryName:
                        currentDirectory = dir
    elif "dir " in line:
        name = line.split(" ")[1]
        details = \
            {
                "name": name,
                "size": 0,
                "parent": currentDirectory,
                "subItems": [],
                "isDirectory": True
            }
        currentDirectory["subItems"].append(details)
    else:
        size, name = line.split(" ")
        size = int(size)
        currentDirectory["subItems"].append(\
            {
                "name": name,
                "size": size,
                "parent": currentDirectory,
                "isDirectory": False
            }
        )

def calcDirSizes(currentDir):
    subItems = currentDir["subItems"]
    currentSize = 0
    for item in subItems:
        if item["isDirectory"] == False:
            currentSize += int(item["size"])
        else:
            currentSize += calcDirSizes(item)
    currentDir["size"] = currentSize
    return currentSize

rootDirectory = directoryMap["/"]
calcDirSizes(rootDirectory)

sumDirs = 0
def sumDirsBelowSize(currentDir, threshold):
    global sumDirs
    if currentDir["isDirectory"] == False:
        return 
    if currentDir["size"] <= threshold:
        sumDirs += currentDir["size"]
    for dir in currentDir["subItems"]:
        sumDirsBelowSize(dir, threshold)

def part1():
    sumDirsBelowSize(directoryMap["/"], 100000)
    return sumDirs
    
def smallestDirAboveSize(currentDir, sizeRequired, currentSmallest):
    currentDirSize = currentDir["size"]
    if currentDirSize > sizeRequired and currentDirSize < currentSmallest:
        currentSmallest = currentDirSize
    
    for dir in currentDir["subItems"]:
        if dir["isDirectory"]:
            currentSmallest = smallestDirAboveSize(dir, sizeRequired, currentSmallest)

    return currentSmallest

def part2():
    TOTAL_SPACE = 70_000_000
    SPACE_REQUIRED = 30_000_000
    SPACE_USED = rootDirectory["size"]
    DELETE_AMOUNT = SPACE_REQUIRED - (TOTAL_SPACE - SPACE_USED)
    return smallestDirAboveSize(directoryMap["/"], DELETE_AMOUNT, SPACE_USED)

print("PART 1:", part1())
print("PART 2:", part2())