#
# Actions.py
# 
# This file contains definitions for each ActionCard that tell it how
# to act when played. Each function gets a pointer to the current
# player ('player') and their opponents ('opponents'). Note that the
# names of these function definitions MUST MATCH EXACTLY the name of
# the card in your set.
# 
from ComputerPlayer import ComputerPlayer
from ActionCard import ActionCard
from TreasureCard import TreasureCard
from VictoryCard import VictoryCard

def woodcutter(player,opponents):
    player.coin += 2
    player.numBuys += 1

def festival(player,opponents):
    player.numActions += 2
    player.numBuys += 1
    player.coin += 2

def market(player,opponents):
    player.numActions += 1
    player.numBuys += 1
    player.coin += 1
    player.drawCard()

def chapel(player,opponents):
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

def cellar(player,opponents):
    which = raw_input("Discard a card (<enter> when finished)? ")
    counter = 0
    while len(which) > 0:
        if not player.discardCard(which):
            print "You don't have that card."
        else:counter+=1
        which = raw_input("Discard another card (<enter> when finished)? ")
    player.numActions += 1
    for i in range(counter):player.drawCard()

def feast(player,opponents):
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

def moneylender(player,opponents):
    try:
        copper = filter(lambda x:x.name=="copper",player.hand)[0]
        player.hand.remove(copper)
        player.coin += 3
    except IndexError:
        pass

def throneroom(player,opponents):
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
        
def moat(player,opponents):
    for i in range(2):player.drawCard()

def workshop(player,opponents):
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

def village(player,opponents):
    player.numActions += 2
    player.drawCard()

def chancellor(player,opponents):
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

def smithy(player,opponents):
    for i in range(3):player.drawCard()

def remodel(player,opponents):
    toRemodel = None
    while toRemodel is None:
        which = raw_input("Which card should be remodeled? ")
        toRemodel = player.findCard(which)
    # Trash the card
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

def laboratory(player,opponents):
    for i in range(2):player.drawCard()
    player.numActions += 1

def library(player,opponents):
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

def councilroom(player,opponents):
    for i in range(4):player.drawCard()
    for o in opponents:o.drawCard()
    player.numBuys += 1

def mine(player,opponents):
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
        
def adventurer(player,opponents):
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

def militia(player,opponents):
    player.coin += 2
    for o in opponents:
        # This is what the attack is. Each opponent must react to this
        def attack(p):
            for i in range(2):p.discardCardChoice()
        o.react(player,attack)

def bureaucrat(player,opponents):
    silver = player.game.supply.drawCard("silver")
    if silver:
        player.deck.append(silver)
        print "{} puts a silver on top of their deck.".format(player.name)
    for o in opponents:
        def attack(p):
            vcs = [c for c in p.hand if isinstance(c,VictoryCard)]
            if len(vcs) == 0:
                return
            p.cardToDeck(vcs)
        o.react(player,attack)

def witch(player,opponents):
    for i in range(2):player.drawCard()
    def attack(p):
        curse = p.game.supply.drawCard("curse")
        if curse:
            p.gain(curse)
