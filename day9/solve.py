f = open("input", "r")

instructions = []
for line in f.readlines():
    line = line.strip()
    instructions.append(line)

# Updated to accept an array of tails for Part 2
def processInstruction(instruction, head, tails, visited):
    direction, steps = instruction.split(" ")
    steps = int(steps)

    for step in range(0, steps):
        # print(direction, step)
        if direction == "R":
            head = (head[0] + 1, head[1])
        elif direction == "L":
            head = (head[0] - 1, head[1])
        elif direction == "U":
            head = (head[0], head[1] + 1)
        elif direction == "D":
            head = (head[0], head[1] - 1)
        # Process the first tail
        tails[0] = moveTail(head, tails[0])
        # visited.add(tails[0])

        # Process the remaining tails in the array
        for index, tail in enumerate(tails):
            if index == 0:
                continue
            tails[index] = moveTail(tails[index - 1], tails[index])
        visited.add(tails[len(tails) - 1])
    return head, tails

# Check whether we need to move tail or not
def isTailOneStepFromHead(head, tail):
    # Check Tail X is within 1 step of head X
    if (tail[0] >= head[0] - 1 and tail[0] <= head[0] + 1):
        # Check Tail Y is within 1 step of tail Y
        if (tail[1] >= head[1] - 1 and tail[1] <= head[1] + 1):
            # print("Tail within one step of Head")
            return True
    return False

def moveTail(head, tail):
    if isTailOneStepFromHead(head, tail):
        return tail
    # Calculate Tail Move
    # Calculate new X for Tail
    newX = tail[0]
    if head[0] != tail[0]:
        if tail[0] < head[0]:
            newX += 1
        else:
            newX -= 1
    # Calculate new Y for Tail
    newY = tail[1]
    if head[1] != tail[1]:
        if tail[1] < head[1]:
            newY += 1
        else:
            newY -= 1
    tail = (newX, newY)
    return tail

def part1():
    visited = set()
    head = (0,0)
    tail = [(0,0)]
    for instruction in instructions:
        head, tail = processInstruction(instruction, head, tail, visited)
    return len(visited)

def printGrid(head, tails):
    for y in range(head[0] - 20, head[0] + 20):
        for x in range(head[1] - 20, head[1] + 20):
            printed = False
            if head == (x,y):
                print("H", end="")
            else:
                for index, tail in enumerate(tails):
                    if tail == (x, y):
                        printed = True
                        print(index, end="")
                        break
            if not printed:
                print(".",end="")
        print("")
    print("")

def part2():
    visited = set()
    head = (0,0)
    tails = [(0,0) for x in range(9)]
    for instruction in instructions:
        head, tails = processInstruction(instruction, head, tails, visited)
        # printGrid(head, tails)
    return len(visited)

print("PART 1:", part1())
print("PART 2:", part2())