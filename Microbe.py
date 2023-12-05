import pygame
from Food import Food
import random
from typing import Iterable

MAX_NUM_OF_MICROBES = 100


class Microbe:
    microbes = []

    def __init__(self, color: Iterable = (0, 184, 179,), speed: int = 20, radius: int = 10, center: list = None,
                 e_to_create_child: int = 110, generation: int = 1):
        self.color = color
        self.__speed = speed

        self.radius = radius
        self.center = [random.randint(self.radius, 1400 - self.radius),
                       random.randint(self.radius, 700 - self.radius)] if \
            center is None else center
        self.generation = generation

        self.target = None

        # Evolution
        self.__energy = 100
        self.e_to_create_child = e_to_create_child
        self.e_to_move = 1 if speed >= 20 else -1

        self.microbes.append(self)

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def energy(self):
        return self.__energy

    @energy.setter
    def energy(self, value):
        self.__energy = value
        if self.__energy <= 0:
            self.delete()

    def enough_to_create_child(self):
        if self.energy >= self.e_to_create_child:
            return True
        return False

    def create_child(self):
        if len(self.microbes) >= MAX_NUM_OF_MICROBES:
            self.color = self.choose_random_color()
            self.energy -= self.e_to_create_child // 2
        child_color = self.choose_random_color()
        child_speed = max(1, self.speed + self.randint_with_random_sign(10))
        child_center = self.center
        child_radius = self.radius
        child_e_to_create_child = self.e_to_create_child + self.generation
        child_generation = self.generation + 1

        Microbe(color=child_color, speed=child_speed,
                center=child_center, generation=child_generation,
                radius=child_radius, e_to_create_child=child_e_to_create_child)

        self.energy = self.e_to_create_child // 2

    def randint_with_random_sign(self, num):
        minus = -random.randint(0, num)
        plus = random.randint(0, num)
        if self.speed > 5:
            return random.choice([plus, *tuple(minus for _ in range(10))])
        else:
            return random.choice([*tuple(plus for _ in range(10)), minus])

    def eat(self, food: Food):
        food.delete()
        self.target = None
        self.energy += food.radius * 10 - self.generation

    def eat_life(self, microbe):
        if self.color == microbe.color:
            return
        if self.radius > microbe.radius:
            microbe.delete()
        elif self.radius < microbe.radius:
            self.delete()
        elif self.energy > microbe.energy:
            self.energy -= microbe.energy
            microbe.delete()
        elif self.energy < microbe.energy:
            microbe.energy -= self.energy
            self.delete()
        elif self.speed > microbe.speed:
            microbe.delete()
        elif self.speed < microbe.speed:
            self.delete()
        elif self.generation > microbe.generation:
            self.delete()
        else:
            microbe.delete()

    def delete(self):
        if self in self.microbes:
            self.microbes.remove(self)

    def show_me(self):
        return self.color, self.center, self.radius

    def move_to_nearest_food(self):
        if self.target is None:
            self.find_nearest_food()

        vector1 = pygame.math.Vector2(self.center)
        vector2 = pygame.math.Vector2(self.target.center)

        vector1.move_towards_ip(vector2, self.speed)
        self.center = vector1.xy
        self.can_eat(self.target, vector1.distance_to(vector2))

        self.energy -= self.e_to_move
        self.is_opponent_eatable()

    def find_nearest_food(self):
        nearest_distance_and_food = [10000, None]
        vector1 = pygame.math.Vector2(self.center)
        for food in Food.foods:
            vector2 = pygame.math.Vector2(food.center)
            if (distance := vector1.distance_to(vector2)) < nearest_distance_and_food[0]:
                nearest_distance_and_food = [distance, food]

        self.target = nearest_distance_and_food[1]

    def can_eat(self, food: Food, distance):
        if distance < self.radius + food.radius:
            self.eat(food)

    def is_opponent_eatable(self):
        self_vector = pygame.Vector2(self.center)
        for microbe in Microbe.microbes:
            if self.color == microbe.color:
                continue
            microbe_vector = pygame.Vector2(microbe.center)
            if self_vector.distance_to(microbe_vector) < self.radius + microbe.radius:
                self.eat_life(microbe)

    def choose_random_color(self, proc_of_another_color: int = 20):
        return self.color if random.choice([1 for _ in range(100 - proc_of_another_color)] +
                                           [0 for _ in range(proc_of_another_color)]) else \
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
