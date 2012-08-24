from ActionCard import ActionCard
from TreasureCard import TreasureCard
from VictoryCard import VictoryCard

class Supply (object):

    def __init__(self):
        self.treasures = {}
        self.actions = {}
        self.vcs = {}

    def addDeck(self, template, count):
        '''
        Adds a deck to the supply.
        template = a Card instance to create a deck out of
        count = how many cards to add to form the deck
        '''
        cards = count * [template]
        if isinstance(template, ActionCard):
            self.actions[template.name] = cards
        elif isinstance(template, VictoryCard):
            self.vcs[template.name] = cards
        elif isinstance(template, TreasureCard):
            self.treasures[template.name] = cards

    def countEmpties(self):
        '''
        Counts the number of empty piles in the supply (action cards).
        '''
        return len(filter(lambda x:len(x)==0,self.actions.values()))

    def count(self, cardName):
        '''
        Returns the count of an arbitrary card. Returns 0 if the card doesn't exist.
        '''
        for category in (self.actions,self.treasures,self.vcs):
            if cardName in category.keys():
                return len(category[cardName])
        return 0
        
    def viewCard(self, cardName):
        '''
        Returns an instance of the card with name cardName, if any exist.
        The card is not removed from the supply.
        Returns None if no such card exists.
        '''
        for category in (self.actions,self.treasures,self.vcs):
            try:
                if cardName in category.keys():
                    return category[cardName][0]
            except IndexError:
                return None
        return None
        

    def drawCard(self, cardName):
        '''
        Removes a card of "cardName" from the supply and returns it.
        Returns None if no such card exists, or if the pile is empty.
        '''
        for category in (self.actions,self.treasures,self.vcs):
            try:
                if cardName in category.keys():
                    return category[cardName].pop()
            except IndexError:
                print "No more of that card left."
                return None

        print "No such card."
        return None

    def __str__(self):
        value = ""
        for title,category in (('TREASURE CARDS',self.treasures),
                               ('ACTION CARDS',self.actions),
                               ('VICTORY CARDS',self.vcs)):
            value += "%s:\n"%title
            value += 30*'-' + "\n"
            for key,val in category.iteritems():
                value += "* %s *\n"%key.upper()
                if len(category[key]) > 0:
                    value += "cost: %s\n"%str(category[key][0].cost)
                    value += "%d left in supply\n"%len(category[key])
                else:
                    value += "None left."
                value += "\n"

        return value
