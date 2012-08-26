from ActionCard import ActionCard
from TreasureCard import TreasureCard
from VictoryCard import VictoryCard
import Actions
import Reactions
import re

class CardParser (object):

    def loadCards(self):
        '''
        Opens the file carddefs.txt to find the definitions for all possible
        cards in gameplay. Returns a list of all these cards.
        '''
        try:
            with open("carddefs.txt","r") as input:
                contents = input.read()
        except IOError:
            print "Could not find carddefs.txt!"
            exit(1)

        cardList = []
        successMatch = None
        # The card language is REGULAR, I SWEAR!!!
        for statement in re.findall("([a-z]+\s*\{(\s*[a-z]+=[-a-z0-9]+\s*)+)",contents,re.IGNORECASE|re.MULTILINE):
            cardName = cardType = cardCost = cardValue = cardReaction = None
            try:
                cardName = re.search("[a-z]+(?=\s*\{)",statement[0],re.IGNORECASE).group(0)
                print cardName
                cardType = re.search("(?<=type=).*",statement[0],re.IGNORECASE).group(0)
                cardCost = re.search("(?<=cost=).*",statement[0],re.IGNORECASE).group(0)
            except AttributeError:
                print "There was a problem while parsing carddefs.txt."
                approxLine = successMatch.start()
                print "Check around character {}.".format(approxLine)

            cardValueMatch = re.search("(?<=value=).*",statement[0],re.IGNORECASE)
            # Optional attributes
            if cardValueMatch:
                cardValue = cardValueMatch.group(0)
            cardDescriptionMatch = re.search("(?<=description=).*",statement[0],re.IGNORECASE)
            if cardDescriptionMatch:
                cardDescription = cardDescriptionMatch.group(0)
            cardReactionMatch = re.search("(?<=reaction=).*",statement[0],re.IGNORECASE)
            if cardReactionMatch:
                cardReaction = cardReactionMatch.group(0).lower()
                
            # Building the card
            if cardType == "action":
                card = ActionCard(name=cardName,cost=cardCost,action=getattr(Actions,cardName))
            elif cardType == "victory" or cardType == "treasure":
                card = VictoryCard(name=cardName,cost=cardCost,value=cardValue)
            if cardDescriptionMatch:
                card.description = cardDescription
            if cardReactionMatch and cardReaction == 'true':
                card.reaction = getattr(Reactions,cardName)

            cardList.append(card)
            successMatch = re.search("[a-z]+(?=\s*\{)",statement[0],re.IGNORECASE)

        return cardList

# A little test for the parser
def main():
    parser = CardParser()
    print "Parsed all the cards---here they are!"
    print parser.loadCards()

if __name__=='__main__':main()
