f = open("input", "r")

inputArray = []
for line in f.readlines():
    inputArray.append(line.strip())

def part1():
    numOfPairs = 0
    for pair in inputArray:
        firstElf, secondElf = pair.split(",")
        firstElfStart, firstElfEnd = firstElf.split("-")
        secondElfStart, secondElfEnd = secondElf.split("-")
        firstElfStart = int(firstElfStart)
        firstElfEnd = int(firstElfEnd)
        secondElfStart = int(secondElfStart)
        secondElfEnd = int(secondElfEnd)
        if (firstElfStart <= secondElfStart
            and firstElfEnd >= secondElfEnd):
            numOfPairs += 1        
        elif (secondElfStart <= firstElfStart
               and secondElfEnd >= firstElfEnd):
            numOfPairs += 1
    return numOfPairs

def part2():
    numOfPairs = 0
    for pair in inputArray:
        firstElf, secondElf = pair.split(",")
        firstElfStart, firstElfEnd = firstElf.split("-")
        secondElfStart, secondElfEnd = secondElf.split("-")
        firstElfStart = int(firstElfStart)
        firstElfEnd = int(firstElfEnd)
        secondElfStart = int(secondElfStart)
        secondElfEnd = int(secondElfEnd)
        firstSet = set(range(firstElfStart, firstElfEnd + 1))
        secondSet = set(range(secondElfStart, secondElfEnd + 1))
        if len(firstSet.intersection(secondSet)) != 0:
            numOfPairs += 1
    return numOfPairs

print("PART 1:", part1())
print("PART 2:", part2())