
import random
import time

import subprocess #for playing sound


card_values={'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}


def prepare_deck():
    cards_type=('A','2','3','4','5','6','7','8','9','10','J','Q','K')

    one_deck=cards_type*4

    num_decks_temp = enter_num_decks()
    deck_in_game_initial=list(one_deck)*num_decks_temp
    current_deck=deck_in_game_initial*1 #This to create a copy and be sure they are not linked
    random.shuffle(current_deck)
    card_drawer=iter(current_deck)
    play_sound('shuffle')

    return card_drawer, num_decks_temp, deck_in_game_initial

def reload_drawer(card_drawer, game_counter, num_decks, deck_in_game_initial):

    '''
    Function to reload deck when deck is more or less half spent.
    Assumed every round it is spent on average 6 cards.
    If 1 deck is used, deck is reloaded every 5 rounds.
    '''
    divisor = num_decks * 5

    if (game_counter % divisor == 0) and (game_counter != 0):

        print(f'You have played already {game_counter} rounds.\nThe casino does not want you to count cards. Hence, deck is reloaded and shuffled again')
        current_deck=deck_in_game_initial*1
        random.shuffle(current_deck)
        card_drawer=iter(current_deck)
        play_sound('shuffle')
        return card_drawer
    else:
        return card_drawer

def play_sound(sound):
    if sound == 'win':
        bashCommand = "play -q sounds/win.wav -t alsa"

    elif sound == 'defeat':
        bashCommand = "play -q sounds/gameover.wav -t alsa"

    elif sound == 'tie':
        bashCommand = "play -q sounds/tie.wav -t alsa"

    elif sound == 'draw':
        bashCommand = "play -q sounds/draw.wav -t alsa"

    elif sound == 'shuffle':
        bashCommand = "play -q sounds/shuffle.wav -t alsa"

    # How to solve the problem of getting warn t alsa on bash
    #https://www.mail-archive.com/debian-bugs-dist@lists.debian.org/msg1057438.html

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
        




def enter_num_decks():
    '''
    This function asks user to input number of decks to play game.
    Input: None for function
    Output: Integer

    '''
    num_decks=input('How many decks you want to play with at start of game? Input integer please.')
    if num_decks.isdigit():
        return int(num_decks)
    else:
        print('Wrong input value. Please enter an integer')
        return enter_num_decks()


def draw_card(card_drawer):
    '''
    This function is called when dealer draws a card
    Input: none
    Output: The next item in the deck
    '''
    card_drawn=next(card_drawer)
    play_sound('draw')

    print(f'The card is a....{card_drawn}!!')
    return card_drawn


def user_decision(user_cards,card_drawer):
    '''
    '''
    check = True
    while check:
        decision=input('Now is your turn again! What\'s gonna be, hit or stand?\n\'0\' for stand.\n\'1\' for hit)\n')
        if decision == str(0):
            print('You stand')

            return user_cards

        elif decision == str(1):
            print('Here it comes your new card...')
            time.sleep(1)
            user_cards.append(draw_card(card_drawer))
            user_count=get_count(user_cards)
            print(f'Your count is {user_count}')
        else:
            print('Wrong input value. Please enter either 0 to stand or 1 to hit')
            return user_decision()

        if user_count > 21:

            return user_cards

def get_count(card_list):
    '''
    This function updates the count of cards
    '''
    
    def reorder_aces(card_list):
        '''
        This function reorder Aces and places them at the end of the list
        '''

        if 'A' in card_list:
            card_list=sorted(card_list, key= lambda x: card_values[x])

        else:
            pass
        return card_list



    count = 0

    card_list=reorder_aces(card_list) #This is needed to deal with Aces
    for card in card_list:
        if card != 'A':
            count += card_values[card]
        else: #it means it is an Ace
            if count + card_values['A'] <= 21: #This checks if Ace as 11 exceeds 21 or not
                count += card_values['A']
            else:
                count += 1
    
    return count




def initial_user_two_cards(card_drawer):
    '''
    This functions is for hitting first two cards for player
    '''
    temp_list=[]
    for x in range(2):
        temp_list.append(draw_card(card_drawer))
        time.sleep(1)
    return temp_list


def check_user_game(user_cards):
    '''
    This checks based on the cards of the user, whether the game should continue 
    with the dealer or the user has already lost.
    '''
    user_count=get_count(user_cards)
    
    if user_count > 21:
        play_sound('gameover')
        print(f'You lose!! Sorry but you exceeded 21.\n You got a total number of {user_count}')
        return False
    else:
        return True
        

def dealer_play(dealer_cards,card_drawer):
    check = True
    while check:
        print('Here it comes a new card for dealer...')
        time.sleep(1)
        dealer_cards.append(draw_card(card_drawer))
        dealer_count=get_count(dealer_cards)
        
        if dealer_count > 21:
            return dealer_cards
        
        elif dealer_count >=17:
            return dealer_cards
        
        else:
            print(f'Dealer\'s count is now {dealer_count}')
            print(f'Count is below 17, therefore dealer decides to hit one more card')
            
def who_win(user_count, dealer_count, user_wins, dealer_wins):
    if dealer_count > 21:
        print('Congratulations!! You won!')
        print(f'Dealer exceeded 21. Dealer got {dealer_count}')
        play_sound('win')
        return user_wins + 1, dealer_wins

    elif dealer_count < user_count:
        print('Congratulations!! You won!')
        print(f'Dealer got {dealer_count} ... but you got {user_count}!!')
        play_sound('win')
        return user_wins + 1, dealer_wins

    elif user_count < dealer_count:
        print('You lose!!')
        print(f'Dealer got {dealer_count} ... but you got {user_count}....')
        print(f'It is so sad a machine outplayed you...')
        play_sound('defeat')
        return user_wins, dealer_wins + 1
    else:
        
        print('it was a tie!!')
        print(f'Dealer got {dealer_count} ... but you got {user_count}....')
        play_sound('tie')
        return user_wins, dealer_wins



def new_round_continue(user_wins, dealer_wins, game_counter):
    answer=input('What do you want to do next?\nPress 0 for a new round\nPress 1 for review statistics on this game\nPress 2 for a total new game\nPress other key to escape.')
    if answer == '0':
        return True

    elif answer == '1':
        tie_rounds = game_counter - (user_wins + dealer_wins)
        print(f'Total number of rounds: {game_counter} rounds.\n User wins:  {user_wins} rounds.\n Dealer wins: {dealer_wins} rounds.\n Tie rounds: {tie_rounds} rounds')
        return new_round_continue(user_wins, dealer_wins, game_counter)
        time.sleep(2)
    elif answer == '2':
        return False

    else:
        exit()    

