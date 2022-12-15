f = open("input", "r")

instructions = []
for line in f.readlines():
    line = line.strip()
    instructions.append(line)

# Made global as it is reused in Part 2
cycleMap = dict()
def part1():
    tick = 0
    x = 1
    global cycleMap
    cycleMap[0] = x
    for instruction in instructions:
        if instruction == "noop":
            tick += 1
            cycleMap[tick] = x
        else:
            op, value = instruction.split(" ")
            value = int(value)
            if op == "addx":
                cycleMap[tick + 1] = x
                cycleMap[tick + 2] = x
                tick += 2
                x += value
                cycleMap[tick] = x

    twenty = 20 * cycleMap[19]
    sixty = 60 * cycleMap[59]
    hundredth = 100 * cycleMap[99]
    onefourty = 140 * cycleMap[139]
    oneeighty = 180 * cycleMap[179]
    twotwenty = 220 * cycleMap[219]

    return sum([twenty, sixty, hundredth, onefourty, oneeighty, twotwenty])

def part2():
    print("PART 2:")
    x = 0
    cycleMap.pop(240)
    for cycle in cycleMap:
        cycleVal = cycleMap[cycle]
        if cycleVal >= x - 1 and cycleVal <= x + 1:
            print("#", end="")
        else:
            print(".", end="")
        x += 1
        if x % 40 == 0:
            print("")
            x = 0
    return 0

print("PART 1:", part1())
part2()
