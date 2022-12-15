import copy
f = open("input", "r")

monkeysStart = dict()
currentMonkeyId = 0
currentMonkeyObject = { "inspectionCount": 0}
for line in f.readlines():
    line = line.strip()
    if "Monkey" in line:
        continue

    if "Starting items:" in line:
        items = line.split(": ")[1].split(", ")
        items = [int(x) for x in items]
        currentMonkeyObject["items"] = items
    
    if "Operation: " in line:
        op = line.split(" = ")[1]
        currentMonkeyObject["op"] = op
    
    if "Test: " in line:
        divisibleBy = line.split("divisible by")[1]
        divisibleBy = int(divisibleBy)
        currentMonkeyObject["divisibleBy"] = divisibleBy

    if "true: " in line:
        testPasses = line.split("throw to monkey ")[1]
        testPasses = int(testPasses)
        currentMonkeyObject["testPasses"] = testPasses
    
    if "false: " in line:
        testFails = line.split("throw to monkey ")[1]
        testFails = int(testFails)
        currentMonkeyObject["testFails"] = testFails

    if line == "":
        monkeysStart[currentMonkeyId] = currentMonkeyObject
        currentMonkeyObject = { "inspectionCount": 0}
        currentMonkeyId += 1

# Add the last monkey
monkeysStart[currentMonkeyId] = currentMonkeyObject

# Returns the old value as an int if the value is "old"
# Otherwise returns in the int value
def convertOpValue(value, old):
    if value == "old":
        return old
    else:
        return int(value)

def operate(old, op):
    if " * " in op:
        lhs, rhs = op.split(" * ")
        lhs = convertOpValue(lhs, old)
        rhs = convertOpValue(rhs, old)
        return lhs * rhs
    elif " + " in op:
        lhs, rhs = op.split(" + ")
        lhs = convertOpValue(lhs, old)
        rhs = convertOpValue(rhs, old)
        return lhs + rhs

# manageWorryLevels is to handle Part 2 where we don't divide worryLevel by 3
def runRound(monkeys, manageWorryLevels = True, worryLevelMod = 0):
    # Go through the items in the list of each Monkey
    for monkey in monkeys.values():
        # print(monkey)
        while (len(monkey["items"]) > 0):
            monkey["inspectionCount"] += 1
            worryLevel = monkey["items"].pop(0)
            newWorry = operate(worryLevel, monkey["op"])
            if manageWorryLevels:
                newWorry = newWorry // 3
            else:
                newWorry = newWorry % worryLevelMod 
            if (newWorry % monkey["divisibleBy"]) == 0:
                throwTo = monkey["testPasses"]
            else:
                throwTo = monkey["testFails"]
            monkeys[throwTo]["items"].append(newWorry)
    return monkeys


# Monkeys is the collection of monkeys
# monkeys[x] =
#   items = Queue of items the monkey holds pop(0).
#   op = string e.g. old * old | old * 13.
#   divisibleBy = The test the monkey uses to determine who to throw to.
#   testPasses = The number of the monkey to throw to if the test passes.
#   testFails = The number of the monkey to throw to if the test fails.
def part1():
    monkeys = copy.deepcopy(monkeysStart)
    currentRound = 0
    numOfRounds = 20
    while currentRound < numOfRounds:
        monkeys = runRound(monkeys)
        # print(monkeys[0])
        currentRound += 1
    
    inspectionCounts = []
    for monkey in monkeys.values():
        inspectionCounts.append(monkey["inspectionCount"])
    
    inspectionCounts.sort()
    inspectionCounts.reverse()
    return inspectionCounts[0] * inspectionCounts[1]

# Instead of going round each monkey every round
# Can we iterate around each item to simulate 1,000 rounds instead?
def part2():
    monkeys = copy.deepcopy(monkeysStart)
    worryMod = 1
    for monkey in monkeys.values():
        worryMod *= monkey["divisibleBy"]

    currentRound = 0
    numOfRounds = 10000
    while currentRound < numOfRounds:
        monkeys = runRound(monkeys, manageWorryLevels=False, worryLevelMod=worryMod)
        currentRound += 1
    inspectionCounts = []
    for monkey in monkeys.values():
        inspectionCounts.append(monkey["inspectionCount"])
    
    inspectionCounts.sort()
    inspectionCounts.reverse()
    return inspectionCounts[0] * inspectionCounts[1]
    
print("PART 1:", part1())
print("PART 2:", part2())
