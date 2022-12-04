f = open("input", "r")

inputArray = []
for line in f.readlines():
    inputArray.append(line.strip())

priorities = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    
    "A": 27,
    "B": 28,
    "C": 29,
    "D": 30,
    "E": 31,
    "F": 32,
    "G": 33,
    "H": 34,
    "I": 35,
    "J": 36,
    "K": 37,
    "L": 38,
    "M": 39,
    "N": 40,
    "O": 41,
    "P": 42,
    "Q": 43,
    "R": 44,
    "S": 45,
    "T": 46,
    "U": 47,
    "V": 48,
    "W": 49,
    "X": 50,
    "Y": 51,
    "Z": 52,
}

# 2 Large Compartments
# Items of a given type in 1 of the compartments
# Failed for 1 item per rucksack
# Input - list of items in a rucksack (each line)
# Rucksack has same no. of items in each compartment
# First half of line = Compartment 1
# Second half of line = Compartment 2
# The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp,
# which means its first compartment contains the items vJrwpWtwJgWr,
# while the second compartment contains the items hcsFMMfFFhFp.
# The only item type that appears in both compartments is lowercase p.
def part1():
    sumOfPriorities = 0
    for rucksack in inputArray:
        firstComp, secondComp = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]
        firstCompSet = set(firstComp)
        secondCompSet = set(secondComp)
        repeatedItemSet = firstCompSet.intersection(secondCompSet)
        repeatedItem = repeatedItemSet.pop()
        sumOfPriorities += priorities[repeatedItem]
    return sumOfPriorities

def part2():
    sumOfPriorities = 0
    for rucksackIndex in range(0, len(inputArray), 3):
        firstRucksack = set(inputArray[rucksackIndex])
        secondRucksack = set(inputArray[rucksackIndex + 1])
        thirdRucksack = set(inputArray[rucksackIndex + 2])
        badgeItem = firstRucksack.intersection(secondRucksack).intersection(thirdRucksack)
        sumOfPriorities += priorities[badgeItem.pop()]
    return sumOfPriorities

print("PART 1:", part1())
print("PART 2:", part2())