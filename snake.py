import pygame
import random
from stupidArtnet import StupidArtnet


# ArtNet connection
target_ip = '2.0.0.1'
universe = 0
packet_size = 300 # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 30, True, False)
print(artnet)


# Colours
SNAKE_COLOUR = (0, 255, 0)
FOOD_COLOUR = (255, 0, 0)
BACKGROUND_COLOUR = (0, 0, 100)
SCORE_COLOUR = (255, 255, 255)


# Grid config
GRID_WIDTH = 600
GRID_HEIGHT = 600
BLOCK_SIZE = 50


# Initialize Pygame
pygame.init()
font = pygame.font.Font(None, 36)
pygame.display.set_caption('Window Vipers')
screen = pygame.display.set_mode([GRID_WIDTH, GRID_HEIGHT])
clock = pygame.time.Clock()


# Constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# Define initial states
direction = RIGHT
snake_pos = [(GRID_WIDTH / 2, GRID_HEIGHT / 2)]
game_over = False
score = 0


def draw_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, SNAKE_COLOUR, [pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE])


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
    update_artnet((x, y), SNAKE_COLOUR)

    # Remove tail
    snake_pos.pop()
    update_artnet(snake_pos[-1], BACKGROUND_COLOUR)

    return snake_pos


def check_collision(snake_pos):
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= GRID_WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= GRID_HEIGHT:
        return True
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            return True
    return False


def draw_score(score):
    text = font.render("Score: " + str(score), True, SCORE_COLOUR)
    screen.blit(text, [10, 10])
    

def update_artnet(pos, color):
    print(pos, color)
    artnet.set_single_value(2, random.randint(0,255))
    artnet.show()


def create_food():
    while True:
        food_pos = (random.randint(0, (GRID_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE, 
                    random.randint(0, (GRID_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        if food_pos not in snake_pos:
            update_artnet(food_pos, FOOD_COLOUR)
            return food_pos


# Define the initial position of the food
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
            elif event.key == pygame.K_LEFT:
                direction = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                direction = RIGHT


    # Move the snake
    snake_pos = move_snake(snake_pos, direction)
    print('.')


    # Check for collisions
    if check_collision(snake_pos):
        game_over = True


    # Check if the snake has eaten the food
    if snake_pos[0] == food_pos:
        snake_pos.append(snake_pos[-1])
        food_pos = create_food()
        score += 10


    # Draw the snake/food/score
    screen.fill(BACKGROUND_COLOUR)
    draw_snake(snake_pos)
    pygame.draw.rect(screen, FOOD_COLOUR, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])
    draw_score(score)
    pygame.display.update()


    # Framerate
    clock.tick(5)


# Fin
artnet.blackout()
pygame.quit()