class Card (object):
    '''
    Models a Dominion card.
    '''
    
    def __init__(self,**kwargs):
        self.cost = int(kwargs['cost'])
        self.name = kwargs['name']
        self.description = "" if 'description' not in kwargs else kwargs['description']

    def play(self, player, opponents):
        '''
        This method should do whatever the card does when you put it into play.
        '''
        raise NotImplementedError

    def __str__(self):
        return "(%d) %s: %s"%(self.cost,self.name,self.description)

    def __repr__(self):
        return self.__str__()

class ActionCard (Card):
    def __init__(self,**kwargs):
        super(ActionCard, self).__init__(**kwargs)

    def play(self, player, opponents):
        self.action(player,opponents)
        player.numActions -= 1

    def action(self, player, opponents):
        raise NotImplementedError

class VictoryCard (Card):
    def __init__(self,**kwargs):
        super(VictoryCard, self).__init__(**kwargs)

    def play(self, player, opponents):
        raise NotImplementedError

    def getValue(self,player):
        raise NotImplementedError

class TreasureCard (Card):
    def __init__(self,**kwargs):
        super(TreasureCard, self).__init__(**kwargs)

    def play(self, player, opponents):
        player.coin += self.getValue(player)

    def getValue(self,player):
        raise NotImplementedError
