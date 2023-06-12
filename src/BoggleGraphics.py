from tkinter import *

class BoggleGraphics:

    def __init__(self): #### TODO finish graphical layout of button and canvas
        font_labels_and_buttons = ("Arial", 20)
        font_words_found = ("Arial", 16)
        theme_bg = "#202020"
        theme_text = "#f0f0f0"
        theme_highlight = "#ff0000"

        root = Tk()
        root.title("Boggle")
        root.geometry("600x600")
        root.minsize(500, 500)
        root.configure(bg=theme_bg)
        root.bind("<Escape>", lambda e: e.widget.quit())
        root.grid_columnconfigure(0, weight=2, minsize=400)
        root.grid_columnconfigure(1, weight=1, minsize=200)
        root.grid_rowconfigure(0, weight=1, minsize=200)
        root.grid_rowconfigure(1, weight=2, minsize=400)

        frame_top = Frame(root, bg="red")
        frame_side = Frame(root, bg="green")
        frame_main = Frame(root, bg="purple")
        frame_top.grid(column=0, row=0, columnspan=2, sticky="nsew")
        frame_side.grid(column=1, row=0, rowspan=2, sticky="nsew")
        frame_main.grid(column=0, row=1, sticky="nsew")

        
        Label(frame_side, text="Words found:", font=font_labels_and_buttons, bg=theme_bg, fg=theme_text).pack(side=TOP, fill=X)
        # scrollbar_word_found = Scrollbar(frame_side, bg=theme_bg)
        # scrollbar_word_found.pack(side = RIGHT, fill = BOTH)
        listbox_words_found = Listbox(frame_side, font=font_words_found, bg=theme_bg, fg=theme_text,
                                      highlightthickness=0, state="disabled", selectmode=SINGLE)
        listbox_words_found.pack(fill=BOTH, expand=True)
        # listbox_words_found.config(yscrollcommand = scrollbar_word_found.set)
        # scrollbar_word_found.config(command = listbox_words_found.yview)
        
        label_time = Label(frame_top, text = "Time:", font=font_labels_and_buttons)
        label_time.pack(side=RIGHT)
        
        label_score = Label(frame_top, text = "Score:", font=font_labels_and_buttons)
        label_score.pack()

        button_reset = Button(frame_top, text = "Reset")
        button_reset.pack(side=LEFT)
        
        button_submit = Button(frame_top, text = "Submit")
        button_submit.pack(side=LEFT)

        label_input = Label(frame_top, text = "input word")
        label_input.pack(side=LEFT)

        canvas = Canvas(frame_main, bg=theme_bg)
        canvas.grid(column=0, row=1, sticky="nsew")

        #export all needed widgets:
        self.label_time = label_time
        self.label_score = label_score
        self.button_reset = button_reset
        self.button_submit = button_submit
        self.label_input = label_input
        self.listbox_words_found = listbox_words_found
        self.canvas = canvas
        self.root = root
    
    def start(self):
        self.root.mainloop()
    
    def display_board(self): ### TODO write
        #display a boggle board on a canvas
        pass

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

    def set_time(self, time: str):
        self.label_time.config(text=time)

    def set_score(self, score: str):
        self.label_score.config(text=score)
    
    def set_input(self, string: str):
        self.label_input.config(text=string)
    
    def set_reset_or_startover(self, reset_or_startover):
        self.button_reset.configure(text = ("Reset" if reset_or_startover else "Startover"))

    def set_guess_text(self, note :str): ##################TODO delete this function
        """_summary_

        Args:
            note (str): _description_
        """     
        """ param: a single note:str """
        self.guess_text = note
        pass
        # אני לא מבין את הכתב שלך ולא מצליח לקרוא את התמונה!! וגם לא זוכר את הפונקציות שלנו
        #😂
        #שים לב לסטנדרט שבו דוקסטרינג לפונקציות נכתב!
        # אבל עדיף להשאיר את זה לסוף
    
    def set_cb_button_reset(self, func):
        self.button_reset.configure(command=func)
    
    def set_cb_button_submit(self, func):
        self.button_submit.configure(command=func)
    
    def set_cb_board(self, func): ##########TODO not finished
        pass
        # another function which translate canvas clicks into coordinants is needed.
        # self.canvas.configure(command=func)
    
    def set_cb_word_selected(self, func):
        self.listbox_words_found.bind("<<ListboxSelect>>", lambda e: func(self.listbox_words_found.curselection()))

if __name__ == "__main__":
    g = BoggleGraphics()
    g.start()