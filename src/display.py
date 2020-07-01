import copy
import math
import time
import tkinter as tk
import keyboard
from PIL import Image, ImageTk
import board
import game
import player
import territory
from state import State
from territory import Territory
import evaluator
import csv

LOCATIONS = {
    "Alaska": (90, 160),
    "Alberta": (230, 250),
    "Central America": (270, 360),
    "Eastern United States": (355, 310),
    "Greenland": (480, 150),
    "Northwest Territory": (300, 170),
    "Ontario": (280, 215),
    "Quebec": (370, 215),
    "Western United States": (200, 300),

    "Argentina": (380, 565),
    "Brazil":  (460, 510),
    "Peru": (400, 525),
    "Venezuela": (360, 410),

    "Great Britain": (600, 230),
    "Iceland": (600, 150),
    "Northern Europe": (690, 250),
    "Scandinavia": (680, 150),
    "Southern Europe": (670, 305),
    "Ukraine": (780, 190),
    "Western Europe": (580, 290),

    "Congo": (700, 465),
    "East Africa": (765, 415),
    "Egypt": (705, 330),
    "Madagascar": (770, 500),
    "North Africa": (600, 350),
    "South Africa": (690, 550),

    "Afghanistan": (800, 290),
    "China": (900, 290),
    "India": (870, 380),
    "Irkutsk": (1020, 220),
    "Japan": (1110, 290),
    "Kamchatka": (1150, 195),
    "Middle East": (800, 330),
    "Mongolia": (1020, 280),
    "Siam": (940, 390),
    "Siberia": (930, 200),
    "Ural": (860, 200),
    "Yakutsk": (1050, 140),

    "Eastern Australia": (1130, 590),
    "Indonesia": (1000, 470),
    "New Guinea": (1110, 450),
    "Western Australia": (1020, 590)
}

class Display():

    def __init__(self, game):
        self.g = game

    def circle(self, c, x, y, tag, num_units, color):
        c.create_oval(x, y, x + 30, y + 30, fill=color, tag=tag)
        c.create_text(x + 7, y + 7, text=num_units, anchor=tk.NW, font=("Times New Roman", 12))

    def refresh(self, canvas, bg_image, master):
        canvas.delete("all")
        canvas.create_image(650, 450, image=bg_image, anchor=tk.CENTER)
        canvas.pack()

        canvas.create_text(500, 680, anchor=tk.W, font=("Times New Roman", 16), text="Current Player: " + str(self.g.turn.name))
        canvas.create_text(700, 680, anchor=tk.W, font=("Times New Roman", 16), text="Target: " + str(self.g.turn.target_continent))
        for x in board.Board.OCCUPIED:
            self.circle(canvas, LOCATIONS[x.name][0], LOCATIONS[x.name][1], x.name, x.num_armies, x.occupant.color)

        master.update_idletasks()
        master.update()

    def start(self):
        turns = 0
        start = time.time()
        master = tk.Tk()
        master.title("Risk")
        master.resizable(0, 0)
        bg_image = ImageTk.PhotoImage(Image.open("Risk_board.png"))
        canvas = tk.Canvas(master, width = 1300, height = 900)
        self.refresh(canvas, bg_image, master)
        players = []

        while len(self.g.players) > 1:
            for player in self.g.players:
                self.g.turn = player
                player.update_target()
                self.refresh(canvas, bg_image, master)
                if self.g.isTerminal(player) == 0:
                    players.append(player)
                    self.g.players.remove(player)
                
                ######### 1) Recieving/placing new armies #########
                totalSetsTraded = 0     # total sets of cards traded in so far
                cardSetValue = 5        # current value in armies for a set of cards
                armiesRecieved = self.g.addArmies(player)
                cardset = player.create_set()
                if cardset is not None:
                    for c in cardset:
                        if c.territory in player.territories:
                            armiesRecieved += 2
                        armiesRecieved += cardSetValue

                        if totalSetsTraded == 7:
                            cardSetValue += 5
                        else:
                            cardSetValue += 2
                    totalSetsTraded += 1
                    player.trade_set(cardset)                
            
                player.armies += armiesRecieved
                
                print('\n' + player.name + ' recieved ' + str(armiesRecieved) + ' armies')
                print(player.name + ' now has ' + str(player.armies) + ' armies')
                print(player.name + ' placing reinforcements...')
                player.place_reinforcements()
                self.g.board_update()
                self.refresh(canvas, bg_image, master)

                ######### 2) Attacking #########
                print("Beginning Attack")
                prev = len(player.territories)
                attack = 1
                att_start = time.time()
                while attack is not None:
                    player.update_target()
                    attack = self.g.battle(player)
                    self.refresh(canvas, bg_image, master)
                att_end = time.time()
                att_total = math.floor(att_end-att_start)
                player.att_time.append(att_total)
                if len(player.territories) > prev:
                    player.drawcard(board.DECK)
                    
                ######### 3) Fortifying #########
                self.g.fortify(player)
                turns += 1
                print("Finished Turn")

        winner = self.g.players[0]
        self.g.turn = winner
        self.refresh(canvas, bg_image, master)
        end = time.time()
        totalTime = math.floor(end-start)
        
        '''
        with open('results.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            data = [totalTime, turns, winner.name, len(winner.att_time), round(sum(winner.att_time)/len(winner.att_time),2)]
            writer.writerow(data)
            for p in players:
                data = [totalTime, turns, p.name, len(p.att_time), round(sum(p.att_time)/len(p.att_time),2)]
                writer.writerow(data)
        '''    
        canvas.create_text(500, 720,anchor = tk.W, font=("Times New Roman", 12), text=("Took " + str(totalTime) + " seconds for the game to end"))
        canvas.create_text(500, 740, anchor=tk.W, font=("Times New Roman", 12), text="Player " + str(self.g.players[0].name) +" has won")
        canvas.create_text(500, 760, anchor=tk.W, font=("Times New Roman", 12), text=str(turns) +" turns occurred durring the game")
        canvas.create_text(500, 780, anchor=tk.W, font=("Times New Roman", 12), text="Press Z to play again")
        canvas.pack()
        
        while not keyboard.is_pressed("z"):
            master.update_idletasks()
            master.update()
        master.destroy()