import tkinter as tk

class BoggleGraphics:
        
    def button_1_pressed(self):
        print("hello world!")
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Boggle")
        
        self.root.focus_set()
        self.root.bind("<Escape>", lambda e: e.widget.quit())
        self.root.bind("1", lambda e: self.label.configure(text="isdugihdbgjhd"))

        frame = tk.Frame(self.root, background="green", borderwidth=20)
        frame.pack()
        
        leftframe = tk.Frame(self.root, background="purple")
        leftframe.pack(side=tk.LEFT)

        # self.label = tk.Label(frame, text = "Hello world")
        # self.label.pack()
        self.counter = 0
        self.label_score = tk.Label(frame, text = "Hello world")
        self.label_score.pack()

        self.button_reset_or_startover = tk.Button(leftframe, text = "left_frame_1", command = self.button_1_pressed)
        self.button_reset_or_startover.pack(padx = 3, pady = 3)
    
    def start(self):
        self.root.mainloop()

    def button_1_pressed(self):
        self.counter += 1
        self.label.config(text= f"I was clicked {self.counter} times")
    

    def set_time(self, updated_time):
        self.time = updated_time
        pass


    def set_score(self, score_value: int):
        self.label_score.config(text= str(score_value))
        
    def set_words(self, words_list: list):
        self.words = words_list
        pass
        
    def set_reset_or_startover(self, reset_or_startover):
        self.button_reset_or_startover.configure(
            text = ("Reset Game" if reset_or_startover else "Startover"))
        
    
    def set_button_reset_or_startover_clicked_function(self, func):
        self.button_reset_or_startover.configure(command=func)

    

    def set_guess_text(note):
        """ param: a single note:str """
        self.guess_text = note
        pass
        # אני לא מבין את הכתב שלך ולא מצליח לקרוא את התמונה!! וגם לא זוכר את הפונקציות שלנו
    
    
    def draw():
        pass

if __name__ == "__main__":
    ksdjvnjs = BoggleGraphics()