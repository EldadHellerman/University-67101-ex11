#################################################################
# FILE : BoggleGraphicsTheme.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex10 2023
# DESCRIPTION: A class that is used as a boggle game theme.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

class BoggleGraphicsTheme:
    """
    Boggle graphics stores all the parameters needed to fully configure a Boggle Game look.
    """        
    def __init__(self, **theme_args):
        """
        Initiate a new BoggleGraphicsTheme. Custome theme settings can be passed in as dictionary.
        Options (key: value):
            font_labels: tuple(font_name: str, font_size: int)
            font_buttons: tuple(font_name: str, font_size: int)
            font_input: tuple(font_name: str, font_size: int)
            font_words_found: tuple(font_name: str, font_size: int)
            font_click_to_start: tuple(font_name: str, font_size: int)
            color_bg: "#RRGGBB"
            color_bg_canvas: "#RRGGBB"
            color_bg_selected: "#RRGGBB"
            color_text: "#RRGGBB"
            color_input: "#RRGGBB"
            color_cube: "#RRGGBB"
            color_cube_edges: "#RRGGBB"
            color_cube_text: "#RRGGBB"
            color_text_click_to_start: "#RRGGBB"
            color_word_found: "#RRGGBB"
            color_word_already_found: "#RRGGBB"
            color_word_not_found: "#RRGGBB"
            colors_path = list["#RRGGBB"]
            paths_offsets_percent = list[tuple(offset_1_x, offset_1_y)]
            path_width = int
            size_board_percent = float
            size_cubes_percent = float
        """        
        #defaults:
        self.font_labels = ("Arial", 20)
        self.font_buttons = ("Arial", 20)
        self.font_input = ("Arial", 30)
        self.font_words_found = ("Arial", 16)
        self.font_click_to_start = ("Arial", 40)
        self.color_bg = "#202020"
        self.color_bg_canvas = "#606060"
        self.color_bg_selected = "#404040"
        self.color_text = "#f0f0f0"
        self.color_input = "#f0f0f0"
        self.color_cube = "#D0D0D0"
        self.color_cube_edges = "#b0b0b0"
        self.color_cube_text = "#000000"
        self.color_text_click_to_start = "#000000"
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