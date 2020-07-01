import random
import itertools
import territory
from board import *
from territory import *
from card import *
import evaluator
import copy

######### PLAYER CLASS ###########
class Player(object):
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.state = 0  # state of a players turn (0 for not going, 1 for reinforce, 2 for attack, 3 for fortify)
        self.territories = []
        self.cards = []
        self.armies = 35
        self.target_continent = ''
        self.att_time = []
        self.status = True
    
    # To string to view details about a player
    def __str__(self):
        return  (
            'Player: ' + self.name + '\n' +'Color: ' + self.color + '\n' +  
            'Owns: ' + ''.join([x.name + ', ' for x in self.territories]) + '\n' + 
            'Cards: ' + ''.join([str(x) + ', ' for x in self.cards]) + '\n' + 
            'Armies: ' + str(self.armies) + '\n'
        )

    # simulates a player rolling dice during their turn
    def roll_dice(self, dice):
        min = 1
        max = 6
        res = []
        for i in range(dice):
            res.append(random.randint(min, max))
        return res
    
    # checks if a player controls a continent and returns the num of armies recieved or 0
    def controls_continent(self):
        continent = ''
        
        for c in CONTINENTS.keys():
            length = len(CONTINENTS.get(c))
            count = 0   # count for num of players territories in a continent
            for t in self.territories:
                if t.name in CONTINENTS.get(c):
                    count += 1
            if count == length:
                continent = c
                break
        if continent in ARMY_BONUS.keys():
            return ARMY_BONUS.get(continent)
        return 0

    # checks how close a player is to controlling each continent
    # returns a list of continents in order of: most controlled -> least controlled
    def control_percentage(self):
        control = []
        ratio = 0

        for c in CONTINENTS.keys():
            length = len(CONTINENTS.get(c))
            count = 0
            for t in self.territories:
                if t.name in CONTINENTS.get(c):
                    count += 1
            ratio = round(count/length, 2)
            control.append((c, ratio))
        control.sort(key = lambda x : x[1], reverse = True)
        return control

    # updates a players target continent
    def update_target(self):
        control = self.control_percentage()
        for c in control:
            if c[1] < 1 and c[1] > 0:
                self.target_continent = c[0]
                break

    def drawcard(self, deck):
        if len(deck) <= 1:
            deck = copy.deepcopy(DECK)
        card = random.choice(deck)
        deck.remove(card)
        self.cards.append(card)
        return card

    # organizes players cards into a set
    def create_set(self):
        if len(self.cards) < 3:
            return None

        # Potential sets of cards for trading
        # 3 cards of the same design, with one of each army value, or any two cards plus a wildcard
        cardSet = []
        infantry = []
        cavalry = []
        artillery = []
        wild = []
        
        inf = 0
        cav = 0
        art = 0
        numWild = 0
        
        for card in self.cards:
            if card.symbol == 'Infantry':
                infantry.append(card)
                inf += 1
            elif card.symbol == 'Cavalry':
                cavalry.append(card)
                cav += 1
            elif card.symbol == 'Artillery':
                artillery.append(card)
                art += 1
            else:
                wild.append(card)
                numWild += 1
        
        # 3 of a kind
        if inf % 3 == 0:
            cardSet = infantry[0:3]
        elif cav % 3 == 0:           
            cardSet = cavalry[0:3]
        elif art % 3 == 0:            
            cardSet = artillery[0:3]
        
        # 1 of each symbol
        if inf > 0 & cav > 0 & art > 0:
            cardSet.clear()
            cardSet.append(infantry[0])
            cardSet.append(cavalry[0])
            cardSet.append(artillery[0])

        # two cards plus a wild card
        if numWild > 0:
            if (len(infantry) > 0) & (len(cavalry) > 0):
                cardSet.append(infantry[0])
                cardSet.append(cavalry[0])
            elif (len(infantry) > 0) & (len(artillery) > 0):
                cardSet.append(infantry[0])
                cardSet.append(artillery[0])
            elif (len(cavalry) > 0) & (len(artillery) > 0):
                cardSet.append(cavalry[0])
                cardSet.append(artillery[0])
            cardSet.append(wild[0])

        return cardSet
    
    # function for players trading in a set of cards
    def trade_set(self, cardset):
        for card in cardset:
            print(self.name + ' trades in card ' + str(card))
            if card in self.cards:
                self.cards.remove(card) # update player cards

        # simulates a player placing armies on some territory during game initialization
    def place_armies_init(self, armies):
        if len(Board.UNOCCUPIED) == 0:
            return "All territories acquired"

        # choose an unoccupied territory
        choice = random.choice(Board.UNOCCUPIED)
        print(self.name + ' claimed ' + choice.name)

        # update params for the territory armies are being placed on
        choice.occupant = self
        choice.num_armies += armies

        # update player's list of owned territories and num of armies
        self.territories.append(choice)
        self.armies -= armies

        # set the territory as occupied
        Board.UNOCCUPIED.remove(choice)
        Board.OCCUPIED.append(choice)
    
    # function for players placing armies on a territory they own
    def place_armies(self, territory, armies):
        if territory in self.territories:
            print(self.name + ' places ' + str(armies) + ' on ' + territory.name)
            territory.num_armies += armies
            self.armies -= armies
        else:
            return 'Territory not owned by player. '

    # For players strategically placing reinforcment armies during their turn
    def place_reinforcements(self):
        rank = []

        for t in self.territories:
            r = evaluator.territory_rank(self, t)
            if r > 0:
                rank.append( (t,r) )
        rank.sort(key = lambda x : x[1], reverse = True)

        armies = round(self.armies/2)  
        for r in rank[0:2]:
            self.place_armies(r[0], armies)
            armies = round(armies/2)

            if self.armies == 1:
                self.place_armies(r[0], 1)

    # function to simulate a player attacking an adjacent territory
    def attack(self, from_t, to_t):
        if from_t is None:
            return None
        if from_t.num_armies <= 1:
            return None
        while from_t.num_armies > 1 and to_t.num_armies > 0:
            if to_t.num_armies == 0:
                break
            
            ad = min(3,from_t.num_armies)
            dd = min(2,to_t.num_armies)

            a_rolls = self.roll_dice(ad)
            d_rolls = self.roll_dice(dd)

            for i in itertools.zip_longest(a_rolls, d_rolls):
                if i[0] is None or i[1] is None:
                    break
                if from_t.num_armies <= 1:
                    return None
                if i[0] > i[1]:
                    to_t.num_armies -= 1
                elif i[0] < i[1]:
                    from_t.num_armies -= 1
            print(from_t.num_armies, to_t.num_armies)
        print(from_t.num_armies, to_t.num_armies)
        return from_t,to_t

    # updates both territories from the result of an attack
    def attack_update(self, from_t, to_t):
        w = self.attack(from_t, to_t)
        if w is not None and from_t.num_armies != 1:
            print(self.name +  ' Conquered ' + w[1].name + ' From ' + w[0].name)
            loser = w[1].occupant # loser of battle is occupant of target territory
            loser.territories.remove(w[1]) # territory is removed from loser's territories
            w[1].occupant = self # winner obtains target territory
            w[1].num_armies = w[0].num_armies - 1
            w[0].num_armies = 1
            self.territories.append(w[1])
        else:
            print(' failed to conquer ' + to_t.name)
        
