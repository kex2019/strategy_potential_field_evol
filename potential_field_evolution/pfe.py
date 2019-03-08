import robotic_warehouse.robotic_warehouse as warehouse
import robotic_warehouse_utils.data_collection as data_collection
import potential_field_evolution.naviagtion as navigation
import potential_field_evolution.evolution as evolution
import potential_field_evolution.initialization as initialization
import kex_robot.robot as KR
import pandas as pd
import random
import time
import queue


class PFE():
    def __init__(self, robots, gym, capacity: int, num_robots: int,
                 generation_steps: int):
        self.gym = gym
        self.capacity = capacity
        self.num_robots = num_robots
        self.generation_steps = generation_steps

        self.tags = set()
        self.robots = []
        for i in range(num_robots):
            robot = KR.Robot(robots[i], gym.gym, capacity, self.tags,
                             self.robots)
            """ Inject robots model of the world. """
            robot.model = initialization.build_map_model(robot)

            self.robots.append(robot)

        self.steps = 1

    def gc_tags(self, packages):
        self.tags = self.tags.intersection(set(packages))

    def __call__(self, packages) -> "instructions":
        """ Maybe dont do this each time?"""
        self.gc_tags(packages)

        if self.steps % self.generation_steps == 0:
            evolution.evolve(self.robots)

        self.steps += 1

        instructions = []
        for i, robot in enumerate(self.robots):
            robot.reservations = self.tags
            instructions.append(robot(packages, navigation.navigate))

        return instructions


def evaluate(**kwargs):
    robots = 1
    if "robots" in kwargs:
        robots = kwargs["robots"]

    capacity = 1
    if "capacity" in kwargs:
        capacity = kwargs["capacity"]

    spawn = 10
    if "spawn" in kwargs:
        spawn = kwargs["spawn"]

    shelve_length = 2
    if "shelve_length" in kwargs:
        shelve_length = kwargs["shelve_length"]

    shelve_height = 2
    if "shelve_height" in kwargs:
        shelve_height = kwargs["shelve_height"]

    shelve_width = 2
    if "shelve_width" in kwargs:
        shelve_width = kwargs["shelve_width"]

    shelve_throughput = 1
    if "shelve_throughput" in kwargs:
        shelve_throughput = kwargs["shelve_throughput"]

    cross_throughput = 5
    if "cross_throughput" in kwargs:
        cross_throughput = kwargs["cross_throughput"]

    seed = 105
    if "seed" in kwargs:
        seed = kwargs["seed"]

    periodicity_lower = 20
    if "periodicity_lower" in kwargs:
        periodicity_lower = kwargs["periodicity_lower"]

    periodicity_upper = 100
    if "periodicity_upper" in kwargs:
        periodicity_upper = kwargs["periodicity_upper"]

    data = pd.DataFrame()
    if "data" in kwargs:
        data = kwargs["data"]

    output = "data"
    if "output" in kwargs:
        output = kwargs["output"]

    name = "random_package_random_drop"
    if "name" in kwargs:
        name = kwargs["name"]

    steps = 10000
    if "steps" in kwargs:
        steps = kwargs["steps"]

    collect = True
    if "collect" in kwargs:
        collect = kwargs["collect"]

    gym = warehouse.RoboticWarehouse(
        robots=robots,
        capacity=capacity,
        spawn=spawn,
        shelve_length=shelve_length,
        shelve_height=shelve_height,
        shelve_width=shelve_width,
        shelve_throughput=shelve_throughput,
        cross_throughput=cross_throughput,
        seed=seed,
        periodicity_lower=periodicity_lower,
        periodicity_upper=periodicity_upper)

    gym = data_collection.initGymCollect(gym, data, output, name, steps,
                                         collect)

    generation_steps = 200
    if "generation_steps" in kwargs:
        generation_steps = kwargs["generation_steps"]

    R, packages = gym.reset()
    swarm = PFE(R, gym, capacity, robots, generation_steps)

    render = False
    if "render" in kwargs:
        render = kwargs["render"]

    curr_step = 0
    print()
    while True:
        if render:
            gym.render()

        instructions = swarm(packages)

        (_, packages), _, _, _ = gym.step(instructions)

        if not (curr_step % 1000):
            print("{}/{}    ".format(curr_step, steps), end="\r")

        curr_step += 1


if __name__ == "__main__":
    evaluate(render=True)
