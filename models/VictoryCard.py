from Card import Card

class VictoryCard (Card):

    def __init__(self,**kwargs):
        super(VictoryCard, self).__init__(**kwargs)
        self.value = int(kwargs['value'])

    def play(self, player, opponents):
        pass
