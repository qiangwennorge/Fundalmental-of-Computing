# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand?"
score = 0
stand_flag = True
hit_flag = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        output = ""
        
        for card in self.cards:
            output += " " + card.__str__()
        # return a string representation of a hand
        return "Hand contains" + output

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
        

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        aces = False
        
        for card in self.cards:
            rank = card.get_rank()
            
            if rank == 'A':
                aces = True
            
            value += VALUES[rank]
        
        if value <= 11 and aces:
            value += 10
         
        return value
   
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 74

            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        output = ""
        
        for card in self.cards:
            output += " " + card.__str__()
        # return a string representation of a deck
        return "Deck contains" + output
        
        
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, stand_flag
    
    stand_flag = True
    hit_flag = True

    # your code goes here
    
    if in_play:
        outcome = "Player lost because player gives up. New Deal?"
        score -= 1
        in_play = False
        
    else:
        deck = Deck()
        deck.shuffle()
        
        outcome = "Hit or Stand?"
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(deck.deal_card())        
        dealer_hand.add_card(deck.deal_card())
        
        player_hand.add_card(deck.deal_card())        
        dealer_hand.add_card(deck.deal_card())
        
        in_play = True
    


def hit():
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    global outcome, in_play, player_hand, score, hit_flag
    
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            if player_hand.get_value() > 21:
                outcome = "Player lost because of busted, New Deal?"
                score -= 1
                in_play = False
        else:
            outcome = "Player lost because of busted, New Deal?"
            
            if hit_flag:
                score -= 1
            hit_flag = False
            in_play = False
    
       
def stand():
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    global outcome, in_play, player_hand, dealer_hand, score, stand_flag
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
        in_play = False
        
    if dealer_hand.get_value() > 21:
        outcome = "Dealer lost because of busted, Congratulations!"
        if stand_flag:
            score += 1
        stand_flag = False
    
    elif player_hand.get_value() > 21:
        outcome = "Player lost because of busted, New Deal?"
        if stand_flag:
            score -= 1
        stand_flag = False
    
    elif dealer_hand.get_value() < player_hand.get_value():
        outcome = "Dealer lost because of lower value, Congratulations!"
        if stand_flag:
            score += 1
        stand_flag = False
        
    else:
        outcome = "Player lost because of lower value, New Deal?"
        if stand_flag:
            score -= 1
        stand_flag = False
      

    
# draw handler    

def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, in_play, score, player_hand, dealer_hand

    canvas.draw_text("Blackjack", [200, 50], 50 ,"White")
    

    player_hand.draw(canvas, [100, 350])
    dealer_hand.draw(canvas, [100, 200])
    
    canvas.draw_text("Dealer", [80, 180], 20, "Black")
    canvas.draw_text("Player", [80, 330], 20, "Black")

    canvas.draw_text(outcome, [30, 145], 20 ,"Red")

    canvas.draw_text("Current Score: %s" % score, [200, 100], 20 ,"Black")

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,249), CARD_BACK_SIZE)

#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

# remember to review the gradic rubric