import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the dimensions of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Set the dimensions of the snake block
BLOCK_SIZE = 50

# Initialize Pygame
pygame.init()

# Set the font for displaying the score
font = pygame.font.Font(None, 36)

# Set the caption of the screen
pygame.display.set_caption("Snake Game")

# Create the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Define the direction constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Define the initial direction
direction = RIGHT

# Define the initial position of the snake
snake_pos = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]

# Define the initial position of the food
food_pos = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

# Define the initial score
score = 0

# Define the clock for controlling the frame rate
clock = pygame.time.Clock()

# Define a function for drawing the snake
def draw_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, [pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE])
        update_block_color(pos, GREEN)

# Define a function for moving the snake
def move_snake(snake_pos, direction):
    # Get the head position of the snake
    x = snake_pos[0][0]
    y = snake_pos[0][1]

    # Move the snake in the specified direction
    if direction == UP:
        y -= BLOCK_SIZE
    elif direction == DOWN:
        y += BLOCK_SIZE
    elif direction == LEFT:
        x -= BLOCK_SIZE
    elif direction == RIGHT:
        x += BLOCK_SIZE

    # Add the new head position to the front of the snake
    snake_pos.insert(0, (x, y))

    # Remove the tail position from the back of the snake
    snake_pos.pop()
    update_block_color(snake_pos[-1], BLACK)

    return snake_pos

# Define a function for checking if the snake has collided with the walls or itself
def check_collision(snake_pos):
    # Check if the snake has collided with the walls
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= SCREEN_WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= SCREEN_HEIGHT:
        return True

    # Check if the snake has collided with itself
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            return True

    return False

# Define a function for drawing the score
def draw_score(score):
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, [10, 10])

def update_block_color(pos, color):
    x, y = pos
    print(x,y,color)
    pygame.draw.rect(screen, color, [x, y, BLOCK_SIZE, BLOCK_SIZE])

# Set the game loop flag
done = False

# Start the game loop
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
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

    # Check for collisions
    if check_collision(snake_pos):
        done = True

    # Check if the snake has eaten the food
    if snake_pos[0] == food_pos:
        # Add a new block to the snake
        snake_pos.append(snake_pos[-1])

        # Generate a new position for the food
        food_pos = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

        # Increment the score
        score += 10

    # Fill the background
    screen.fill(BLACK)

    # Draw the snake and the food
    draw_snake(snake_pos)
    pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])

    # Draw the score
    draw_score(score)

    # Update the screen
    pygame.display.update()

    # Set the frame rate
    clock.tick(0.5)

# Quit Pygame
pygame.quit()
