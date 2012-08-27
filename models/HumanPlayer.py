from Card import TreasureCard, ActionCard, VictoryCard
from Player import Player

class HumanPlayer (Player):

    def __init__(self,name,game):
        super(HumanPlayer,self).__init__(name,game)

    def drawCard(self):
        card = Player.drawCard(self)
        print "{} draws {}".format(self.name,card.name)
        return card

    def cardToDeckChoice(self,selection):
        choice = ""
        while len(choice) == 0:
            for s in selection:
                print s
            choice = raw_input("Choose a card to put on top of your deck: ")
            select = [c for c in selection if c.name == choice]
            if len(select) == 0:
                print "You can't select that card."
                choice = ""
            else:
                c = select[0]
                self.hand.remove(c)
                self.deck.append(c)

    def discardCardChoice(self):
        which = raw_input("Discard a card (name)? ")
        if which == 'none' or len(which) == 0:
            return None
        return self.discardCard(which)

    def selectCard(self):
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
                cards = [card for card in self.hand if isinstance(card,TreasureCard)]
                if len(cards) > 0:
                    return cards
                else:
                    print "You have no treasure cards."
                    which = ""
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

        return [card]

    def buyCard(self):
        what = ""
        while len(what) < 1:
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
                        self.discard.append(card)
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

    def react(self,attacker,attack):
        # For human players, just ask if they want to use a defense card, and play it here.
        defenseCards = [card for card in self.hand if 'react' in dir(card)]
        if len(defenseCards) > 0:
            print "{} has played an attack card.".format(attacker.name)
            defense = ""
            while len(defense) == 0:
                defense = raw_input("Would you like to reveal a defense card (name or 'none')? ")
                if defense.lower() == 'none':
                    attack(self)
                try:
                    card = defenseCards.filter(lambda x:x.name == defense,defenseCards)[0]
                    card.react(self,self.game.getOpponents(self),attack)
                except IndexError:
                    print "You don't have that card."
                    defense = ""
        else:
            attack(self)
