from TreasureCard import TreasureCard
from VictoryCard import VictoryCard
from ActionCard import ActionCard
from Supply import Supply
from Player import Player
from ComputerPlayer import ComputerPlayer
import Actions

class Game:
    def __init__(self, players=2):
        assert(players>=2)

        self.supply = Supply()
        self.user = None
        self.players = []

        # Build the base deck
        # TREASURE CARDS
        self.supply.addDeck(TreasureCard(value=1,cost=0,name="copper"),20)
        self.supply.addDeck(TreasureCard(value=2,cost=3,name="silver"),20)
        self.supply.addDeck(TreasureCard(value=3,cost=6,name="gold"),20)

        # VICTORY CARDS
        vcs = players * 2 + 4
        self.supply.addDeck(VictoryCard(value=1,cost=2,name="estate"),vcs)
        self.supply.addDeck(VictoryCard(value=3,cost=5,name="duchy"),vcs)
        self.supply.addDeck(VictoryCard(value=6,cost=8,name="province"),vcs)

        # ACTION CARDS
        self.supply.addDeck(ActionCard(cost=3,name="woodcutter",action=Actions.woodcutter),vcs)

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
            newHand = 3*[VictoryCard(cost=2,value=1,name="estate")] + 7*[TreasureCard(cost=0,value=1,name="copper")]
            p.deck.extend( newHand )
            p.shuffleDeck()

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
                player.takeTurn()

    def getOpponents(self):
        return self.players[1:]

def main():
    game = Game()
    
if __name__ == '__main__':main()





