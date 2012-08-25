class Card (object):
    '''
    Models a Dominion card.
    '''
    
    def __init__(self,**kwargs):
        self.cost = int(kwargs['cost'])
        self.name = kwargs['name']
        self.description = "" if 'description' not in kwargs else kwargs['description']
        self.defense = True if 'defense' in kwargs else False

    def play(self, player, opponents):
        '''
        This method should do whatever the card does when you put it into play.
        '''
        return

    def __str__(self):
        return "(%d) %s: %s"%(self.cost,self.name,self.description)

    def __repr__(self):
        return self.__str__()
