from datetime import time
from board import *
from display import *
from player import *
from card import *
from territory import *
from game import *
import time
from state import *
from evaluator import *
import keyboard

i = 1
while i <= 5:
    g = Game()
    g.add_player('red', 'red')
    g.add_player('yellow', 'yellow')
    g.add_player('blue', 'cyan')
    g.initialize()

    d = Display(g)
    d.start()
    i += 1





