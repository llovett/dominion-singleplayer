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
