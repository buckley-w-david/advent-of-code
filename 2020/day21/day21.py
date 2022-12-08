#!/usr/bin/env python

import re
from collections import namedtuple, defaultdict
from pprint import pprint
from aocd import get_data, submit
import numpy as np

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=21, block=True)
# data = """
# mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)
# """.strip()

pa = re.compile(r"(.*) \(contains (.*)\)$")
foods = []

Food = namedtuple('Food', 'ingredients alergens')
all_alergens = defaultdict(set)

for line in data.splitlines():
    m = pa.search(line)
    ingredients = {i for i in m.group(1).split(" ")}
    alergens = {a for a in m.group(2).split(", ")}
    foods.append(Food(ingredients, alergens))

from more_itertools import flatten

ingredients = np.array(sorted(set(flatten([f.ingredients for f in foods]))))
alergens = np.array(sorted(set(flatten([ f.alergens for f in foods ]))))
ingredient_idx = {v: k for k, v in dict(enumerate(ingredients)).items()}
alergen_idx = {v: k for k, v in dict(enumerate(alergens)).items()}

matrix = np.zeros((len(ingredient_idx), len(alergen_idx)), dtype=bool)
for food in foods:
    fidx = [ingredient_idx[i] for i in food.ingredients]
    aidx = [alergen_idx[i] for i in food.alergens]
    x = matrix[fidx]
    x[:, aidx] = True
    matrix[fidx] = x

for f1 in foods:
    for ingredient in f1.ingredients:
        for alergen in f1.alergens:
            for f2 in foods:
                if f1 is not f2:
                    if alergen in f2.alergens and ingredient not in f2.ingredients:
                        matrix[ingredient_idx[ingredient]][alergen_idx[alergen]] = False


the_answer = {}
while True:
    x =  np.where(matrix.sum(axis=0) == 1) 
    if not len(x[0]):
        break
    ingred = np.where(matrix[:, x[0]][:, 0] == True)
    the_answer[ingredients[ingred[0][0]]] = alergens[x[0][0]]
    matrix[ingred] = False

print(','.join(k for k, v in sorted(the_answer.items(), key=lambda kv: kv[1])))
