from Card import Card

class ActionCard (Card):

    def __init__(self,**kwargs):
        super(ActionCard, self).__init__(**kwargs)
        self.callback = kwargs['action']

    def play(self, player, opponents):
        self.callback(player,opponents)
        player.numActions -= 1
