from Card import TreasureCard, ActionCard, VictoryCard
from random import random

ACTION_PHASE = 0
BUY_PHASE = 1
CLEANUP_PHASE = 2

class Player (object):

    def __init__(self,name,game):
        self.name = name
        self.hand = []
        self.active_cards = []
        self.discard = []
        self.deck = []
        self.score = 0
        self.game = game

    def drawCard(self):
        '''
        Draws a card from the player's deck and adds it to their hand.
        Returns the card drawn.
        '''
        # Shuffle deck if necessary
        if len(self.deck) < 5:
            self.shuffle(self.discard)
            self.deck = self.discard + self.deck
            self.discard = []
        card = self.deck.pop()
        self.hand.append(card)
        return card

    def gain(self,card,**kwargs):
        to = self.discard if 'to' not in kwargs else kwargs['to']
        '''
        Player gains a card.
        '''
        if card:
            to.append(card)

    def discardCard(self,cardName):
        '''
        Discards a named card from the player's hand. Returns the card discarded,
        or None if no such card exists.
        '''
        cards = filter(lambda x:x.name == cardName,self.hand)
        if len(cards) == 0:
            return None
        self.hand.remove(cards[0])
        self.discard.append(cards[0])
        return cards[0]

    def cardToDeckChoice(self,selection):
        '''
        Select a card from 'selection' to put on top of the deck.
        '''
        raise NotImplementedError
        
    def discardCardChoice(self):
        '''
        Prompts the user to discard a card. Returns the card discarded, or None.
        '''
        raise NotImplementedError

    def printStatus(self):
        def round5(num):
            return int(float(num)/5)*5
        print 30 * '-'
        print "About {} cards left in your deck, {} in the discard.".format(round5(len(self.deck)),
                                                                            round5(len(self.discard)))
        print "BUYS: %d, ACTIONS: %d, COIN: %d"%(self.numBuys,self.numActions,self.coin)
        print 30 * '-'

    def takeTurn(self):
        '''
        The player takes a turn. Do not override this method. See selectCard()
        and buyCard() instead.
        '''
        # Reset coins, actions, buys
        self.coin = 0
        self.numBuys = self.numActions = 1
        self.turn_phase = ACTION_PHASE

        cards = self.selectCard()
        while cards:
            for card in cards:
                self.hand.remove(card)
            self.active_cards.extend(cards)
            for card in cards:
                print "{} plays {}".format(self.name,card.name)
                card.play(self,self.game.getOpponents(self))
            cards = self.selectCard()

        self.turn_phase = BUY_PHASE
        while self.numBuys > 0:
            card = self.buyCard()
            if card:
                print "{} buys a {}.".format(self.name,card.name)
                self.numBuys -= 1
                self.coin -= card.cost
            else:
                break

        self.turn_phase = CLEANUP_PHASE
        # Hand goes into discard
        self.discard.extend(self.hand + self.active_cards)
        self.hand = []
        self.active_cards = []
        for i in range(5):self.drawCard()

        return

    def selectCard(self):
        '''
        Promt the user for a card to play, or choose one programmatically.
        Remove the card from the user's hand. Make sure that the card is
        able to be played (e.g., action card is not played in the buy phase, etc.)
        Return the a list of the cards selected.
        '''
        raise NotImplementedError

    def findCard(self,cardName):
        '''
        Finds the card called 'cardName' in the user's hand. Returns None
        if no such card exists. The card should not be removed from the hand.
        '''
        try:
            card = filter(lambda x:x.name == cardName,self.hand)[0]
        except IndexError:
            return None
        return card
        
    def buyCard(self):
        '''
        Prompt the user for a card to buy from the supply, or a treasure/victory card,
        or choose one of these programmatically. Subtract the cost of the card
        from the coin of the user. Add the card to the user's discard pile.
        Return the card if a card was purchased successfully, else None.
        '''
        raise NotImplementedError

    def shuffle(self,deck):
        for c in deck:
            index1 = int(random()*len(deck))
            index2 = int(random()*len(deck))
            deck[index1], deck[index2] = deck[index2], deck[index1]

    def react(self,attacker,attack):
        '''
        Gives the player an opportunity to react to an attack card.
        The 'attack' parameter is a function that can be applied to the player to
        effect the attack (e.g., discard 2 cards, gain a curse, etc).
        '''
        raise NotImplementedError
                    
    def __str__(self):
        return "%s: <%s>"%(self.name,str(self.deck))
