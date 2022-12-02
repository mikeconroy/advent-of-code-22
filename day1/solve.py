f = open("input", "r")

highestCals = 0
currentCals = 0
elvesCals = []
for line in f.readlines():
    if line == "\n":
        if currentCals > highestCals:
            highestCals = currentCals
        elvesCals.append(currentCals)
        currentCals = 0
    else:
        currentCals += int(line)

if currentCals > highestCals:
    highestCals = currentCals
elvesCals.append(currentCals)
currentCals = 0

elvesCals.sort(reverse=True)
print("PART 1:", highestCals)
print("PART 2:", elvesCals[0] + elvesCals[1] + elvesCals[2])