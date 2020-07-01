# Risk AI

This is the final project for my introduction to artificial intelligenece class during my senior year at Indiana University. 
Our assignment was to create a functional AI that makes non-trivial decisions over a problem space of our choosing. My partner 
Stephen Pace and I decided to choose this board game as our topic due to its challenging and strategic nature, and it is a childhood
favorite for both of us.

Risk is a strategy-based board game based on conflict, conquest, and diplomacy. The board consists of regions called continents, each
containing various territories. The objective of this game is to conquer the entire map by controlling all 42 territories on the board.
The game is played with a unit called armies which players can use to reinforce their occupied territories or battle an opposing player
for control over one of their occupied territories.

After approximately a month, we successfully developed an intelligent agent that can play the game efficiently and utilize strategies
and thought processes similar to that of a human. We could not implement functionality for a human to play due to the two minute
time constraint of our project demonstration, so an actual game only consists of AI agents playing against eachother. A normal game of risk with all human players can last 6 hours or more. Even with one human player against two intelligent agents, we found that a game can still take 30 minutes or more so adding functionality for a human player was not a feasable option for us. 

We developed the game structure and AI agent using Python 3 and the tkinkter interface for our graphical display. Our intelligent agent 
utilizes a modified version of the Minimax search algorithm to evalute potential game states, and primarily plays using a greedy or agressive strategy.  
