from random import randint
import pygame
import sys
from Microbe import Microbe, MAX_NUM_OF_MICROBES
from Food import Food, MIN_NUM_OF_FOOD

pygame.init()

size = width, height = 1400, 700

screen = pygame.display.set_mode(size)

[Microbe(color=[randint(0, 255) for _ in range(3)]) for _ in range(MAX_NUM_OF_MICROBES)]


def reload_food():
    if len(Food.foods) < MIN_NUM_OF_FOOD:
        [Food() for _ in range(50)]


def move_microbe():
    for microbe in Microbe.microbes.copy():
        microbe.move_to_nearest_food()


def draw_food_and_microbes():
    for food in Food.foods.copy():
        pygame.draw.circle(screen, *food.show_me())

    for microbe in Microbe.microbes.copy():
        pygame.draw.circle(screen, *microbe.show_me())


def day_passed():
    for microbe in Microbe.microbes.copy():
        if microbe.enought_to_create_child():
            microbe.create_child()


def draw_text():
    proprties_of_microbe = []
    font = pygame.font.Font('freesansbold.ttf', 16)
    rendering_prop = True, (0, 255, 0), (0, 0, 128)
    if Microbe.microbes:
        proprties_of_microbe.append(font.render(f"Microbes:{len(Microbe.microbes)}",
                                                *rendering_prop))
        proprties_of_microbe.append(font.render(f"Speed:{Microbe.microbes[-1].speed}",
                                                *rendering_prop))
        proprties_of_microbe.append(font.render(f"Center:{Microbe.microbes[-1].center}",
                                                *rendering_prop))
        proprties_of_microbe.append(font.render(f"Generation:{Microbe.microbes[-1].generation}",
                                                *rendering_prop))
    else:
        proprties_of_microbe.append(font.render(f"ALL DEAD", *rendering_prop))

    for num, text in enumerate(proprties_of_microbe):
        text_rect = text.get_rect()
        text_rect.topleft = (0, num*20)
        screen.blit(text, text_rect)


while True:
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.time.Clock().tick(30)
    # pygame.time.Clock().tick(1)

    day_passed()

    reload_food()
    move_microbe()

    screen.fill((0, 0, 0,))
    draw_food_and_microbes()
    draw_text()

    pygame.display.update()
