from board import *
from player import *
from state import *
import evaluator
import territory
import copy
import display
import time
import math

class Game(object):
    def __init__(self):
        self.board = Board()
        self.players = []
        self.turn = 0
        self.deck = DECK.copy()
        self.d = display.Display(self)
    
    # To string function for viewing details about the current game
    def __str__(self):
        players = ''
        for i in self.players:
            players += str(i)

        return (
            ''.join([str(x) + '\n' for x in self.players]) + 
            'Current Turn: ' + self.turn.name + '\n'
        )

    # print game board
    def print_board(self):
        for t in self.board.OCCUPIED:
            print(str(t))

    # update game board
    def board_update(self):
        print('\nUpdating game board...')
        b = []
        self.board.OCCUPIED.clear()
        for p in self.players:
            for t in p.territories:
                t.occupant = p
            b.extend(p.territories)
        self.board.OCCUPIED.extend(b)

    # checks if the game is in a terminal state
    def isTerminal(self, player):
        control = player.control_percentage()
        count = 0
        for c in control:
            count += c[1]
        return count        

    # function for adding players into a game
    def add_player(self, name, color):
        p = Player(name, color)
        self.players.append(p)

    # helper function for deciding which players goes first during game initialization
    def goes_first(self):
        winner = 0
        values = []
        temp = []

        for p in self.players:
            res = p.roll_dice(1)
            temp.append(res)
            values.append( (p,res) )
            print(p.name + ' ' + 'Rolled: ' + str(res))
        winner = max(values, key = lambda x : x[1])[0]
        return winner  

    # decides how many armies a player recieves at the beginning of their turn
    def addArmies(self, player):
        if len(player.territories) <= 9:
            armiesRecieved = 3
        else:
            armiesRecieved = int(len(player.territories) / 3)

        # if a player controls a continent they get the army bonus for that continent
        if player.controls_continent() != 0:
            armiesRecieved += player.controls_continent()
        return armiesRecieved

    ###### INITIALIZATION ####### 
    # Setup a new game into its base state
    def initialize(self):
        print('Initializing...')
        # 1) Each player rolls a dice, player that rolls highest goes first
        winner = self.goes_first()
        print(winner.name + ' goes first\n')

        # 2) Starting with the player that rolled the highest value, players take turns placing armies on all of the unoccupied territories
        #   until they are claimed
        while len(Board.UNOCCUPIED) > 0:
            for j in self.players:
                currentPlayer = j
                currentPlayer.place_armies_init(1)
                self.turn = j
        print('\n')

        # 3) Players place additional armies on all of their occupied territories until everyone runs out
        for player in self.players:
            print('\n' + player.name + ' placing additional armies...')
            while player.armies > 0:
                choice = random.choice(player.territories)
                player.place_armies(choice, 1)
        self.turn = winner

        print('\n Updating board...')
        self.board_update()
        print('Game initialization complete\n')

    # creates tree for potential attack targets
    def expansion(self, currentState, x, limit):
        print("Expanding")
        if x < limit:
            cS = currentState
            for t in currentState.simulatedTerritories:
                for adj in territory.getAdjacencies(t):
                    if adj.occupant.name != t.occupant.name:
                        adj = copy.deepcopy(copy.deepcopy(adj))
                        prob = evaluator.battle_eval(t.num_armies, adj.num_armies)
                        bestChance = ((0,0), 0)
                        for p in prob.keys():
                            if prob.get(p) > bestChance[1] and p[0] != 0:
                                bestChance = (p, prob.get(p))
                        probOfWinning = evaluator.sum_battle(t.num_armies,adj.num_armies)
                        if probOfWinning[0] > .5:
                            t.num_armies = 1
                            adj.num_armies = bestChance[0][0]-1
                            adj.occupant = t.occupant
                            cS.simulatedTerritories.append(adj)
                            childStates = self.expansion(State(cS.simulatedTerritories, cS.newProbability, probOfWinning[0]),
                                                         x + 1,
                                                         limit)
                            cS.childStates.append(childStates)
            return cS
        else:
            return currentState

    # traverses the expansion tree to find the best territories to attack
    def explore(self, s, p):
        if len(s.childStates) == 0:
            return (len(s.simulatedTerritories)/42 * s.addArmies()), s
        else:
            bestState = (0, None)
            for x in s.childStates:
                currState = self.explore(x, p)
                if currState[0] > bestState[0]:
                    bestState = currState
            return bestState[0], s

    # simulates a player's attack
    def battle(self, player):
        player.update_target()
        currTerr = copy.deepcopy(copy.deepcopy(player.territories))
        playerTree = self.expansion(State(copy.deepcopy(currTerr), 1, 1), 0, 1000)
        bestState = self.explore(playerTree, player)[1]
        l1 = []
        l2 = []
        l3 = []
        l = []

        for x in player.territories:
            l1.append(x.name)
        for x in bestState.simulatedTerritories:
            l2.append(x.name)

        for x in bestState.simulatedTerritories:
            flag = False
            for y in player.territories:
                if x.name == y.name:
                    flag = True
            if not flag:
                l.append(x)

        for x in l:
            l3.append(x.name)

        if len(l) == 0:
            return None

        bestAttacker = None
        for a in range(len(l)):
            if bestAttacker is None:
                target = l[a]
                for x in self.board.OCCUPIED:
                    if x.name == target.name:
                        target = x
            else:
                break
            for adj in territory.getAdjacencies(target):
                if adj in player.territories:
                    if bestAttacker is None or adj.num_armies > bestAttacker.num_armies:
                        bestAttacker = adj

        if target is None:
            return 1

        player.attack_update(bestAttacker, target)
        self.board_update()
        return 1
    
    # player gets one opportunity to strategically move armies from one territory to another
    def fortify(self, player):
        choices = evaluator.fortify_eval(player)
        from_t = choices[0]
        to_t = choices[1]
        
        if from_t is not None and to_t is not None:
            if from_t.num_armies > 1:
                armies = from_t.num_armies - 1
                print('Moving ' + str(armies) + ' from ' + from_t.name + ' to ' + to_t.name)
                to_t.num_armies += armies
                from_t.num_armies -= armies
        self.board_update()

            
