import copy
from functools import cmp_to_key

f = open("input", "r")

pairs = []
pair = []
for line in f.readlines():
    line = line.strip()
    if line == "":
        pairs.append(pair)
        pair = []
    else:
        pair.append(line)

pairs.append(pair)
pair = []

def parse(signal):
    index = 0
    nestedLevel = 0
    listAtLevel = dict()
    while index < len(signal):
        currentChar = signal[index]
        if currentChar == "[":
            nestedLevel += 1
            listAtLevel[nestedLevel] = []
        elif currentChar == "]":
            if nestedLevel == 1:
                return listAtLevel[1]
            listAtLevel[nestedLevel - 1].append(copy.deepcopy(listAtLevel[nestedLevel]))
            listAtLevel[nestedLevel] = []
            nestedLevel -= 1
        elif currentChar != ",":
            nextChar = signal[index + 1]
            # Handle Double Digits
            # Probably could have split by commas earlier on
            if nextChar.isdigit():
                currentChar += nextChar
                index += 1
            listAtLevel.get(nestedLevel, []).append(int(currentChar))
        index += 1
    return listAtLevel[1]

# True if first is smaller than second
def pairsAreInOrder(first, second):
    index = 0
    while True:
        if index >= len(first) and index < len(second):
            return 1
        if index >= len(second) and index < len(first):
            return -1
        if index >= len(first) and index >= len(second):
            return 0

        firstItem = first[index]
        secondItem = second[index]
        if type(firstItem) == int and type(secondItem) == int:
            if firstItem < secondItem:
                return 1
            elif firstItem > secondItem:
                return -1
        else:
            firstItem = firstItem if type(firstItem) == list else [firstItem]
            secondItem = secondItem if type(secondItem) == list else [secondItem]
            result = pairsAreInOrder(firstItem, secondItem)
            if result == 1:
                return 1
            elif result == -1:
                return -1
        index += 1

def part1():
    result = 0
    for index, pair in enumerate(pairs):
        first = parse(pair[0])
        second = parse(pair[1])
        inOrder = pairsAreInOrder([first], [second])
        if inOrder == 1:
            result += index + 1
    return result

def part2():
    flatList = []
    dividerPacket1 = [[2]]
    dividerPacket2 = [[6]]
    for pair in pairs:
        flatList.append(parse(pair[0]))
        flatList.append(parse(pair[1]))
    flatList.append(dividerPacket1)
    flatList.append(dividerPacket2)
    flatList.sort(reverse=True, key=cmp_to_key(pairsAreInOrder))
    
    divider1Index = flatList.index(dividerPacket1) + 1
    divider2Index = flatList.index(dividerPacket2) + 1

    return divider1Index * divider2Index
    
print("PART 1:", part1())
print("PART 2:", part2())
