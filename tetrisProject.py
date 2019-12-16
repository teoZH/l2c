# test this game in console
# for mac users it might not work properly :)
# i am going to try a fresh start of TETRIS ,a console game using OOP

import os
import time
import random
import keyboard



def clear_screen():
    os.system ( 'cls' if os.name == 'nt' else 'clear' )




#this decorater gives additional messages
def add_more_graphic(func):
    def wrapper(self,board):
        print ( '\t\t\tTETRIS GAME' )
        print(f'Points:{func(self,board)}')
        print('Made by Theodor for learning purposes!')
    return wrapper

#ask the player if he/she wants to play more
def ask_the_player():
    choice = ''
    choice = input ( 'Type "y" to restart or "q" to quit:' )
    if choice.lower() != 'y' and choice.lower() != 'q':
        return ask_the_player()
    return choice.lower ( ) == 'y'


# a board on which is going to to be played
class Board:

    def __init__(self):
        self.matrix = [[" "] * 12 for i in range ( 0, 24 )]
        self.can_move_to_the_left = True
        self.can_move_to_the_right = True
        self.cannot_move_downwards = False
        self.is_pressed_s = False
        self.points = 0
        self.end_game = False
        self.switch = False
        self.give_new_figure = False

        for a in range ( 0, 24 ):
            self.matrix[a][0] = "*"
            self.matrix[a][11] = "*"
        for b in range ( 0, 12 ):
            self.matrix[23][b] = "*"
            self.matrix[0][b] = '*'

    #draws the matrix
    @add_more_graphic
    def draw(self, board):
        for c in range ( 0, 24 ):
            for d in range ( 0, 12 ):
                if d == 0:
                    print ( '\t\t ' + board[c][d], end=" " )
                else:
                    print ( board[c][d], end=" " )
            print()
        return (self.points)

    #draws the final messages
    def draw_game_over(self):
        choice = ''
        print('GAME OVER NOOB!Points:',self.points)
        choice = ask_the_player()
        return choice


