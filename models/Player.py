from TreasureCard import TreasureCard
from ActionCard import ActionCard
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
        # Shuffle deck if necessary
        if len(self.deck) < 5:
            self.shuffle(self.discard)
            self.deck = self.discard + self.deck
            self.discard = []
        card = self.deck.pop()
        # This should only happen for human players. Split Player into HumanPlayer and ComputerPlayer?
        print "{} draws a {}".format(self.name,card.name)
        self.hand.append(card)
        return card

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

    def discardCardChoice(self):
        '''
        Prompts the user to discard a card. Returns the card discarded, or None.
        '''
        which = raw_input("Discard a card (name)? ")
        if which == 'none' or len(which) == 0:
            return None
        return self.discardCard(which)

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
            self.active_cards.extend(cards)
            for card in cards:
                print "{} plays {}".format(self.name,card.name)
                card.play(self,self.game.getOpponents())
            cards = self.selectCard()

        self.turn_phase = BUY_PHASE
        card = self.buyCard()
        while card:
            card = self.buyCard()

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

        if len(self.hand) == 0:
            print "You have no cards left."
            return None
        
        print 30 * '-'
        print "Your cards:"
        for i in range(len(self.hand)):
            print str(self.hand[i])
        print 30 * '-'

        which = ""
        card = None
        while len(which) == 0:
            self.printStatus()

            which = raw_input("Which card do you want to play (name, $, or 'none')? ")
            if which == '$':
                def q(list,x):
                    list.remove(x)
                    return x
                cards = [q(self.hand,x) for x in filter(lambda x:isinstance(x,TreasureCard),self.hand)]
                if len(cards) > 0:
                    return cards
                else:
                    print "You have no treasure cards."
            elif which == 'none' or len(which) == 0:
                return None
            else:
                card = filter(lambda x:x.name == which,self.hand)
                if len(card) == 0:
                    print "You don't have that card."
                    which = ""
                else:
                    card = card[0]
                    if isinstance(card,ActionCard) and self.numActions < 1:
                        print "You have no actions left."
                        which = ""

        self.hand.remove(card)
        return [card]

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

        what = ""
        while len(what) < 1 and self.numBuys > 0:
            self.printStatus()
            what = raw_input("What card do you want to buy (name, or 'none')? ")
            try:
                # Exit at user's request
                if what.lower() == "none" or len(what) == 0:
                    return None

                # See if there are cards left
                if self.game.supply.count(what) > 0:
                    card = self.game.supply.viewCard(what)
                    # Can we afford it?
                    if card.cost <= self.coin:
                        card = self.game.supply.drawCard(what)
                        self.coin -= card.cost
                        self.discard.append(card)
                        self.numBuys -= 1
                        print "You gained "+str(card)
                        return card
                    else:
                        print "Not enough coin for that."
                        what = ""
                else:
                    print "That card isn't in the supply."
                    what = ""
            except KeyError:
                what = ""

        return None

    def shuffle(self,deck):
        for c in deck:
            index1 = int(random()*len(deck))
            index2 = int(random()*len(deck))
            deck[index1], deck[index2] = deck[index2], deck[index1]

    # def react(self,attacker,attack):
    #     '''
    #     Gives the player an opportunity to react to an attack card.
    #     The 'attack' parameter is a function that can be applied to the player to
    #     effect the attack (e.g., discard 2 cards, gain a curse, etc). This method
    #     should return True if the attack can be evaded, False otherwise.
    #     '''
    #     # For human players, just ask if they want to use a defense card, and play it here.
    #     defenseCards = filter(lambda x:x.defense,self.hand)
    #     if len(defenseCards) > 0:
    #         print "{} has played an attack card.".format(attacker.name)
    #         defense = ""
    #         while len(defense) == 0:
    #             defense = raw_input("Would you like to reveal a defense card (name or 'none')? ")
    #             if defense.lower() == 'none':
    #                 return False
    #             try:
    #                 card = defenseCards.filter(lambda x:x.name == defense,defenseCards)[0]
    #                 card.defend
    #             except IndexError:
    #                 print "You don't have that card."
    #                 defense = ""
                    
    def __str__(self):
        return "%s: <%s>"%(self.name,str(self.deck))
