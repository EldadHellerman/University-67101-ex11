#################################################################
# FILE : XXX XXX XXX XXX
# WRITER : Eldad Hellerman , hellerman , 322898552
# EXERCISE : intro2cs2 ex? XXX XXX XXX XXX 2023
# DESCRIPTION: XXX XXX XXX XXX
# STUDENTS I DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES I USED: none.
# NOTES: none.
#################################################################
# https://prod.liveshare.vsengsaas.visualstudio.com/join?09888DA74A84BD18D0986217122F3336C096


from boggle_board_randomizer import randomize_board
from BoggleGraphics import BoggleGraphics


def main():
    graphics= BoggleGraphics()

    board = randomize_board()
    print(board)

    graphics.set_score(10)
    graphics.set_board(board)
    while False:
        pass

if __name__ == "__main__":
    main()