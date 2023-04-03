#!/usr/bin/env python3

import config
import pygame
import random
from stupidArtnet import StupidArtnet


# Init Pygame & Art-Net
pygame.init()
font = pygame.font.Font(None, 36)
pygame.display.set_caption('Window Vipers')
screen = pygame.display.set_mode([config.grid.width, config.grid.height])
clock = pygame.time.Clock()
artnet = StupidArtnet(config.artnet.target, config.artnet.universe, config.artnet.packet_size, 30, True, config.artnet.broadcast)
print(artnet)


# Constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# Initial states
score = 0
game_over = False
direction = RIGHT
snake_pos = [(config.grid.width / 2, config.grid.height / 2)]


def draw_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, config.colour.snake, [pos[0], pos[1], config.grid.block_size, config.grid.block_size])


def move_snake(snake_pos, direction):
    x = snake_pos[0][0]
    y = snake_pos[0][1]

    if direction == UP:
        y -= config.grid.block_size
    elif direction == DOWN:
        y += config.grid.block_size
    elif direction == LEFT:
        x -= config.grid.block_size
    elif direction == RIGHT:
        x += config.grid.block_size

    # Add head
    snake_pos.insert(0, (x, y))
    update_artnet((x, y), config.colour.snake)

    # Remove tail
    snake_pos.pop()
    update_artnet(snake_pos[-1], config.colour.background)

    return snake_pos


def check_collision(snake_pos):
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= config.grid.width or snake_pos[0][1] < 0 or snake_pos[0][1] >= config.grid.height:
        return True
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            return True
    return False


def draw_score(score):
    text = font.render("Score: " + str(score), True, config.colour.score)
    screen.blit(text, [10, 10])
    

def update_artnet(pos, color):
    channel = int(((pos[0] // config.grid.block_size) * 3) + 1)
    universe = int(pos[1] // config.grid.block_size)
    print('Universe: %s, Channel: %s, Colour: %s' % (universe, channel, color))
    artnet.set_single_value(2, random.randint(0,255))
    # Untested, but should be the answer
    # artnet.set_universe(universe)
    # artnet.set_rgb(channel, color[0], color[1], color[2])
    artnet.show()


def create_food():
    while True:
        food_pos = (random.randint(0, (config.grid.width - config.grid.block_size) // config.grid.block_size) * config.grid.block_size, 
                    random.randint(0, (config.grid.height - config.grid.block_size) // config.grid.block_size) * config.grid.block_size)
        if food_pos not in snake_pos:
            update_artnet(food_pos, config.colour.food)
            return food_pos


food_pos = create_food()


# Game loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                direction = UP
            elif event.key == pygame.K_DOWN and direction != UP:
                direction = DOWN
            elif event.key == pygame.K_LEFT and direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                direction = RIGHT


    # Move the snake
    snake_pos = move_snake(snake_pos, direction)
    print(' ')


    # Check for collisions
    if check_collision(snake_pos):
        game_over = True


    # Check if the snake has eaten the food
    if snake_pos[0] == food_pos:
        snake_pos.append(snake_pos[-1])
        food_pos = create_food()
        score += 10


    # Draw the snake/food/score
    screen.fill(config.colour.background)
    draw_snake(snake_pos)
    pygame.draw.rect(screen, config.colour.food, [food_pos[0], food_pos[1], config.grid.block_size, config.grid.block_size])
    draw_score(score)
    pygame.display.update()


    # Framerate
    clock.tick(config.misc.speed)


# Fin
artnet.blackout()
pygame.quit()