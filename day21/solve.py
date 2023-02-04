import copy

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

def calc_new_yell(current, too_high, min, max):
    if too_high:
        max = current
    else:
        min = current
    
    new_yell = (min + max) // 2
    return new_yell, min, max

def part2():
    vals, ops = parse_input()
    root_lhs = ops['root']['lhs']
    root_rhs = ops['root']['rhs']
    ops.pop("root")
    min = 0
    # max = 3_876_907_167_499
    max = 5_000_000_000
    yell = max // 2
    root_lhs_value = -1
    root_rhs_value = -2
    while True:
        vals["humn"] = yell
        new_vals = copy.deepcopy(vals)
        new_ops = copy.deepcopy(ops)
        root_lhs_value = get_monkey_value(root_lhs, new_vals, new_ops)
        root_rhs_value = get_monkey_value(root_rhs, new_vals, new_ops)
        if root_lhs_value == root_rhs_value:
            return yell
        too_high = True if root_lhs_value > root_rhs_value else False
        yell, min, max = calc_new_yell(yell, too_high, min, max)

print("PART 1:", part1())
# 3876907167501 is too high
# 3876907167499 is too high
# 3876907167495 is the right answer
print("PART 2:", part2())
