import robotic_warehouse.robotic_warehouse as warehouse
import robotic_warehouse_utils.path_finder as path_finder
import robotic_warehouse_utils.data_collection as data_collection
import strategy_heuristic.robot as robot
import pandas as pd
import random
import time
import queue


class PFE():
    def __init__(self, gym, capacity: int, a_star: "Astar Pathfinder",
                 num_robots: int):
        self.gym = gym
        self.capacity = capacity
        self.a_star = a_star
        self.num_robots = num_robots
        self.idle_positions = []
        self.distribute_robots(0, 0, self.gym.gym.map_width,
                               self.gym.gym.map_height)
        self.tags = set()
        self.robots = [
            robot.Robot(gym, capacity, a_star, self.tags)
            for _ in range(num_robots)
        ]

    def distribute_robots(self, x0, y0, x1, y1):
        q = queue.Queue()
        q.put((x0, x1, y0, y1))
        while True:
            if len(self.idle_positions) >= self.num_robots:
                return
            (x0, x1, y0, y1) = q.get()
            x = (x0 + x1) // 2
            y = (y0 + y1) // 2
            self.idle_positions.append(self.a_star.available_pos_near((y, x)))
            q.put((x0, x, y0, y))
            q.put((x0, x, y, y1))
            q.put((x, x1, y0, y))
            q.put((x, x1, y, y1))

    def gc_tags(self, packages):
        self.tags = self.tags.intersection(set(packages))

    def __call__(self, robots, packages) -> "instructions":
        """ Maybe dont do this each time?"""
        self.gc_tags(packages)

        instructions = []
        for i, robot in enumerate(self.robots):
            instructions.append(
                robot.run_standard_logic(robots[i].position,
                                         self.idle_positions[i],
                                         robots[i].packages, packages))
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

    pf = path_finder.Astar(gym)

    gym = data_collection.initGymCollect(gym, data, output, name, steps,
                                         collect)

    swarm = PFE(gym, capacity, pf, robots)

    render = False
    if "render" in kwargs:
        render = kwargs["render"]

    (robots, packages), _, _, _ = gym.reset()
    curr_step = 0
    print()
    while True:
        if render:
            gym.render()

        instructions = swarm(robots, packages)

        (robots, packages), _, _, _ = gym.step(instructions)

        if not (curr_step % 1000):
            print("{}/{}    ".format(curr_step, steps), end="\r")

        curr_step += 1


if __name__ == "__main__":
    evaluate(render=True)
