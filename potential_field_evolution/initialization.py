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
