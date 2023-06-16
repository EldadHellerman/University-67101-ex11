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

import boggle_board_randomizer as bbr
from BoggleLogic import BoggleLogic
from BoggleGraphics import BoggleGraphics
from BoggleGraphicsTheme import BoggleGraphicsTheme
import time

#support timed game, start over, hiding board until player clicks start,
#TODO maybe do types for Board, cell, path?

class BoggleGame:
    def __init__(self):
        self.graphics = BoggleGraphics(BoggleGraphicsTheme())
        self.graphics.audio_load_sound("images/pop.mp3")
        self.logic = BoggleLogic("src/boggle_dict.txt")
        self.start_new_game()
    
    def start_new_game(self):
        self.score = 0
        self.time_now = 0
        self.time_start_of_game = 0
        self.time_game_duration = 180
        self.words_found_paths = {} #{word: list[path]}
        self.words_all_paths = {} #{word: list[path]}
        board = bbr.randomize_board()
        # board = [['a','b']]
        # board = [['a','b'], ['c','d']]
        # board = [['a','b','c','d','e','f'], ['a','b','c','d','e','f']]
        # board = [['a','b','c','d','e','f'] for i in range(6)]
        # board = [['Z' for i in range(4)] for j in range(4)]
        # bbr.BOARD_SIZE = 50
        # board = bbr.randomize_board(bbr.LETTERS*200)
        self.logic.set_board(board)
        self.current_path = []
        self.after_id_delete_path = None
        self.graphics.set_board_hidden(True)
        self.graphics.listbox_words_clear()
        self.graphics.listbox_enable(False) #could be set to true, user preference
        self.graphics.set_board(board)
        self.graphics.set_input_from_path([])
        self.graphics.set_cb_button_reset(self.cb_reset)
        self.graphics.set_cb_path_dragged(self.cb_path_dragged)
        self.graphics.set_cb_path_released(self.cb_path_released)
        self.graphics.set_cb_word_selected(self.cb_word_selected)
        self.graphics.set_cb_reveal_board(self.cb_reveal_board)
        self.graphics.set_reset_or_endgame(True)
        self.update_score()
        self.update_time()
    
    def cb_reveal_board(self):
        self.time_start_of_game = time.time()
        self.timer_main_start()
        self.graphics.set_board_hidden(False)
        self.graphics.draw_board()

    def check_next_cell_valid(self, cell):
        if(len(self.current_path) == 0): return True
        if(cell in self.current_path): return False #if was already in that cell before
        x1, y1 = cell
        x2, y2 = self.current_path[-1]
        if(max(abs(x1-x2), abs(y1-y2)) > 1): return False #if not one of 8 neighbors
        return True
    
    def path_submitted(self, path):
        # print(f"path submitted! path is: {path}")
        if len(path) <= 1: #paths can be only starting cell.
            return
        word = self.logic.path_to_word(self.current_path)
        if(word in self.words_found_paths): #word was already found (though maybe on a different path)
            self.graphics.set_input_background(1)
            self.words_found_paths[word] += [path]
            return
        #check if word is in dictionary! (which implies a valid word length)
        if not self.logic.word_in_words(word):
            self.graphics.set_input_background(2)
            return
        #valid word was found:
        self.graphics.set_input_background(0)
        self.score += len(path)**2
        self.update_score()
        self.words_found_paths[word] = [path]
        self.graphics.listbox_words_add(word)

    def start(self):
        self.graphics.start()
    
    def timer_main_start(self):
        self.timer_main_enabled = True
        self.timer_main_id = self.graphics.after(100, self.cb_timer_main)
    
    def timer_main_stop(self):
        self.timer_main_enabled = False
    
    def cb_timer_main(self):
        if(not self.timer_main_enabled): return
        self.time_now = time.time()
        self.update_time()
        self.timer_main_id = self.graphics.after(100, self.cb_timer_main)
        

    def end_game(self):
        t = time.time()
        print("starting")
        self.words_all_paths = self.logic.find_all_paths()
        print(f"found {len(self.words_all_paths)} paths {time.time()-t}")
        self.graphics.listbox_enable(True)
        self.graphics.listbox_words_clear()
        for word in self.words_all_paths:
            self.graphics.listbox_words_add(word, auto_enable=False, mark_as_found=(word in self.words_found_paths))
        print(f"added everything {time.time()-t}")
    
    def cb_reset(self):
        # self.start_new_game()
        self.end_game()

    def cb_word_selected(self, selection):
        if(len(selection) != 1): return
        index = selection[0]
        word = self.graphics.listbox_words_found.get(index)
        paths = self.words_all_paths[word]
        self.graphics.set_input_from_path(paths[0])
        self.graphics.set_input_background(0 if (word in self.words_found_paths) else None)
        self.graphics.paths_delete_all() 
        self.draw_paths(paths)

    def cb_path_dragged(self, current_cell):
        if(not self.check_next_cell_valid(current_cell)):
            return
        self.current_path.append(current_cell)
        self.graphics.set_input_from_path(self.current_path)
        if(len(self.current_path) == 1): #this is the first cell selected
            self.cb_path_clear() #clear previous path selection
            #cancel timer which was suppose to delete the paths:
            if(self.after_id_delete_path is not None):
                self.graphics.after_cancel(self.after_id_delete_path)
        else:
            self.graphics.audio_play_sound()
            self.graphics.paths_add(self.current_path[-2], self.current_path[-1], 0)
            self.graphics.draw_paths()
    
    def cb_path_released(self):
        if(self.current_path != []): self.path_submitted(self.current_path)
        #start a timer to delete the paths:
        self.after_id_delete_path = self.graphics.after(1000, self.cb_path_clear)
        self.current_path = []
    
    def cb_path_clear(self):
        self.graphics.paths_delete_all() 
        self.graphics.set_input_from_path([])
        self.graphics.set_input_background(None)
        self.graphics.draw_paths()

    def draw_paths(self, paths):
        self.graphics.paths_delete_all()
        for i, path in enumerate(paths): #can be limited here to 9 paths with paths[:9]
            for cell_1, cell_2 in zip(path[:-1], path[1:]):
                self.graphics.paths_add(cell_1, cell_2, i)
        self.graphics.draw_paths()
    
    def update_score(self):
        self.graphics.set_score(f"Score: {self.score}")
    
    def update_time(self):
        seconds = self.time_game_duration - (self.time_now - self.time_start_of_game)
        minutes = int(seconds // 60)
        seconds %= 60
        self.graphics.set_time(f"Time Left: {minutes:02d}:{seconds:04.1f}")

    