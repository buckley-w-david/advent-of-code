#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=19, block=True)

blueprints = map(ints, data.splitlines())

ORE = 0
CLAY = 1
OBS = 2
GEO = 3

time = 32

q = 1

for bpid, ore_robot, clay_robot, obs_robot_ore, obs_robot_clay, geo_robot_ore, geo_robot_obs  in list(blueprints)[:3]:
    robots = (
        1,
        0,
        0,
        0,
    )

    resources = (
        0,
        0,
        0,
        0,
    )

    costs = (
        ore_robot,
        clay_robot,
        (obs_robot_ore, obs_robot_clay),
        (geo_robot_ore, 0, geo_robot_obs),
    )
    max_ore = max(ore_robot, clay_robot, obs_robot_ore, geo_robot_ore)
    max_clay = obs_robot_clay
    max_obs = geo_robot_obs

    mg = 0

    def neighbours(state):
        robots, resources, t = state
        if t == 0:
            global mg
            if resources[GEO] > mg:
                mg = resources[GEO]
            return []
        # filter out branches that can't do better than current best (build a geo every time step)
        if resources[GEO]+(robots[GEO]*t)+(t*(t+1)//2) < mg:
            return []

        if robots[ORE] < max_ore and resources[ORE] >= costs[ORE]:
            yield 1000, ((robots[ORE]+1, robots[CLAY], robots[OBS], robots[GEO]), (resources[ORE]-costs[ORE]+robots[ORE], resources[CLAY]+robots[CLAY], resources[OBS]+robots[OBS], resources[GEO]+robots[GEO]), t-1)
        if robots[CLAY] < max_clay and resources[ORE] >= costs[CLAY]:
            yield 100, ((robots[ORE], robots[CLAY]+1, robots[OBS], robots[GEO]), (resources[ORE]-costs[CLAY]+robots[ORE], resources[CLAY]+robots[CLAY], resources[OBS]+robots[OBS], resources[GEO]+robots[GEO]), t-1)
        if robots[OBS] < max_obs and resources[ORE] >= costs[OBS][ORE] and resources[CLAY] >= costs[OBS][CLAY]:
            yield 10, ((robots[ORE], robots[CLAY], robots[OBS]+1, robots[GEO]), (resources[ORE]-costs[OBS][ORE]+robots[ORE], resources[CLAY]-costs[OBS][CLAY]+robots[CLAY], resources[OBS]+robots[OBS], resources[GEO]+robots[GEO]), t-1)
        if resources[ORE] >= costs[GEO][ORE] and resources[OBS] >= costs[GEO][OBS]:
            yield 1, ((robots[ORE], robots[CLAY], robots[OBS], robots[GEO]+1), (resources[ORE]-costs[GEO][ORE]+robots[ORE], resources[CLAY]+robots[CLAY], resources[OBS]-costs[GEO][OBS]+robots[OBS], resources[GEO]+robots[GEO]), t-1)
        yield 10000, (robots, (resources[ORE]+robots[ORE], resources[CLAY]+robots[CLAY], resources[OBS]+robots[OBS], resources[GEO]+robots[GEO]), t-1)

    g = LazyGraph(neighbours)
    d = g.dijkstra((robots, resources, time))
    q *= mg

print(q)
