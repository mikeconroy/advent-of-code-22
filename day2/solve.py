f = open("input", "r")

inputArray = []
for line in f.readlines():
    inputArray.append(line.strip())

# Rock = 1
# Paper = 2
# Scissors = 3
scores = {
    "A": 1,
    "B": 2,
    "C": 3
}

defeats = {
    "A": "C",
    "B": "A",
    "C": "B"
}

losesTo = {
    "A": "B",
    "B": "C",
    "C": "A"  
}

# Rock = X = A
# Paper = Y = B
# Scissors = Z = C
def part1():
    translation = {
        "X": "A",
        "Y": "B",
        "Z": "C"
    }

    totalScore = 0
    for game in inputArray:
        game = game.split(" ")
        oppMove = game[0]
        myMove = translation[game[1]]
        gameScore = scores[myMove]
        if oppMove == defeats[myMove]:
            gameScore += 6
        elif oppMove == myMove:
            gameScore += 3
        totalScore += gameScore
    return totalScore

# OUTCOMES
# Lose = X
# Draw = Y
# Win = Z
def part2():
    totalScore = 0
    for game in inputArray:
        game = game.split(" ")
        oppMove = game[0]
        outcome = game[1]
        gameScore = 0
        # Draw
        if outcome == "Y":
            gameScore += 3
            myMove = oppMove
        # Win
        elif outcome == "Z":
            gameScore += 6
            myMove = losesTo[oppMove]
        # Lose
        else:
            myMove = defeats[oppMove]

        gameScore += scores[myMove]
        totalScore += gameScore
    return totalScore

print("PART 1:", part1())
print("PART 2:", part2())