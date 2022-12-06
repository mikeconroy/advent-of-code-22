f = open("input", "r")

input = f.readline()

# Lock onto signal
# Signal is a series of 'seemingly' random chars.
# Start of a packet is a sequence of 4 chars that are different.
# First position where the 4 last were different


# Find Start of Packet Marker
def getStartOfPacket(buffer, uniqueChars):
    for index, char in enumerate(buffer):
        # Check previous X unique chars
        duplicateFound = False
        setOfPreviousChars = set(char)
        for i in range(1, uniqueChars):
            if i > index:
                duplicateFound = True
                break
            charToCheck = buffer[index - i]
            if charToCheck in setOfPreviousChars:
                duplicateFound = True
                break
            setOfPreviousChars.add(charToCheck)
        if not duplicateFound:
            return index + 1

def part1():
    return getStartOfPacket(input, 4)
    
def part2():
    return getStartOfPacket(input, 14)

print("PART 1:", part1())
print("PART 2:", part2())