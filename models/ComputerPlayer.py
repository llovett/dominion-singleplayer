from Player import Player
from Card import TreasureCard
from random import random, choice

PLAYER_NAMES = ("Wild Throneroomin' Bob",
                "Duke Maxwell",
                "Silvester Stallone",
                "Pippy the Gardener")

class ComputerPlayer (Player):
    InstanceCount = 0

    def __init__(self,game):
        super(ComputerPlayer,self).__init__(PLAYER_NAMES[ComputerPlayer.InstanceCount],game)
        ComputerPlayer.InstanceCount += 1

    def cardToDeckChoice(self,selection):
        # Choose randomly
        return choice(selection)

    def discardCardChoice(self):
        # Try to choose a victory card
        vcs = [c for c in self.hand if isinstance(c,VictoryCard)]
        if len(vcs) > 0:
            discarded = choice(vcs)
        # Return lowest-valued treasure
        treasures = sorted([c for c in self.hand if isinstance(c,TreasureCard)],key=lambda x:x.getValue(self))
        if len(treasures) > 0:
            discarded = treasures[0]
        # Return random card from hand
        discarded = choice(self.hand)
        print "{} discards {}.".format(self.name,discarded.name)
        return discarded
        
    def buyCard(self):
        # Buy province if possible, else treasure
        treasures = self.game.supply.treasures.keys()
        # Low province count --> buy duchies
        if self.game.supply.count("province") <= 3 and self.coin >= 5:
            duchy = self.game.supply.drawCard("duchy")
            if duchy:return duchy
        if self.coin >= 8:
            return self.game.supply.drawCard("province")
        if self.coin >= 6:
            return self.game.supply.drawCard("gold")
        if self.coin >= 3:
            return self.game.supply.drawCard("silver")
        return self.game.supply.drawCard("copper")
    
    def selectCard(self):
        # Choose all the money
        return [card for card in self.hand if isinstance(card,TreasureCard)]
    
    def react(self,attacker,attack):
        # Search for defense cards, play one if found
        defenses = [c for c in self.hand if 'react' in dir(c)]
        if len(defenses) > 0:
            choice(defenses).react(attack)
        else:
            attack(self)
