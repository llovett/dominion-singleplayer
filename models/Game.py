from Supply import Supply
from Player import Player
from Card import TreasureCard, ActionCard, VictoryCard
from ComputerPlayer import ComputerPlayer
import Actions
import Cards

class Game:
    def __init__(self, players=2):
        assert(players>=2)

        self.supply = Supply()
        self.user = None
        self.players = []

        # Build the base deck
        # TREASURE CARDS
        self.supply.addDeck(Cards.Copper(),20)
        self.supply.addDeck(Cards.Silver(),20)
        self.supply.addDeck(Cards.Gold(),20)

        # VICTORY CARDS
        vcs = players * 2 + 4
        self.supply.addDeck(Cards.Estate(),vcs)
        self.supply.addDeck(Cards.Duchy(),vcs)
        self.supply.addDeck(Cards.Province(),vcs)

        # ACTION CARDS
        self.supply.addDeck(Cards.Woodcutter(),10)
        self.supply.addDeck(Cards.Festival(),10)
        self.supply.addDeck(Cards.Market(),10)
        self.supply.addDeck(Cards.Chapel(),10)
        self.supply.addDeck(Cards.Cellar(),10)
        self.supply.addDeck(Cards.Feast(),10)
        self.supply.addDeck(Cards.Moneylender(),10)
        self.supply.addDeck(Cards.Throneroom(),10)
        self.supply.addDeck(Cards.Moat(),10)
        self.supply.addDeck(Cards.Workshop(),10)
        self.supply.addDeck(Cards.Smithy(),10)
        self.supply.addDeck(Cards.Remodel(),10)
        self.supply.addDeck(Cards.Village(),10)
        self.supply.addDeck(Cards.Mine(),10)
        self.supply.addDeck(Cards.Adventurer(),10)
        self.supply.addDeck(Cards.Library(),10)
        self.supply.addDeck(Cards.Councilroom(),10)
        self.supply.addDeck(Cards.Militia(),10)
        self.supply.addDeck(Cards.Bureaucrat(),10)
        self.supply.addDeck(Cards.Witch(),10)

        # Create the players
        user = raw_input("What is your name? ")
        self.user = Player(user,self)
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

        print "Number of empties: %d"%self.supply.countEmpties()
        print "provies: %d"%self.supply.count("province")
            
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

def main():
    game = Game()
    
if __name__ == '__main__':main()





