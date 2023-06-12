#################################################################
# FILE : boggle.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex10 2023
# DESCRIPTION: A class that is the backend of a snake game.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

# https://prod.liveshare.vsengsaas.visualstudio.com/join?94A6EC3EB4731E7321EA50F0AD9212A046A6

# https://www.pythonguis.com/faq/pack-place-and-grid-in-tkinter/
# https://www.pythontutorial.net/tkinter/tkinter-grid/


from boggle_board_randomizer import randomize_board
from BoggleGraphics import BoggleGraphics


graphics: BoggleGraphics = None

def main():
    global graphics
    graphics = BoggleGraphics()

    board = randomize_board()
    print(board)
    graphics.set_cb_button_reset(cb_reset)
    graphics.set_cb_button_submit(cb_submit)
    graphics.set_cb_word_selected(cb_word_selected)
    graphics.set_cb_board(cb_board)
    graphics.set_score(10)
    graphics.words_found_add("hello!")
    graphics.words_found_add("hello! snfkj")
    graphics.words_found_add("bye!")
    # graphics.set_board(board)
    graphics.start()

def cb_reset():
    # graphics.words_found_add("byksjdvndksje!")
    graphics.words_found_clear()
    graphics.set_score(0)

def cb_submit():
    graphics.set_input("this is a user input that is submited")
    graphics.set_score(100)
    graphics.words_found_enable(True)

def cb_word_selected(selection):
    if(len(selection) != 1): return
    index = selection[0]
    print("a word was selected!", index)

def cb_board():
    print("board was clicked")


if __name__ == "__main__":
    main()