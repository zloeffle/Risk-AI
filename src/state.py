from player import *
from board import *
import evaluator
import territory


class State():

    def __init__(self, simulatedTerritories,  currProbability, probability):
        self.simulatedTerritories = simulatedTerritories
        self.probability = probability
        self.currProbability = currProbability
        self.childStates = []
        #print(simulatedTerritories)
        self.newProbability = currProbability * probability

    def addArmies(self):
        if len(self.simulatedTerritories) <= 9:
            armiesRecieved = 3
        else:
            armiesRecieved = int(len(self.simulatedTerritories) / 3)

        # if a player controls a continent they get the army bonus for that continent
        if self.controls_continent() != 0:
            armiesRecieved += self.controls_continent()
        return armiesRecieved

    def controls_continent(self):
        continent = ''

        for c in CONTINENTS.keys():
            length = len(CONTINENTS.get(c))
            count = 0  # count for num of players territories in a continent
            for t in self.simulatedTerritories:
                if t==[]:
                    break
                if t.name in CONTINENTS.get(c):
                    count += 1
            if count == length:
                continent = c
                break
        if continent in ARMY_BONUS.keys():
            return ARMY_BONUS.get(continent)
        return 0