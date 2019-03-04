import robotic_warehouse_utils.path_finder as path_finder
import numpy as np


class Robot():
    NOTHING = 0
    WALKING_TO_PACKAGE = 1
    DROPPING_OFF_PACKAGE = 2

    def __init__(self, gym, capacity: int, a_star: "Astar Pathfinder",
                 tagged_package: set):
        self.gym = gym
        self.capacity = capacity
        self.instructions = []
        self.eip = 0
        self.a_star = a_star
        self.state = Robot.NOTHING
        self.tagged_package = tagged_package

    def is_standing_next_to_package(self, position, free_packages):
        for fp in free_packages:
            if path_finder.l1norm_dist(position, fp.start) == 1:
                return True
        return False

    def is_standing_next_to_dropoff(self, position, packages):
        for package in packages:
            if path_finder.l1norm_dist(position, package.dropoff) == 1:
                return True
        return False

    def get_non_tagged_packages(self, free_packages):
        non_tagged = []
        for package in free_packages:
            if package not in self.tagged_package:
                non_tagged.append(package)
        return non_tagged

    def get_closest_package(self, positon, packages):
        return packages[
                np.argmin(
                    list(
                        map(
                            lambda package: path_finder.l1norm_dist(positon, package.start),
                            packages
                        )
                    )
                )]

    def run_standard_logic(self, position, idle_position, packages,
                           free_packages):
        non_tagged = self.get_non_tagged_packages(free_packages)
        """ If has instruction, run them """
        if len(self.instructions) > self.eip and not (
                len(non_tagged) != 0 and self.state == Robot.NOTHING):
            i = self.instructions[self.eip]
            self.eip += 1
            return i
        """ If we are standing next to a package pick it up!"""
        if len(packages) != self.capacity and self.is_standing_next_to_package(
                position, free_packages):
            return self.gym.PICKUP_INSTRUCTION
        """ Check for standard drop conditions. """
        if len(packages) == self.capacity or\
            (self.state == Robot.DROPPING_OFF_PACKAGE and len(packages) >= 1) or\
            (len(non_tagged) == 0 and len(packages) >= 1):
            self.state = Robot.DROPPING_OFF_PACKAGE

            if self.is_standing_next_to_dropoff(position, packages):
                return self.gym.DROP_INSTRUCTION
            """ Find closest drop off. """
            closest_drop_off = packages[np.argmin(
                list(
                    map(
                        lambda package: path_finder.l1norm_dist(position, package.dropoff),
                        packages)
                    )
                )
                ].dropoff
            """ Get instructions to walk there. """
            self.instructions = self.a_star(
                position, self.a_star.available_pos_near(
                    closest_drop_off)).get_instructions()
            """ Execute instructions. """
            self.eip = 1
            return self.instructions[0]
        """ If there are non-tagged packages we go get em. """
        if non_tagged:
            closest = self.get_closest_package(position, non_tagged)
            ourdistance = path_finder.l1norm_dist(position, closest.start)
            distances = [
                path_finder.l1norm_dist(robot.position, closest.start)
                for robot in self.gym.gym.robots
            ]
            mindistance = min(distances)
            if ourdistance <= mindistance:
                self.tagged_package.add(closest)
                self.instructions = self.a_star(
                    position, self.a_star.available_pos_near(
                        closest.start)).get_instructions()
                """ Execute instruction. """
                self.state = Robot.WALKING_TO_PACKAGE
                self.eip = 1
                return self.instructions[0]
        """ At this point the robot has no standard logic.. unless we come up with more stuff. """
        self.state = Robot.NOTHING
        if list(position) == list(idle_position):
            return self.gym.PICKUP_INSTRUCTION

        self.instructions = self.a_star(position,
                                        idle_position).get_instructions()
        self.eip = 1
        if self.instructions:
            return self.instructions[0]

        return self.gym.PICKUP_INSTRUCTION
