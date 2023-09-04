#!/usr/bin/env python3

import config
import hid
import pygame
import random
import time
import threading
from stupidArtnet import StupidArtnet
from pythonosc.udp_client import SimpleUDPClient


# TODO: fix artnet object creation
# TODO: fix artnet missing crash
# TODO: infinate game loop, controller start button to begin
# TODO: select button to toggle pyro lock, and a/b triggers


# Init OSC
osc_ip = "2.0.0.100"
client = SimpleUDPClient(osc_ip, 8010)
#client.send_message("/cues/selected/cues/by_cell/col_28/row_1", 1)
time.sleep(2)


# Init Pygame & Art-Net
pygame.init()
pygame.display.set_caption('Window Vipers')
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode([config.grid.WIDTH, config.grid.HEIGHT])
clock = pygame.time.Clock()


# TODO - fix this so we generate objects based on config files!!!
artnet1 = StupidArtnet(config.artnet.TARGET, 21, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST)
artnet2 = StupidArtnet(config.artnet.TARGET, 22, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST)
artnet3 = StupidArtnet(config.artnet.TARGET, 23, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST)
artnet4 = StupidArtnet(config.artnet.TARGET, 24, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST)
artnet5 = StupidArtnet(config.artnet.TARGET, 25, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST)


# NES Gamepad
try:
    gamepad = hid.device()
    gamepad.open(0x0810, 0xe501)
    gamepad.set_nonblocking(True)
    key_map = {
        (1, 128, 128, 127,   0, 15,  0, 0): pygame.K_UP,
        (1, 128, 128, 127, 255, 15,  0, 0): pygame.K_DOWN,
        (1, 128, 128, 0,   127, 15,  0, 0): pygame.K_LEFT,
        (1, 128, 128, 255, 127, 15,  0, 0): pygame.K_RIGHT
    }
except Exception as e:
    gamepad = None


# Constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# Initial states
score = 0
game_over = False
direction = RIGHT
snake_pos = [(config.grid.BLOCK_SIZE * 2, config.grid.BLOCK_SIZE * 2)]


def draw_snake(snake_pos, snake_pos_previous):
    update_artnet(snake_pos_previous[-1], config.colour.BACKGROUND)
    for pos in snake_pos:
        pygame.draw.rect(screen, config.colour.SNAKE, [pos[0], pos[1], config.grid.BLOCK_SIZE, config.grid.BLOCK_SIZE])
        update_artnet(pos, config.colour.SNAKE)


def move_snake(snake_pos, direction):
    x = snake_pos[0][0]
    y = snake_pos[0][1]
    
    if direction == UP:
        y -= config.grid.BLOCK_SIZE
    elif direction == DOWN:
        y += config.grid.BLOCK_SIZE
    elif direction == LEFT:
        x -= config.grid.BLOCK_SIZE
    elif direction == RIGHT:
        x += config.grid.BLOCK_SIZE

    snake_pos.insert(0, (x, y)) # Add head
    snake_pos.pop() # Remove tail

    return snake_pos


def check_collision(snake_pos):
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= config.grid.WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= config.grid.HEIGHT:
        return True
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            return True
    return False


def draw_score(score):
    text = font.render("Score: " + str(score), True, config.colour.SCORE)
    screen.blit(text, [10, 10])
    

def update_artnet(pos, color):
    x = int(pos[0] // config.grid.BLOCK_SIZE) + 1
    y = int(pos[1] // config.grid.BLOCK_SIZE) + 1
    #print('x: %s, y: %s' % (x, y))

    channel_base = int(((pos[0] // config.grid.BLOCK_SIZE) * 24) + 1)
    universe = config.artnet.UNIVERSE_BASE + int(pos[1] // config.grid.BLOCK_SIZE)
    #artnet.set_universe(universe)

    if universe == 21:
        artnet = artnet1
    if universe == 22:
        artnet = artnet2
    if universe == 23:
        artnet = artnet3
    if universe == 24:
        artnet = artnet4
    if universe == 25:
        artnet = artnet5 

    # LED fixture is 8 segments of 3 channels, so total 24 channels - Set all of these
    for channel in range(channel_base, channel_base + 24, 3):
        #print('Universe: %s, Channel: %s, Colour: %s' % (universe, channel, color))
        artnet.set_rgb(channel, color[0], color[1], color[2]) 
        artnet.show()


def read_gamepad_input():
    while not game_over:
        input = tuple(gamepad.read(64))
        if input != () and input != (1, 128, 128, 127, 127, 15, 0, 0):
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": key_map.get(input, input)}))
        time.sleep(0.005)  


def create_food():
    print('creating food')
    while True:
        food_pos = (random.randint(0, (config.grid.WIDTH - config.grid.BLOCK_SIZE) // config.grid.BLOCK_SIZE) * config.grid.BLOCK_SIZE, 
                    random.randint(0, (config.grid.HEIGHT - config.grid.BLOCK_SIZE) // config.grid.BLOCK_SIZE) * config.grid.BLOCK_SIZE)
        if food_pos not in snake_pos:
            update_artnet(food_pos, config.colour.FOOD)
            return food_pos
    

food_pos = create_food()

# Start the gamepad input thread
if gamepad is not None:
    input_thread = threading.Thread(target=read_gamepad_input)
    input_thread.start()


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
    snake_pos_previous = snake_pos.copy()
    snake_pos = move_snake(snake_pos, direction)
    print(' ')


    # Check for collisions
    if check_collision(snake_pos):
        game_over = True


    # Check if the snake has eaten the food
    if snake_pos[0] == food_pos:
        snake_pos.append(snake_pos[-1])
        food_pos = create_food()
        score += 1


    # Draw the snake/food/score
    screen.fill(config.colour.BACKGROUND)
    draw_snake(snake_pos, snake_pos_previous)
    pygame.draw.rect(screen, config.colour.FOOD, [food_pos[0], food_pos[1], config.grid.BLOCK_SIZE, config.grid.BLOCK_SIZE])
    draw_score(score)
    pygame.display.update()


    # Framerate
    clock.tick(config.misc.SPEED)


# Fin
client.send_message("/cues/selected/cues/by_cell/col_28/row_1", 1)
time.sleep(2)
client.send_message("/cues/selected/cues/by_cell/col_3/row_1", 50)
pygame.quit()