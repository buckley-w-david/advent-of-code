#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2019, day=4, block=True)

start, end = map(int, data.split("-"))
s = start // 100000
count = 0

# WTF is this shit?
for a in range(s, 10):
    for b in range(a, 10):
        for c in range(b, 10):
            for d in range(c, 10):
                for e in range(d, 10):
                    for f in range(e, 10):
                        if (a <= b <= c <= d <= e <= f) and ((a == b and b != c) or (b == c and b != a and c != d) or (c == d and c != b and d != e) or (d == e and e != f and d != c) or (e == f and e != d)):
                            x = a*100000 + b*10000 + c*1000 + d*100 + e*10 + f
                            if x < start:
                                continue
                            count += 1
                            if x > end:
                                print(count-1)
                                exit()

                                

