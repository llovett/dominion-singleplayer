from TreasureCard import TreasureCard
from VictoryCard import VictoryCard
from ActionCard import ActionCard
from Player import Player
import Actions

class Game:
    def __init__(self, players=2):
        assert(players>=2)

        self.supply = {"copper":[],
                       "silver":[],
                       "gold":[],
                       "estate":[],
                       "duchy":[],
                       "province":[],
                       "woodcutter":[]}
        self.user = None
        self.players = []

        # Build the base deck
        # TREASURE CARDS
        self.supply['copper'].extend(20*[TreasureCard(value=1,cost=0,name="copper")])
        self.supply['silver'].extend(20*[TreasureCard(value=2,cost=3,name="silver")])
        self.supply['gold'].extend(20*[TreasureCard(value=3,cost=6,name="gold")])

        # VICTORY CARDS
        vcs = players * 2 + 4
        self.supply['estate'].extend(vcs * [VictoryCard(value=1,cost=2,name="estate")])
        self.supply['duchy'].extend(vcs * [VictoryCard(value=3,cost=5,name="duchy")])
        self.supply['province'].extend(vcs * [VictoryCard(value=6,cost=8,name="province")])

        # ACTION CARDS
        self.supply['woodcutter'].extend(10 * [ActionCard(cost=3,name="woodcutter",action=Actions.woodcutter)])

        # Create players, deal out hands
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
            self.players.append(Player("qasdfasdgasdfasdf",self))

        for p in self.players:
            newHand = [VictoryCard(cost=2,value=1,name="estate") for i in range(3)] + [TreasureCard(cost=0,value=1,name="copper") for i in range(7)]
            p.deck.extend( newHand )
            p.shuffleDeck()

            # Draw a hand for each player
            for i in range(5):p.drawCard()

        print "Supply:"
        self.printSupply()

        self.user.takeTurn()

    def printSupply(self):
        for key,val in self.supply.iteritems():
            print key.upper()
            if len(self.supply[key]) > 0:
                print "cost: "+str(self.supply[key][0].cost)
                print "%d left in supply"%len(self.supply[key])
            else:
                print "None left."
            print ""

def main():
    game = Game()
    
if __name__ == '__main__':main()





