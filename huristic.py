from itertools import combinations
from collections import Counter

def CalcExpectedValue(hand, deck):
    " This function calculates the expected value of the hand given the deck"
    # Merge hand and deck
    card_prob = 1/(len(deck)+0.001)
    open_slots = 5 - len(hand)
    all_cards = hand + deck
    rank_order = "23456789TJQKA"
    value = 0
    hand_ranks = [card[0] for card in hand]
    hand_ranks_values = sorted([rank_order.index(rank) for rank in hand_ranks])
    hand_rank_counts = Counter(hand_ranks_values)
    hand_suits = [card[1] for card in hand]


    deck_ranks = [card[0] for card in deck]
    deck_ranks_values = sorted([rank_order.index(rank) for rank in deck_ranks], reverse=True)
    deck_rank_counts = Counter(deck_ranks_values)
    deck_suits = [card[1] for card in deck]

    all_cards_rank_counts = hand_rank_counts + deck_rank_counts
    # build a dictionary of wigehts for each rank
    weights_dic = {'2': [0]*13,'3': [0]*13,'4': [0]*13,'22': [0]*13,'23': [0]*13,'s': [0]*5,'f': [0],'sf': [0]}
    
    for rank in range(13):
        # look for pairs
        if all_cards_rank_counts[rank] >= 2:
            if hand_rank_counts[rank] == 2:
                weights_dic['2'][rank] += 1
            elif hand_rank_counts[rank] == 1:
                weights_dic['2'][rank] += card_prob if open_slots >= 1 else 0
            elif hand_rank_counts[rank] == 0:
                weights_dic['2'][rank] += card_prob**2 if open_slots >= 2 else 0
        # look for triaples
        if all_cards_rank_counts[rank] >= 3:
            if hand_rank_counts[rank] == 3:
                weights_dic['3'][rank] += 1
            elif hand_rank_counts[rank] == 2:
                weights_dic['3'][rank] += card_prob    
            elif hand_rank_counts[rank] == 1:
                weights_dic['3'][rank] += card_prob**2 if open_slots >=2 else 0
            elif hand_rank_counts[rank] == 0:
                weights_dic['3'][rank] += card_prob**3 if open_slots >=3 else 0
        # look for quads
        if all_cards_rank_counts[rank] == 4:
            if hand_rank_counts[rank] == 4:
                weights_dic['4'][rank] += 1
            elif hand_rank_counts[rank] == 3:
                weights_dic['4'][rank] += card_prob if open_slots >=1 else 0    
            elif hand_rank_counts[rank] == 2:
                weights_dic['4'][rank] += card_prob**2 if open_slots >=2 else 0
            elif hand_rank_counts[rank] == 1:
                weights_dic['4'][rank] += card_prob**3 if open_slots >=3 else 0
   
    for r1 in range(13):
         # look for two pairs
        #  weights_dic['22'] equals the elemnt wise product of the weights in weights_dic['2'] placed in two different ranks
        weights_dic['22'][r1] = sum([weights_dic['2'][r1] * weights_dic['2'][r2] for r2 in range(r1+1,13)]) 
    
        # look for full house
        #  weights_dic['23'] equals the product of the weights in weights_dic['2'] and weights_dic['3'] placed in two different ranks
        weights_dic['23'][r1] = sum([weights_dic['2'][r1] * weights_dic['3'][r2] for r2 in range(r1+1,13)]) 

    # look for flash
    if len(set(hand_suits)) == 1:
        if deck_suits.count(hand_suits[0]) >= open_slots:
                weights_dic['f'][0] = (card_prob*deck_suits.count(hand_suits[0]))**(open_slots)
        
    # look for straight
    # check if hand has any of the rank 4,5,6,7,8 and if them max rank - min rank <= 4 and if all ranks in hand different from each other
    # if so, the hand has a straight possibility
    if len(set(all_cards_rank_counts).intersection(set(range(4,9)))) >= 1 \
        and max(hand_ranks_values) - min(hand_ranks_values) <= 4 \
        and len(set(hand_ranks_values)) == (5-open_slots):
        # chech if the hand has the rank 5
        for i in range(5):
            if max(hand_ranks_values) - (i+4) <=4 and (i+4) - min(hand_ranks_values) <=4:
                missing_ranks = [rank for rank in range(i+4,i+9) if rank not in hand_ranks_values]
                # check if the deck has the missing cards
                if all([rank in deck_ranks_values for rank in missing_ranks]):
                # set the weights for the card_prob*the times the missing cards are in the deck
                    weights_dic['s'][i] = sum([card_prob*deck_ranks_values.count(rank) for rank in missing_ranks])**open_slots

    # calculate straight flash possibility
    if sum(weights_dic['s']) > 0 and weights_dic['f'][0] > 0:
        weights_dic['sf'][0] = sum(weights_dic['s'])*weights_dic['f'][0]


    

    value = 1*sum(weights_dic['2'])  + 2*sum(weights_dic['22']) + 4*sum(weights_dic['3']) + \
            16*weights_dic['s'][0] + 32*weights_dic['f'][0] + 64*sum(weights_dic['23']) +\
            128*sum(weights_dic['4']) + 256*weights_dic['sf'][0]
    return value
   