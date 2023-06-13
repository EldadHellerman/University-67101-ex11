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
# from PIL import Image, ImageTk

SIZE_BOARD_PERCENT = 0.8 #percent of min(width,height) the board is at
SIZE_CUBES_PERCENT = 0.8 #percent of cube in remainging size

class BoggleGraphics:

    def __init__(self):
        self.cb_function_board = None
        self.cb_function_timer = None

        font_labels_and_buttons = ("Arial", 20)
        font_words_found = ("Arial", 16)
        theme_bg = "#202020"
        theme_bg_main = "#606060"
        theme_bg_selected = "#404040"
        theme_text = "#f0f0f0"
        theme_highlight = "#ff0000"
        theme_cube_color = "#D0D0D0"
        theme_cube_color_edges = "#b0b0b0"
        label_settings = {"font": font_labels_and_buttons, "bg": theme_bg, "fg": theme_text}

        root = Tk()
        root.title("Boggle")
        root.geometry("600x600")
        root.minsize(600, 600)
        root.configure(bg=theme_bg)
        root.bind("<Escape>", lambda e: e.widget.quit())
        root.grid_columnconfigure(0, weight=2, minsize=400)
        root.grid_columnconfigure(1, weight=1, minsize=200)
        root.grid_rowconfigure(0, weight=0)
        root.grid_rowconfigure(1, weight=10)

        frame_top = Frame(root, bg=theme_bg)
        frame_side = Frame(root, bg=theme_bg)
        frame_main = Frame(root, bg=theme_bg)
        frame_top.grid(column=0, row=0, columnspan=1, sticky="nsew")
        frame_side.grid(column=1, row=0, rowspan=2, sticky="nsew")
        frame_main.grid(column=0, row=1, sticky="nsew")
        
        frame_top.grid_rowconfigure(0, weight=2)
        frame_top.grid_rowconfigure(1, weight=5)
        frame_top.grid_columnconfigure(0, weight=1)
        frame_top.grid_columnconfigure(1, weight=1)
        frame_top.grid_columnconfigure(2, weight=1)

        Label(frame_side, text="Words found:", **label_settings).pack(side=TOP, fill=X)
        # scrollbar_word_found = Scrollbar(frame_side, bg=theme_bg)
        # scrollbar_word_found.pack(side = RIGHT, fill = BOTH)
        listbox_words_found = Listbox(frame_side, font=font_words_found, bg=theme_bg, fg=theme_text,
                                      activestyle="none", selectbackground= theme_bg_selected, selectmode=SINGLE,
                                      highlightthickness=0, state="disabled")
        listbox_words_found.pack(fill=BOTH, expand=True)
        # listbox_words_found.config(yscrollcommand = scrollbar_word_found.set)
        # scrollbar_word_found.config(command = listbox_words_found.yview)
        

        label_time = Label(frame_top, text = "Time Left: ", **label_settings)
        label_score = Label(frame_top, text = "Score", **label_settings)
        button_reset = Button(frame_top, text = "Reset")
        label_input = Label(frame_top, text = "input word", **label_settings)
        
        label_time.grid(row=0, column=1)
        label_score.grid(row=0, column=2)
        button_reset.grid(row=0, column=0)
        label_input.grid(row=1, column=0, columnspan=3)

        canvas = Canvas(frame_main, bg=theme_bg_main, border=0, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)
        canvas.bind("<Configure>", self.cb_canvas_resized)

        #export all needed widgets:
        self.label_time = label_time
        self.label_score = label_score
        self.button_reset = button_reset
        self.label_input = label_input
        self.listbox_words_found = listbox_words_found
        self.frame_main = frame_main
        self.canvas = canvas
        self.root = root

        self.theme_bg = theme_bg
        self.theme_bg_selected = theme_bg_selected
        self.theme_text = theme_text
        self.theme_highlight = theme_highlight
        self.theme_cube_color = theme_cube_color
        self.theme_cube_color_edges = theme_cube_color_edges

    def start(self):
        self.root.mainloop()
    
    def words_found_enable(self, enabled: bool):
            self.listbox_words_found.configure(state=NORMAL if enabled else DISABLED)
    
    def words_found_add(self, string: str):
            state = self.listbox_words_found.cget("state")
            self.words_found_enable(True)
            self.listbox_words_found.insert(END, string)
            self.words_found_enable(state=="normal")
    
    def words_found_clear(self):
            state = self.listbox_words_found.cget("state")
            self.words_found_enable(True)
            self.listbox_words_found.delete(0, END)
            self.words_found_enable(state=="normal")

    def set_time(self, string: str):
        self.label_time.config(text=string)

    def set_score(self, string: str):
        self.label_score.config(text=string)
    
    def set_input(self, string: str):
        self.label_input.config(text=string)
    
    def set_input_background(self, correct):
        color = self.theme_bg
        if(correct is not None):
            color = "#008800" if correct else "#880000"
        self.label_input.configure(background=color)
    
    def set_reset_or_startover(self, reset_or_startover):
        self.button_reset.configure(text = ("Reset" if reset_or_startover else "Startover"))
    
    def set_selected(self, board: list[list[bool]]):
        self.board = board
        self.draw_board()
    
    def set_board(self, board: list[list[str]]):
        self.board = board
        self.draw_board()

    def set_cb_button_reset(self, func):
        self.button_reset.configure(command=func)
    
    def set_cb_timer(self, delay_ms: int, func):
         self.cb_function_timer = func
         self.cb_function_timer_delay = delay_ms
         self.cb_timer()
    
    def cb_timer(self):
        if(self.cb_function_timer):
            self.cb_function_timer()
            self.root.after(self.cb_function_timer_delay, self.cb_timer)
    
    def set_cb_path_dragged(self, func):
        self.cb_function_path_dragged = func
    
    def set_cb_path_released(self, func):
        self.cb_function_path_released = func
    



    def cb_canvas_dragged(self, e):
        loc = self.canvas_position_to_cell(e.x, e.y)
        if(loc is not None and self.cb_function_path_dragged is not None): self.cb_function_path_dragged(loc)
    
    def cb_canvas_released(self, e):
        if(self.cb_function_path_released is not None): self.cb_function_path_released()

    def cb_canvas_resized(self, e):
        self.calculate_paddings()
        self.draw_board()
    
    def calculate_paddings(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_amount_x = len(self.board[0])
        self.cell_amount_y = len(self.board)
        size_board = int(min(width, height) * SIZE_BOARD_PERCENT) #width and height of entire board in pixels

        self.canvas_size_cell_x = int(size_board / self.cell_amount_x) #width and height of a cube cell in pixels
        self.canvas_size_cell_y = int(size_board / self.cell_amount_y) #width and height of a cube cell in pixels
        
        self.canvas_size_cube = int(min(self.canvas_size_cell_x, self.canvas_size_cell_y) * SIZE_CUBES_PERCENT) #width and height of a cube inside cell
        self.canvas_padding_board_x = int((width - size_board)/2)
        self.canvas_padding_board_y = int((height - size_board)/2)
        self.canvas_padding_cube_x = int((self.canvas_size_cell_x - self.canvas_size_cube) / 2)
        self.canvas_padding_cube_y = int((self.canvas_size_cell_y - self.canvas_size_cube) / 2)
    
    def canvas_position_to_cell(self, x, y):
        w = self.canvas_size_cube
        for cell_y in range(self.cell_amount_y):
            for cell_x in range(self.cell_amount_x):
                (sx, sy) = self.canvas_cell_to_position((cell_x, cell_y))
                ex = sx + w
                ey = sy + w
                if((sx <= x <= ex) and (sy <= y <= ey)): return (cell_x, cell_y)
        return None
    
    def canvas_cell_to_position(self, cell):
        #upper left corner (x,y)
        x = self.canvas_padding_board_x + cell[0] * self.canvas_size_cell_x + self.canvas_padding_cube_x
        y = self.canvas_padding_board_y + cell[1] * self.canvas_size_cell_y + self.canvas_padding_cube_y
        return (x, y)

    def draw_board(self):
        self.canvas.delete("all")
        self.calculate_paddings()
        # started working on using images:
        # self.image_dice = PhotoImage(file="images/dice.gif", format='gif')
        # self.image_dice = Image.open("images/dice.gif")
        #Resize the Image using resize method
        # self.image_dice.resize((size_cube,size_cube), Image.LANCZOS)
        # self.canvas.create_image(20,20, image = ImageTk.PhotoImage(self.image_dice))

        t = "cube"
        w = self.canvas_size_cube
        font_cube = ("Arial", w//3)
        for y in range(self.cell_amount_y):
            for x in range(self.cell_amount_x):
                (sx, sy) = self.canvas_cell_to_position((x,y))
                self.canvas.create_rectangle(sx, sy, sx + w, sy + w, fill=self.theme_cube_color_edges, outline="", tags=t)
                self.canvas.create_oval(sx, sy, sx + w, sy + w, fill=self.theme_cube_color, outline="")
                self.canvas.create_text(sx + w/2, sy + w/2, text=self.board[y][x], font=font_cube, fill="#000000", tags=t)
        self.canvas.tag_bind(t, "<B1-Motion>", self.cb_canvas_dragged)
        self.canvas.tag_bind(t, "<ButtonRelease-1>", self.cb_canvas_released)
    
    def set_cb_word_selected(self, func):
        self.listbox_words_found.bind("<<ListboxSelect>>", lambda e: func(self.listbox_words_found.curselection()))
    
    def after(self, ms, func):
        return self.root.after(ms, func)
    
    def after_cancel(self, id):
        return self.root.after_cancel(id)
    
    def path_draw(self, cell_1, cell_2, color):
        w = self.canvas_size_cube / 2
        sx, sy = self.canvas_cell_to_position(cell_1)
        ex, ey = self.canvas_cell_to_position(cell_2)
        self.canvas.create_line(sx + w, sy + w, ex + w, ey + w, width=3, fill=color, arrow="last", tag="path")
    
    def path_delete_all(self):
        self.canvas.delete("path")



if __name__ == "__main__":
    from BoggleGame import BoggleGame ################removeeeeeeeeeeee just for testing
    game = BoggleGame()
    game.start()