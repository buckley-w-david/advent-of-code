from aocd import get_data

data = get_data(year=2021, day=2, block=True)
lines = data.splitlines()

depth = 0
hor = 0
aim = 0
for line in lines:
    dir, m = line.strip().split()
    m = int(m)
    if dir == 'forward':
        hor += m
        depth += (aim*m)
    elif dir == 'down':
        aim += m
    elif dir == 'up':
        aim -= m

print(depth, hor, aim, depth*hor)
