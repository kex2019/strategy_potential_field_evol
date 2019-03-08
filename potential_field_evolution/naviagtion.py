import numpy as np


def navigate(self):
    # print("Hello", self.robot.position)

    mx = -10
    mxp = [0, 0]
    for yp in range(self.gym.map_height):
        for xp in range(self.gym.map_width):
            score = 0
            for y in range(self.gym.map_height):
                for x in range(self.gym.map_width):
                    score += self.model[y][x].F([yp, xp])
                # print(int(100 * score) / 100, end=" ")
                # print()
            if score > mx:
                mx = score
                mxp = [yp, xp]

    # grad_x, grad_y = 0, 0
    # for y in range(self.gym.map_height):
        # for x in range(self.gym.map_width):
            # if [y, x] != list(self.robot.position):
                # grx = self.model[y][x].dxF(self.robot.position)
                # gry = self.model[y][x].dyF(self.robot.position)

                # grad_x += grx
                # grad_y += gry

    # print("Position", self.robot.position)
    # print("Gradient", [grad_y, grad_x])

    # y = np.clip(
        # int(self.robot.position[0] + int(grad_y * 50)), 0, self.gym.map_height)
    # x = np.clip(
        # int(self.robot.position[1] + int(grad_x * 50)), 0, self.gym.map_width)
    # """ Waiting. """
    self.state = 3


    # print()
    # print()
    # print()

    return mxp
