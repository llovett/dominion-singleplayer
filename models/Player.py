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
        self.game = game

    def drawCard(self):
        '''
        Draws a card from the player's deck and adds it to their hand.
        Returns the card drawn.
        '''
        card = self.deck.pop()
        self.hand.append(card)
        return card

    def takeTurn(self):
        '''
        The player takes a turn. Do not override this method. See selectCard()
        and buyCard() instead.
        '''
        # Reset coins, actions, buys
        self.coin = 0
        self.numBuys = self.numActions = 1
        self.turn_phase = ACTION_PHASE

        card = self.selectCard()
        while card:
            self.active_cards.append(card)
            card = self.selectCard()

        self.turn_phase = BUY_PHASE
        card = self.buyCard()
        while card:
            card = self.buyCard()

        self.turn_phase = CLEANUP_PHASE
        return

    def selectCard(self):
        '''
        Promt the user for a card to play, or choose one programmatically.
        Remove the card from the user's hand. Make sure that the card is
        able to be played (e.g., action card is not played in the buy phase, etc.)
        Return the card selected.
        '''

        print "Your cards:"
        print 30 * '-'
        for i in range(len(self.hand)):
            print "%d) %s"%(i+1,self.hand[i])
        print 30 * '-'

        which = 0
        while which < 1 or which > len(self.hand):
            try:
                which = int(raw_input("Which card do you want to play? "))
            except ValueError:
                pass

        card = self.hand[which-1]
        self.hand.pop(which-1)
        return card

    def buyCard(self):
        '''
        Prompt the user for a card to buy from the supply, or a treasure/victory card,
        or choose one of these programmatically. Subtract the cost of the card
        from the coin of the user. Add the card to the user's discard pile.
        Return the card if a card was purchased successfully, else None.
        '''

        what = ""
        while len(what) < 1 and self.numBuys > 0:
            what = raw_input("What card do you want to buy (name, or 'none')? ")
            try:
                # Exit at user's request
                if what.lower() is "none":
                    return None

                # See if there are cards left
                if len(self.game.supply[what]) > 0:
                    card = self.game.supply[what][-1]
                    # Can we afford it?
                    if card.cost <= self.coin:
                        self.game.supply[what].pop()
                        self.coin -= card.cost
                        self.discard.append(card)
                        self.numBuys -= 1
                        print "You gained "+str(card)
                        return card
                    else:
                        print "Not enough coin for that."
                        what = ""
                else:
                    print "No more of that card left."
                    what = ""
            except KeyError:
                what = ""

        return None

    def shuffleDeck(self):
        for c in self.deck:
            index1 = int(random()*len(self.deck))
            index2 = int(random()*len(self.deck))
            self.deck[index1], self.deck[index2] = self.deck[index2], self.deck[index1]

    def __str__(self):
        return "%s: <%s>"%(self.name,str(self.deck))
