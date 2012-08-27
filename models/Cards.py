#
# Cards.py
# 
# Listing of all cards
#
from ComputerPlayer import ComputerPlayer
from Card import ActionCard, TreasureCard, VictoryCard

# TREASURE CARDS
class Copper (TreasureCard):
    def __init__(self,**kwargs):
        super(Copper,self).__init__(name="copper",cost=0,**kwargs)
    def getValue(self,player):
        return 1

class Silver (TreasureCard):
    def __init__(self,**kwargs):
        super(Silver,self).__init__(name="silver",cost=3,**kwargs)
    def getValue(self,player):
        return 2

class Gold (TreasureCard):
    def __init__(self,**kwargs):
        super(Gold,self).__init__(name="gold",cost=6,**kwargs)
    def getValue(self,player):
        return 3

# VICTORY CARDS
class Estate (VictoryCard):
    def __init__(self,**kwargs):
        super(Estate,self).__init__(name="estate",cost=2,**kwargs)
    def getValue(self,player):
        return 1

class Duchy (VictoryCard):
    def __init__(self,**kwargs):
        super(Duchy,self).__init__(name="duchy",cost=5,**kwargs)
    def getValue(self,player):
        return 2

class Province (VictoryCard):
    def __init__(self,**kwargs):
        super(Province,self).__init__(name="province",cost=8,**kwargs)
    def getValue(self,player):
        return 3
    
class Gardens (VictoryCard):
    def __init__(self,**kwargs):
        super(Gardens,self).__init__(name="gardens",cost=4,**kwargs)
    def getValue(self,player):
        return len([c for c in player.hand + player.discard + player.deck if isinstance(c,VictoryCard)])/10

# ACTION CARDS
class Woodcutter (ActionCard):
    def __init__(self,**kwargs):
        super(Woodcutter,self).__init__(name="woodcutter",cost=3,**kwargs)
    def action(self,player,opponents):
        player.coin += 2
        player.numBuys += 1

class Festival (ActionCard):
    def __init__(self,**kwargs):
        super(Festival,self).__init__(name="festival",cost=5,**kwargs)
    def action(self,player,opponents):
        player.numActions += 2
        player.numBuys += 1
        player.coin += 2

class Market (ActionCard):
    def __init__(self,**kwargs):
        super(Market,self).__init__(name="market",cost=5,**kwargs)
    def action(self,player,opponents):
        player.numActions += 1
        player.numBuys += 1
        player.coin += 1
        player.drawCard()

class Chapel (ActionCard):
    def __init__(self,**kwargs):
        super(Chapel,self).__init__(name="chapel",cost=2,**kwargs)
    def action(self,player,opponents):
        counter = 4
        which = raw_input("Trash a card ({} left, <enter> when finished)? ".format(counter))
        while counter > 0 and len(which) > 0:
            cards = filter(lambda x:x.name == which, player.hand)
            if len(cards) > 0:
                player.hand.remove(cards[0])
                counter -= 1
            else:
                print "You don't have that card."
            which = raw_input("Trash another card ({} left, <enter> when finished)? ".format(counter))

class Cellar (ActionCard):
    def __init__(self,**kwargs):
        super(Cellar,self).__init__(name="cellar",cost=2,**kwargs)
    def action(self,player,opponents):
        which = raw_input("Discard a card (<enter> when finished)? ")
        counter = 0
        while len(which) > 0:
            if not player.discardCard(which):
                print "You don't have that card."
            else:counter+=1
            which = raw_input("Discard another card (<enter> when finished)? ")
        player.numActions += 1
        for i in range(counter):player.drawCard()

class Feast (ActionCard):
    def __init__(self,**kwargs):
        super(Feast,self).__init__(name="feast",cost=5,**kwargs)
    def action(self,player,opponents):
        feastCard = filter(lambda x:x.name == "feast",player.active_cards)[0]
        player.active_cards.remove(feastCard)
        fiveCard = ""
        while len(fiveCard) == 0:
            fiveCard = raw_input("Select a card costing up to (5) from the supply (name) ")
            card = player.game.supply.viewCard(fiveCard)
            if not card:
                print "There is no card like that in the supply."
                fiveCard = ""
            elif card.cost > 5:
                print "That card is too expensive."
                fiveCard = ""
            else:
                player.discard.append(player.game.supply.drawCard(fiveCard))

