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

def get_new_heights(last_rock_settled, current_height, current_heights=[]):
    for point in last_rock_settled:
        if point[1] > current_height:
            current_height = point[1]
        # Only used in Part 2:
        if current_heights and current_heights[point[0]] < point[1]:
            current_heights[point[0]] = point[1]
    return current_height, current_heights

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
        current_height = get_new_heights(rock, current_height)[0]
        rocks_dropped += 1

    return current_height

def remove_points_below_floor(settled_rocks):
    heights = [0 for x in range(0,7)]
    new_points = dict()
    for point in settled_rocks:
        if point[1] >= heights[point[0]]:
            heights[point[0]] = point[1]
            new_points[point[0]] = point
    
    return set(new_points.values())

def settle_rock(rock, settled_rocks):
    # TODO: THIS IS BROKEN - OR some part of the code after is broken.
    # Trying to just track the highest points in each column.
    # Any point below one of these points shouldn't be required.
    # This is likely failing as column 0 could be height 0 whilst column 1 height 100.
    # Allowing Rocks to slip through gaps.
    settled_rocks.update(rock)
    heights = [0 for x in range(0,7)]
    new_points = dict()
    for point in settled_rocks:
        if point[1] >= heights[point[0]]:
            heights[point[0]] = point[1]
            new_points[point[0]] = point

    return set(new_points.values())

def get_relative_heights(current_heights, current_height):
    relative_heights = []
    for height in current_heights:
        relative_heights.append(height - current_height)
    return tuple(relative_heights)

# Repeat part 1 but for 1_000_000_000_000 Rocks...
# Ideas -
#   Don't need to store the full grid of settled rocks.
#   Just store the heighest point in each 'column'.
#   This would reduce the number of checks required on each drop (only check 7 points). 
#   Can't loop around 1 Trillion times...

# Does the cycle ever repeat?
#   If we hit a point where the jet_index & shape have been seen before then
#   We can take that current height and multiply the cycle n times as it would reach the same height?
#   ... The floor would also need to be the same pattern
# Track the current floor Pattern?? For the state & cycle check?
# Current floor y_values=[0,0,0,0,0,0,0]
# Always keep them relative to column 0?
def part2():
    target = 1_000_000_000_000
    num_jets = len(jets)
    rocks_dropped = 0
    jet_index = 0
    current_height = 0
    # Set of settled Rocks - starting with the floor:
    settled_rocks = {(0,0), (1,0), (2,0),(3,0),(4,0),(5,0),(6,0)}

    # An array where each element represents a column.
    # Column 0 will always be 0 and the rest relative to that column.
    current_heights = [0, 0, 0, 0, 0, 0, 0]
    cached_states = dict()
    cycle_hit = False
    cycle_length = 0
    cycle_height = 0
    height_added_in_cycle = 0
    height_at_cycle = 0
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
        current_height, current_heights = get_new_heights(rock, current_height, current_heights)
        rocks_dropped += 1
        relative_heights = get_relative_heights(current_heights, current_height)
        state = (rocks_dropped % 5, jet_index % num_jets, relative_heights)

        if state in cached_states and cycle_hit == False:
            cycle_hit = True
            # Amount of height added in the cycle
            cycle_height = current_height - cached_states[state][0]
            # Number of rocks dropped in the cycle
            cycle_length = rocks_dropped - cached_states[state][1]
            times_to_repeat_cycle = (target - rocks_dropped) // cycle_length
            print(" Cycle Hit.")
            print(" Rocks Dropped:", rocks_dropped)
            print(" Rocks Dropped at Cycle Start:", (rocks_dropped - cycle_length))
            print(" Cycle Length:", cycle_length)
            print(" Cycle Height:", cycle_height)
            print(" Cached State (height, rocks_dropped):", cached_states[state])
            print(" Repeat Cycle:", times_to_repeat_cycle)
            height_added_in_cycle = cycle_height * times_to_repeat_cycle
            rocks_dropped += (cycle_length * times_to_repeat_cycle)
            print(" Rocks Dropped:", rocks_dropped)
            print(" Height Added:", height_added_in_cycle)
            next
        else:
            cached_states[state] = (current_height, rocks_dropped)

    current_height += height_added_in_cycle
    print(" Rocks Dropped:", rocks_dropped)
    return current_height
    
print("PART 1:", part1(2022))
print("PART 2:", part2())
