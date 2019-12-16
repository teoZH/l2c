####CREATING A GAME OF BLACK JACK
import random
import time
import os


def systema():
    os.system( 'cls' if os.name == 'nt' else 'clear' )


# CREATING THE DECK OF CARDS   # cards normal pack of 52
types = ['♠Spades♠', '♥Hearts♥', '♦Diamоnds♦', '♣Clubs♣']
cards = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10, 'Jack': 10, 'Queen': 10,
         'King': 10, 'Ace': 11}


# CREATING PLAYERS
class Player:
    my_score = 0
    #for testing purposes
    #create_deck = ['Ace ♥Hearts♥', '7 ♦Diamоnds♦','King ♦Diamоnds♦', '10 ♣Clubs♣', 'Jack ♣Clubs♣', 'Ace ♠Spades♠',
                       # '6 ♥Hearts♥']

    def __init__(self, deck_cards):
        #gets instance of cards from Class
        self.deck_cards = deck_cards
        # that will be used only by the cpu
        self.create_deck = deck_cards.shuffle()
        #shuffles all of the cards
        self.my_cards = []
        self.money = 0

    def get_cards(self, been_given,player_turn,cpu_turn):
        choice = ''
        score_got = 0
        self.my_cards.append( been_given )
        if player_turn:
            if 'Ace' in been_given:
                while choice != '11' and choice != '1':
                    choice = (input(f"!!!Score:{self.my_score}.You have an Ace! Choose 11 or 1:"))
                score_got = int(choice)
            else:
                score_got = self.deck_cards.cards[been_given.split()[0]]
        elif cpu_turn:
            if 'Ace' in been_given:
                if self.my_score + 11 <= 21:
                    score_got = 11
                else:
                    score_got = 1
            else:
                score_got = self.deck_cards.cards[been_given.split()[0]]
        self.my_score += score_got


# what does each player do ?
class Human( Player ):

    def hit(self, given,player_t,cpu_t):
        self.get_cards( given ,player_t,cpu_t)


class CPU( Player ):

    def hit(self, given,player_t,cpu_t):
        self.get_cards( given,player_t,cpu_t)

    # giving cards to players
    def give(self):
        give_card_from_deck = self.create_deck.pop( 0 )
        return give_card_from_deck


# creating cards
class Cards:
    # should take  parameters "types" and "cards"
    def __init__(self, types, cards):
        self.types = types
        self.cards = cards

    # the cards should be able to be  shuffled
    # a deck of cards must be created :) with mixed cards :)
    def shuffle(self):
        cards_real = list( self.cards.keys() )
        deck_ordered = [card + " " + colour for card in cards_real for colour in self.types]
        mixed = random.sample( deck_ordered, 52 )
        return mixed


# drawing the of the board , displaying the game
class Board:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    # this is an empty board
    def empty_board(self, bet):
        print( 'THIS IS A SIMPLE VERSION OF THE GAME BLACKJACK!' )
        print( 'CREATED BY TEO FOR LEARNING PURPOSES! SORRY FOR BUGS\n' )
        print( f"Result CPU:{self.player1.my_score}\t\t\t\t\tMoney:{self.player1.money}" )
        print( 'No cards' )
        print( f':\n:\t\t\tBet:{bet}\n:\n:' )
        print( 'No cards' )
        print( f"Result Player:{self.player2.my_score}\t\t\t\t\tMoney:{self.player2.money}" )


    # this draws before the player refuses to take more cards
    def draw_while_player(self, bet):
        print( 'THIS IS A SIMPLE VERSION OF THE GAME BLACKJACK!' )
        print( 'created by TEO for learning purposes :) Sorry for bugs!\n' )
        score = self.player1.deck_cards.cards[self.player1.my_cards[0].split()[0]]
        print( f"Result CPU:{score}\t\t\t\t\tMoney:{self.player1.money}" )
        print( self.player1.my_cards[0] )
        print( f":\n:\t\t\tBet:{bet}\n:\n:" )
        for result in self.player2.my_cards:
            print( result, end=" / " )
        print()
        print( f"Result Player:{self.player2.my_score}\t\t\t\tMoney:{self.player2.money}" )


    # this draws after the player refuses to take cards
    def draw_after(self, bet):
        print( 'THIS IS A SIMPLE VERSION OF THE GAME BLACKJACK!' )
        print( 'CREATED BY TEO FOR LEARNING PURPOSES! SORRY FOR BUGS\n')
        print( f"Result CPU:{self.player1.my_score}\t\t\t\t\t\t\tMoney:{self.player1.money}" )
        for result in self.player1.my_cards:
            print( result, end=" / " )
        print()
        print( f':\n:\t\t\tBet:{bet}\n:\n:' )
        for result in self.player2.my_cards:
            print( result, end=" / " )
        print()
        print( f"Result Player:{self.player2.my_score}\t\t\t\t\t\tMoney:{self.player2.money}" )


