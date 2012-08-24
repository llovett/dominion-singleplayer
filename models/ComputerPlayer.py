from Player import Player

PLAYER_NAMES = ("Wild Throneroomin' Bob",
                "Duke Maxwell",
                "Silvester Stallone",
                "Pippy the Gardener")

class ComputerPlayer (Player):
    InstanceCount = 0

    def __init__(self,game):
        super(ComputerPlayer,self).__init__(PLAYER_NAMES[ComputerPlayer.InstanceCount],game)
        ComputerPlayer.InstanceCount += 1
