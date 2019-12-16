##REMAKING OF THE GAME TIC TAC TOE USING FUCTIONS
import os

#clearing the console
def system():
    os.system('cls' if os.name == 'nt' else 'clear')


# a function that is drawing the board
def draw_board(storeItems):
    print( f" {storeItems[0]} | {storeItems[1]} | {storeItems[2]}" )
    print( '---|---|---' )
    print( f" {storeItems[3]} | {storeItems[4]} | {storeItems[5]}" )
    print( '---|---|---' )
    print( f" {storeItems[6]} | {storeItems[7]} | {storeItems[8]}" )


# a function asking for input at the beginning defining player1 and player2
def player_input():
    player1 = None
    player2 = None
    print( 'Hello this is a game of TIC-TAC-TOE\n' )
    while player1 != 'X' and player1 != 'O':
        player1 = (input( 'Please, Player 1 choose your marker: X or O :' )).upper()

    if player1 == 'X':
        player2 = 'O'
    else:
        player2 = 'X'

    return player1, player2


#restarting the game if needed
def restart_quit():
    action = input( "Do you want to play another game? Type 'yes' or 'no' :" ).lower()
    if action == 'yes':
        return play_the_fucking_game()
    else:
        print( "Thanks for playing!" )
        quit()

# this function checks for win
def check_for_win(player, board):
    someone_won = board[0] == player and board[1] == player and board[2] == player or \
                  board[3] == player and board[4] == player and board[5] == player or \
                  board[6] == player and board[7] == player and board[8] == player or \
                  board[0] == player and board[3] == player and board[6] == player or \
                  board[1] == player and board[4] == player and board[7] == player or \
                  board[2] == player and board[5] == player and board[8] == player or \
                  board[0] == player and board[4] == player and board[8] == player or \
                  board[2] == player and board[4] == player and board[6] == player
    has_free_spaces = board[0] == 1 or board[1] == 2 or board[2] == 3 or \
                      board[3] == 4 or board[4] == 5 or board[5] == 6 or \
                      board[6] == 7 or board[7] == 8 or board[8] == 9
    if someone_won:
        return "have won!"
    elif not has_free_spaces:
        return "draw"




#checking who is winning ,and printing the appropriate things
def print_last(pl1, pl2, player, board):
    check = check_for_win(player, board)
    if check == 'have won!':
        if player == pl1:
            print( 'Player 1', check )
        elif player == pl2:
            print( 'Player 2', check )
        restart_quit()
    elif check == "draw" :
        print('You are draw!')
        restart_quit()




# function for checking if the input is the right one or it is over
def check_input(message, board, pl):
    update = int( input( message ) )
    if update < 1 or update > 9:
        print( "Please, pick a number from 1 to 9!" )
        return check_input( message, board, pl )
    elif board[update - 1] == 'X' or board[update - 1] == 'O':
        print( "Please, do not make repetitions of a numbers, pick again!" )
        return check_input( message, board, pl )
    else:
        board[update - 1] = pl


# a function thats taking input from Player 1 and Player 2 and for every turn updating the board
def updating_board(counter, board, pl1, pl2):
    if counter % 2 != 0:
        check_input( 'Player 1 choose a number on the board: ', board, pl1 )
        print_last( pl1, pl2, pl1, board )
    else:
        check_input( 'Player 2 choose a number on the board: ', board, pl2 )
        print_last( pl1, pl2, pl2, board )



#function for playing the game
def play_the_fucking_game():
    places = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pl1, pl2 = player_input()
    counter = 0
    while True:
        system()
        print(f'Now play the game! Player 1 plays with {pl1}, Player 2 plays with {pl2} !\n' )
        counter += 1
        draw_board(places)
        updating_board(counter,places,pl1,pl2)


play_the_fucking_game()