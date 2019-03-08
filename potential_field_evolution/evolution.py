import numpy as np
import random


def learn_from(master, apprentice):
    for y in range(master.gym.map_height):
        for x in range(master.gym.map_width):
            apprentice.model[y][x].goodness = (
                master.model[y][x].goodness + apprentice.model[y][x].goodness
            ) / 2


def mutation(individual):
    for y in range(individual.gym.map_height):
        for x in range(individual.gym.map_width):
            individual.model[y][x].goodness += individual.model[y][
                x].goodness * 0.5 * (np.random.rand() - 0.5)


def evolve(robots):
    """ First implemention is a simple elitist variant, i suggest we look into adaptive GA for final version. """
    """ Ranking... """
    robots = sorted(robots, key=lambda r: r.fitness, reverse=True)

    print()
    print(robots[0].fitness)
    """ Selection """
    masters = robots[:int(len(robots) * 0.5 + 0.5)]
    apprentices = robots[int(len(robots) * 0.5 + 0.5):]
    """ Cross Overs """
    for appr in apprentices:
        learn_from(random.choice(masters), appr)
    """ Mutations """
    for appr in apprentices:
        mutation(appr)
    """ Reset fitness. """
    for robot in robots:
        robot.fitness = 0