class Moneylender (ActionCard):
    def __init__(self,**kwargs):
        super(Moneylender,self).__init__(name="moneylender",cost=4,**kwargs)
    def action(self,player,opponents):
        try:
            copper = filter(lambda x:x.name=="copper",player.hand)[0]
            player.hand.remove(copper)
            player.coin += 3
        except IndexError:
            pass

class Throneroom (ActionCard):
    def __init__(self,**kwargs):
        super(Throneroom,self).__init__(name="throneroom",cost=4,**kwargs)
    def action(self,player,opponents):
        def applyTR(card):
            player.hand.remove(card)
            player.active_cards.append(card)
            print "{} attaches {} to the throneroom.".format(player.name,card.name)
            for i in range(2):card.action(player,opponents)

        actionCards = filter(lambda x:isinstance(x,ActionCard),player.hand)

        if len(actionCards) == 0:
            return
        elif len(actionCards) == 1:
            actionCard = actionCards[0]
            applyTR(actionCard)
        else:
            ac = ""
            while len(ac) == 0:
                ac = raw_input("What card would you like to apply throneroom to? ")
                actionCards = filter(lambda x:x.name == ac,actionCards)
                if len(actionCards) == 0:
                    print "That's not an action card you have."
                    ac = ""
                else:
                    actionCard = actionCards[0]
                    applyTR(actionCard)
        
class Moat (ActionCard):
    def __init__(self,**kwargs):
        super(Moat,self).__init__(name="moat",cost=4,**kwargs)
    def action(self,player,opponents):
        for i in range(2):player.drawCard()
    def react(self,player,opponents,action):
        pass

class Workshop (ActionCard):
    def __init__(self,**kwargs):
        super(Workshop,self).__init__(name="workshop",cost=4,**kwargs)
    def action(self,player,opponents):
        which = ""
        while len(which) == 0:
            which = raw_input("Gain a card costing up to (4)? ")
            card = player.game.supply.viewCard(which)
            if not card:
                print "That card isn't in the supply."
                which = ""
            elif card.cost > 4:
                print "That card costs more than (4)."
                which = ""
            else:
                print "You gain a {}.".format(card.name)
                player.gain(player.supply.drawCard(which))

class Village (ActionCard):
    def __init__(self,**kwargs):
        super(Village,self).__init__(name="village",cost=3,**kwargs)
    def action(self,player,opponents):
        player.numActions += 2
        player.drawCard()

class Chancellor (ActionCard):
    def __init__(self,**kwargs):
        super(Chancellor,self).__init__(name="chancellor",cost=3,**kwargs)
    def action(self,player,opponents):
        player.coin += 2
        doDiscard = ""
        while len(doDiscard) == 0:
            doDiscard = raw_input("Put deck into discard pile (y/n)? ")
            if doDiscard.lower() == 'yes' or doDiscard.lower() == 'y':
                player.discard.extend(player.deck)
                player.deck = []
            elif doDiscard.lower() == 'no' or doDiscard.lower() == 'n':
                pass
            else:
                doDiscard = ""

class Smithy (ActionCard):
    def __init__(self,**kwargs):
        super(Smithy,self).__init__(name="smithy",cost=4,**kwargs)
    def action(self,player,opponents):
        for i in range(3):player.drawCard()

class Remodel (ActionCard):
    def __init__(self,**kwargs):
        super(Remodel,self).__init__(name="remodel",cost=4,**kwargs)
    def action(self,player,opponents):
        toRemodel = None
        while toRemodel is None:
            which = raw_input("Which card should be remodeled? ")
            toRemodel = player.findCard(which)
        player.hand.remove(toRemodel)
        remodeled = None
        maxCost = toRemodel.cost+2
        while remodeled is None:
            which = raw_input("Remodel into which card (cost up to {})? ".format(maxCost))
            remodeled = player.game.supply.viewCard(which)
            if remodeled and remodeled.cost > maxCost:
                print "That card is too expensive."
                remodeled = None
            elif remodeled:
                print "{} remodels {} into {}.".format(player.name,toRemodel.name,remodeled.name)
                player.discard.append(player.game.supply.drawCard(which))
            else:
                print "You don't have that card."

class Laboratory (ActionCard):
    def __init__(self,**kwargs):
        super(Laboratory,self).__init__(name="laboratory",cost=5,**kwargs)
    def action(self,player,opponents):
        for i in range(2):player.drawCard()
        player.numActions += 1

