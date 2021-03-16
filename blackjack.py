import random

suits = ("Hearts","Diamond","Spades","Clubs")
ranks = ("Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace")
values = {"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,
"Ten":10,"Jack":10,"Queen":10,"King":10,"Ace":11}
playing = True

class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank +" Of "+ self.suit

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(str(Card(suit,rank)))
    def __str__(self):
        deck_comp=" " 
        for y in self.deck:
            deck_comp = deck_comp+ "\n" + y
        return "The deck has: "+deck_comp
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        singlecard = self.deck.pop()
        return singlecard                           
""" c1=Deck()
print(c1.deal()) """

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces =  0
    def add_card(self,card):                        #card passed from deck.deal->singlecard(suit,rank)
        self.cards.append(card)
        r=card.split()[0]
        self.value+=values[r]
        if r == "Ace":                        #track aces
            self.aces=self.aces+1
    def adjust_for_aces(self):
        while self.value>21 and self.aces>0: #total>21,we have ace then change value of ace from 11 to 1
            self.value-=10
            self.aces-=1            #ace used, then decrease track also

class Chips():
    def __init__(self,total=100):
        self.total=total
        self.bet=0
    def win_bet(self):
        self.total+=self.bet
    def lose_bet(self):
        self.total-=self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet=int(input("How many chips you want to bet  "))
        except ValueError as all:
             print("please provide an integer!!")
        else:
            if chips.bet>chips.total:
                print("Sorry you don't have enough chips, you have {}".format(chips.total))
            else:
                break

def hit(deck,hand):
    single_card=deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_aces()

def hit_or_stand(deck,hand):
    global playing
    while True:
        x=input("Hit or stand? Enter h or s   ")
        if x[0].lower()=='h':
            hit(deck,hand)
        elif x[0].lower()=='s':
            print("Player Stand,Dealer's Turn")
            playing = False
        else:
            print("Sorry i did not understand that, please enter h or s only")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_bust(player,dealer,chips):
    print("Player Busts")
    chips.lose_bet()
def player_win(player,dealer,chips):
    print("Player wins!!")
    chips.win_bet()
def dealer_burst(player,dealer,chips):
    print("Player wins!! Dealer busts")
    chips.win_bet()
def dealer_win(player,dealer,chips):
    print("Dealer wins!!")
    chips.lose_bet()
def push(player,dealer):
    print("Player Dealer Tie!! Push")    

while True:
    print("Welcome to BLACKJACK!!")
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()               #deal two cards to each player
    player_hand.add_card(deck.deal())    
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())    
    dealer_hand.add_card(deck.deal())
    
    player_chips = Chips()                  #set up the players chip
    #prompt the player for bet
    take_bet(player_chips)
    show_some(player_hand,dealer_hand)            #show cards but one card of dealer is hidden

    while playing:
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)    #if player hand exceeds 21, playerbusts and break loop
        if player_hand.value>21:
            player_bust(player_hand,dealer_hand,player_chips)
            break
        if player_hand.value<=21:                 #if player hasn't busted play dealers hand till 17
            while dealer_hand.value<player_hand.value:
                hit(deck,dealer_hand)
        show_all(player_hand,dealer_hand)       #show all cards

        if dealer_hand.value>21:                    #different running scenario
            dealer_burst(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_win(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_win(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    print("\n Players total chips are {}".format(player_chips.total))
    new_game=input("Would you like to play again? enter y or n  ")
    if new_game[0].lower()=='y':
        playing=True
        continue    
    else:
        print("Thankyou for playing!!")
        break  
