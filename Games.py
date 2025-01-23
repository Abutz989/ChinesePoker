from GameWrapper import *
from logic import *
import copy
import tkinter as tk
import time
import constants as c
from ComPlayer import *
import copy

class KeyBoardGame(GameLogic):
    def __init__(self,Player: AbstractMovePlayer):
        GameLogic.__init__(self)
        self.master.bind("<Key>", self.key_down)
        self.com_player = Player
      
        self.commands = {c.KEY_1: 0, c.KEY_2: 1,
                         c.KEY_3: 2, c.KEY_4: 3,
                         c.KEY_5: 4, c.KEY_0: 9}
        self.initGame()
    
    def initGame(self):
        # draw 5 cards for player and computer
        for i in range(5):
            self.player_slots[0][i] = self.draw_card()
            self.update_grid_cells()
            time.sleep(1)
            self.computer_slots[0][i] = self.draw_card()
            self.update_grid_cells()
            time.sleep(0.2)
       
        self.player_card = self.draw_card()
        self.update_grid_cells()


    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            done = self.set_card(self.commands[repr(event.char)])
            if done:
                self.hide_card()
                self.update_grid_cells()
                time.sleep(0.3)
                computer_card = self.draw_card()
                move = self.com_player.get_move(self.getPlayerSlots(),self.getComputerSlots(),computer_card,self.game_state())
                done = self.computer_move(move,computer_card)
                if not done:
                    popupmsg("Computer Illegal Move")
                self.update_grid_cells()
                time.sleep(0.3)
                if self.game_state() == 'End':
                    win = self.calculate_score()
                    if win:
                        popupmsg("You Win :)")
                    else:
                        popupmsg("You Lose :(")
                else:
                    self.player_card = self.draw_card()
                    self.update_grid_cells()
            else:
            # popup window message of illegal move
                popupmsg("Illegal Move")
            
    def run_game(self):
        self.mainloop()

def popupmsg(msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()


class AutoGame(VirtualGameLogic):
    def __init__(self,Player1: AbstractMovePlayer, Player2: AbstractMovePlayer):
        VirtualGameLogic.__init__(self)
        self.player1 = Player1
        self.player2 = Player2
        self.initGame()
    
    def initGame(self):
        for i in range(5):
            self.player_slots[0][i] = self.draw_card()
            self.computer_slots[0][i] = self.draw_card()
    
    def run_game(self):
        while True:
            try:
                player1_card = self.draw_card()
                self.player_card = player1_card
            except:
                break
            move1 = self.player1.get_move(self.getComputerSlots(),self.getPlayerSlots(),player1_card,self.game_state())
            done = self.auto_player_move(move1,player1_card)
            if not done:
                print("Player1 Illegal Move")
                break
            player2_card = self.draw_card()
            move2 = self.player2.get_move(self.getPlayerSlots(),self.getComputerSlots(),player2_card,self.game_state())
            # if move2 == 9:
            #     move2 = self.player2.get_move(self.getPlayerSlots(),self.getComputerSlots(),player2_card,self.game_state())
            
            done = self.computer_move(move2,player2_card)
            self.hide_card()
            if not done:
                print("Player2 Illegal Move")
                # move2 = self.player2.get_move(self.getPlayerSlots(),self.getComputerSlots(),player2_card,self.game_state())
                break
            if self.game_state() == 'End':
                win = self.calculate_score()
                if win:
                    print("Player1 Win")
                else:
                    print("Player2 Win")
                print("Player1 Slots:",repr(self.player_slots))
                print("Player2 Slots:",repr(self.computer_slots))
                break 


