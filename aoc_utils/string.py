import re

def ints(s):
    return [int(d) for d in re.findall(r"-?\d+", s)]

def floats(s):
    return [float(f) for f in re.findall(r"-?\d+(?:\.\d+)?", s)]
