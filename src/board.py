from card import *
from territory import *

# List of all cards available in the deck.
# dictionary of adjacent territories in a list by territory
# List of all cards held by the player
DECK = [Card("WILD", "WILD"), Card("WILD", "WILD"),
        Card('Alaska', 'Infantry'), Card('Alberta', 'Infantry'), Card('Central America', 'Infantry'), Card('Eastern United States', 'Infantry'),
        Card('Greenland', 'Infantry'), Card('Northwest Territory', 'Infantry'), Card('Ontario', 'Infantry'), Card('Quebec', 'Infantry'),
        Card('Western United States', 'Infantry'), Card('Argentina', 'Infantry'), Card('Brazil', 'Infantry'), Card('Peru', 'Infantry'),
        Card('Venezuela', 'Infantry'), Card('Great Britain', 'Infantry'),
        Card('Iceland', 'Cavalry'), Card('Northern Europe', 'Cavalry'), Card('Scandinavia', 'Cavalry'), Card('Southern Europe', 'Cavalry'),
        Card('Ukraine', 'Cavalry'), Card('Western Europe', 'Cavalry'), Card('Congo', 'Cavalry'), Card('East Asia', 'Cavalry'),
        Card('Egypt', 'Cavalry'), Card('Madagascar', 'Cavalry'), Card('North Africa', 'Cavalry'), Card('South Africa', 'Cavalry'),
        Card('Afghanistan', 'Cavalry'), Card('China', 'Cavalry'),
        Card('India', 'Artillery'), Card('Irkutsk', 'Artillery'),Card('Japan', 'Artillery'), Card('Kamchatka', 'Artillery'),
        Card('Middle East', 'Artillery'), Card('Mongolia', 'Artillery'),Card('Siam', 'Artillery'), Card('Siberia', 'Artillery'),
        Card('Ural', 'Artillery'), Card('Yakutsk', 'Artillery'),Card('Eastern Australia', 'Artillery'), Card('Indonesia', 'Artillery'),
        Card('New Guinea', 'Artillery'), Card('Western Australia', 'Artillery')]

TERRITORIES = ["Middle East", "Afghanistan", "India", "Siam", "China", "Mongolia" ,"Japan", "Kamchatka" ,"Irkutsk", "Yakutsk", "Siberia", "Ural",
               "Alaska", "Northwest Territory", "Greenland", "Alberta", "Ontario", "Quebec", "Western United States", "Eastern United States", "Central America","Iceland",
               "Great Britain", "Scandinavia", "Ukraine", "Northern Europe", "Western Europe", "Southern Europe", "North Africa", "Egypt", "East Africa",
               "Congo", "South Africa", "Madagascar","Venezuela", "Brazil", "Peru", "Argentina","Indonesia", "New Guinea", "Eastern Australia", "Western Australia"
]

# Each continent is represented as a dictionary
# key = armies received if controlled, values = list of territories in that continent
CONTINENTS = {
    'Asia' : ["Middle East", "Afghanistan", "India", "Siam", "China", "Mongolia" ,"Japan", "Kamchatka" ,"Irkutsk", "Yakutsk", "Siberia", "Ural"],
    'North America' : ["Alaska", "Northwest Territory", "Greenland", "Alberta", "Ontario", "Quebec", "Western US", "Eastern US", "Central America"],
    'Europe' : ["Iceland", "Great Britain", "Scandinavia", "Ukraine", "Northern Europe", "Western Europe", "Southern Europe"],
    'Africa' : ["North Africa", "Egypt", "East Africa", "Congo", "South Africa", "Madagascar"],
    'South America' : ["Venezuela", "Brazil", "Peru", "Argentina"],
    'Australia' : ["Indonesia", "New Guinea", "Eastern Australia", "Western Australia"]
    }

# number of border territories in each continent
INVASION_PATHS = {'Asia' : 5, 'North America' : 2,'Europe' : 4, 'Africa' : 3, 'South America' : 2, 'Australia' : 1}

# number of bonus armies recieved if a continent is controlled
ARMY_BONUS = {'Asia' : 7, 'North America' : 5, 'Europe' : 5, 'Africa' : 3, 'South America' : 3, 'Australia' : 2}

######### BOARD CLASS ###########
class Board(object):
    UNOCCUPIED = []
    OCCUPIED = []

    def __init__(self):
        self.continents = 6
        self.territories = 42

        # initialize territories as unoccupied
        for i in TERRITORIES:
            self.UNOCCUPIED.append(Territory(i))

    def __str__(self):
        return ('Occupied: ' + '\n' + ''.join([str(x) + '\n' for x in self.OCCUPIED]) + '\n' + 
                'Unoccupied: ' + '\n' + ''.join([str(x) + '\n' for x in self.UNOCCUPIED]) + '\n'
        )
