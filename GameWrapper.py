import random
import constants as c
from tkinter import Frame, Label, CENTER
from abc import abstractmethod

class GameBoard(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('Chinese Poker')
        self.grid_cells = []
        self.init_grid()
        self.total_score = 0
        
        self.player_slots = [['' for _ in range(5)] for _ in range(5)]
        self.computer_slots = [['' for _ in range(5)] for _ in range(5)]
        self.player_card = ''
        self.deck = [f"{rank}{suit}" for suit in c.SUITS for rank in c.RANKS]
        random.shuffle(self.deck)
        self.update_grid_cells()

    def init_grid(self):
        # Init grid with 5x5 cells for the player and 5x5 cells computer showing against each other verticly
        # 1 cell for player card showing beside the plyer slots

        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()
        #build the computer cells
        for i in range(5):
            grid_row = []
            for j in range(5):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE/5, height=c.SIZE/5)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text='',
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)
       
       # build a gap between the player and computer slots, in the middle of the gap set the player card cell
        grid_row = []
        for i in range(5):
            if i == 2:
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                         width=c.SIZE/5, height=c.SIZE/5)
                cell.grid(row=5, column=i, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text='',
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=4, height=2)
            else:
                cell = Frame(background, bg=c.BACKGROUND_COLOR_GAME,
                            width=c.SIZE/5, height=c.SIZE/5)
                cell.grid(row=5, column=i, padx=c.GRID_PADDING,
                        pady=c.GRID_PADDING)
                t = Label(master=cell, text='',
                        bg=c.BACKGROUND_COLOR_GAME,
                        justify=CENTER, font=c.FONT, width=4, height=2)
            t.grid()
            grid_row.append(t)
        self.grid_cells.append(grid_row)
        
        #build the player cells
        for i in range(6,11):
            grid_row = []
            for j in range(5):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE/5, height=c.SIZE/5)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text='',
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def getDeck(self):
        return self.deck

    def getPlayerSlots(self):
        return self.player_slots

    def getComputerSlots(self):
        return self.computer_slots

    def update_grid_cells(self):
        # update the computer slots
        for i in range(5):      
            for j in range(5):
                card = self.computer_slots[i][j]
                if card == '':
                        self.grid_cells[i][j].configure(
                            text='', bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    if i == 4 and self.game_state() != 'End':
                        self.grid_cells[i][j].configure(
                            text='☻', bg=c.BACKGROUND_COLOR_HIDE,
                            fg="#eee4da")
                    else:
                        # replace only 'T' in card with '10'
                        cardText = card.replace('T', '10')
                        self.grid_cells[i][j].configure(
                            text=cardText, bg=c.BACKGROUND_COLOR_DICT[card[1]],
                            fg="#eee4da")
        
        # update the player card
        card = self.player_card
        if card == '':
            if self.game_state() != 'End':
                self.grid_cells[5][2].configure(
                    text='☻', bg=c.BACKGROUND_COLOR_HIDE,
                    fg="#eee4da")
            else:
                self.grid_cells[5][2].configure(
                    text='', bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        else:
            cardText = card.replace('T', '10')
            self.grid_cells[5][2].configure(
                text=cardText, bg=c.BACKGROUND_COLOR_DICT[card[1]],
                fg="#eee4da")
        
       
        # update the player slots
        for i in range(6, 11):
            for j in range(5):
                card = self.player_slots[i-6][j]
                if card == '':
                    self.grid_cells[i][j].configure(
                        text='', bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    cardText = card.replace('T', '10')
                    self.grid_cells[i][j].configure(
                        text=cardText, bg=c.BACKGROUND_COLOR_DICT[card[1]],
                        fg="#eee4da")
        self.update_idletasks()

    def recolor_player_column(self, column):
        for i in range(5):
            self.grid_cells[i+6][column].configure(bg=c.BACKGROUND_COLOR_WIN)
        self.update_idletasks()    

    def recolor_computer_column(self, column):
        for i in range(5):
            self.grid_cells[i][column].configure(bg=c.BACKGROUND_COLOR_WIN)
        self.update_idletasks()

    @abstractmethod
    def run_game(self):
        pass

class GameVirtual():

    def __init__(self):
        self.player_slots = [['' for _ in range(5)] for _ in range(5)]
        self.computer_slots = [['' for _ in range(5)] for _ in range(5)]
        self.player_card = ''
        self.deck = [f"{rank}{suit}" for suit in c.SUITS for rank in c.RANKS]
        random.shuffle(self.deck)

    def getDeck(self):
        return self.deck

    def getPlayerSlots(self):
        return self.player_slots

    def getComputerSlots(self):
        return self.computer_slots

    @abstractmethod
    def run_game(self):
        pass
