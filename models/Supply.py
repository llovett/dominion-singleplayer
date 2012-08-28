from Card import ActionCard, TreasureCard, VictoryCard 

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
        return len([deck for deck in self.actions.values() if len(deck)==0])

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
        def makeColumns(data):
            sep,cur,last = 25,0,0
            string = "{}".format(data[0])
            last = len(data[0])
            for i in range(1,len(data)):
                arg = data[i]
                cur = len(arg)
                string += ("{:>"+str(sep-last+cur)+"}").format(arg)
                last = cur
            return string

        for title,category in (('TREASURE CARDS',self.treasures),
                               ('ACTION CARDS',self.actions),
                               ('VICTORY CARDS',self.vcs)):
            value += "%s:\n"%title
            value += 30*'-' + "\n"
            byPrice = [l[0] for l in sorted(category.values(),key=lambda x:x[0].cost)]
            for i in range(0,len(byPrice),3):
                cards = [byPrice[c] for c in range(i,min(i+3,len(byPrice)))]
                titles = makeColumns(["* {} *".format(c.name.upper()) for c in cards])
                costs = makeColumns(["cost: {}".format(c.cost) if self.count(c.name) > 0 else "None left." for c in cards])
                counts = makeColumns(["{} left in supply.".format(self.count(c.name)) if self.count(c.name) > 0 else "" for c in cards])
                value += "\n".join([titles,costs,counts])
                value += "\n\n"

        return value
