class Card (object):
    '''
    Models a Dominion card.
    '''
    
    def __init__(self,**kwargs):
        self.cost = int(kwargs['cost'])
        self.name = kwargs['name']
        self.description = "" if 'description' not in kwargs else kwargs['description']
        # Reaction = defense card, reaction card, or anything played out-of-turn
        self.reaction = None if not 'reaction' in kwargs else kwargs['reaction']

    def play(self, player, opponents):
        '''
        This method should do whatever the card does when you put it into play.
        '''
        return

    def __str__(self):
        return "(%d) %s: %s"%(self.cost,self.name,self.description)

    def __repr__(self):
        return self.__str__()

class ActionCard (Card):
    def __init__(self,**kwargs):
        super(ActionCard, self).__init__(**kwargs)
        self.callback = kwargs['action']

    def play(self, player, opponents):
        self.callback(player,opponents)
        player.numActions -= 1

    def action(self, player, opponents):
        self.callback(player,opponents)

class VictoryCard (Card):
    def __init__(self,**kwargs):
        super(VictoryCard, self).__init__(**kwargs)
        self.value = int(kwargs['value'])
        if 'description' not in kwargs:
            self.description = "worth {} victory points".format(self.value)

    def play(self, player, opponents):
        pass

class TreasureCard (Card):
    def __init__(self,**kwargs):
        super(TreasureCard, self).__init__(**kwargs)
        self.value = int(kwargs['value'])
        if 'description' not in kwargs:
            self.description = "worth {} coin".format(self.value)

    def play(self, player, opponents):
        player.coin += self.value
