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
        # Choose randomly
        return choice(self.hand).name

    def buyCard(self):
        # Choose randomly
        cardsAvailable = self.game.supply.treasures.keys() + self.game.supply.actions.keys() + self.game.supply.vcs.keys()
        attempt = None
        while not attempt or attempt.cost > self.coin:
            attempt = self.game.supply.viewCard(choice(cardsAvailable))
        return attempt
    
    def selectCard(self):
        # Choose all the money
        return [card for card in self.hand if isinstance(card,TreasureCard)]
    
    def react(self,attacker,attack):
        # Accept the attack
        attack(self)






