from tqdm import tqdm

f = open("input", "r")

encrypted_values = []
for line in f.readlines():
    line = line.strip()
    encrypted_values.append(int(line))

class Node:
    def __init__(self, orig_index, value, next, prev):
        self.orig_index = orig_index
        self.value = value
        self.next = next
        self.prev = prev
    
    def __repr__(self):
        return str(self.orig_index) + " : " + str(self.value)

class CLL:
    def __init__(self):
        self.root = None
        self.end = None
        self.count = 0

    def add(self, orig_index, value):
        if self.count == 0:
            new_node = Node(orig_index, value, None, None)
            self.root = new_node
            self.end = self.root
        else:
            new_node = Node(orig_index, value, self.root, self.end)
            if self.end != None:
                self.end.next = new_node
            self.end = new_node
            self.root.prev = self.end
        self.count += 1

    def insert_after_node(self, prev_node, new_node):
        next_node = prev_node.next
        next_node.prev = new_node
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = next_node
        if prev_node == self.end:
            self.end = new_node
        self.count += 1

    def remove(self, node):
        if node == self.end:
            self.end = node.prev
        next_node = node.next
        prev_node = node.prev
        next_node.prev = prev_node
        prev_node.next = next_node
        if node == self.root:
            self.root = next_node
        self.count -= 1

    def find_by_orig_index(self, orig_index):
        if self.root.orig_index == orig_index:
            return self.root
        
        current_node = self.root.next
        while current_node != self.root:
            if current_node.orig_index == orig_index:
                return current_node
            current_node = current_node.next
        return None

    def find_by_value(self, value):
        if self.root.value == value:
            return self.root
        
        current_node = self.root.next
        while current_node != self.root:
            if current_node.value == value:
                return current_node
            current_node = current_node.next
        return None

    def __repr__(self):
        current_node = self.root
        output = str(self.count) + " [" + str(current_node) + "]"
        if self.count == 1:
            return output
        current_node = current_node.next
        while current_node != self.root:
            output += " <-> [" + str(current_node) + "]"
            current_node = current_node.next
        return output

def part1():
    cll = CLL()
    for index, val in enumerate(encrypted_values):
        cll.add(index, val)

    # Decrypt values
    for index, val in enumerate(encrypted_values):
        node = cll.find_by_orig_index(index)
        move_by = abs(val) % (cll.count - 1)
        position = node if val > 0 else node.prev
        while move_by > 0:
            if val < 0:
                position = position.prev
            else:
                position = position.next
            move_by -= 1
        if position != node:
            cll.remove(node)
            cll.insert_after_node(position, node)

    node = cll.find_by_value(0).next
    thousandth = -1
    two_thousandth = -1
    three_thousandth = -1
    for i in range(1, 3001):
        if i == 1_000:
            thousandth = node.value
        elif i == 2_000:
            two_thousandth = node.value
        elif i == 3_000:
            three_thousandth = node.value
        node = node.next
    
    print(thousandth, two_thousandth, three_thousandth)
    return thousandth + two_thousandth + three_thousandth

def part2():
    updated_values = []
    for value in encrypted_values:
        updated_values.append(value * 811589153)

    cll = CLL()
    for index, val in enumerate(updated_values):
        cll.add(index, val)

    # Mix the values 10 times
    for i in tqdm(range(10)):
        for index, val in enumerate(updated_values):
            node = cll.find_by_orig_index(index)
            move_by = abs(val) % (cll.count - 1)
            position = node if val > 0 else node.prev
            while move_by > 0:
                if val < 0:
                    position = position.prev
                else:
                    position = position.next
                move_by -= 1
            if position != node:
                cll.remove(node)
                cll.insert_after_node(position, node)

    # Find the 1,000th, 2,000th, & 3,000th Digits
    node = cll.find_by_value(0).next
    thousandth = -1
    two_thousandth = -1
    three_thousandth = -1
    for i in range(1, 3001):
        if i == 1_000:
            thousandth = node.value
        elif i == 2_000:
            two_thousandth = node.value
        elif i == 3_000:
            three_thousandth = node.value
        node = node.next
    
    print(thousandth, two_thousandth, three_thousandth)
    return thousandth + two_thousandth + three_thousandth
    
print("PART 1:", part1())
print("PART 2:", part2())
