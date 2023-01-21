f = open("input", "r")

jets = []
for jet_direction in f.readline():
    jet_direction = jet_direction.strip()
    jets.append(jet_direction)

# Tetrominos
# Stores the relative (to the 'floor') starting position of the shapes as Tuples (x, y)
rocks = [
    #   @@@@
    {(2, 4), (3, 4), (4, 4), (5, 4)},

    #   .@.
    #   @@@
    #   .@.
    {(3, 4), (2, 5), (3, 5), (4, 5), (3, 6)},
    
    #   ..@
    #   ..@
    #   @@@
    {(2, 4), (3, 4), (4, 4), (4, 5), (4, 6)},

    #   @
    #   @
    #   @
    #   @
    {(2, 4), (2, 5), (2, 6), (2, 7)},

    #   @@
    #   @@
    {(2, 4), (3, 4), (2, 5), (3, 5)}
]

# TODO: Needs to create the rock 3 blocks higher than the current height
def create_falling_rock(rock_type, current_height):
    falling_rock = set()
    for point in rock_type:
        new_point = (point[0], point[1] + current_height)
        falling_rock.add(new_point)
    return falling_rock

def shift_rock(rock, jet, settled_rocks):
    direction = 1 if jet == '>' else -1

    new_rock = set()
    for point in rock:
        new_point = (point[0] + direction, point[1])
        if new_point[0] > 6 or new_point[0] < 0:
            return rock
        new_rock.add(new_point)

    # Ensure the jet didn't push the rock into an existing rock
    if new_rock.isdisjoint(settled_rocks):
        return new_rock
    else:
        return rock

def drop_rock(rock, settled_rocks):
    new_rock = set()
    for point in rock:
        new_point = (point[0], point[1] - 1)
        if new_point in settled_rocks:
            return rock, False
        else:
            new_rock.add(new_point)
    return new_rock, True

def get_height(settled_rocks):
    height = 0
    for point in settled_rocks:
        if point[1] > height:
            height = point[1]
    
    return height

def print_grid(settled_rocks):
    height = get_height(settled_rocks)

    for y in range (height, 0, -1):
        for x in range(0, 7):
            if (x,y) in settled_rocks:
                print('#', end='')
            else:
                print('.', end='')
        print()

def part1(target):

    num_jets = len(jets)
    rocks_dropped = 0
    jet_index = 0
    current_height = 0
    # Set of settled Rocks - starting with the floor:
    settled_rocks = {(0,0), (1,0), (2,0),(3,0),(4,0),(5,0),(6,0)}

    while rocks_dropped < target:
        # Rocks Dropped increases by 1 for every new rock.
        # Mod 5 gives us the appropriate shape to spawn.
        rock_type = rocks[rocks_dropped % 5]

        # Create a new rock so we don't modify the shapes array
        rock = create_falling_rock(rock_type, current_height)
        
        # Shift Rock in the appropriate direction based on the jet
        able_to_drop = True
        while able_to_drop:
            jet = jets[jet_index % num_jets]
            rock = shift_rock(rock, jet, settled_rocks)
            rock, able_to_drop = drop_rock(rock, settled_rocks)
            jet_index += 1

        settled_rocks.update(rock)
        current_height = get_height(settled_rocks)
        rocks_dropped += 1
        if rocks_dropped % 100_000 == 0:
            print(rocks_dropped, current_height)
    return current_height

# Repeat part 1 but for 1_000_000_000_000 Rocks...
# Ideas -
#   Don't need to store the full grid of settled rocks.
#   Just store the heighest point in each 'column'.
#   This would reduce the number of checks required on each drop (only check 7 points). 
#   Can't loop around 1 Trillion times...
def part2():
    return 0
    
print("PART 1:", part1(2022))
print("PART 2:", part2())
