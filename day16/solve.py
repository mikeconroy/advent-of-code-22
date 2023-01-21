f = open("input", "r")
from tqdm import tqdm


inputArray = []
for line in f.readlines():
    line = line.strip()
    inputArray.append(line)
    
class Valve():
    def __init__(self, key, rate, leadsTo):
        self.key = key
        self.open = False
        self.rate = int(rate)
        self.leadsTo = leadsTo
        self.distance_to = dict()

    def print(self):
        print("\nKey:", self.key, "Rate:", self.rate, "Open:", self.open, "Leads:", self.leadsTo, "Distances:\n", self.distance_to)

def createValveMap():
    valves = dict()
    for scan in inputArray:
        key = scan.split(" has ")[0].replace("Valve ", "")
        rate = scan.split("=")[1].split(";")[0]
        if " to valves" in scan:
            leadsTo = scan.split("valves ")[1].split(", ")
        else:
            leadsTo = [scan.split("valve ")[1]]
        valves[key] = Valve(key, rate, leadsTo)
    return valves

def bfs(valves, start):
    queue = list()
    queue.append((start, 0))
    seen = set()
    seen.add(start.key)
    while queue:
        valve, distance = queue.pop(0)
        for connected_valve_key in valve.leadsTo:
            connected_valve = valves[connected_valve_key]
            # Only go to valves not already seen
            if not connected_valve_key in seen:
                # Ignore distances to valves with a rate of 0 - we don't need to visit them.
                if connected_valve.rate > 0:
                    start.distance_to[connected_valve_key] = distance + 1
                queue.append((connected_valve, distance + 1))
                seen.add(connected_valve_key)

# Guided by:
# https://www.reddit.com/r/adventofcode/comments/zo21au/2022_day_16_approaches_and_pitfalls_discussion/
# https://www.reddit.com/r/adventofcode/comments/zph9em/2022_day_16_part_1_where_do_i_even_begin/
# Check all permutations of valve paths with DFS and return the one that has the best rate within the time frame.
# Optimization:
#   from functools import cache
#   @cache
#   Could have been used if frozenset was used instead of set in the parameters.
# 
# https://youtu.be/bLMj50cpOug?t=1100
# The state of the 15 valves could have been stored in a bitmask where 0 is closed & 1 is openn.
# bit = 1 << valve_index
# if bitmask & bit:
#   Valve is already enabled
#   110100
#   000100
#  =000100 
# Then calculating new bitmask:
#   bitmask | bit:
def find_best_rate(time, current_valve, valves_turned_on, TOTAL_TIME=30):    
    if time >= (TOTAL_TIME - 1):
        return 0
 
    current_rate = 0

    # Handle the first valve
    if current_valve.rate > 0:
        time += 1
        valves_turned_on.add(current_valve.key)
        current_rate = (TOTAL_TIME - time) * current_valve.rate

    best_rate = 0

    for valve_key in current_valve.distance_to:
        valve = valves[valve_key]
        if valve_key in valves_turned_on:
            continue
        new_time = time + current_valve.distance_to[valve_key]
        new_rate = find_best_rate(new_time, valve, set(valves_turned_on), TOTAL_TIME=TOTAL_TIME)
        if new_rate > best_rate:
            best_rate = new_rate
    
    current_rate += best_rate

    return current_rate

# Parse the input and create the Valve Objects
valves = createValveMap()
# Populate distances to each valve and remove valves with a rate of 0.
for valve in valves.values():
    bfs(valves, valve)

def part1():
    return find_best_rate(0, valves["AA"], set())

def get_all_path_rates(current_valve, current_time, valves_turned_on, current_rate, complete_paths, total_time):
    if current_time >= (total_time - 1):
        complete_paths.append((valves_turned_on, current_rate))
        return
    
    if current_valve.rate > 0:
        current_time += 1
        valves_turned_on.add(current_valve.key)
        current_rate += (total_time - current_time) * current_valve.rate

    for valve_key in current_valve.distance_to:
        new_time = current_time
        valve = valves[valve_key]
        if valve_key in valves_turned_on:
            continue
        new_time += current_valve.distance_to[valve_key]
        
        get_all_path_rates(valve, new_time, set(valves_turned_on), current_rate=current_rate, complete_paths=complete_paths, total_time=total_time)

    if current_rate:
        complete_paths.append((valves_turned_on, current_rate))
    return

# https://www.reddit.com/r/adventofcode/comments/zqpud2/comment/j11pxfd/?utm_source=share&utm_medium=web2x&context=3
# https://www.reddit.com/r/adventofcode/comments/zqpud2/comment/j1146yu/?utm_source=share&utm_medium=web2x&context=3
def part2():
    # FAILED STRATEGY:
    #   Do same as part 1 BUT
    #   Once the time reaches 26 minutes
    #   Reset the timer to 1 minute (only once) and go to 26 again.
    #   DFS will still find the path to maximise the rate
    #   Timer has to be reset due to the calculation of the pressure released.
    #   rate * time_left
    #   If we doubled the time to 52 minutes this wouldn't be solved.
    
    # Next Strategy:
    #   Calculate all paths of valves possible in 26 minutes along with the rate.
    #   Find the 2 paths that:
    #       Don't share any valves
    #       Produce the highest combined rate (Add the rates together).

    all_paths = list()
    get_all_path_rates(valves["AA"], 0, valves_turned_on=set(), current_rate=0, complete_paths=all_paths, total_time=26)
    print("Paths Retrieved:", len(all_paths))

    all_paths.sort(reverse=True, key=lambda path: path[1])
    # print(all_paths)

    best_rate = 0
    # Likely a more efficient way to check these paths.
    # The paths could also be pruned further
    for human_path in tqdm(all_paths):
        rate = 0
        for elephant_path in all_paths:
            if human_path[0].isdisjoint(elephant_path[0]):
                rate = human_path[1] + elephant_path[1]
                break
        if rate > best_rate:
            best_rate = rate
    
    return best_rate
    
print("PART 1:", part1())
print("PART 2:", part2())