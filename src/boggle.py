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

from BoggleGame import BoggleGame

def main():
    game = BoggleGame()
    game.start()

if __name__ == "__main__":
    main()