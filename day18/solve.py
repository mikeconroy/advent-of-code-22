f = open("input", "r")

cubes_array = []
for line in f.readlines():
    line = line.strip()
    cube = tuple(map(int, line.split(",")))
    
    cubes_array.append(cube)

class Cube():
    def __init__(self, coordinates, cubes=list()):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.coords = coordinates
        self.neighbours = self.calculate_neighbours(cubes)
    
    def calculate_neighbours(self, cubes):
        neighbours = set()
        neighbour_candidates = {
            (self.x + 1, self.y, self.z),
            (self.x - 1, self.y, self.z),
            (self.x, self.y + 1, self.z),
            (self.x, self.y - 1, self.z),
            (self.x, self.y, self.z + 1),
            (self.x, self.y, self.z - 1),
        }
        for cube in cubes:
            # Ignore the current cube
            if cube == self.coords:
                continue
            
            if (cube[0], cube[1], cube[2]) in neighbour_candidates:
                neighbours.add(cube)
                neighbour_candidates.remove(cube)
            if not neighbour_candidates:
                break
        return neighbours

    def get_surface_area(self):
        return 6 - len(self.neighbours)

    def __repr__(self):
        return str(self.coords) + str(self.neighbours)

def get_total_surface_area(cubes):
    total_surface_area = 0
    for cube in cubes.values():
        total_surface_area += cube.get_surface_area()
    return total_surface_area

def part1():
    cubes = dict()
    for cube in cubes_array:
        cubes[cube] = Cube(cube, cubes_array)

    return get_total_surface_area(cubes)


# Find all Cubes in the search space (total container)
# that aren't inside the droplet.
# BFS search from (0,0,0) and find the set of all 
def bfs_container(container, droplet):
    exterior_cubes = set()
    seen = set()
    queue = list()
    queue.append(container[(-1,-1,-1)])
    count = 0
    while queue:
        current_cube = queue.pop(0)
        count += 1
        if current_cube not in droplet:
            exterior_cubes.add(current_cube.coords)
        for neighbour in current_cube.neighbours:
            if not container[neighbour] in seen:
                queue.append(container[neighbour])
                seen.add(container[neighbour])
    return exterior_cubes

# Minimum Value = 0
# Maximum Value = 21
# Idea:
#   Create a Superset of Cubes
#   (0,0,0)
#   (22,22,22)
#   Loop through each cube:
#       Only look at cubes not in the droplet (Aka BFS from 0,0,0)
#       BFS neighbours
#       Don't search cubes that are part of the droplet
#   Add the cubes inside the droplets to the droplet shape
#   Calculate total surface area
# Another option is to use DFS against every cube in search space:
#   If cube is on the edge of search space
#   Mark the cube as exterior in a set
#   Mark any cubes that visit this cube as exterior in the same set
#   Any cubes that are droplet or don't reach the edge are marked as interior.
# Quick and dirty but works-
def part2():
    
    # Initial droplet
    droplet = dict()
    for cube in cubes_array:
        droplet[cube] = Cube(cube)

    # All cubes in the 'container' including droplet.
    search_space = []
    # All cubes in the 'container' excluding the droplet
    exterior = []
    for x in range(-1, 23):
        for y in range(-1, 23):
            for z in range(-1, 23):
                search_space.append((x,y,z))
                if (x,y,z) not in droplet:
                    exterior.append((x,y,z))

    exterior_dict = dict()
    for cube in search_space:
        #TODO: Double check this - remove if necesarry
        if (x,y,z) not in droplet:
            exterior_dict[cube] = Cube(cube, exterior)
    
    # Exterior cubes are the cubes external to the droplet
    # AKA the space the water can reach outside.
    exterior_cubes = bfs_container(exterior_dict, droplet)
    # Create list of tuples in the droplet
    solid_droplet_list = list()
    for cube in search_space:
        if cube not in exterior_cubes:
            solid_droplet_list.append(cube)

    new_droplet_cubes = dict()
    for cube in solid_droplet_list:
        new_droplet_cubes[cube] = Cube(cube, solid_droplet_list)

    return get_total_surface_area(new_droplet_cubes)

print("PART 1:", part1())
print("PART 2:", part2())
