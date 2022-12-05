import copy

f = open("input", "r")

inputArray = []
for line in f.readlines():
    inputArray.append(line)

# Move Creates between Stacks
#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 
# 
# 3 Stacks of Crates
# move 1 from 2 to 1
# Results in:
# [D]        
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 
# 
# Moves the top crate(s) over

# 3 Chars + 1 Space = 4 Chars per Stack
# No space added to the last stack so +1
noOfStacks = (len(inputArray[0]) + 1) // 4
stacks = [list() for i in range(noOfStacks)]

for stack in inputArray:
    # Check if we have reached the end of the stacks.
    if "[" not in stack:
        break
    # Iterate over a stack (4 chars) at a time
    for itemIndex in range(1, noOfStacks*4, 4):
        if stack[itemIndex] != " ":
            stacks[itemIndex // 4].append(stack[itemIndex])
    
for stack in stacks:
    stack.reverse()

def part1():
    outputStacks = copy.deepcopy(stacks)
    for instruction in inputArray:
        instruction = instruction.strip()
        if "move" not in instruction:
            continue
        numToMove, location = instruction.split(" from ")
        numToMove = int(numToMove.replace("move ",""))
        start, destination = location.split(" to ")
        # Substract 1 due to array indexing starting at 0
        start = int(start) - 1
        destination = int(destination) - 1
        for i in range(numToMove):
            outputStacks[destination].append(outputStacks[start].pop())
    
    # Create output string by popping off the top of each stack
    output = ""
    for stack in outputStacks:
        output += stack.pop()
    return output
    
def part2():
    outputStacks = copy.deepcopy(stacks)
    for instruction in inputArray:
        instruction = instruction.strip()
        if "move" not in instruction:
            continue
        numToMove, location = instruction.split(" from ")
        numToMove = int(numToMove.replace("move ",""))
        start, destination = location.split(" to ")
        # Substract 1 due to array indexing starting at 0
        start = int(start) - 1
        destination = int(destination) - 1
        cratesToMove = []
        for i in range(numToMove):
            cratesToMove.append(outputStacks[start].pop())
        cratesToMove.reverse()
        outputStacks[destination].extend(cratesToMove)
    
    # Create output string by popping off the top of each stack
    output = ""
    for stack in outputStacks:
        output += stack.pop()
    return output

print("PART 1:", part1())
print("PART 2:", part2())