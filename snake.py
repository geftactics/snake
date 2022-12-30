import config
import pygame
import random
import sys
import time
import uuid

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        self.alive = True

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        cur_y = int(cur[0]/gridsize)
        cur_x = int(cur[1]/gridsize)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            lights(new, config.colors.snake)
            if len(self.positions) > self.length:
                old = self.positions.pop()
                if (cur_x+cur_y)%2 == 0:
                    lights(old, config.colors.grid1)
                else:
                    lights(old, config.colors.grid2)

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        self.alive = False
        print('DIED')

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, config.colors.snake, r)
            pygame.draw.rect(surface, config.colors.grid1, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.randomize_position()

    def randomize_position(self):
        time.sleep(0.2)
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)
        lights(self.position, config.colors.food)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, config.colors.food, r)
        pygame.draw.rect(surface, config.colors.grid1, r, 1)
        lights((self.position[0], self.position[1]), config.colors.food)

def drawGrid(surface, setup=False):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            game_x = x*20
            game_y = y*20
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, config.colors.grid1, r)
                if setup:
                   lights((game_x, game_y), config.colors.grid1)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, config.colors.grid2, rr)
                if setup:
                    lights((game_x, game_y), config.colors.grid2)

def lights(position, colour):
    x = int(position[0] / gridsize)
    y = int(position[1] / gridsize)
    print('TURN_ON: %s,%s @ %s' % (x, y, colour))
    with open('mock-lights/' + str(uuid.uuid4()) + '.dat', 'w') as f:
        f.write(str(x) + ',' + str(y) + ',' + str(colour[0]) + ',' + str(colour[1]) + ',' + str(colour[2]))

def draw_score(score):
    # TODO
    lights((2*gridsize,1*gridsize), config.colors.score)

    lights((5*gridsize,1*gridsize), config.colors.score)
    lights((6*gridsize,1*gridsize), config.colors.score)
    lights((7*gridsize,1*gridsize), config.colors.score)
    lights((8*gridsize,1*gridsize), config.colors.score)

    lights((11*gridsize,1*gridsize), config.colors.score)
    lights((12*gridsize,1*gridsize), config.colors.score)
    lights((13*gridsize,1*gridsize), config.colors.score)
    lights((14*gridsize,1*gridsize), config.colors.score)
    lights((15*gridsize,1*gridsize), config.colors.score)


screen_width = 360
screen_height = 120

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface, setup=True)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(5)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if not snake.alive:
            drawGrid(surface, setup=True)
            print('GRID RESET')
            pygame.time.wait(5 * 1000)
            draw_score(108)
            pygame.time.wait(10 * 1000)
            drawGrid(surface, setup=True)
            pygame.time.wait(2 * 1000)
            food.randomize_position()
            snake.alive = True
        if snake.get_head_position() == food.position:
            lights(food.position, config.colors.snake)
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()

main()
