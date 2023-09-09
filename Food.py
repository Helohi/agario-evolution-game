from random import randint
import pygame

MIN_NUM_OF_FOOD = 200


class Food:
    foods = []

    def __init__(self):
        self.color = 176, 184, 45
        self.radius = 1
        self.center = pygame.Vector2(
            (randint(self.radius, 1400 - self.radius), randint(self.radius, 700 - self.radius)))

        self.foods.append(self)

    def delete(self):
        if self in self.foods:
            self.foods.remove(self)
        del self

    def show_me(self):
        return self.color, self.center, self.radius
