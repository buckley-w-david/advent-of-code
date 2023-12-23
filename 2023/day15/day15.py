import re

def hash(s):
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current

def parse_instructions(data):
    return data.replace("\n", "").split(",")

def part_one(data):
    instructions = parse_instructions(data)

    s = 0
    for ins in instructions:
        s += hash(ins)
    return s

def part_two(data):
    boxes = [[] for _ in range(256)]
    instructions = parse_instructions(data)
    for ins in instructions:
        if match := re.match(r"([a-zA-Z]+)(-|=)(\d+)?", ins):
            ins_label = match.group(1)
            operation = match.group(2)
            lense = None
            if operation == "=":
                lense = int(match.group(3))

            box = boxes[hash(ins_label)]
            for i, (label, _) in enumerate(box):
                if label == ins_label:
                    if operation == "-":
                        box.pop(i)
                    else:
                        box[i] = (label, lense)
                    break
            else: 
                if operation == "=":
                    box.append((ins_label, lense))

    power = 0
    for i, box in enumerate(boxes):
        for j, (label, lense) in enumerate(box):
            power += (i+1)*(1+j)*lense
    return power


with open('day15.txt', 'r') as f:
    data = f.read()

print(part_one(data))
print(part_two(data))
