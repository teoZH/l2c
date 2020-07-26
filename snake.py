import pygame
from copy import deepcopy
import random
import time

DIRECTIONS = {'up': lambda x, y: [x, y - 20],
              'down': lambda x, y: [x, y + 20],
              'left': lambda x, y: [x - 20, y],
              'right': lambda x, y: [x + 20, y]}
WIDTH = 800
HEIGHT = 600
starting_width = 360
starting_height = 260
pixels = 20
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PURE PYTHON SIMPLE SNAKE")
snake = [[starting_width - pixels, starting_height],
         [starting_width, starting_height],
         [starting_width + pixels, starting_height]]
clock = pygame.time.Clock()
initial_dir = 'right'
popped = False
apple_coord = []
score = 0
my_font = pygame.font.SysFont('Arial', 30, True)


def draw_snake_and_score(snk):
    global screen
    for bd in snk:
        pygame.draw.rect(screen, (255, 0, 0), (bd[0], bd[1], pixels, pixels))
    text_score = my_font.render(f'Score: {score}', False, (102, 255, 255))
    screen.blit(text_score, (WIDTH - 200, HEIGHT - 100))


def move_snake():
    global initial_dir, snake, snake_copy, popped, apple_coord, running, eaten, score
    snake[-1] = DIRECTIONS[initial_dir](snake[-1][0], snake[-1][1])
    for x in range(len(snake_copy[:-1])):
        snake[x] = snake_copy[x + 1]
    if snake.count(snake[-1]) == 2:
        eaten = True
    if snake[-1] == apple_coord:
        snake.insert(0, snake_copy[0])
        score += 1
        popped = False
        apple_coord = []
    if snake[-1][0] >= WIDTH:
        snake[-1][0] = 0
    if snake[-1][0] < 0:
        snake[-1][0] = WIDTH - pixels
    if snake[-1][1] >= HEIGHT:
        snake[-1][1] = 0
    if snake[-1][1] < 0:
        snake[-1][1] = HEIGHT - pixels


def draw_game_over(scr):
    global screen, running
    game_over_surface = my_font.render(f'GAME OVER!Your score is {scr}!', False, (102, 255, 255))
    quit = my_font.render('Press Q to quit the game! :)', False, (102, 255, 255))
    screen.blit(game_over_surface, (WIDTH // 4, HEIGHT // 2))
    screen.blit(quit, (WIDTH // 4, HEIGHT // 2 + 60))


def check_events():
    global initial_dir, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and initial_dir != 'right':
                initial_dir = 'left'
            if event.key == pygame.K_RIGHT and initial_dir != 'left':
                initial_dir = 'right'
            if event.key == pygame.K_DOWN and initial_dir != 'top':
                initial_dir = 'down'
            if event.key == pygame.K_UP and initial_dir != 'down':
                initial_dir = 'up'


def check_event_game_over():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False


def pop_apple():
    global popped, apple_coord

    if not popped:
        x = WIDTH / 20
        y = HEIGHT / 20
        apple_coord.append((random.randint(1, x - 1) * 20))
        apple_coord.append((random.randint(1, y - 1) * 20))
        popped = True

    pygame.draw.rect(screen, (0, 255, 0), (*apple_coord, pixels, pixels))


eaten = False
running = True
while running:
    screen.fill((0, 0, 0))
    if eaten is False:
        check_events()
        snake_copy = deepcopy(snake)
        draw_snake_and_score(snake)
        if eaten is True:
            continue
        pop_apple()
        move_snake()
    else:
        check_event_game_over()
        draw_game_over(score)
    pygame.display.flip()
    clock.tick(8)
