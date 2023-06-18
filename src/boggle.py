#################################################################
# FILE : boggle.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex10 2023
# DESCRIPTION: Main file that starts a boggle game.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

from BoggleGame import BoggleGame

def main():
    """
    Main function. runs a boggle game.
    """    
    game = BoggleGame()
    game.start()

if __name__ == "__main__":
    main()