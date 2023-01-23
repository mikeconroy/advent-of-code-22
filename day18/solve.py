f = open("input", "r")

cubes_array = []
for line in f.readlines():
    line = line.strip()
    cube = tuple(map(int, line.split(",")))
    cubes_array.append(cube)

class Cube():
    def __init__(self, coordinates, cubes=dict()):
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
        for cube in cubes_array:
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

def part1():
    cubes = dict()
    for cube in cubes_array:
        cubes[cube] = Cube(cube)

    total_surface_area = 0
    for cube in cubes.values():
        total_surface_area += cube.get_surface_area()

    return total_surface_area

    # The following worked for the example input but not the proper input.
    # Detected which faces were connected and then subtracted those from the total faces.
    # total_faces = len(cubes) * 6

    # x_y_combs = dict()
    # x_z_combs = dict()
    # y_z_combs = dict()
    # connections = 0
    # for cube in cubes:
    #     x = cube[0]
    #     y = cube[1]
    #     z = cube[2]
    #     # Check whether cubes are adjacents on each axis.
    #     if (x,y) in x_y_combs:
    #         if (z-1) in x_y_combs[(x,y)] or (z+1) in x_y_combs[(x,y)]:
    #             connections += 1
    #         x_y_combs[(x,y)].add(z)
    #     else:
    #         x_y_combs[(x,y)] = {z}
    #     if (x,z) in x_z_combs:
    #         if (y-1) in x_z_combs[(x,z)] or (y+1) in x_z_combs[(x,z)]:
    #             connections += 1
    #         x_z_combs[(x,z)].add(y)
    #     else:
    #         x_z_combs[(x,z)] = {y}
    #     if (y,z) in y_z_combs:
    #         if (x-1) in y_z_combs[(y,z)] or (x+1) in y_z_combs[(y,z)]:
    #             connections += 1
    #         y_z_combs[(y,z)].add(x)
    #     else:
    #         y_z_combs[(y,z)] = {x}
    #     print(cube, connections)

    # print("Total Faces:", total_faces)
    # print("Connections:", connections)
    # return total_faces - (connections * 2)


    # The following doesn't work as it is all sides not connected to another cube.
    # This assumes looking at the shape from each side (x,y,z) tells you the surface area.
    # This is incorrect as cubes can overhang and 'hide'.
    # print(connections)
    # print(total_faces)
    # return total_faces - connections
    # x_y_coords = set()
    # x_z_coords = set()
    # y_z_coords = set()
    # for cube in cubes:
    #     x_y_coords.add((cube[0], cube[1]))
    #     x_z_coords.add((cube[0], cube[2]))
    #     y_z_coords.add((cube[1], cube[2]))
    
    # return (len(x_y_coords) * 2) + (len(x_z_coords) * 2) + (len(y_z_coords) * 2) 

def part2():
    return 0

# 7292 is too high
print("PART 1:", part1())
print("PART 2:", part2())