# the logic of the game
class TheGamePlay:
    final_messages = ['☻ You have BLACKJACK! YOU WIN THE DEAL! ☻',
                      '☹ CPU has BLACKJACK! YOU LOSE THE DEAL! ☹',
                      'YOU ARE DRAW!',
                      '☹ CPU WINS THE DEAL BECAUSE YOU BUSTED! ☹',
                      '☻ YOU WIN THE DEAL, BECAUSE CPU BUSTED! ☻',
                      '☻ YOU WIN THE DEAL! ☻',
                      '☹ CPU WINS THE DEAL! ☹']

    def __init__(self, pl1, pc):
        self.pl1 = pl1
        self.pc = pc
        self.duska = Board( self.pc, self.pl1 )
        self.total = 0
        self.is_checked = False
        self.player_has_to_play = True
        self.cpu_has_to_play = False

    # function that is simplifing  check_for_blackjack
    def check_someone(self, hand_of_cards):
        ten_in_card = False
        ace_in_cards = False
        for card in hand_of_cards:
            if 'Ace' in card:
                ace_in_cards = True
            elif 'King' in card or 'Queen' in card or 'Jack' in card or '10' in card:
                ten_in_card = True
        return ten_in_card and ace_in_cards

    # this checks after dealing two cards if the player or the dealer has blackjack
    def check_for_blackjack(self):
        cpu_has_blackjack = False

        player_has_blackjack = self.check_someone( self.pl1.my_cards )

        if "Ace" in self.pc.my_cards[0] or 'King' in self.pc.my_cards[0] or 'Queen' in self.pc.my_cards[0] \
                or 'Jack' in self.pc.my_cards[0] or '10' in self.pc.my_cards[0]:
            cpu_has_blackjack = self.check_someone( self.pc.my_cards )

        if player_has_blackjack is True and cpu_has_blackjack is True:
            return "Draw"
        elif player_has_blackjack is True and cpu_has_blackjack is False:
            return 'Win'
        elif player_has_blackjack is False and cpu_has_blackjack is True:
            return 'Lose'

    # checks who has won restarts values and restarts the game
    def winner_check(self, message):
        if 'BLACKJACK' in message and 'YOU WIN' in message:
            self.pl1.money +=  self.total
            if self.pc.money - (0.25 * self.total) < 0:
                self.pl1.money += self.pc.money
                self.pc.money = 0
            else:
                self.pl1.money += 0.25 * self.total
                self.pc.money -= 0.25 * self.total


        elif 'BLACKJACK' in message and 'YOU LOSE' in message:
            self.pc.money += self.total

        elif 'YOU WIN' in message:
            self.pl1.money += self.total

        elif 'CPU WINS' in message:
            self.pc.money += self.total

        elif 'YOU ARE DRAW' in message:
            self.pc.money += 0.5 * self.total
            self.pl1.money += 0.5 * self.total

        self.pc.create_deck += self.pl1.my_cards + self.pc.my_cards
        self.total = 0
        systema()
        self.duska.draw_after( self.total )
        print(message)
        time.sleep(0.5)
        self.pl1.my_score = 0
        self.pc.my_score = 0
        self.pl1.my_cards = []
        self.pc.my_cards = []
        self.is_checked = False
        self.cpu_has_to_play = False
        self.player_has_to_play = True
        return self.second_part()

    #ask how much money are going to be used from the player and the cpu
    def ask_for_money(self):
        money = ''
        self.duska.empty_board(self.total)
        print( '☛ Hey how much money are you going to use for this game?' )
        while not money.isdigit():
            money = ( input() )
            if not money.isdigit():
                print('✘ Use numbers RETARD! ✘')
        self.pl1.money = float(money)
        self.pc.money = float(money)
        print( f'☛ Okey, press ENTER to start playing!' )
        input()


    #this gives you the option to restart or quit when you finish the game
    def quit_restart(self):
        izbor = input( "Type 'y' to restart or 'n' to quit:" )
        if izbor.lower() == 'y': return self.play()
        elif izbor.lower() == 'n' : quit()
        else: return self.quit_restart()


    #this checks the bet if it is bigger ot not enough etc...
    def check_the_bet(self,bet_money):
        if bet_money > self.pl1.money:
            print('✘ Not enough money to make this bet! ✘')
            return self.second_part()
        elif bet_money > self.pc.money:
            self.total = 2 * self.pc.money
            self.pl1.money -= self.pc.money
            self.pc.money = 0
        else:
            self.pl1.money -= bet_money
            self.pc.money -= bet_money
            self.total = 2 * bet_money

    #this checks how much money do you have
    def check_availability(self):
        if self.pl1.money <= 0:
            print('☹ GAME OVER! YOU LOSE! ☹')
            self.quit_restart()
        elif self.pc.money <= 0:
            print("☻ CONGRATULATIONS , YOU WON! ☻")
            self.quit_restart()

    #this checks the money, and gives cards to players
    def first_deal(self):
        bet = ''
        self.check_availability()
        bet = input( "☛ Please make a bet:" )
        if not bet.isdigit():
            print("✘ DIGITS NOOB ✘")
            return self.first_deal()
        self.check_the_bet(float(bet))
        for deal in range( 1, 5 ):
            if deal % 2 != 0:
                given = self.pc.give()
                self.pl1.get_cards( given, player_turn=True,cpu_turn=False)
            else:
                given = self.pc.give()
                self.pc.get_cards( given, player_turn=False, cpu_turn=True )

    #this checks the cards for blackjack after the cards are given, (only the first time by the rules)
    def after_deal_check(self):
        result = None
        if self.is_checked is False:
            result = self.check_for_blackjack()
            self.is_checked = True
        if result:
            self.duska.draw_after( self.total )
            if result == 'Win':
                print( self.final_messages[0] )
                self.winner_check( self.final_messages[0] )
            elif result == 'Lose':
                print( self.final_messages[1] )
                self.winner_check( self.final_messages[1] )
            elif result == 'Draw':
                print( self.final_messages[2] )
                self.winner_check( self.final_messages[2] )
            time.sleep( 0.5 )

    #this function wants from the player an action to get a new card or to stop taking cards
    def players_turn(self, choice):
        igrach, procesor = True, False
        while choice.lower() != 'hit' and choice.lower() != 'stand':
            choice = input( 'What do you choose: Stand ot Hit:\n' )
        if choice.lower() == 'hit':
            self.pl1.hit( self.pc.give(),self.player_has_to_play,self.cpu_has_to_play )
            time.sleep(0.5)
        elif choice.lower() == 'stand':
            igrach = False
            procesor = True
        return igrach, procesor

    #this checks if the player has more than 21 points
    def check_player_for_busting(self):
        if self.pl1.my_score > 21:
            systema()
            self.duska.draw_after( self.total )
            print( self.final_messages[3] )
            self.winner_check( self.final_messages[3] )
            time.sleep(0.5)

    #the cpu gives cards to itself
    def cpu_turn(self):
        if self.pc.my_score < 17:
            systema()
            self.duska.draw_after( self.total )
            self.pc.get_cards( self.pc.give(),self.player_has_to_play,self.cpu_has_to_play )
            time.sleep(1.5)

    #this checks if the cpu has more than 21 points
    def check_cpu_for_busting(self):
        igrach, procesor = False, True
        if self.pc.my_score > 21:
            systema()
            self.duska.draw_after( self.total )
            print( self.final_messages[4] )
            self.winner_check(self.final_messages[4])
            time.sleep(0.5)

    #this compares both scores if it is reached and gives some of the results
    def compare_both(self):
        systema()
        self.duska.draw_after( self.total )
        if self.pc.my_score == self.pl1.my_score:
            print( self.final_messages[2] )
            self.winner_check( self.final_messages[2] )
        elif self.pc.my_score < self.pl1.my_score:
            print( self.final_messages[5] )
            self.winner_check( self.final_messages[5] )
        elif self.pc.my_score > self.pl1.my_score:
            print( self.final_messages[6] )
            self.winner_check( self.final_messages[6] )
        time.sleep( 0.5 )


    #this function defines the logic of the taking more  cards from
    # the cpu and making all of the checks that are required
    def stand_or_hit(self):
        while True:
            choice = ''
            if self.player_has_to_play is True:
                systema()
                self.duska.draw_while_player( self.total )
                self.after_deal_check()
                self.player_has_to_play, self.cpu_has_to_play = self.players_turn( choice )
                self.check_player_for_busting()
            elif self.cpu_has_to_play is True:
                self.cpu_turn()
                self.check_cpu_for_busting()
            if self.cpu_has_to_play is True and self.pc.my_score >= 17:
                self.cpu_has_to_play = False
                self.player_has_to_play = True
                self.compare_both()

    #asking how much money you and the cpu will use for the game
    def first_part(self):
        self.ask_for_money()

    #the whole logic of givig cards,getting more if required , and making the needed checks
    def second_part(self):
        self.first_deal()
        self.stand_or_hit()
    #the whole logic of the game
    def play(self):
        self.first_part()
        self.second_part()



cards = Cards( types, cards )
cpu = CPU( cards )
player = Human( cards )
game = TheGamePlay( player, cpu )
game.play()
