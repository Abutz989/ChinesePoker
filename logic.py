import random
from GameWrapper import *
import constants as c
from collections import Counter


# help functions

class GameLogic(GameBoard):
    def __init__(self):
        GameBoard.__init__(self)
    
    def game_state(self):
        # return 'End' if the deck is empty and the player card is empty
        if self.player_card == '' and len(self.deck) == 0:
            return 'End'
        elif len(self.deck) <= 1:
            return 'Last'
        return 'Continue'

    def draw_card(self):
        return self.deck.pop()
    
    def set_card(self,place):
        # take player card and put it in player column 1 and the first empty row , do it only if the slot is empty and the previos row is full
        # find the last full row in the column
        if self.game_state() == 'Last':
            if place < 5:
                self.player_slots[4][place] = self.player_card
            return True
        
        for i in range(1,5):
            if '' not in self.player_slots[i-1] and self.player_slots[i][place] == '' and place < 5:
                self.player_slots[i][place] = self.player_card
                return True
        return False
    
    def computer_move(self,place,computer_card):
        # computer move is to put the computer card in the first empty row in the first empty column
        
        if self.game_state() == 'Last' or self.game_state() == 'End':
            if place < 5:
                self.computer_slots[4][place] = self.player_card
            return True
        
        for i in range(1,5):
            if '' not in self.computer_slots[i-1] and self.computer_slots[i][place] == '':
                self.computer_slots[i][place] = computer_card
                return True
        return False
   
    def auto_player_move(self,place,player_card):
        # computer move is to put the computer card in the first empty row in the first empty column
        
        if self.game_state() == 'Last':
            if place < 5:
                self.player_slots[4][place] = player_card
            return True
        
        for i in range(1,5):
            if '' not in self.player_slots[i-1] and self.player_slots[i][place] == '':
                self.player_slots[i][place] = player_card
                return True
        return False
    
    def hide_card(self):
        # hide the player card
        self.player_card = ''
    
    def calculate_score(self):
        # calculate the score of each column in the player slots and the computer slots and return True if the player score is higher than the computer score in at least 3 columns
        # the score is given by Poker ruls ranking
        player_count = 0
        computer_count = 0
        for j in range(5):
            player_score = 0
            computer_score = 0
            player_score,explain_player = evaluate_poker_hand([row[j] for row in self.player_slots])
            computer_score,explain_com = evaluate_poker_hand([row[j] for row in self.computer_slots])
            if player_score > computer_score:
                player_count += 1
                self.recolor_player_column(j)
                print("player win in column",j,explain_player)
            else:
                computer_count += 1
                self.recolor_computer_column(j)
                print("computer win in column",j,explain_com)
        if player_count >= 3:
            return True
        return False
    
    def getBoard(self):
        return self.Board
    
