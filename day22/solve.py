f = open("input", "r")

input_array = []
for line in f.readlines():
    line = line.replace("\n", "")
    input_array.append(line)

# Last line is the path
path_str = input_array.pop()
# Remove empty line betwee Grid & Path
input_array.pop()
grid_str = input_array
num_cols = max([len(row) for row in grid_str])
num_rows = len(grid_str)
    
def parse_path(path_str):
    path = []
    buffer = ""
    for char in path_str:
        if char.isnumeric():
            buffer += char
                
        else:
            if buffer != "":
                path.append(int(buffer))
                buffer = ""
            path.append(char)
    if buffer != "":
        path.append(int(buffer))
    return path

def parse_grid(grid_str):
    grid = dict()
    for y, row in enumerate(grid_str):
        row_length = len(row)
        for x in range(num_cols):
            grid[(x,y)] = row[x] if x < row_length else " "
    return grid

def print_grid(grid):
    for y in range(len(grid_str)):
        for x in range(num_cols):
            print(grid[(x, y)], end="")
        print()

def get_start_point(grid):
    y = 0
    for x in range(num_cols):
        if grid[(x,y)] == ".":
            return (x,y)

# Facing Direction
#   R = (1,0)       Turn R = D Turn L = U
#   L = (-1, 0)     Turn R = U Turn L = D
#   U = (0, -1)     Turn R = R Turn L = L
#   D = (0, 1)      Turn R = L Turn L = R
def turn(facing, direction):
    turn_map = dict()
    turn_map["R"] = {"R": "D", "L": "U"}
    turn_map["L"] = {"R": "U", "L": "D"}
    turn_map["U"] = {"R": "R", "L": "L"}
    turn_map["D"] = {"R": "L", "L": "R"}
    return turn_map[facing][direction]

def take_step(grid, facing, position):
    x = position[0]
    y = position[1]
    # Wraps around
    if facing == "R":
        x += 1
        if x >= num_cols:
            x = 0
    elif facing == "L":
        x -= 1
        if x < 0:
            x = num_cols - 1
    elif facing == "U":
        # TODO: DOUBLE CHECK THIS IS THE RIGHT DIRECTION
        y -= 1
        if y < 0:
            y = num_rows - 1
    elif facing == "D":
        y += 1
        if y >= num_rows:
            y = 0
    return (x,y)

def move(grid, steps, facing, position):
    for step in range(steps):
        new_pos = take_step(grid, facing, position)
        if grid[new_pos] == ".":
            position = new_pos
        if grid[new_pos] == "#":
            return position
        while grid[new_pos] == " ":
            new_pos = take_step(grid, facing, new_pos)
        if grid[new_pos] == "#":
            return position
        position = new_pos
    return position

def walk_grid(grid, directions, facing, start_point):
    position = start_point
    for direction in directions:
        print(direction, position, facing)
        if type(direction) == str:
            facing = turn(facing, direction)
        else:
            position = move(grid, direction, facing, position)
    return position, facing

face_value = {
    "R": 0,
    "D": 1,
    "L": 2,
    "U": 3
}
def part1():
    grid = parse_grid(grid_str)
    directions = parse_path(path_str)
    facing = "R"
    start_point = get_start_point(grid)
    position, facing = walk_grid(grid, directions, facing, start_point)
    col = position[0] + 1
    row = position[1] + 1
    face = face_value[facing]
    return (1000 * row) + (4 * col) + face

def part2():
    return 0
    
print("PART 1:", part1())
print("PART 2:", part2())