class Library (ActionCard):
    def __init__(self,**kwargs):
        super(Library,self).__init__(name="library",cost=5,**kwargs)
    def action(self,player,opponents):
        while len(player.hand) < 7:
            card = player.drawCard()
            if isinstance(card, ActionCard):
                keep = ""
                while len(keep) == 0:
                    keep = raw_input("Library revealed a {}. Keep it (y/n)? ".format(card.name))
                    if keep.lower() == 'yes' or keep.lower() == 'y':
                        pass
                    elif keep.lower() == 'no' or keep.lower() == 'n':
                        player.discardCard(card.name)
                    else:
                        keep = ""

class Councilroom (ActionCard):
    def __init__(self,**kwargs):
        super(Councilroom,self).__init__(name="councilroom",cost=5,**kwargs)
    def action(self,player,opponents):
        for i in range(4):player.drawCard()
        for o in opponents:o.drawCard()
        player.numBuys += 1

class Mine (ActionCard):
    def __init__(self,**kwargs):
        super(Mine,self).__init__(name="mine",cost=5,**kwargs)
    def action(self,player,opponents):
        treasureCards = filter(lambda x:isinstance(x,TreasureCard),player.hand)
        card = None
        while not card:
            toMine = raw_input("Which treasure would you like to mine? ")
            try:
                card = filter(lambda x:x.name==toMine,treasureCards)[0]
                # Trash the treasure
                player.hand.remove(card)
            except IndexError:
                print "That's not a treasure card you have."
        mined = None

        while not mined:
            which = raw_input("Exchange this treasure for which other treasure? ")
            mined = player.game.supply.findCard(which)
            if not card:
                print "That card isn't in the supply."
            elif not isinstance(card,TreasureCard):
                print "That is not a treasure card."
                mined = None
            elif mined.cost > card.cost + 3:
                print "That card is too expensive."
                mined = None
            else:
                player.hand.append(player.game.supply.drawCard(which))

class Adventurer (ActionCard):
    def __init__(self,**kwargs):
        super(Adventurer,self).__init__(name="adventurer",cost=6,**kwargs)
    def action(self,player,opponents):
        maxDraws = len(player.deck) + len(player.discard)
        treasuresFound = 0
        while maxDraws > 0 and treasuresFound < 2:
            card = player.drawCard()
            if isinstance(card,TreasureCard):
                print "Adventurer revealed a {}.".format(card.name)
                treasuresFound += 1
            else:
                player.discardCard(card.name)
            maxDraws -= 1

class Militia (ActionCard):
    def __init__(self,**kwargs):
        super(Militia,self).__init__(name="militia",cost=4,**kwargs)
    def action(self,player,opponents):
        player.coin += 2
        for o in opponents:
            # This is what the attack is. Each opponent must react to this
            def attack(p):
                for i in range(2):p.discardCardChoice()
            o.react(player,attack)

class Spy (ActionCard):
    def __init__(self,**kwargs):
        super(Spy,self).__init__(name="spy",cost=4,**kwargs)
    def action(self,player,opponents):
        player.drawCard()
        player.numActions += 1
        def attack(p):
            card = p.drawCard()
            print "{} reveals a {}."
            todo = ""
            while len(todo) == 0:
                todo = raw_input("Should {} discard {} or put it back (discard/put)? ")
                if todo.lower() == "discard" or todo.lower() == "d":
                    p.discard.append(card)
                elif todo.lower() == "put" or todo.lower() == "p":
                    p.deck.append(card)
                else:
                    print "I don't understand that."
                    todo = ""
        attack(player)
        for o in opponents:
            o.react(player,attack)

class Bureaucrat (ActionCard):
    def __init__(self,**kwargs):
        super(Bureaucrat,self).__init__(name="bureaucrat",cost=4,**kwargs)
    def action(self,player,opponents):
        silver = player.game.supply.drawCard("silver")
        if silver:
            player.deck.append(silver)
            print "{} puts a silver on top of their deck.".format(player.name)
        for o in opponents:
            def attack(p):
                vcs = [c for c in p.hand if isinstance(c,VictoryCard)]
                if len(vcs) == 0:
                    return
                p.cardToDeckChoice(vcs)
            o.react(player,attack)

class Witch (ActionCard):
    def __init__(self,**kwargs):
        super(Witch,self).__init__(name="witch",cost=5,**kwargs)
    def action(self,player,opponents):
        for i in range(2):player.drawCard()
        def attack(p):
            curse = p.game.supply.drawCard("curse")
            if curse:
                p.gain(curse)
