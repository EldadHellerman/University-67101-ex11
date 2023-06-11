#################################################################
# FILE : boggle.py
#################################################################
#https://prod.liveshare.vsengsaas.visualstudio.com/join?94A6EC3EB4731E7321EA50F0AD9212A046A6


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