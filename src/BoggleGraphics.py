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
# from PIL import Image, ImageTk

class BoggleGraphics:
    """_summary_
    """
    def __init__(self, theme: BoggleGraphicsTheme):
        """_summary_

        Args:
            theme (BoggleGraphicsTheme): _description_
        """        
        self.audio_init()
        self.path_to_draw: list[Path] = []
        self.board_hidden: bool = False
        self.cb_function_reveal_board: function = None
        self.cb_function_word_selected: function = None
        self.init_graphics(theme)
    
    def init_graphics(self, theme: BoggleGraphicsTheme):
        """_summary_

        Args:
            theme (BoggleGraphicsTheme): _description_
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
        """_
        """        
        self.root.mainloop()
    
    def set_time(self, string: str):
        """_summary_

        Args:
            string (str): _description_
        """        
        self.label_time.config(text=string)

    def set_score(self, string: str):
        """_summary_

        Args:
            string (str): _description_
        """        
        self.label_score.config(text=string)
    
    def set_input_from_path(self, path: Path):
        """_summary_

        Args:
            path (Path): _description_
        """        
        self.label_input.config(text = "".join([self.board[y][x] for (x,y) in path]))
    
    def set_input_background(self, found_already_found_or_not_found: int):
        """_summary_

        Args:
            found_already_found_or_not_found (int): _description_
        """        
        color = self.theme.color_bg
        if(found_already_found_or_not_found == 0):
            color = self.theme.color_word_found
        elif(found_already_found_or_not_found == 1):
            color = self.theme.color_word_already_found
        elif(found_already_found_or_not_found == 2):
            color = self.theme.color_word_not_found
        self.label_input.configure(background=color)
    
    def set_button_endgame_or_reset(self, endgame_or_reset: bool):
        """_summary_

        Args:
            endgame_or_reset (bool): _description_
        """        
        self.button_reset.configure(text = ("End Game" if endgame_or_reset else "Reset"))
    
    def set_board_hidden(self, hidden: bool):
        """_summary_

        Args:
            hidden (bool): _description_
        """        
        self.board_hidden = hidden
    
    def set_board(self, board: Board):
        """_summary_

        Args:
            board (Board): _description_
        """        
        self.board = board

    def set_cb_button_endgame_or_reset(self, func: function):
        """_summary_

        Args:
            func (function): _description_
        """        
        self.button_reset.configure(command=func)
    
    def set_cb_reveal_board(self, func: function):
        """_summary_

        Args:
            func (function): _description_
        """        
        self.cb_function_reveal_board = func

    def set_cb_path_dragged(self, func: function):
        """_summary_

        Args:
            func (function): _description_
        """        
        self.cb_function_path_dragged = func
    
    def set_cb_path_released(self, func: function):
        """_summary_

        Args:
            func (function): _description_
        """        
        self.cb_function_path_released = func
    
    def set_cb_word_selected(self, func: function):
        """_summary_

        Args:
            func (function): _description_
        """        
        self.cb_function_word_selected = func
        self.listbox_words_found.bind("<<ListboxSelect>>", lambda e: func(self.listbox_words_found.curselection()))
    
    def listbox_enable(self, enabled: bool):
        """_summary_

        Args:
            enabled (bool): _description_
        """        
        self.listbox_words_found.configure(state=NORMAL if enabled else DISABLED)
    
    def listbox_words_add(self, string: str, mark_as_found: bool = False, auto_enable: bool = True):
        """_summary_

        Args:
            string (str): _description_
            mark_as_found (bool, optional): _description_. Defaults to False.
            auto_enable (bool, optional): _description_. Defaults to True.
        """        
        color = self.theme.color_word_found if mark_as_found else self.theme.color_bg
        if(auto_enable):
            state = self.listbox_words_found.cget("state")
            self.listbox_enable(True)
        self.listbox_words_found.insert(END, string)
        if(mark_as_found): self.listbox_words_found.itemconfigure(END, background = color)
        if(auto_enable):
            self.listbox_enable(state=="normal")
    
    def listbox_words_clear(self):
        """_summary_
        """            
        state = self.listbox_words_found.cget("state")
        self.listbox_enable(True)
        self.listbox_words_found.delete(0, END)
        self.listbox_enable(state=="normal")
    
    def __cb_keyboard_arrows(self, direction: str):
        """_summary_

        Args:
            direction (str): _description_
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
    
    def audio_init(self):
        """_summary_
        """        
        try:
            mixer.init() #audio
        except NameError:
            pass
    
    def audio_load_sound(self, file: str):
        """_summary_

        Args:
            file (str): _description_
        """        
        try:
            mixer.music.load(file)
        except NameError:
            pass
    
    def audio_play_sound(self):
        """_summary_
        """        
        try:
            if(mixer.music.get_busy()):
                mixer.music.rewind()
            else:
                mixer.music.play()
        except NameError:
            pass

    def __cb_canvas_dragged(self, e: Event[Canvas]):
        """_summary_

        Args:
            e (Event[Canvas]): _description_
        """        
        loc = self.__canvas_position_to_cell(e.x, e.y)
        if(loc is not None and self.cb_function_path_dragged is not None): self.cb_function_path_dragged(loc)
    
    def __cb_canvas_released(self, e: Event[Canvas]):
        """_summary_

        Args:
            e (Event[Canvas]): _description_
        """        
        if(self.cb_function_path_released is not None): self.cb_function_path_released()

    def __cb_canvas_resized(self, e: Event[Canvas]):
        """_summary_

        Args:
            e (Event[Canvas]): _description_
        """        
        #set input label to be the width of the canvas:
        self.label_input.configure(width = self.canvas.winfo_width())
        self.draw_board()

    def __cb_canvas_clicked(self, e: Event[Canvas]):
        """_summary_

        Args:
            e (Event[Canvas]): _description_
        """        
        if(self.board_hidden):
            self.cb_function_reveal_board()

    def __calculate_paddings(self):
        """_summary_
        """        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_amount_x = len(self.board[0])
        self.cell_amount_y = len(self.board)
        self.size_board = int(min(width, height) * self.theme.size_board_percent) #width and height of entire board in pixels

        self.canvas_size_cell_x = int(self.size_board / self.cell_amount_x) #width and height of a cube cell in pixels
        self.canvas_size_cell_y = int(self.size_board / self.cell_amount_y) #width and height of a cube cell in pixels
        
        self.canvas_size_cube = int(min(self.canvas_size_cell_x, self.canvas_size_cell_y) * self.theme.size_cubes_percent) #width and height of a cube inside cell
        self.canvas_padding_board_x = int((width - self.size_board)/2)
        self.canvas_padding_board_y = int((height - self.size_board)/2)
        self.canvas_padding_cube_x = int((self.canvas_size_cell_x - self.canvas_size_cube) / 2)
        self.canvas_padding_cube_y = int((self.canvas_size_cell_y - self.canvas_size_cube) / 2)
    
    def __canvas_position_to_cell(self, x: int, y: int):
        """_summary_

        Args:
            x (int): _description_
            y (int): _description_

        Returns:
            _type_: _description_
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
    
    def __canvas_cell_to_cell_position(self, cell: Cell):
        """_summary_

        Args:
            cell (Cell): _description_

        Returns:
            _type_: _description_
        """        
        #upper left corner (x,y)
        x = self.canvas_padding_board_x + cell[0] * self.canvas_size_cell_x
        y = self.canvas_padding_board_y + cell[1] * self.canvas_size_cell_y
        return (x, y)
    
    def __canvas_cell_to_cube_position(self, cell: Cell):
        """_summary_

        Args:
            cell (Cell): _description_

        Returns:
            _type_: _description_
        """        
        #upper left corner (x,y)
        x, y = self.__canvas_cell_to_cell_position(cell)
        return (x + self.canvas_padding_cube_x, y + self.canvas_padding_cube_y)

    def draw_board(self):
        """_summary_
        """        
        self.__calculate_paddings()
        self.canvas.delete("all")
        # started working on using images:
        # self.image_dice = PhotoImage(file="images/dice.gif", format='gif')
        # self.image_dice = Image.open("images/dice.gif")
        #Resize the Image using resize method
        # self.image_dice.resize((size_cube,size_cube), Image.LANCZOS)
        # self.canvas.create_image(20,20, image = ImageTk.PhotoImage(self.image_dice))
        
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
                    self.canvas.create_text(sx + hw, sy + hw, text=self.board[y][x], font=font_cube, fill=self.theme.color_cube_text, tags=t)
        #drawing "click to start" if board is hidden:
        if(self.board_hidden):
            (sx, sy) = self.__canvas_cell_to_cell_position((0,0))
            (ex, ey) = sx + self.size_board, sy + self.size_board
            self.canvas.create_text((sx + ex)/2, (sy + ey)/2, text="Click to Start!", font=self.theme.font_click_to_start, fill=self.theme.color_text_click_to_start)
        self.draw_paths()
    
    def draw_paths(self):
        """_summary_
        """        
        # drawing paths:
        self.canvas.delete("path")
        w = self.canvas_size_cube
        hw = w / 2
        for (cell_1, cell_2, color, variation) in self.path_to_draw:
            offset = self.theme.paths_offsets_percent[variation]
            ox, oy = hw + hw * offset[0], hw + hw * offset[1]
            sx, sy = self.__canvas_cell_to_cube_position(cell_1)
            ex, ey = self.__canvas_cell_to_cube_position(cell_2)
            self.canvas.create_line(sx + ox, sy + oy, ex + ox, ey + oy, width=self.theme.path_width, fill=color, arrow="last", tag="path")

    def after(self, ms: int, func: function) -> str:
        """_summary_

        Args:
            ms (int): _description_
            func (function): _description_

        Returns:
            str: _description_
        """        
        return self.root.after(ms, func)
    
    def after_cancel(self, id: str):
        """_summary_

        Args:
            id (str): _description_
        """        
        self.root.after_cancel(id)
    
    def paths_add(self, cell_1: Cell, cell_2: Cell, variation: int=0):
        """_summary_

        Args:
            cell_1 (Cell): _description_
            cell_2 (Cell): _description_
            variation (int, optional): _description_. Defaults to 0.
        """        
        if(variation >= len(self.theme.paths_offsets_percent)): variation = 0
        color = self.theme.colors_path[variation]
        self.path_to_draw.append((cell_1, cell_2, color, variation))
    
    def paths_delete_all(self):
        """_summary_
        """        
        self.path_to_draw = []
