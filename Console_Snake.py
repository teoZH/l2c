from os import system
from os import name
from time import sleep
from random import randint
import keyboard

# function which clears the console

down = lambda x: (x[0] + 1, x[1]) if not x[0] + 1 == 14 else (1, x[1])
top = lambda x: (x[0] - 1, x[1]) if not x[0] - 1 == 0 else (13, x[1])
right = lambda x: (x[0], x[1] + 1) if not x[1] + 1 == 14 else (x[0], 1)
left = lambda x: (x[0], x[1] - 1) if not x[1] - 1 == 0 else (x[0], 13)


def clear_console():
    if name == 'nt':
        system('cls')
    elif name == 'posix':
        system('clear')


# function for drawing the shit out on your console :D
def draw(mtx):
    for x in range(15):
        for y in range(15):
            print(mtx[x][y], end=' ')
        print()


def check_for_change(move_down, move_up, move_right, move_left):
    for x in range(400):
        if keyboard.is_pressed('s'):
            if move_up is False:
                move_down = True
                move_up, move_right, move_left = False, False, False
        elif keyboard.is_pressed('a'):
            if move_right is False:
                move_left = True
                move_right, move_up, move_down = False, False, False
        elif keyboard.is_pressed('d'):
            if move_left is False:
                move_right = True
                move_left, move_up, move_down = False, False, False
        elif keyboard.is_pressed('w'):
            if move_down is False:
                move_up = True
                move_down, move_right, move_left = False, False, False
    return move_down, move_up, move_right, move_left


def moving(body):
    last = body[len(body) - 1]
    new = None
    for x in range(len(body) - 2, -1, -1):
        new = body[x]
        body[x] = last
        last = new
    return body


class Matrix:
    # here we create something like a blueprint for your matrix that will be created on every cycle
    def __init__(self):
        self.board = [[' ' for x in range(15)] for x in range(15)]
        for x in range(15):
            self.board[0][x] = "*"
            self.board[14][x] = "*"
            self.board[x][0] = '*'
            self.board[x][14] = '*'


class Snake:

    def __init__(self):
        self.inital_values = [(2, 6), (3, 6), (4, 6)]
        self.body = [(2, 6), (3, 6), (4, 6)]
        self.move_down = False
        self.move_right = False
        self.move_left = False
        self.move_up = False

    def eat(self, matrix):
        x, y = self.body[len(self.body) - 1]
        added = False
        if matrix[x][y] == '@':
            self.body.append((x, y))
            added = True
            clear_console()
            draw(matrix)
            clear_console()
        return added

    def move(self):
        self.move_down, self.move_up, self.move_right, self.move_left = check_for_change(self.move_down, self.move_up,
                                                                                         self.move_right,
                                                                                         self.move_left)

        if self.move_down:
            self.body = moving(self.body)
            self.body[len(self.body) - 1] = down(self.body[len(self.body) - 1])
        elif self.move_up:
            self.body = moving(self.body)
            self.body[len(self.body) - 1] = top(self.body[len(self.body) - 1])
        elif self.move_right:
            self.body = moving(self.body)
            self.body[len(self.body) - 1] = right(self.body[len(self.body) - 1])
        elif self.move_left:
            self.body = moving(self.body)
            self.body[len(self.body) - 1] = left(self.body[len(self.body) - 1])


class Apple:

    def __init__(self):
        self.fruit = None

    def generate_random_apple(self):
        row = randint(1, 13)
        col = randint(1, 13)
        self.fruit = (row, col)


class Game:

    def __init__(self, matrix, snake, apple):
        self.matrix = matrix
        self.snake = snake
        self.apple = apple
        self.eaten = True
        self.self_bitten = False

    def import_snake_apple(self, some_board):
        for x in self.snake.body:
            some_board[x[0]][x[1]] = '#'
        if self.eaten is True:
            while self.apple.fruit in self.snake.body or self.apple.fruit is None:
                self.apple.generate_random_apple()
            self.eaten = False
        row, col = self.apple.fruit
        some_board[row][col] = '@'

        return some_board

    def play(self):
        field = []
        length_before = None
        length_after = None

        while True:
            clear_console()
            field = list(map(list, self.matrix.board))
            field = self.import_snake_apple(field)
            self.eaten = self.snake.eat(field)
            draw(field)
            length_before = len(set(self.snake.body))
            self.snake.move()
            length_after = len(set(self.snake.body))
            if length_after < length_before:
                over = ''
                while over.lower() != 'y' and over.lower() != 'n':
                    over = input('Game Over! Type y to restart or n to exit: ')
                if over.lower() == 'y':
                    self.snake.body = list(map(tuple, self.snake.initial_values))
                    self.snake.move_down = False
                    self.snake.move_right = False
                    self.snake.move_left = False
                    self.snake.move_up = False
                    return self.play()
                else:
                    print('Thank you for playing!')
                    break
            sleep(0.15)


apl = Apple()
snk = Snake()
matrica = Matrix()
game = Game(matrica, snk, apl)
game.play()