class VirtualGameLogic(GameVirtual):
    def __init__(self):
        GameVirtual.__init__(self)
    
    def game_state(self):
        # return 'End' if the deck is empty and the player card is empty
        if self.player_card == '' and len(self.deck) == 0:
            return 'End'
        elif len(self.deck) <= 1:
            return 'Last'
        return 'Continue'

    def draw_card(self):
        return self.deck.pop()
    
    def set_card(self,place):
        # take player card and put it in player column 1 and the first empty row , do it only if the slot is empty and the previos row is full
        # find the last full row in the column
        if self.game_state() == 'Last':
            if place < 5:
                self.player_slots[4][place] = self.player_card
            return True
        
        for i in range(1,5):
            if '' not in self.player_slots[i-1] and self.player_slots[i][place] == '' and place < 5:
                self.player_slots[i][place] = self.player_card
                return True
        return False
    
    def computer_move(self,place,computer_card):
        # computer move is to put the computer card in the first empty row in the first empty column
        
        if self.game_state() == 'Last' or self.game_state() == 'End':
            if place < 5:
                self.computer_slots[4][place] = self.player_card
            return True
        
        for i in range(1,5):
            if '' not in self.computer_slots[i-1] and self.computer_slots[i][place] == '' and place < 5:
                self.computer_slots[i][place] = computer_card
                return True
        return False
   
    def auto_player_move(self,place,player_card):
        # computer move is to put the computer card in the first empty row in the first empty column
        
        if self.game_state() == 'Last':
            if place < 5:
                self.player_slots[4][place] = player_card
            return True
        
        for i in range(1,5):
            if '' not in self.player_slots[i-1] and self.player_slots[i][place] == '' and place < 5:
                self.player_slots[i][place] = player_card
                return True
        return False
    
    def hide_card(self):
        # hide the player card
        self.player_card = ''
    
    def calculate_score(self):
        # calculate the score of each column in the player slots and the computer slots and return True if the player score is higher than the computer score in at least 3 columns
        # the score is given by Poker ruls ranking
        player_count = 0
        computer_count = 0
        for j in range(5):
            player_score = 0
            computer_score = 0
            player_score,explain_player = evaluate_poker_hand([row[j] for row in self.player_slots])
            computer_score,explain_com = evaluate_poker_hand([row[j] for row in self.computer_slots])
            if player_score > computer_score:
                player_count += 1
                print("player win in column",j,explain_player)
            else:
                computer_count += 1
                print("computer win in column",j,explain_com)
        if player_count >= 3:
            return True
        return False
    

def evaluate_poker_hand(hand):
    """
    Evaluates the rank of a five-card poker hand.

    Args:
        hand (list): A list of five strings representing the cards. 
                     Each card is in the format "<rank><suit>", e.g., "2H", "KD", "AS".
    
    Returns:
        tuple: The rank of the hand and its details.
    """
    # Define rank order for evaluation
    rank_order = "123456789TJQKA"
    # Split ranks and suits
    ranks = [card[:-1] for card in hand]
    suits = [card[-1] for card in hand]
    
    # Convert ranks to numerical values
    rank_values = sorted([rank_order.index(rank) for rank in ranks], reverse=True)
    
    # Check for flush (all cards have the same suit)
    is_flush = len(set(suits)) == 1
    
    # Check for straight (consecutive ranks)
    is_straight = (
        len(set(rank_values)) == 5 and 
        rank_values[0] - rank_values[-1] == 4
    )
    # Special case for a low Ace straight
    if set(rank_values) == {12, 0, 1, 2, 3}:  # A, 2, 3, 4, 5
        is_straight = True
        rank_values = [3, 2, 1, 0, -1]  # Assign low Ace value
    
    # Count occurrences of each rank
    rank_counts = Counter(rank_values)
    most_common = rank_counts.most_common()
    
    # Determine the hand rank
    if is_straight and is_flush:
        # Straight Flush
        return (8*0xff + (rank_values[0] == 12)*0x0f + rank_values[1]),'Straight Flush'
    elif most_common[0][1] == 4:
        # Four of a Kind
        return (7*0xff + most_common[0][0]*0x0f + most_common[1][0]),'Four of a Kind'
    elif most_common[0][1] == 3 and most_common[1][1] == 2:
        # Full House
        return (6*0xff + most_common[0][0]*0x0f + most_common[1][0]),'Full House'
    elif is_flush:
        # Flush
        return (5*0xff + rank_values[0]*0x0f + rank_values[1]),'Flush'
    elif is_straight:
        # Straight
        return (4*0xff + rank_values[0]*0x0f),'Straight'
    elif most_common[0][1] == 3:
        # Three of a Kind
        return (3*0xff + most_common[0][0]*0x0f + most_common[1][0]),'Three of a Kind'
    elif most_common[0][1] == 2 and most_common[1][1] == 2:
        # Two Pair
        return (2*0xff + most_common[0][0]*0x0f + most_common[2][0]),'Two Pair'
    elif most_common[0][1] == 2:
        # One Pair
        return (1*0xff + most_common[0][0]*0x0f +rank_values[0]),'One Pair'
    else:
        # High Card
        return (rank_values[0]*0x0f+rank_values[1]),'High Card'
       
   