#################################################################
# FILE : BoggleGraphicsTheme.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex10 2023
# DESCRIPTION: A class that is used as a boggle game theme
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

class BoggleGraphicsTheme:
        def __init__(self, **theme_args):
            #defaults:
            self.font_labels = ("Arial", 20)
            self.font_buttons = ("Arial", 20)
            self.font_input = ("Arial", 30)
            self.font_words_found = ("Arial", 16)
            self.color_bg = "#202020"
            self.color_bg_canvas = "#606060"
            self.color_bg_selected = "#404040"
            self.color_text = "#f0f0f0"
            self.color_input = "#f0f0f0"
            self.color_cube = "#D0D0D0"
            self.color_cube_edges = "#b0b0b0"
            self.color_cube_text = "#000000"
            self.color_word_found = "#008800"
            self.color_word_already_found = "#d0a020"
            self.color_word_not_found = "#880000"
            self.colors_path = ["#ff0000", "#2f4f4f", "#008000", "#ffff00", "#00ffff", "#0000ff", "#1e90ff", "#ff1493", "#ffdead"]
            f = 0.4 #offset percentage
            self.paths_offsets_percent = [(0,0), (-f, f), (f,f), (f,-f), (-f,-f), (0,f), (0,-f), (f,0), (-f,0)]
            self.path_width = 3
            self.size_board_percent = 0.8 #percent of min(width,height) the board is at
            self.size_cubes_percent = 0.8 #percent of cube in remainging size
            #get used set values:
            self.__dict__.update(theme_args)