# figures that will fall (that are gonna be a subclass)
class Figures ( Board ):
    kvadrat = [[" ", " ", " ", " "], [" ", "*", "*", " "], [" ", "*", "*", " "], [" ", " ", " ", " "]]
    l_block = [[" ", " ", " ", " "], ["*", " ", " ", " "], ["*", "*", "*", " "], [" ", " ", " ", " "]]
    l_block1 = [[" ", " ", " ", " "], [" ", "*", " ", " "], [" ", "*", "", " "], ["*", "*", " ", " "]]
    l_block2 = [[" ", " ", " ", " "], ["*", "*", "*", " "], [" ", " ", "*", " "], [" ", " ", " ", " "]]
    l_block3 = [[" ", " ", " ", " "], ["*", "*", " ", " "], ["*", " ", " ", " "], ["*", " ", " ", " "]]
    l_blockType1 = [[" ", " ", " ", " "], ["*", " ", " ", " "], ["*", " ", " ", " "], ["*", "*", " ", " "]]
    l_blockType2 = [[" ", " ", " ", " "], [" ", " ", "*", " "], ["*", "*", "*", " "], [" ", " ", " ", " "]]
    l_blockType3 = [[" ", " ", " ", " "], ["*", "*", " ", " "], [" ", "*", " ", " "], [" ", "*", " ", " "]]
    l_blockType4 = [[" ", " ", " ", " "], ["*", "*", "*", " "], ["*", " ", " ", " "], [" ", " ", " ", " "]]
    z_block1 = [[' ', ' ', ' ', ' '], ['*', '*', ' ', ' '], [' ', '*', '*', ' '], [' ', ' ', ' ', ' ']]
    z_block2 = [[' ', ' ', ' ', ' '], [' ', '*', ' ', ' '], ['*', '*', ' ', ' '], ['*', ' ', ' ', ' ']]
    z_blockType1 = [[' ', ' ', ' ', ' '], [' ', '*', '*', ' '], ['*', '*', ' ', ' '], [' ', ' ', ' ', ' ']]
    z_blockType2 = [[' ', ' ', ' ', ' '], ['*', ' ', ' ', ' '], ['*', '*', ' ', ' '], [' ', '*', ' ', ' ']]
    line_block = [[' ', ' ', ' ', ' '], ['*', '*', '*', '*'], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]
    line_block1 = [[' ', '*', ' ', ' '], [' ', '*', ' ', ' '], [' ', '*', ' ', ' '], [' ', '*', ' ', ' ']]
    strange1 = [[' ', ' ', ' ', ' '], [' ', '*', ' ', ' '], ['*', '*', '*', ' '], [' ', ' ', ' ', ' ']]
    strange2 = [[' ', ' ', ' ', ' '], ['*', '*', '*', ' '], [' ', '*', ' ', ' '], [' ', ' ', ' ', ' ']]
    strange3 = [[' ', ' ', ' ', ' '], [' ', '*', ' ', ' '], ['*', '*', ' ', ' '], [' ', '*', ' ', ' ']]
    strange4 = [[' ', ' ', ' ', ' '], ['*', ' ', ' ', ' '], ['*', '*', ' ', ' '], ['*', ' ', ' ', ' ']]

    all = {1: kvadrat, 2: l_block, 3: l_block1, 4: l_block2, 5: l_block3, 6: l_blockType1, 7: l_blockType2,
           8: l_blockType3, 9: l_blockType4, 10: z_block1, 11: z_block2, 12: z_blockType1, 13: z_blockType2,
           14: line_block1, 15: strange1, 16: strange2, 17: strange3, 18: strange4}

    types = {'kvadrat':[kvadrat],'l_block':[l_block,l_block1,l_block2,l_block3],
             'l_blockType':[l_blockType1,l_blockType2,l_blockType3,l_blockType4],
             'z_block':[z_block1,z_block2],'z_blockType':[z_blockType1,z_blockType2],
             'strange':[strange1,strange2,strange3,strange4],
             'line_block':[line_block,line_block1]}

    move_aside = 5

    # this function takes a parameter random number and gets the desired figure from the dictionari
    def get_random_figure(self):
        random_number = random.randint ( 1, 18 )
        figure = self.all.get ( random_number )
        return figure

    # this function finds which type of figure it is and returns its position from the types dictionary
    def get_type_and_index(self,figure, type_figures):
        for keys in type_figures:
            obj = type_figures.get ( keys )
            if figure in obj:
                return keys, obj.index ( figure )

    #this function returns the next figure from the same type (it 'switches its positions')
    def get_next_of_type(self,figure, type_figures):
        name, ind = self.get_type_and_index ( figure, type_figures )
        if ind < len ( type_figures[name] ) - 1:
            ind += 1
        elif ind == len ( type_figures[name] ) - 1:
            ind = 0
        return type_figures[name][ind]

    # this function takes side borders
    def get_side_borders(self,board):
        l_rows = []
        l_cols = []
        r_rows = []
        r_cols = []
        for x in range ( 0, 24 ):
            for y in range ( 12 ):
                if board[x][y] == ' ' and board[x][y - 1] == "*":
                    l_rows.append ( x )
                    l_cols.append ( y )
                if board[x][y] == ' ' and board[x][y + 1] == '*':
                    r_rows.append ( x )
                    r_cols.append ( y )
        return l_rows, l_cols, r_rows, r_cols

    #this function does not allow moving outside borders of the game
    def check_for_side_bords_ver2(self,l_row,l_col,r_row,r_col,row,column,board):
            broke_right = False
            broke_left = False
            range_figure = len(row)
            range_right_border = len(r_row)
            range_left_border = len(l_row)

            for x in range(range_right_border):
                for y in range(range_figure):
                    if (r_row[x],r_col[x]) == (row[y],column[y]):
                        self.can_move_to_the_right = False
                        broke_right = True
                        break
                if broke_right:
                    break
            if not broke_right:
                self.can_move_to_the_right = True

            for x in range(range_left_border):
                for y in range(range_figure):
                    if (l_row[x],l_col[x]) == (row[y],column[y]):
                        self.can_move_to_the_left = False
                        broke_left = True
                        break
                if broke_left:
                    break
            if not broke_left:
                self.can_move_to_the_left = True



    #this function gets the bottom borders
    def get_bottom_border(self,board):
        rows = []
        cols = []
        for x in range ( 1, 11 ):
            for y in range ( 1, 23 ):
                if board[y + 1][x] == "*":
                    rows.append ( y )
                    cols.append ( x )
                    break
        row = []
        col = []
        for x in range ( len ( cols ) ):
            y: int
            for y in range ( rows[x], 23 ):
                pos_r = y
                pos_c = cols[x]
                if board[pos_r][pos_c] == ' ' and board[pos_r + 1][pos_c] == '*':
                    row.append ( (pos_r) )
                    col.append ( pos_c )
        del rows, cols
        return row, col

    #checks if there is something below the figure
    def check_bottom_and_add(self,b_row,b_col,row,column,board):
        broke = False
        if len(row) != len(column):
            print("ERROR!")
            quit()
        range_figure = len(row)
        range_bottom_border = len(b_row)
        for x in range(range_bottom_border):
            for y in range(range_figure):
                if (b_row[x],b_col[x]) == (row[y],column[y]):
                    self.cannot_move_downwards = True
                    self.matrix = list ( map ( list, board ) )
                    broke = True
                    break
            if broke:
                break
        if not broke:
            self.cannot_move_downwards = False

    #this function checks for full lines and removes them
    def check_for_full_lines(self,board):
        add_points = False
        full_line = None
        cleaned_lines = []
        for x in range ( 22, 0, -1 ):
            if  ' ' in board[x]:
                full_line = False
            else:
                full_line = True
            if full_line:
                add_points = True
                for y in range ( 1, 11 ):
                    board[x][y] = ' '
                cleaned_lines.append(x)
                for z in range ( x, 1, -1 ):
                    board[z] = board[z - 1]
        self.matrix = list ( map ( list, board ) )
        if add_points:
            self.points += len(cleaned_lines)

    #this function checks if game cannot continue ('the player made "*" to the top')
    def checks_for_end(self,count):
        if count == 0 and self.cannot_move_downwards == True:
            self.end_game = True


    #this function "draws" the figure inside the matrix
    def figure_inside_matrix(self,board,figure,cols,rows,count):
        for x in range ( 4 ):
            for y in range ( 4 ):
                    if figure[x][y] == '*':
                        board[x + count][y + self.move_aside] = '*'
                        cols.append(y+self.move_aside)
                        rows.append(x+count)


    # sometimes when the figure is switched and its on the right side a glitch shows up
    # so the figure gets out of the "board"
    def checks_for_getting_out(self, switched, l_rows,l_cols,r_rows,r_cols,rows,cols,figure,board,count):
        correct_right = False
        correct_left = False
        if switched:
            for x in range(len(rows)):
                for y in range(len(l_rows)):
                    if (rows[x],cols[x]) == (l_rows[y],l_cols[y]-1):
                        correct_left = True
                        break
            for x in range(len(rows)):
                for y in range(len(l_rows)):
                    if (rows[x],cols[x]) == (r_rows[y],r_cols[y]+1):
                        correct_right = True
                        break
            if correct_left is True and correct_right is False:
                self.move_aside += 1
            elif correct_left is False and correct_right is True:
                self.move_aside -= 1
            elif correct_right is True and correct_left is True:
                figure = self.get_next_of_type(figure,self.types)
        return self.figure_inside_matrix(board,figure,cols,rows,count)





    #this function implements figures into the board
    def implement(self, count, figure):
        columns = []
        rows = []
        board = list ( map ( list, self.matrix ) )
        self.check_for_full_lines ( board )
        b_rows,b_cols = self.get_bottom_border(board)
        l_rows, l_cols, r_rows, r_cols = self.get_side_borders(board)
        self.figure_inside_matrix(board,figure,columns,rows,count)
        self.checks_for_getting_out (self.switch,l_rows,l_cols,r_rows,r_cols,rows,columns,figure,board,count)
        self.check_for_side_bords_ver2(l_rows,l_cols,r_rows,r_cols,rows, columns,board)
        self.check_bottom_and_add(b_rows,b_cols,rows,columns,board)
        self.checks_for_end(count)
        self.switch = False
        return board




