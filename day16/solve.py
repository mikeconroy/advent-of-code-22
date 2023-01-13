from queue import PriorityQueue

f = open("input", "r")

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


TOTAL_TIME = 30
TIME_TO_OPEN = 1

# Guided by:
# https://www.reddit.com/r/adventofcode/comments/zo21au/2022_day_16_approaches_and_pitfalls_discussion/
# https://www.reddit.com/r/adventofcode/comments/zph9em/2022_day_16_part_1_where_do_i_even_begin/
# Check all permutations of valve paths with DFS and return the one that has the best rate within the time frame. 
def find_best_rate(time, current_valve, valves_turned_on, valves):
    if time >= (TOTAL_TIME - 1):
        return 0

    current_rate = 0

    if current_valve.rate > 0:
        time += TIME_TO_OPEN
        valves_turned_on.add(current_valve.key)
        current_rate = (TOTAL_TIME - time) * current_valve.rate

    best_rate = 0

    for valve_key in current_valve.distance_to:
        valve = valves[valve_key]
        if valve_key in valves_turned_on:
            continue
        new_time = time + current_valve.distance_to[valve_key]
        new_rate = find_best_rate(new_time, valve, set(valves_turned_on), valves)
        if new_rate > best_rate:
            best_rate = new_rate
    
    current_rate += best_rate

    return current_rate

def part1():
    # Parse the input and create the Valve Objects
    valves = createValveMap()
    # Populate distances to each valve and remove valves with a rate of 0.
    for valve in valves.values():
        bfs(valves, valve)

    return find_best_rate(0, valves["AA"], set(), valves)

def part2():
    return 0
    
print("PART 1:", part1())
print("PART 2:", part2())