from collections import defaultdict
import re

with open("input", "r") as f:
    rules = f.readlines()

subject_pattern = re.compile(r"^((?:[a-zA-Z] ?)+) bags contain")
target_pattern = re.compile(r"(\d+) ([a-zA-Z]+ [a-zA-Z]+) bags?")

graph = defaultdict(dict)

for rule in rules:
    subject = subject_pattern.match(rule).group(1)
    for target in target_pattern.findall(rule):
        c, target_name = target
        graph[subject][target_name] = int(c)


def to_the_moon(graph, target):
    containers = {k: v for k, v in graph.items() if target in v}
    matches = set(containers.keys())
    for match in list(matches):
        for submatch in to_the_moon(graph, match):
            matches.add(submatch)
    return matches

def count_bags(graph, target):
    sub_bags = graph[target]
    count = 0
    for bag, c in sub_bags.items():
        count += c + c*count_bags(graph, bag)
    return count


# print(len(to_the_moon(graph, 'shiny gold')))
print(count_bags(graph, 'shiny gold'))
