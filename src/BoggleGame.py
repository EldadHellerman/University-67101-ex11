#################################################################
# FILE : BoggleGraphics.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex11 2023
# DESCRIPTION: A class used for a boggle game. It uses BoggleGraphics for the graphics.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

from boggle_board_randomizer import randomize_board
from BoggleGraphics import BoggleGraphics
import time

class BoggleGame:
    def __init__(self):
        self.time_start_of_game = 0
        self.graphics = BoggleGraphics()
        self.start_new_game()
    
    def start_new_game(self):
        self.score = 0
        self.words_found = []
        self.board = randomize_board()
        self.current_path = []
        self.after_id_delete_path = None

        self.graphics.words_found_clear()
        self.graphics.set_board(self.board)
        self.graphics.set_cb_button_reset(self.cb_reset)
        self.graphics.set_cb_path_dragged(self.cb_path_dragged)
        self.graphics.set_cb_path_released(self.cb_path_released)
        self.graphics.set_cb_word_selected(self.cb_word_selected)
        self.graphics.set_cb_timer(100, self.cb_timer)
        self.time_start_of_game = time.time()
        self.set_score(self.score)
        self.set_time(0)
    
    def check_next_cell_valid(self, cell):
        if(len(self.current_path) == 0): return True
        if(cell in self.current_path): return False #if was already in that cell before
        x1, y1 = cell
        x2, y2 = self.current_path[-1]
        if(max(abs(x1-x2), abs(y1-y2)) > 1): return False #if not one of 8 neighbors
        return True
    
    def path_submitted(self, path):
        print(f"path submitted! path is: {path}")
        self.graphics.set_input_background(len(path) > 3)

    def get_current_path_word(self):
        return "".join([self.board[y][x] for (x,y) in self.current_path])

    def start(self):
        self.graphics.start()
    
    def cb_timer(self):
        elapsed_time = time.time() - self.time_start_of_game
        self.set_time(elapsed_time)

    def cb_reset(self):
        self.start_new_game()

    def cb_word_selected(self, selection):
        if(len(selection) != 1): return
        index = selection[0]
        print("a word was selected!", index)

    def cb_path_dragged(self, current_cell):
        if(not self.check_next_cell_valid(current_cell)):
            return
        self.current_path.append(current_cell)
        self.graphics.set_input(self.get_current_path_word())
        if(len(self.current_path) == 1): #this is the first cell selected
            self.cb_path_selection_clear() #clear previous path selection
            #cancel timer which was suppose to delete the paths:
            if(self.after_id_delete_path is not None):
                self.graphics.after_cancel(self.after_id_delete_path)
        else:
            self.graphics.path_draw(self.current_path[-2], self.current_path[-1], "#ff0000")
    
    def cb_path_released(self):
        if(self.current_path != []): self.path_submitted(self.current_path)
        #start a timer to delete the paths:
        self.after_id_delete_path = self.graphics.after(1000, self.cb_path_selection_clear)
        self.current_path = []

    def cb_path_selection_clear(self):
        self.graphics.path_delete_all()
        self.graphics.set_input("")
        self.graphics.set_input_background(None)
    
    def draw_path(self, path):
        for cell_1, cell_2 in zip(path[:-1], path[1:]):
            self.graphics.path_draw(cell_1, cell_2, "#ff0000")
    
    def set_score(self, score: int):
        self.graphics.set_score(f"Score: {score}")
    
    def set_time(self, seconds: int):
        minutes = int(seconds // 60)
        seconds = seconds % 60
        self.graphics.set_time(f"Time Left: {minutes:02d}:{seconds:04.1f}")

    