f = open("input", "r")

inputArray = []
for line in f.readlines():
    line = line.strip()
    inputArray.append(line)
    
def parse_input():
    vals = dict()
    ops = dict()
    for monkey in inputArray:
        key, value = monkey.split(": ")
        if " " in value:
            lhs, op, rhs = value.split(" ")
            object = {"lhs": lhs, "rhs": rhs, "op": op}
            ops[key] = object
        else:
            vals[key] = int(value)
    return vals, ops

def get_monkey_value(key, vals, ops):
    if key in vals:
        return vals[key]
    monkey = ops[key]
    lhs = get_monkey_value(monkey['lhs'], vals, ops)
    rhs = get_monkey_value(monkey['rhs'], vals, ops)
    op = monkey['op']
    if op == "+":
        result = lhs + rhs
    elif op == "*":
        result = lhs * rhs
    elif op == "-":
        result = lhs - rhs
    elif op == "/":
        result = lhs // rhs
    
    vals[key] = result
    return result

def part1():
    vals, ops = parse_input()
    return get_monkey_value("root", vals, ops)

def part2():
    return 0
    
print("PART 1:", part1())
print("PART 2:", part2())
