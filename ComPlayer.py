import constants as c
import random
import time
from GameWrapper import *
from abc import abstractmethod
from itertools import combinations
from collections import Counter
from huristic import *
from logic import evaluate_poker_hand

class AbstractMovePlayer():

    @abstractmethod
    def get_move(self,player_slots,computer_slots,computer_card,game_state) -> int:
        pass


class StupidPlayer(AbstractMovePlayer):
   
    def get_move(self,player_slots,computer_slots,computer_card,game_state) -> int:
        
        if game_state == 'Last'  or game_state == 'End':
            return 0
        for i in range(5):
            for j in range(5):
                if computer_slots[i][j] == '':
                    return j
        return 0
   
class GreedyMovePlayer(AbstractMovePlayer):
    """ Greedy move player is a player that always choose the move that maximize the expected value of the hand.
    """
    # python main.py -player1 ImprovedGreedyMovePlayer -player2 RandomIndexPlayer
    
    def __init__(self):
        AbstractMovePlayer.__init__(self)

    def get_move(self,player_slots,computer_slots,computer_card,game_state) -> int:
        
        inner_deck = [f"{rank}{suit}" for suit in c.SUITS for rank in c.RANKS]
        # make a list of all the cards in player slots,computer slots and computer card
        for i in range(5):
            for j in range(5):
                if player_slots[i][j] != '':
                    inner_deck.remove(player_slots[i][j])
                if computer_slots[i][j] != '':
                    inner_deck.remove(computer_slots[i][j])
    
        inner_deck.remove(computer_card)

        optional_moves_score = {0 : -100, 1 : -100, 2 : -100, 3 : -100, 4 : -100,9:-10}
        if game_state == 'Last'  or game_state == 'End':
            for j in range(5):
                current_hand = [row[j] for row in computer_slots if row[j] != ''] 
                current_hand_expected_value = CalcExpectedValue(current_hand, inner_deck)
                hand = current_hand[:-1] + [computer_card]
                optional_value = CalcExpectedValue(hand, inner_deck) 
                if optional_value > current_hand_expected_value:
                    optional_moves_score[j] = optional_value

        else:
            RowCheckedFlag = False
            for i in range(5):
                for j in range(5):
                    if computer_slots[i][j] == '':
                        hand = [row[j] for row in computer_slots if row[j] != ''] + [computer_card]
                        optional_moves_score[j] = CalcExpectedValue(hand, inner_deck)
                        RowCheckedFlag = True
                if RowCheckedFlag:
                    break   
              
        return max(optional_moves_score, key=optional_moves_score.get)   
        
class CompetativePlayer(AbstractMovePlayer):
    """ Competative move player is a player that always choose the move that maximize the expected value of the hand.
    """
    # python main.py -player1 ImprovedGreedyMovePlayer -player2 RandomIndexPlayer
    
    def __init__(self):
        AbstractMovePlayer.__init__(self)

    def get_move(self,player_slots,computer_slots,computer_card,game_state) -> int:
        
        inner_deck = [f"{rank}{suit}" for suit in c.SUITS for rank in c.RANKS]
        # make a list of all the cards in player slots,computer slots and computer card
        for i in range(5):
            for j in range(5):
                if player_slots[i][j] != '':
                    inner_deck.remove(player_slots[i][j])
                if computer_slots[i][j] != '':
                    inner_deck.remove(computer_slots[i][j])
    
        inner_deck.remove(computer_card)

        optional_moves_score = {0 : -1000, 1 : -1000, 2 : -1000, 3 : -1000, 4 : -1000, 9:-100}
        if game_state == 'Last' or game_state == 'End':
            for j in range(5):
                current_hand = [row[j] for row in computer_slots if row[j] != ''] 
                oppennet_hand = [row[j] for row in player_slots if row[j] != '']
                oppennet_hand_expected_value = CalcExpectedValue(oppennet_hand, inner_deck)
                current_hand_expected_value = CalcExpectedValue(current_hand, inner_deck)- oppennet_hand_expected_value
                hand = current_hand[:-1] + [computer_card]
                optional_value = CalcExpectedValue(hand, inner_deck) - oppennet_hand_expected_value
                if optional_value > current_hand_expected_value:
                    optional_moves_score[j] = optional_value
        else:
            RowCheckedFlag = False
            for i in range(5):
                for j in range(5):
                    if computer_slots[i][j] == '':
                        hand = [row[j] for row in computer_slots if row[j] != ''] + [computer_card]
                        oppennet_hand = [row[j] for row in player_slots if row[j] != '']
                        optional_moves_score[j] = CalcExpectedValue(hand, inner_deck) - CalcExpectedValue(oppennet_hand, inner_deck)
                        RowCheckedFlag = True
                if RowCheckedFlag:
                    break   

        return max(optional_moves_score, key=optional_moves_score.get)   
    
