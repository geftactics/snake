#!/usr/bin/env python3

import config
import hid
import pygame
import random
import socket
import time
import threading
from stupidArtnet import StupidArtnet
from pythonosc.udp_client import SimpleUDPClient


# Init Pygame
pygame.init()
pygame.display.set_caption('Window Vipers')
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode([config.grid.WIDTH, config.grid.HEIGHT])
clock = pygame.time.Clock()


# Init OSC and Artnet objects (one per row/floor)
osc = SimpleUDPClient(config.artnet.OSC, 8010)
artnets = []
for universe in range(0, int(config.artnet.UNIVERSE_BASE+config.grid.HEIGHT/config.grid.BLOCK_SIZE+1)):
    artnets.append(StupidArtnet(config.artnet.TARGET, universe, config.artnet.PACKET_SIZE, 30, True, config.artnet.BROADCAST))




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
        time.sleep(0.01)


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
    artnet = artnets[universe]

    # LED fixture is 8 segments of 3 channels, so total 24 channels - Set all of these
    for channel in range(channel_base, channel_base + 24, 3):
        if channel > 0:
            #print('Universe: %s, Channel: %s, Colour: %s' % (universe, channel, color))
            artnet.set_rgb(channel, color[0], color[1], color[2]) 
            artnet.show()


def read_gamepad_input():
    while not game_over:
        input = tuple(gamepad.read(64))
        if input != () and input != (1, 128, 128, 127, 127, 15, 0, 0):
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": key_map.get(input, input)}))
        time.sleep(0.001)



def create_food():
    while True:
        food_pos = (random.randint(0, (config.grid.WIDTH - config.grid.BLOCK_SIZE) // config.grid.BLOCK_SIZE) * config.grid.BLOCK_SIZE, 
                    random.randint(0, (config.grid.HEIGHT - config.grid.BLOCK_SIZE) // config.grid.BLOCK_SIZE) * config.grid.BLOCK_SIZE)
        if food_pos not in snake_pos:
            update_artnet(food_pos, config.colour.FOOD)
            return food_pos


def read_tcp_control():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1234))
    server_socket.listen(1)
    server_socket.settimeout(1)  # Set a timeout for accept()

    print("Listening for incoming connections")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break  # No more data, exit the loop
                command = data.decode("utf-8").strip()
                result = f"ACK {command}"
                if command == 'space':
                    print(command)
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE }))
                if command == 'up':
                    print(command)
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP }))
                if command == 'down':
                    print(command)
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN }))
                if command == 'left':
                    print(command)
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT }))
                if command == 'right':
                    print(command)
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT }))

                print(result)
                client_socket.send(result.encode("utf-8"))

            client_socket.close()

        except socket.timeout:
            if game_over:
                break
        except socket.error as e:
            if game_over:
                break
            else:
                print("Error accepting connection")

    server_socket.close()
    print("Server socket closed")


# Start the tcp input thread
tcp_thread = threading.Thread(target=read_tcp_control)
tcp_thread.start()


while True:

    score = 0
    game_over = False
    direction = RIGHT
    snake_pos = [(config.grid.BLOCK_SIZE * 2, config.grid.BLOCK_SIZE * 2)]
    snake_pos_previous = snake_pos.copy()
    time.sleep(1)
    print(snake_pos)
    draw_snake(snake_pos, snake_pos_previous)
    
    # Waiting area before game starts
    print('Press [Space] or [Start] to play!')
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                break
            elif event.key == pygame.K_a:
                print('FIRE A')
            elif event.key == pygame.K_b:
                print('FIRE B')
    osc.send_message("/fixtures/All/visible", 0)
    time.sleep(3)

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
        snake_pos_previous = snake_pos.copy()
        snake_pos = move_snake(snake_pos, direction)


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
    time.sleep(1)
    print('Game over! Score', score)
    osc.send_message("/medias/number_" + str(score) + ".png/assign_to_all_surfaces", 1)
    osc.send_message("/fixtures/All/visible", 1)
    time.sleep(10)
    print('OSC animation trigger')
    osc.send_message("/cues/selected/cues/by_cell/col_2/row_1", 50)