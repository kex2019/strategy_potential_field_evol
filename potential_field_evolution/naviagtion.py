import numpy as np


def l1norm_dist(p1: [], p2: []) -> float:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class point_model():
    """ A entities model of a point. """

    def __init__(self, point: []):
        self.point = point
        self.goodness = (np.random.rand() - 0.5) * 2
        # self.goodness = 0.5 * np.sign(np.random.rand() - 0.5)

    def F(self, point: []):
        return self.goodness / (l1norm_dist(self.point, point) + 2)

    def dxF(self, point: []):
        return (self.goodness * (self.point[1] - point[1])) / (np.square(
            (l1norm_dist(self.point, point) + 2
             )) * np.abs(self.point[1] - point[1] + 1e-5))

    def dyF(self, point: []):
        return (self.goodness * (self.point[0] - point[0])) / (np.square(
            (l1norm_dist(self.point, point) + 2
             )) * np.abs(self.point[0] - point[0] + 1e-5))


def build_map_model(robot):
    width = robot.gym.map_width
    height = robot.gym.map_height

    map_model = [[point_model([y, x]) for x in range(width)]
                 for y in range(height)]

    return map_model


def learn_from(master, apprentice):
    for y in range(self.gym.map_height):
        for x in range(self.gym.map_width):
            apprentice.model[y][x].goodness = (
                master.model[y][x].goodness + apprentice.model[y][x].goodness
            ) / 2


def navigate(self):
    print("Hello", self.robot.position)

    print("Map potential Field")
    for yp in range(self.gym.map_height):
        for xp in range(self.gym.map_width):
            score = 0
            for y in range(self.gym.map_height):
                for x in range(self.gym.map_width):
                    score += self.model[y][x].F([yp, xp])
            print(int(100 * score) / 100, end=" ")
        print()

    grad_x, grad_y = 0, 0
    for y in range(self.gym.map_height):
        for x in range(self.gym.map_width):
            if [y, x] != list(self.robot.position):
                grx = self.model[y][x].dxF(self.robot.position)
                gry = self.model[y][x].dyF(self.robot.position)

                grad_x += grx
                grad_y += gry

    print("Position", self.robot.position)
    print("Gradient", [grad_y, grad_x])

    print()
    print()
    print()

    y = int(self.robot.position[0] + np.sign(grad_y))
    x = int(self.robot.position[1] + np.sign(grad_x))

    return y, x