class MinMaxPlayer(AbstractMovePlayer):
    
    def __init__(self):
        AbstractMovePlayer.__init__(self)

    def get_move(self,player_slots,computer_slots,computer_card,game_state) -> int:
        
        inner_deck = [f"{rank}{suit}" for suit in c.SUITS for rank in c.RANKS]
        # make a list of all the cards in player slots,computer slots and computer card
        for i in range(5):
            for j in range(5):
                if player_slots[i][j] != '':
                    inner_deck.remove(player_slots[i][j])
                if computer_slots[i][j] != '':
                    inner_deck.remove(computer_slots[i][j])
    
        inner_deck.remove(computer_card)
        MinMaxFlag = True if len(inner_deck) <= 22 else False
        greedy_moves_score = self.max_value(computer_slots,computer_card,game_state,inner_deck)
        minmax_moves_score = greedy_moves_score.copy()
        if MinMaxFlag:
            # loop in all the possible moves when optional_move_score > 0
            for j in range(5):
                if greedy_moves_score[j] > 0:
                    for card in inner_deck:
                        temp_deck = inner_deck.copy()
                        temp_deck.remove(card)
                        oppennet_hand = [row[j] for row in player_slots if row[j] != '']
                        oppennet_hand_expected_value = CalcExpectedValue(oppennet_hand, temp_deck)
                        if oppennet_hand_expected_value >= greedy_moves_score[j]:
                            for card in temp_deck:
                                temp_deck_sec = temp_deck.copy()
                                temp_deck_sec.remove(card)
                                sec_geme_state = 'Last' if len(temp_deck_sec) <= 2 else 'Continue'
                                computer_score_sec = self.max_value(computer_slots,card,sec_geme_state,temp_deck_sec)
                                minmax_moves_score[j] = max(min(minmax_moves_score[j],computer_score_sec[j]),0)
            # where greedy_moves_score < 0 the minmax_move_score will be the same as greedy_moves_score
            for j in range(5):
                if greedy_moves_score[j] < 0:
                    minmax_moves_score[j] = greedy_moves_score[j]

            return max(minmax_moves_score, key=minmax_moves_score.get)
        else: 
            return max(greedy_moves_score, key=greedy_moves_score.get)
        

    def max_value(self,computer_slots,computer_card,game_state,inner_deck):
        optional_moves_score = {0 : -100, 1 : -100, 2 : -100, 3 : -100, 4 : -100,9:-10}
        if game_state == 'Last' or game_state == 'End':
            for j in range(5):
                current_hand = [row[j] for row in computer_slots if row[j] != ''] 
                current_hand_expected_value = CalcExpectedValue(current_hand, inner_deck)
                hand = current_hand[:-1] + [computer_card]
                optional_value = CalcExpectedValue(hand, inner_deck) 
                if optional_value > current_hand_expected_value:
                    optional_moves_score[j] = optional_value

        else:
            RowCheckedFlag = False
            for i in range(5):
                for j in range(5):
                    if computer_slots[i][j] == '':
                        hand = [row[j] for row in computer_slots if row[j] != ''] + [computer_card]
                        optional_moves_score[j] = CalcExpectedValue(hand, inner_deck)
                        RowCheckedFlag = True
                if RowCheckedFlag:
                    break   
              
        return optional_moves_score   
    
class MinMaxPlayerV2(AbstractMovePlayer):
    
    def __init__(self):
        AbstractMovePlayer.__init__(self)

    def get_move(self,player_slots,computer_slots,computer_card,game_state) -> int:
        
        inner_deck = [f"{rank}{suit}" for suit in c.SUITS for rank in c.RANKS]
        # make a list of all the cards in player slots,computer slots and computer card
        for i in range(5):
            for j in range(5):
                if player_slots[i][j] != '':
                    inner_deck.remove(player_slots[i][j])
                if computer_slots[i][j] != '':
                    inner_deck.remove(computer_slots[i][j])
    
        inner_deck.remove(computer_card)
        # check the first raw that is not full
        first_open_idx = sum([1 for j in range(5) if computer_slots[j] != ['']*5])
        MinMaxFlag = True if first_open_idx >= 5 else False
        greedy_moves_score = self.max_value(computer_slots,computer_card,game_state,inner_deck)
        minmax_moves_score = {0 : -100, 1 : -100, 2 : -100, 3 : -100, 4 : -100,9:-10}
        if MinMaxFlag:
            # loop in all the possible moves when optional_move_score > 0
            for j in range(5):
                if greedy_moves_score[j] > 0:
                    for card in inner_deck:
                        temp_deck = inner_deck.copy()
                        temp_deck.remove(card)
                        oppennet_hand = [row[j] for row in player_slots if row[j] != ''] + [card]
                        oppennet_hand_value = evaluate_poker_hand(oppennet_hand)
                        if oppennet_hand_value >= minmax_moves_score[j]:
                            for card in temp_deck:
                                temp_deck_sec = temp_deck.copy()
                                temp_deck_sec.remove(card)
                                
                                com_hand = [row[j] for row in computer_slots if row[j] != ''] + [card]
                                computer_score_sec = evaluate_poker_hand(com_hand)
                                minmax_moves_score[j] = max(min(minmax_moves_score[j],computer_score_sec-oppennet_hand_value),0)
            # where greedy_moves_score < 0 the minmax_move_score will be the same as greedy_moves_score
            for j in range(5):
                if greedy_moves_score[j] < 0:
                    minmax_moves_score[j] = greedy_moves_score[j]

            return max(minmax_moves_score, key=minmax_moves_score.get)
        else: 
            return max(greedy_moves_score, key=greedy_moves_score.get)
        

    def max_value(self,computer_slots,computer_card,game_state,inner_deck):
        optional_moves_score = {0 : -100, 1 : -100, 2 : -100, 3 : -100, 4 : -100,9:-10}
        if game_state == 'Last' or game_state == 'End':
            for j in range(5):
                current_hand = [row[j] for row in computer_slots if row[j] != ''] 
                current_hand_expected_value = CalcExpectedValue(current_hand, inner_deck)
                hand = current_hand[:-1] + [computer_card]
                optional_value = CalcExpectedValue(hand, inner_deck) 
                if optional_value > current_hand_expected_value:
                    optional_moves_score[j] = optional_value

        else:
            RowCheckedFlag = False
            for i in range(5):
                for j in range(5):
                    if computer_slots[i][j] == '':
                        hand = [row[j] for row in computer_slots if row[j] != ''] + [computer_card]
                        optional_moves_score[j] = CalcExpectedValue(hand, inner_deck)
                        RowCheckedFlag = True
                if RowCheckedFlag:
                    break   
              
        return optional_moves_score   