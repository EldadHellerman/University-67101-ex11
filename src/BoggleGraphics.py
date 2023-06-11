import tkinter as tk

class BoggleGraphics:
        
    def button_1_pressed(self):
        print("hello world!")
    khgbkhgb
    def __init__(self):
        root = tk.Tk()
        root.geometry("500x500")
        root.title("Boggle")
        
        frame = tk.Frame(root, background="green", borderwidth=20)
        frame.pack()
        
        leftframe = tk.Frame(root, background="purple")
        # leftframe.background = "green"
        leftframe.pack(side=tk.LEFT)
        
        rightframe = tk.Frame(root, background = "red")
        rightframe.pack(side=tk.RIGHT)
        

        label = tk.Label(frame, text = "Hello world")
        label.pack()
        
        button1 = tk.Button(leftframe, text = "left_frame_1", command = self.button_1_pressed)
        button1.pack(padx = 3, pady = 3)
        button3 = tk.Button(leftframe, text = "left_frame_2")
        button3.pack(padx = 3, pady = 3)
        
        button2 = tk.Button(rightframe, text = "right_frame_1")
        button2.pack(padx = 3, pady = 3)
        root.mainloop()

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