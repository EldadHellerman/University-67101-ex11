#################################################################
# FILE : BoggleGame.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex11 2023
# DESCRIPTION: A class used to manage a boggle game.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

import boggle_board_randomizer as bbr
from BoggleLogic import *
from BoggleGraphics import BoggleGraphics
from BoggleGraphicsTheme import BoggleGraphicsTheme
import time

class BoggleGame:
    """
    Boggle Game is used to manage a game of boggle, handle all the events generated from
    the graphics and controls what exactly the graphics draw.
    """    
    def __init__(self):
        """
        Initializes a Boggle game class.
        Loads the theme, sound, and words dictionary.
        """        
        self.graphics = BoggleGraphics(BoggleGraphicsTheme())
        self.graphics.audio_load_sound("src/pop.mp3")
        self.logic = BoggleLogic()
        self.logic.read_words_from_file("src/boggle_dict.txt")
        self.time_game_duration = 180
        self.time_end_of_game = None
        self.start_new_game()
    
    def start_new_game(self):
        """
        Setup everything for a new game of boggle.
        """        
        self.game_in_progress = False
        self.score = 0
        self.words_found_paths = {} #{word: list[path]}
        self.words_all_paths = {} #{word: list[path]}
        self.current_path = []
        self.timer_delete_path_id = None
        # board = [['a','b']]
        # board = [['a','b'], ['c','d']]
        # board = [['a','b','c','d','e','f'], ['a','b','c','d','e','f']]
        # board = [['a','b','c','d','e','f'] for i in range(6)]
        # board = [['Z' for i in range(4)] for j in range(4)]
        # board = [['Z','Z','Z'], ['A','S','D'],['H','A','F']] #first and last word in dictinoary are ZZZS and AAH
        # bbr.BOARD_SIZE = 50
        # board = bbr.randomize_board(bbr.LETTERS*200)
        board = bbr.randomize_board()
        self.logic.set_board(board)
        self.setup_graphics_for_new_game()
    
    def setup_graphics_for_new_game(self):
        """
        Setups graphics for a new game.
        """        
        self.graphics.set_board_hidden(True)
        self.graphics.set_board(self.logic.board)
        self.graphics.listbox_words_clear()
        self.graphics.listbox_enable(False) #could be set to true, user preference
        self.graphics.set_button_endgame_or_reset(self.game_in_progress)
        self.graphics.set_input_from_path([])
        self.graphics.set_input_background(None)
        self.update_score()
        self.update_time()
        self.graphics.set_cb_button_endgame_or_reset(self.cb_endgame_or_reset)
        self.graphics.set_cb_path_dragged(self.cb_path_dragged)
        self.graphics.set_cb_path_released(self.cb_path_released)
        self.graphics.set_cb_word_selected(self.cb_word_selected)
        self.graphics.set_cb_reveal_board(self.cb_reveal_board)
        self.graphics.paths_delete_all()
        self.graphics.draw_board()
    
    def start(self):
        """
        Start's the graphics.
        """        
        self.graphics.start()
    
    def end_game(self):
        """
        End's a game - reveals all the word there are in the board, marks all the words that were found.
        """        
        self.game_in_progress = False
        self.time_end_of_game = None
        self.update_time()
        self.cb_path_clear()
        self.graphics.set_button_endgame_or_reset(self.game_in_progress)
        self.words_all_paths = self.logic.find_all_paths()
        # self.logic.create_lookup_sets()
        # self.words_all_paths = self.logic.find_all_paths_faster()
        self.graphics.listbox_enable(True)
        self.graphics.listbox_words_clear()
        for word in self.words_all_paths:
            self.graphics.listbox_words_add(word, auto_enable=False, mark_as_found=(word in self.words_found_paths))
    
    def path_submitted(self, path: Path):
        """
        Callback for when a path was submitted.
        Check if the word represented by that path is in the dictionary, or was found before,
        and reacts accordingly.

        Args:
            path (Path): Path submitted.
        """        
        # print(f"path submitted! path is: {path}")
        if len(path) <= 1: #paths can be only starting cell.
            return
        word = self.logic.path_to_word(self.current_path)
        if(word in self.words_found_paths): #word was already found (though maybe on a different path)
            self.graphics.set_input_background(1)
            self.words_found_paths[word] += [path]
            return
        #check if word is in dictionary! (which implies a valid word length)
        if self.logic.word_in_words(word) != self.logic.RESULT_YES:
            self.graphics.set_input_background(2)
            return
        #valid word was found:
        self.graphics.set_input_background(0)
        self.score += self.logic.path_to_score(path)
        self.update_score()
        self.words_found_paths[word] = [path]
        self.graphics.listbox_words_add(word)
    
    def timer_main_start(self):
        """
        Starts maint timer (used to update game countdown timer).
        """        
        self.timer_main_enabled = True
        self.timer_main_id = self.graphics.after(100, self.cb_timer_main)
    
    def timer_main_stop(self):
        """
        Stops maint timer (used to update game countdown timer).
        """        
        self.timer_main_enabled = False
    
    def draw_paths(self, paths: list[Path]):
        """
        Draws several paths, the first 9 with different colors and offsets.

        Args:
            paths (list[Path]): List of paths.
        """        
        self.graphics.paths_delete_all()
        for i, path in enumerate(paths): #can be limited here to 9 paths with paths[:9]
            for cell_1, cell_2 in zip(path[:-1], path[1:]):
                self.graphics.paths_add(cell_1, cell_2, i)
        self.graphics.draw_paths()
    
    def update_score(self):
        """
        Update score in graphics to current score.
        """        
        self.graphics.set_score(f"Score: {self.score}")
    
    def update_time(self):
        """
        Update countdown timer in graphics to current remaining time.
        """        
        seconds = self.time_game_duration if(self.time_end_of_game is None) else self.time_end_of_game - time.time()
        minutes = int(seconds // 60)
        seconds %= 60
        self.graphics.set_time(f"Time Left: {minutes:02d}:{seconds:04.1f}")

    def check_next_cell_valid(self, cell: Cell) -> bool:
        """
        Checks if a cell is a valid next cell for the current path dragged by the user.
        A valid cell is one that is one of the 8 neighbors and is not in the path already.

        Args:
            cell (Cell): Next cell.

        Returns:
            bool: True if a valid option.
        """        
        if(len(self.current_path) == 0): return True
        if(cell in self.current_path): return False #if was already in that cell before
        x1, y1 = cell
        x2, y2 = self.current_path[-1]
        if(max(abs(x1-x2), abs(y1-y2)) > 1): return False #if not one of 8 neighbors
        return True
    
    def cb_path_dragged(self, current_cell: Cell):
        """
        Callback for when a user drags the mouse trying to create a path.
        If the cells the user dragged to is a valid continuation of the current path,
        it adds that cell to the path, and updates the graphics accordingly.

        Args:
            current_cell (Cell): Cell to which the user dragged the mouse.
        """        
        if(not self.game_in_progress): return
        if(not self.check_next_cell_valid(current_cell)): return
        self.current_path.append(current_cell)
        self.graphics.set_input_from_path(self.current_path)
        if(len(self.current_path) == 1): #this is the first cell selected
            self.cb_path_clear() #clear previous path selection
            #cancel timer which was suppose to delete the paths:
            if(self.timer_delete_path_id is not None):
                self.graphics.after_cancel(self.timer_delete_path_id)
        else:
            self.graphics.audio_play_sound()
            self.graphics.paths_add(self.current_path[-2], self.current_path[-1], 0)
            self.graphics.draw_paths()
    
    def cb_path_released(self):
        """
        Callback for when a path is released.
        If a path was built, it submits it to the callback function.
        It also adds a timer to clear the path submitted.
        """        
        if(not self.game_in_progress): return
        if(self.current_path != []): self.path_submitted(self.current_path)
        #start a timer to delete the paths:
        self.timer_delete_path_id = self.graphics.after(1000, self.cb_path_clear)
        self.current_path = []
    
    def cb_path_clear(self):
        """
        Callback for clearing the current path.
        """        
        self.graphics.paths_delete_all() 
        self.graphics.set_input_from_path([])
        self.graphics.set_input_background(None)
        self.graphics.draw_paths()

    def cb_timer_main(self):
        """
        Callback for the main timer, updating time remaining to the end of the game and ending it if reached the end.
        """        
        if(not self.timer_main_enabled or self.time_end_of_game is None): return
        if(time.time() >= self.time_end_of_game): #time is over!
            self.end_game()
        else:
            self.update_time()
            self.timer_main_id = self.graphics.after(100, self.cb_timer_main)
    
    def cb_reveal_board(self):
        """
        Callback for revealing the board when the user wants to begin the new game.
        It reveals the board and starts the countdown timer.
        """
        self.game_in_progress = True
        self.graphics.set_button_endgame_or_reset(self.game_in_progress)
        self.time_end_of_game = time.time() + self.time_game_duration
        self.timer_main_start()
        self.graphics.set_board_hidden(False)
        self.graphics.draw_board()

    def cb_word_selected(self, selection: tuple[int]) -> None:
        """
        Callback for when the user select a word from the words list, in order to show it's path.
        It removes all other paths drawen and draws all the paths of the selected word.

        Args:
            selection (tuple[int]): Selection from TKInter ListBox.cursel()
        """        
        if(len(selection) != 1): return
        index = selection[0]
        word = self.graphics.listbox_words_found.get(index)
        paths = self.words_all_paths[word]
        self.graphics.set_input_from_path(paths[0])
        self.graphics.set_input_background(0 if (word in self.words_found_paths) else None)
        self.graphics.paths_delete_all() 
        self.draw_paths(paths)

    def cb_endgame_or_reset(self):
        """
        Callback for ending or resetting the game.
        If there is a game in progress, it ends it, else, it resets it.
        """        
        if(self.game_in_progress):
            self.end_game()
        else:
            self.start_new_game()