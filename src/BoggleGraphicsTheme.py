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
            self.font_words_found = ("Arial", 16)
            self.color_bg = "#202020"
            self.color_bg_canvas = "#606060"
            self.color_bg_selected = "#404040"
            self.color_text = "#f0f0f0"
            self.color_cube = "#D0D0D0"
            self.color_cube_edges = "#b0b0b0"
            self.color_cube_text = "#000000"
            self.color_word_found = "#008800"
            self.color_word_already_found = "#d0a020"
            self.color_word_not_found = "#880000"
            self.color_path = "#ff0000"
            self.path_width = 3
            #get used set values:
            self.__dict__.update(theme_args)