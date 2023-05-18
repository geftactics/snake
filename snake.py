#!/usr/bin/env python3

import config
import pygame
import random
from stupidArtnet import StupidArtnet


# Constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
BLOCK_SIZE = config.grid.BLOCK_SIZE
GRID_WIDTH = config.grid.WIDTH * BLOCK_SIZE
GRID_HEIGHT = config.grid.HEIGHT * BLOCK_SIZE


# Init Pygame & Art-Net
pygame.init()
pygame.display.set_caption('Window Vipers')
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode([GRID_WIDTH, GRID_HEIGHT])
clock = pygame.time.Clock()
artnet = StupidArtnet(config.artnet.TARGET, config.artnet.UNIVERSE, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST)
print(artnet)


# Initial states
score = 0
game_over = False
direction = RIGHT
snake_pos = [
    (round(GRID_WIDTH / 2 / BLOCK_SIZE) * BLOCK_SIZE, 
     round(GRID_HEIGHT / 2 / BLOCK_SIZE) * BLOCK_SIZE)
]


def draw_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, config.colour.SNAKE, [pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE])


def move_snake(snake_pos, direction):
    x = snake_pos[0][0]
    y = snake_pos[0][1]

    if direction == UP:
        y -= BLOCK_SIZE
    elif direction == DOWN:
        y += BLOCK_SIZE
    elif direction == LEFT:
        x -= BLOCK_SIZE
    elif direction == RIGHT:
        x += BLOCK_SIZE

    # Add head
    snake_pos.insert(0, (x, y))
    update_artnet((x, y), config.colour.SNAKE)

    # Remove tail
    snake_pos.pop()
    update_artnet(snake_pos[-1], config.colour.BACKGROUND)

    return snake_pos


def check_collision(snake_pos):
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= GRID_WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= GRID_HEIGHT:
        return True
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            return True
    return False


def draw_score(score):
    text = font.render("Score: " + str(score), True, config.colour.SCORE)
    screen.blit(text, [10, 10])
    

def update_artnet(pos, color):
    channel = int(((pos[0] // BLOCK_SIZE) * 3) + 1)
    universe = int(pos[1] // BLOCK_SIZE)
    #print('Universe: %s, Channel: %s, Colour: %s' % (universe, channel, color))
    artnet.set_single_value(2, random.randint(0,255))
    # Untested, but should be the answer
    # artnet.set_universe(universe)
    # artnet.set_rgb(channel, color[0], color[1], color[2])
    artnet.show()


def create_food():
    while True:
        food_pos = (random.randint(0, (GRID_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randint(0, (GRID_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        if food_pos not in snake_pos:
            update_artnet(food_pos, config.colour.FOOD)
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
    screen.fill(config.colour.BACKGROUND)
    draw_snake(snake_pos)
    pygame.draw.rect(screen, config.colour.FOOD, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])
    draw_score(score)
    pygame.display.update()


    # Framerate
    clock.tick(config.misc.SPEED)


# Fin
artnet.blackout()
pygame.quit()