class Engine:
    def __init__(self, board):
        self.board = board
        self.figure = None
        self.switch = False

    #this function checks for pressed button and makes the necessary changes
    def check_for_change(self):
        for x in range(500):
            if keyboard.is_pressed ( 'a' ):
                if self.board.can_move_to_the_left:
                    self.board.move_aside += -1
                    break
            elif keyboard.is_pressed ( 'd' ):
                if self.board.can_move_to_the_right:
                    self.board.move_aside += 1
                    break
            elif keyboard.is_pressed('s'):
                self.is_pressed_s = True
            elif keyboard.is_pressed('w'):
                self.board.switch = True
                self.is_pressed_w = True



    #this function is going to give the player a few moments before the new figure starts falling
    def only_in_case(self,board,counter,figure):
        for x in range(30):
            clear_screen()
            if x == 30:
                self.board.give_new_figure = True
            board = self.board.implement(counter,figure)
            self.board.draw(board)
            self.check_for_change()
        time.sleep(0.01)




    #thеse are starting phrases
    def start(self):
        print ( 'Hello this is a game of tetris' )
        print ( 'Press "A" to move left, "D" to move right, "S" to move downwards,"W" to rotate the figure' )
        print ( 'Please enlarge your windows before you start!' )
        print ( 'Press Enter to start' )
        input ( )

    #this function moves figure downards,left,right
    def move(self, counter=0):
        choice = None
        first_counter = 0
        figure = self.board.get_random_figure ( )
        while True:
            self.is_pressed_w = False
            self.is_pressed_s = False
            clear_screen ( )
            first_counter += 1
            if first_counter  % 3 == 0:
                counter += 1
            board= self.board.implement ( counter, figure )
            self.board.draw ( board )
            first_counter += 1
            self.check_for_change ()
            if self.is_pressed_w:
                figure = self.board.get_next_of_type(figure,self.board.types)
            if self.board.cannot_move_downwards:
                return self.play()
            if self.is_pressed_s:
                continue
            time.sleep ( .1 )

    #this function gives you the option to restart the game
    def game_over(self):
        choice = self.board.draw_game_over()
        if choice is True:
            self.board.end_game = False
            return the_game()
        else:
            print('Thanks for playing!')
            quit()


    #play the game
    def play(self):
        if not self.board.end_game:
            self.board.cannot_move_downwards = False
            self.board.move_aside = 5
            counter = 0
            self.move ( counter )
        else:
            self.game_over()

    # start a new game
    def fresh_start(self):
        self.start()
        self.play()


def the_game():
    board = Figures ( )
    game = Engine ( board )
    game.fresh_start ( )


the_game()
