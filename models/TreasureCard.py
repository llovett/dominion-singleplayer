from Card import Card

class TreasureCard (Card):
    def __init__(self,**kwargs):
        super(TreasureCard, self).__init__(**kwargs)
        self.value = int(kwargs['value'])

    def play(self, player, opponents):
        player.coin += self.value
