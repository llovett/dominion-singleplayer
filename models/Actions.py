from ComputerPlayer import ComputerPlayer
from ActionCard import ActionCard

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
        
    
# What do I DO about THIS???
# def militia(player,opponents):
#     player.coin += 2
#     for o in opponents:
#         # This is what the attack is. Each opponent must react to this
#         attack = lambda x:for i in range(2):x.discardCard()
#         if not o.react(player,attack):
#             # Opponent could not cancel the attack
#             attack(o)
            
