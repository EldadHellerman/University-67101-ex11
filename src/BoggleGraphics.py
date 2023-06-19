#################################################################
# FILE : BoggleGraphics.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex11 2023
# DESCRIPTION: A class used for the graphics of a boggle game.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

from tkinter import *
from BoggleLogic import Path, Board, Cell
from BoggleGraphicsTheme import BoggleGraphicsTheme
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    from pygame import mixer
except ImportError:
    print("Boggle graphics - audio not available, no module pygame")

class BoggleGraphics:
    """
    Boggle graphics is a GUI for the game boggle, based on TKInter.
    """
    PathSegment = tuple[Cell, Cell, str, int]

    def __init__(self, theme: BoggleGraphicsTheme = BoggleGraphicsTheme()):
        """Initializes a new boggle GUI.

        Args:
            theme (BoggleGraphicsTheme, optional): Theme to use. Defaults to BoggleGraphicsTheme().
        """
        self.audio_init()
        self.path_segments_to_draw: list[self.PathSegment] = []
        self.board_hidden: bool = False
        self.cb_function_reveal_board: function = None
        self.cb_function_word_selected: function = None
        self.__init_graphics(theme)
    
    def __init_graphics(self, theme: BoggleGraphicsTheme):
        """
        Configures everything related to the graphics.

        Args:
            theme (BoggleGraphicsTheme): Theme to use.
        """        
        root = Tk()
        root.title("Boggle")
        root.geometry("600x600")
        root.minsize(600, 600)
        root.configure(bg=theme.color_bg)
        root.bind("<Escape>", lambda e: e.widget.quit())
        root.grid_columnconfigure(0, weight=2, minsize=400)
        root.grid_columnconfigure(1, weight=1, minsize=200)
        root.grid_rowconfigure(0, weight=0)
        root.grid_rowconfigure(1, weight=10)

        frame_top = Frame(root, bg=theme.color_bg)
        frame_side = Frame(root, bg=theme.color_bg)
        frame_main = Frame(root, bg=theme.color_bg)
        frame_top.grid(column=0, row=0, columnspan=1, sticky="nsew")
        frame_side.grid(column=1, row=0, rowspan=2, sticky="nsew")
        frame_main.grid(column=0, row=1, sticky="nsew")
        
        frame_top.grid_rowconfigure(0, weight=2)
        frame_top.grid_rowconfigure(1, weight=5)
        frame_top.grid_columnconfigure(0, weight=1)
        frame_top.grid_columnconfigure(1, weight=1)
        frame_top.grid_columnconfigure(2, weight=1)

        label_settings = {"font": theme.font_labels, "bg": theme.color_bg, "fg": theme.color_text}
        Label(frame_side, text="Words found:", **label_settings).pack(side=TOP, fill=X)
        # scrollbar_word_found = Scrollbar(frame_side, bg=theme_bg)
        # scrollbar_word_found.pack(side = RIGHT, fill = BOTH)
        listbox_words_found = Listbox(frame_side, font=theme.font_words_found, bg=theme.color_bg, fg=theme.color_text,
                                      activestyle="none", selectbackground= theme.color_bg_selected, selectmode=SINGLE,
                                      highlightthickness=0, state="disabled")
        listbox_words_found.pack(fill=BOTH, expand=True)
        # listbox_words_found.config(yscrollcommand = scrollbar_word_found.set)
        # scrollbar_word_found.config(command = listbox_words_found.yview)
        root.bind("<Up>", lambda e: self.__cb_keyboard_arrows("up"))
        root.bind("<Down>", lambda e: self.__cb_keyboard_arrows("down"))

        label_time = Label(frame_top, text = "Time Left: ", **label_settings)
        label_score = Label(frame_top, text = "Score", **label_settings)
        button_reset = Button(frame_top, text = "Reset")
        label_input = Label(frame_top, text = "", font=theme.font_input, bg=theme.color_bg, fg=theme.color_input)
        
        
        label_time.grid(row=0, column=1, sticky="w")
        label_score.grid(row=0, column=2, sticky="w")
        button_reset.grid(row=0, column=0)
        label_input.grid(row=1, column=0, columnspan=3, sticky="we")

        canvas = Canvas(frame_main, bg=theme.color_bg_canvas, border=0, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)
        canvas.bind("<Configure>", self.__cb_canvas_resized)
        canvas.bind("<B1-Motion>", self.__cb_canvas_dragged)
        canvas.bind("<Button-1>", self.__cb_canvas_clicked)
        canvas.bind("<ButtonRelease-1>", self.__cb_canvas_released)
        
        #export all needed widgets:
        self.theme = theme
        self.label_time = label_time
        self.label_score = label_score
        self.button_reset = button_reset
        self.label_input = label_input
        self.listbox_words_found = listbox_words_found
        self.canvas = canvas
        self.root = root

    def start(self):
        """
        Start the graphics with TKInter's mainloop.
        """
        self.root.mainloop()
    
    def set_time(self, string: str):
        """
        Sets the time label to the given string.

        Args:
            string (str): The desired string.
        """
        self.label_time.config(text=string)

    def set_score(self, string: str):
        """
        Sets the score label to the given string.
        
        Args:
            string (str): The desired string.
        """
        self.label_score.config(text=string)
    
    def set_input_from_path(self, path: Path):
        """
        Sets the input label to the word created from the given path.

        Args:
            path (Path): the desired path.
        """
        self.label_input.config(text = "".join([self.board[y][x] for (x,y) in path]))
    
    INPUT_BACKGROUND_REGULAR = 0
    INPUT_BACKGROUND_VALID = 1
    INPUT_BACKGROUND_INVALID = 2
    INPUT_BACKGROUND_ALREADY_FOUND = 3

    def set_input_background(self, input_background: int):
        """
        Sets input label background.
        Used to indicate to the user if his word is valid, or maybe already found.

        Args:
            input_background (int): Desired input background, one of:
            INPUT_BACKGROUND_VALID, INPUT_BACKGROUND_ALREADY_FOUND, INPUT_BACKGROUND_INVALID, or INPUT_BACKGROUND_REGULAR.
        """
        color = self.theme.color_bg
        if(input_background == self.INPUT_BACKGROUND_VALID):
            color = self.theme.color_word_valid
        elif(input_background == self.INPUT_BACKGROUND_ALREADY_FOUND):
            color = self.theme.color_word_already_found
        elif(input_background == self.INPUT_BACKGROUND_INVALID):
            color = self.theme.color_word_invalid
        self.label_input.configure(background=color)
    
    def set_button_endgame_or_reset(self, endgame_or_reset: bool):
        """
        Selects if reset button is showing 'Endgame' or 'Reset'.

        Args:
            endgame_or_reset (bool): True for endgame, false for reset.
        """
        self.button_reset.configure(text = ("End Game" if endgame_or_reset else "Reset"))
    
    def set_board_hidden(self, hidden: bool):
        """
        Selects if the board is hidden or not.
        A hidden board is used to hide the board from the user until he wants to start to play,
        then the countdown timer starts.

        Args:
            hidden (bool): True to hide the board.
        """
        self.board_hidden = hidden
    
    def set_board(self, board: Board):
        """
        Sets the game board.

        Args:
            board (Board): Board to use for this game.
        """        
        self.board = board

    def set_cb_button_endgame_or_reset(self, func: callable):
        """
        Sets the callback function for when reset button is clicked.

        Args:
            func (callable): Callback function to use.
        """
        self.button_reset.configure(command=func)
    
    def set_cb_reveal_board(self, func: callable):
        """
        Sets the callback function for when the user wants to un-hide the board.

        Args:
            func (callable): Callback function to use.
        """
        self.cb_function_reveal_board = func

    def set_cb_path_dragged(self, func: callable):
        """
        Sets the callback function for when the user drags a path.

        Args:
            func (callable): Callback function to use.
            The function should recive a Cell argument for the current cell the drag is on.
        """
        self.cb_function_path_dragged = func
    
    def set_cb_path_released(self, func: callable):
        """
        Sets the callback function for when the user releases the drag.

        Args:
            func (callable): Callback function to use.
        """
        self.cb_function_path_released = func
    
    def set_cb_word_selected(self, func: callable):
        """
        Sets the callback function for when the user selects a word from the words found listbox.

        Args:
            func (callable): Callback function to use.
        """
        self.cb_function_word_selected = func
        self.listbox_words_found.bind("<<ListboxSelect>>", lambda e: func(self.listbox_words_found.curselection()))
    
    def listbox_enable(self, enabled: bool):
        """
        Selects if the words found listbox is enabled or not.
        When the listbox is enable, words can be selected and select event will be generated.

        Args:
            enabled (bool): True to enable selecting words.
        """
        self.listbox_words_found.configure(state=NORMAL if enabled else DISABLED)
    
    def listbox_words_add(self, string: str, mark_as_found: bool = False, auto_enable: bool = True):
        """
        Adds a word to the wordsfound listbox.
        The listbox needs to be enabled in order to add elements to it, or auto enable can be used.
        Autoenable is used to enable the listbox if it's not enabled so that the word will be inserted
        successfully, then return it back to it's original state.

        Args:
            string (str): Word to add.
            mark_as_found (bool, optional): True to mark as a word that was found. Defaults to False.
            auto_enable (bool, optional): True to enable Autoenable. Defaults to True.
        """        
        color = self.theme.color_word_valid if mark_as_found else self.theme.color_bg
        if(auto_enable):
            state = self.listbox_words_found.cget("state")
            self.listbox_enable(True)
        self.listbox_words_found.insert(END, string)
        if(mark_as_found): self.listbox_words_found.itemconfigure(END, background = color)
        if(auto_enable):
            self.listbox_enable(state=="normal")
    
    def listbox_words_clear(self):
        """
        Clears all words in the words found listbox. Listbox state remains unchanged.
        """            
        state = self.listbox_words_found.cget("state")
        self.listbox_enable(True)
        self.listbox_words_found.delete(0, END)
        self.listbox_enable(state=="normal")
    
    def audio_init(self):
        """
        Initiates the audio mixer.
        Handles the error if pygame module is not found.
        """
        try:
            mixer.init() #audio
        except NameError:
            pass
    
    def audio_load_sound(self, file: str):
        """
        Loads an audio file to the audio mixer.
        Handles the error if pygame module is not found.

        Args:
            file (str): Audio file path.
        """        
        try:
            mixer.music.load(file)
        except NameError:
            pass
    
    def audio_play_sound(self):
        """
        Plays the sound loaded to the audio mixer.
        If the sound is currently playing, it rewinds it to the start.
        Handles the error if pygame module is not found.
        """
        try:
            if(mixer.music.get_busy()):
                mixer.music.rewind()
            else:
                mixer.music.play()
        except NameError:
            pass

    def __cb_keyboard_arrows(self, direction: str):
        """
        Callback function for when keyboard arrows are clicked.
        If the words found list is enabled, this will be used to select words and move between them.

        Args:
            direction (str): Direction of arrow - 'up' or 'down'.
        """
        lb = self.listbox_words_found
        if(lb.cget("state") != "normal"): return
        if(len(lb.curselection()) < 1):
            selection = 0
            if(direction == "up"): new_selection = lb.size()-1
            elif(direction == "down"):  new_selection = 0
        else:
            selection = lb.curselection()[0]
            new_selection = selection
            if(direction == "up" and selection > 0): new_selection -= 1
            elif(direction == "down" and selection < lb.size()-1):  new_selection += 1
        lb.selection_clear(selection)
        lb.selection_set(new_selection)
        lb.see(new_selection)
        if self.cb_function_word_selected is not None:
            self.cb_function_word_selected((new_selection, ))
    
    def __cb_canvas_dragged(self, e: Event):
        """
        Callback function for when canvas is dragged.
        Used to trigger path dragged events.

        Args:
            e (Event): Mouse drag event.
        """
        loc = self.__canvas_position_to_cell(e.x, e.y)
        if(loc is not None and self.cb_function_path_dragged is not None): self.cb_function_path_dragged(loc)
    
    def __cb_canvas_released(self, e: Event):
        """
        Callback function for when the canvas is released.
        Used to trigger path released events.
        Args:
            e (Event): Mouse release event.
        """
        if(self.cb_function_path_released is not None): self.cb_function_path_released()

    def __cb_canvas_resized(self, e: Event):
        """
        Callback function for when canvas is resized.
        Used to trigger redrawing of the board to fit correctly to the new dimensions.
        Also, input label width is set to match that if the canvas.

        Args:
            e (Event): Canvas resized event.
        """
        #set input label to be the width of the canvas:
        self.label_input.configure(width = self.canvas.winfo_width())
        self.draw_board()

    def __cb_canvas_clicked(self, e: Event):
        """
        Callback function for when the canvas is clicked.
        Used to trigger reveal board events.
        Args:
            e (Event): Mouse clicked event.
        """
        if(self.board_hidden):
            self.cb_function_reveal_board()

    def __calculate_paddings(self):
        """
        Calculates all the size and paddings related to drawing a board, based on the current canvas size and the theme.
        The board is padded and centered inside the canvas, and is divided to a grid of cells, with no padding between them.
        Each cell contains a cube that is padded and centered inside it.
        """        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_amount_x = len(self.board[0])
        self.cell_amount_y = len(self.board)
        # width and height of entire board in pixels:
        self.size_board = int(min(width, height) * self.theme.size_board_percent)

        self.canvas_size_cell_x = int(self.size_board / self.cell_amount_x) #width and height of a cube cell in pixels
        self.canvas_size_cell_y = int(self.size_board / self.cell_amount_y) #width and height of a cube cell in pixels
        
        # width and height of a cube inside cell:
        self.canvas_size_cube = int(min(self.canvas_size_cell_x, self.canvas_size_cell_y) * self.theme.size_cubes_percent)
        self.canvas_padding_board_x = int((width - self.size_board)/2)
        self.canvas_padding_board_y = int((height - self.size_board)/2)
        self.canvas_padding_cube_x = int((self.canvas_size_cell_x - self.canvas_size_cube) / 2)
        self.canvas_padding_cube_y = int((self.canvas_size_cell_y - self.canvas_size_cube) / 2)
    
    def __canvas_position_to_cell(self, x: int, y: int) -> Cell | None:
        """
        Finds the cell that contains the pixel coordinates (x, y).

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            Cell | None: Cell that contains these coordinates, or None if there isn't any.
        """        
        w = self.canvas_size_cube
        for cell_y in range(self.cell_amount_y):
            for cell_x in range(self.cell_amount_x):
                (sx, sy) = self.__canvas_cell_to_cube_position((cell_x, cell_y))
                ex = sx + w
                ey = sy + w
                if not (sy <= y <= ey): break
                if not (sx <= x <= ex): continue
                return (cell_x, cell_y)
        return None
    
    def __canvas_cell_to_cell_position(self, cell: Cell) -> tuple[int]:
        """
        Calculates a cell upper left corner coordinates in pixels.

        Args:
            cell (Cell): Desired cell.

        Returns:
            tuple[int]: (x, y) pixel coordinates of the upper left corner of that cell.
        """
        #upper left corner (x,y)
        x = self.canvas_padding_board_x + cell[0] * self.canvas_size_cell_x
        y = self.canvas_padding_board_y + cell[1] * self.canvas_size_cell_y
        return (x, y)
    
    def __canvas_cell_to_cube_position(self, cell: Cell) -> tuple[int]:
        """
        Calculates a cube upper left corner coordinates in pixels.

        Args:
            cell (Cell): Desired cell.

        Returns:
            tuple[int]: (x, y) pixel coordinates of the upper left corner of that cell.
        """
        x, y = self.__canvas_cell_to_cell_position(cell)
        return (x + self.canvas_padding_cube_x, y + self.canvas_padding_cube_y)

    def draw_board(self):
        """
        Draws the board on the canvas.
        
        If the board is hidden, the letters are not shown and instead a 'click to start' test is shown.
        """
        self.__calculate_paddings()
        self.canvas.delete("all")
        
        #drawing cubes:
        t = "cube"
        w = self.canvas_size_cube
        hw = w / 2
        font_cube = ("Arial", w//3)
        for y in range(self.cell_amount_y):
            for x in range(self.cell_amount_x):
                (sx, sy) = self.__canvas_cell_to_cube_position((x,y))
                self.canvas.create_rectangle(sx, sy, sx + w, sy + w, fill=self.theme.color_cube_edges, outline="", tags=t)
                self.canvas.create_oval(sx, sy, sx + w, sy + w, fill=self.theme.color_cube, outline="")
                if(not self.board_hidden):
                    self.canvas.create_text(sx + hw, sy + hw, text=self.board[y][x],
                                            font=font_cube, fill=self.theme.color_cube_text, tags=t)
        #drawing "click to start" if board is hidden:
        if(self.board_hidden):
            (sx, sy) = self.__canvas_cell_to_cell_position((0,0))
            (ex, ey) = sx + self.size_board, sy + self.size_board
            self.canvas.create_text((sx + ex)/2, (sy + ey)/2, text="Click to Start!",
                                    font=self.theme.font_click_to_start, fill=self.theme.color_text_click_to_start)
        self.draw_paths()
    
    def draw_paths(self):
        """
        Draws all paths on the canvas.
        """
        self.canvas.delete("path")
        w = self.canvas_size_cube
        hw = w / 2
        for (cell_1, cell_2, color, variation) in self.path_segments_to_draw:
            offset = self.theme.paths_offsets_percent[variation]
            ox, oy = hw + hw * offset[0], hw + hw * offset[1]
            sx, sy = self.__canvas_cell_to_cube_position(cell_1)
            ex, ey = self.__canvas_cell_to_cube_position(cell_2)
            self.canvas.create_line(sx + ox, sy + oy, ex + ox, ey + oy,
                                    width=self.theme.path_width, fill=color, arrow="last", tag="path")

    def after(self, ms: int, func: callable) -> str:
        """
        Calls TKInter .after() on the root element.
        This does the following:

        Call function once after given time.

        Args:
            ms (int): Delay time in milliseconds.
            func (callable): Function to call.

        Returns:
            str: Identifier to cancel scheduling with after_cancel.
        """
        return self.root.after(ms, func)
    
    def after_cancel(self, id: str):
        """
        Calls TKInter .after_cancel() on the root element.
        This does the following:

        Cancel scheduling of function identified with ID.
    
        Args:
            id (str): Identifier returned by after or after_idle must be given as first parameter.
        """
        self.root.after_cancel(id)
    
    def path_segments_add(self, cell_1: Cell, cell_2: Cell, variation: int=0):
        """
        Adds a path segment to the list of paths segments to draw.
        Variation is the variation index in the theme, used to get a different offset and color for that segment.

        Args:
            cell_1 (Cell): Starting cell.
            cell_2 (Cell): Ending cell.
            variation (int, optional): Variation number. Defaults to 0.
        """        
        if(variation >= len(self.theme.paths_offsets_percent)): variation = 0
        color = self.theme.colors_path[variation]
        self.path_segments_to_draw.append((cell_1, cell_2, color, variation))
    
    def path_segments_delete_all(self):
        """
        Deletes all path segments.
        """        
        self.path_segments_to_draw = []
