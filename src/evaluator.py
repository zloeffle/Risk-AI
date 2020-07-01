from territory import *
from board import *
from player import *
import random
import math



# returns a list of ranks for each continent from high to low
# based on its army bonus, number of borders, and num of territories
def continent_rank():
    rating = []
    score = 0

    for k in CONTINENTS.keys():
        numTerr = len(CONTINENTS.get(k))
        bonus = ARMY_BONUS.get(k)
        borders = INVASION_PATHS.get(k)
        score = round(  ( (bonus - borders) / numTerr ), 3)
        rating.append((k, score))
    rating.sort(key = lambda x : x[1], reverse = True)
    return rating

####### EVALUATIONS FOR REINFORCING #########
# the ratio of hostile armies on neighboring territories to the number of armies on the territory in question,
def army_vantage(player, territory):
    adjacents = getAdjacencies(territory)
    enemy = 0   # number of enemy armies on surrounding territories

    for t in adjacents:
        if t not in player.territories:
            enemy += t.num_armies
    if enemy > 0:
        return territory.num_armies/enemy
    return 0

# the ratio of neighboring territories that are hostile,
def territory_vantage(player, territory):
    adjacents = getAdjacencies(territory)
    enemy = 0
    friendly = 0

    for t in adjacents:
        if t not in player.territories:
            enemy += 1
        else:
            friendly += 1
    if enemy > 0:
        return friendly/enemy
    return 0

# returns a rank for a territory 
# rank is calculated using army/territory vantage, territory is a border, and the territory is in a continent the player is close to controlling 
def territory_rank(player, territory):
    army = army_vantage(player, territory) 
    terr = territory_vantage(player, territory)
    weight = 1  # weight a player assigns to a territory (0:2)

    # territory is in a continent the player is close to controlling
    if len(player.target_continent) > 0:
        if territory.name in CONTINENTS.get(player.target_continent):
            weight += 1
            # territory is a border in a continent the player is close to controlling
            if territory.name in BORDERS:
                weight += 1
    rank = round(army * weight + terr * weight, 2)
    return rank

####### EVALUATIONS FOR ATTACKING #########
# border security threat: sum of all enemy troops in areas adjacent to a territory 
def BST(player, territory):
    adj = getAdjacencies(territory)
    enemies = 0
    for t in adj:
        if t not in player.territories:
            enemies += t.num_armies
    return enemies

# border security ratio: bst divided by the number of units in a territory 
# Countries with a high BSR are more likely to be conquered by an enemy player
def BSR(player, territory):
    enemies = BST(player, territory)
    if enemies == 0:
        return 1
    return territory.num_armies/enemies

# returns a list of territories that are a good origin of attack
def att_origins(player):
    origins = []
    for t in player.territories:
            origins.append(t)
    return origins

# returns a list (origin, target) pairs for the most suitable targets
def best_targets(player):
    origins = att_origins(player)
    targets = []
    for o in origins:
        target = getAdjacencies(o)
        for t in target:
            if t.occupant is player:
                continue
            score = sum_battle(o.num_armies,t.num_armies)
            if score[0] >= 0.5:
                targets.append((o,t,score[0]))
    return targets

# probability of the attacker/defneder winning given a combination of dice
# returns a list: [att troop loss, def troop loss, probability of the event]
# http://datagenetics.com/blog/november22011/index.html
def loss_prob(A, D):
    if D == 0:
        return 1 # attacker wins 100%
    if A == 0:
        return 0  # defender wins 100%
    
    # asumes rolls are always done with the max num of dice
    a = min(3,A) # num of dice for attacker
    d = min(2,D) # num of dice for defender
    outcomes = int(math.pow(6,a+d)) # num of possible outcomes
    result = []
        
    #print('attacker rolling ' + str(a) + ' dice')
    #print('defender rolling ' + str(d) + ' dice')
    #print('possible outcomes ' + str(outcomes))

    k = 1
    p = 0
    while k <= 6:
        if a == 1 and d == 2:
            p += math.pow(k-1,d)/outcomes
            if k == 6:
                t1 = (0,1,round(p,3))
                t2 = (1,0,round(1-p,3))
                result.append(t1)
                result.append(t2)
                return result
        elif a >= 1 and d == 1:
            p += math.pow(k,a)/outcomes
            if k == 6:
                t1 = (0,1,round(1-p,3))
                t2 = (1,0,round(p,3))
                result.append(t1)
                result.append(t2)
                return result
        elif a == 2 and d == 2:
            t1 = (0,2,round(295/outcomes,3))
            t2 = (2,0,round(581/outcomes,3))
            t3 = (1,1,round(420/outcomes,3))
            result.append(t1)
            result.append(t2)
            result.append(t3)
            return result
        else: # att: 3 dice, def: 2 dice
            t1 = (0,2,round(2890/outcomes,3))
            t2 = (2,0,round(2275/outcomes,3))
            t3 = (1,1,round(2611/outcomes,3))
            result.append(t1)
            result.append(t2)
            result.append(t3)
            return result
        k+=1

# evaluation for one battle
# takes num attackers, num defenders, and probability
def one_battle_eval(A,D,p=1):
    loss = loss_prob(A,D)
    outcomes = []
    for i in loss:
        tup = (A-i[0], D-i[1], round(i[2]*p,3))
        outcomes.append(tup)
    return outcomes

# evaluation for an entire battle
# returns tuple: (att prob of winning, def prob of winning)
def battle_eval(A,D):
    # matrix of possible states during of the battle and their probability of occuring
    prob_mat = [[0 for j in range(D+1)] for i in range(A+1)]
    prob_mat[A][D] = 1

    # dict of outcomes: key = (attackers, defenders) value = probability
    outcomes = {}

    # loop through the probability matrix
    for i in range(A,-1,-1):
        for j in range(D,-1,-1):
            p = prob_mat[i][j] # probability of the current battle state
            if p:
                a = i # attacker armies
                d = j # defender armies

                # check if current state is in final form (att or def runs out of armies)
                if i == 0 or j == 0:
                    outcomes[(a,d)] = p # add prob for current state to outcomes
                    continue
                
                # calculate prob of the battle states and add to outcomes
                state = one_battle_eval(a,d,p)
                for s in state:
                    # if state is finished add to outcomes
                    if s[0] < 0 or s[1] < 0:
                        outcomes[(s[0],s[1])] = s[2]
                        continue

                    # update probability matrix
                    prob_mat[s[0]][s[1]] += s[2]
    return outcomes    

# sum the attacker and defender probabilities of potential outcomes to generate the
# total probability for the attacker/defender winning a battle
def sum_battle(A,D):
    at = 0
    df = 0
    outcomes = battle_eval(A,D)
    for k in outcomes.keys():
        if k[1] == 0:
            at += outcomes.get(k)
        if k[0] == 0:
            df += outcomes.get(k)
    return round(at,3),round(df,3)



####### EVALUATIONS FOR FORTIFYING #########

# evaluates which territories should be included in fortification at the end of a players turn
def fortify_eval(player):
    lowest_risk = []
    lowest = None
    highest = None
    rank = []
    
    for t in player.territories:
        r = territory_rank(player, t)
        if r == 0:
            lowest_risk.append(t)
        else:
            rank.append( (t,r) )
    rank.sort(key = lambda x : x[1], reverse = True)
    for r in rank:
        highest = r[0]
        break
    
    armies = []
    for t in lowest_risk:
        armies.append((t,t.num_armies))
    armies.sort(key = lambda x : x[1], reverse = True)
    
    for t in armies:
        lowest = t[0]
        break
        
    return lowest,highest
            