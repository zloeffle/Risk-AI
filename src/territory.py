import board

###### TERRITORY #######
# represent territories
ADJACENTS = {
    "Alaska": ["Alberta", "Northwest Territory", "Kamchatka"],
    "Alberta": ["Alaska", "Northwest Territory", "Ontario", "Western United States"],
    "Central America": ["Western United States", "Eastern United States", "Venezuela"],
    "Eastern United States": ["Central America", "Ontario", "Quebec", "Western United States"],
    "Greenland": ["Northwest Territory", "Ontario", "Quebec", "Iceland"],
    "Northwest Territory": ["Alaska", "Alberta", "Ontario", "Greenland"],
    "Ontario": ["Alberta", "Northwest Territory", "Western United States", "Eastern United States", "Quebec", "Greenland"],
    "Quebec": ["Ontario", "Eastern United States", "Greenland"],
    "Western United States": ["Alberta", "Ontario", "Eastern United States", "Central America"],

    "Argentina": ["Brazil", "Peru"],
    "Brazil": ["Venezuela", "Peru", "Argentina", "North Africa"],
    "Peru": ["Argentina", "Brazil", "Venezuela"],
    "Venezuela": ["Central America", "Brazil", "Peru"],

    "Great Britain": ["Iceland", "Scandinavia", "Northern Europe", "Western Europe"],
    "Iceland": ["Greenland", "Great Britain", "Scandinavia"],
    "Northern Europe": ["Great Britain", "Scandinavia", "Southern Europe", "Ukraine", "Western Europe"],
    "Scandinavia": ["Great Britain", "Iceland", "Northern Europe", "Ukraine"],
    "Southern Europe": ["Northern Europe", "Ukraine", "Western Europe", "Middle East", "Egypt", "North Africa"],
    "Ukraine": ["Northern Europe", "Scandinavia", "Southern Europe", "Afghanistan", "Ural", "Middle East"],
    "Western Europe": ["Great Britain", "Northern Europe", "Southern Europe", "North Africa"],

    "Congo": ["East Africa", "North Africa", "South Africa"],
    "East Africa": ["Congo", "Egypt", "Madagascar", "North Africa", "South Africa", "Middle East"],
    "Egypt": ["East Africa", "North Africa", "Southern Europe", "Middle East"],
    "Madagascar": ["East Africa", "South Africa"],
    "North Africa": ["Congo", "East Africa", "Egypt", "Southern Europe", "Western Europe", "Brazil"],
    "South Africa": ["Congo", "East Africa", "Madagascar"],

    "Afghanistan": ["China", "India", "Middle East", "Ural", "Ukraine"],
    "China": ["Afghanistan", "India", "Siam", "Mongolia", "Ural", "Siberia"],
    "India": ["Afghanistan", "China", "Middle East", "Siam"],
    "Irkutsk": ["Kamchatka", "Mongolia", "Siberia", "Yakutsk"],
    "Japan": ["Kamchatka", "Mongolia"],
    "Kamchatka": ["Japan", "Irkutsk", "Mongolia", "Yakutsk", "Alaska"],
    "Middle East": ["East Africa", "Egypt", "Southern Europe", "Ukraine", "Afghanistan", "India"],
    "Mongolia": ["China", "Japan", "Kamchatka", "Irkutsk", "Siberia"],
    "Siam": ["China", "India", "Indonesia"],
    "Siberia": ["Ural", "China", "Mongolia", "Irkutsk", "Yakutsk"],
    "Ural": ["Afghanistan", "China", "Siberia", "Ukraine"],
    "Yakutsk": ["Irkutsk", "Kamchatka", "Siberia"],

    "Eastern Australia": ["New Guinea", "Western Australia"],
    "Indonesia": ["Siam", "New Guinea", "Western Australia"],
    "New Guinea": ["Indonesia", "Eastern Australia", "Western Australia"],
    "Western Australia": ["Eastern Australia", "Indonesia", "New Guinea"]
}

# Border territories
BORDERS = ['Greenland', 'Central America', 'Brazil', 'North Africa', 'East Africa', 'Southern Europe', 'Western Europe', 'Ukraine', 'Afghanistan', 'Ural', 'Middle East',
            'Siam', 'Indonesia']

class Territory(object):
    def __init__(self,name):
        self.name = name 
        self.adjacents = []                                 # get list of adjacent territories
        self.occupant = None                              # player that owns the territory
        self.num_armies = 0                               # num of armies occupying the territory
        self.border = self.isBorder()                   # boolean that tells if the territory is a border between 2 continents                

    def __str__(self):
        return (self.name + '\n' +
               self.occupant.name + '\n' +
               str(self.num_armies))

    def getName(self):
        return self.name

    # checks if a territory is a border for a continent
    def isBorder(self):
        if self.name in BORDERS:
            return True
        return False

# returns a list of territories adjacent to the current
def getAdjacencies(t):
    adj = []
    for k in ADJACENTS.keys():
        if k == t.name:
            adj = ADJACENTS.get(k)
            break
    temp = []
    for t in board.Board.OCCUPIED:
        if t.name in adj:
            temp.append(t)
    return temp

# returns the continent a territory is in
def inContinent(t):
    for c in board.CONTINENTS.keys():
        if t.name in board.CONTINENTS.get(c):
            return c





    
