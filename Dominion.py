from models.Supply import Supply
from models.Player import Player
from models.Card import TreasureCard, ActionCard, VictoryCard
from models.ComputerPlayer import ComputerPlayer
from models.HumanPlayer import HumanPlayer
import models.Cards as Cards
from random import random
import os

class Game:
    def __init__(self, players=2):
        assert(players>=2)

        self.supply = Supply()
        self.user = None
        self.players = []

        # Choose card set
        cardSet = ""
        while len(cardSet) == 0:
            cardSet = raw_input("What cards would you like to play (random, set, choice)? ")
            if cardSet.lower() == 'random':
                cards = self.chooseRandom()
            elif cardSet.lower() == 'choice':
                cards = self.chooseCards()
            elif cardSet.lower() == 'set':
                cards = self.chooseSet()
            else:
                cardSet = ""

        # Add decks to the supply
        # TREASURE CARDS
        self.supply.addDeck(Cards.Copper(),20)
        self.supply.addDeck(Cards.Silver(),20)
        self.supply.addDeck(Cards.Gold(),20)

        # VICTORY CARDS
        vcs = players * 2 + 4
        self.supply.addDeck(Cards.Estate(),vcs)
        self.supply.addDeck(Cards.Duchy(),vcs)
        self.supply.addDeck(Cards.Province(),vcs)

        for card in cards:
            type = getattr(Cards,card)
            self.supply.addDeck(type(),10)

        # Create the players
        user = raw_input("What is your name? ")
        self.user = HumanPlayer(user,self)
        self.players.append(self.user)

        numPlayers = 0
        while numPlayers < 1:
            try:
                strNumPlayers = raw_input("How many other players? (1) ")
                numPlayers = int(strNumPlayers)
            except ValueError:
                if len(strNumPlayers) == 0:numPlayers=1
        for i in range(numPlayers):
            self.players.append(ComputerPlayer(self))

        for p in self.players:
            newHand = 3*[Cards.Estate()] + 7*[Cards.Copper()]
            p.deck.extend( newHand )
            p.shuffle(p.deck)

            # Draw a hand for each player
            for i in range(5):p.drawCard()

        print "The supply:"
        print self.supply

        # The game loop
        while self.supply.countEmpties() < 3 and self.supply.count("province") > 0:
            for player in self.players:
                if player is self.user:
                    print "Supply:"
                    print self.supply
                print
                print "{}'s turn.".format(player.name)
                print 30*'='
                player.takeTurn()
        # End-of-game
        for player in self.players:
            allCards = player.hand + player.deck + player.discard
            vps = [c for c in allCards if isinstance(c,VictoryCard)]
            player.score = sum(vp.getValue(player) for vp in vps)
        ranks = sorted(self.players,key=lambda x:x.score,reverse=True)
        print
        print "{} is the winner!".format(ranks[0].name)
        for p in ranks:
            print "name:{}\nscore:{}".format(p.name,p.score)
            print 30*'-'

    def getOpponents(self,player):
        return [p for p in self.players if p is not player]

    def chooseCards(self):
        cards = [c for c in dir(Cards) if not c.startswith('__') and issubclass(getattr(Cards,c),ActionCard) and c is not 'ActionCard']
        chosen = []
        print "Choose your cards (number, name, or 'restart')."
        for i in range(len(cards)):
            print "{}) {}".format(i+1,cards[i])
        counter = 0
        while counter < 10:
            if len(chosen) > 0:
                print "Cards chosen so far:",
                for i in range(len(chosen)):
                    print "{}{}".format(chosen[i],"," if i < len(chosen)-1 else ""),
                print
            c = raw_input("Choose a card ({} left): ".format(10-counter))
            card = None
            try:
                index = int(c)-1
                if index >= 0 and index < len(cards):
                    card = cards[index]
            except ValueError:
                if c == 'restart':
                    return self.chooseCards()
                try:
                    card = [ca for ca in cards if ca.lower() == c.lower()][0]
                except IndexError:
                    pass
            if card and card not in chosen:
                chosen.append(card)
                counter += 1
        return chosen

    def chooseSet(self):
        files = {}
        try:
            for f in os.listdir("lib"):
                files[f.split('.')[0]] = f
        except OSError:
            print "Could not find the lib directory!"
            exit(1)
        print "AVAILABLE SETS:"
        print 30*'-'
        for i in range(len(files)):
            print "{}) {}".format(i+1,files.keys()[i])
        choice = ""
        while len(choice) == 0:
            choice = raw_input("Choose your set (name or number): ")
            try:
                index = int(choice)
                if index > 0 and index <= len(files):
                    choice = files.keys()[index-1]
                else:
                    choice = ""
            except ValueError:
                try:
                    f = files[choice]
                except KeyError:
                    choice = ""
        # Make cards from file
        cards = []
        with open(os.path.join("lib",files[choice]),"r") as input:
            contents = [line for line in input.readlines() if not line.startswith('#')]
        for line in contents:
            try:
                cards.append(line.strip().capitalize())
            except AttributeError:
                print "Unrecognized card: {}".format(line)
                exit(1)
        return cards
            
    def chooseRandom(self):
        cards = [c for c in dir(Cards) if not c.startswith('__') and issubclass(getattr(Cards,c),ActionCard) and c is not 'ActionCard']
        chosen = []
        choices = [i for i in range(len(cards))]
        for i in range(10):
            which = int(random()*len(cards))
            card = cards.pop(which)
            # Witch and Curse go together
            if card.lower() == 'witch':
                chosen.append('Curse')
            elif card.lower() == 'curse':
                chosen.append('Witch')
            chosen.append(card.capitalize())
        return chosen

def main():
    game = Game()
    
if __name__ == '__main__':main()
