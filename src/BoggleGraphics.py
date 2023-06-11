import tkinter as tk

class BoggleGraphics:
    
    def __init__(self):
        root = tk.Tk()
        root.geometry("500x500")
        root.title("Boggle")
        
        root.focus_set()
        root.bind("<Escape>", lambda e: e.widget.quit())

        frame = tk.Frame(root, background="green", borderwidth=20)
        frame.pack()
        
        leftframe = tk.Frame(root, background="purple")
        leftframe.pack(side=tk.LEFT)

        self.label = tk.Label(frame, text = "Hello world")
        self.label.pack()
        self.counter = 0

        button1 = tk.Button(leftframe, text = "left_frame_1", command = self.button_1_pressed)
        button1.pack(padx = 3, pady = 3)
        button1.configure()
        root.mainloop()

    def button_1_pressed(self):
        self.counter += 1
        self.label.config(text= f"I was clicked {self.counter} times")
    

    def set_time(self, updated_time):
        self.time = updated_time
        pass


    def set_score(self, score_value=0):
        self.score += score_value
        pass
        
    def set_words(self, words_list: list):
        self.words = words_list
        pass
        
    def reset_or_startover(str):
        
        if str == "reset":
            return True
        elif str == "startover":
            return False
        pass

    # def set_reset_or_start
    
    def draw():
        pass

if __name__ == "__main__":
    ksdjvnjs = BoggleGraphics()