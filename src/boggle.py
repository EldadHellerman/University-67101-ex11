#################################################################
# FILE : boggle.py
#################################################################
#https://prod.liveshare.vsengsaas.visualstudio.com/join?94A6EC3EB4731E7321EA50F0AD9212A046A6


from boggle_board_randomizer import randomize_board
from BoggleGraphics import BoggleGraphics


graphics = None

def main():
    global graphics
    graphics = BoggleGraphics()

    board = randomize_board()
    print(board)
    graphics.set_button_reset_or_startover_clicked_function(cli)
    graphics.set_score(10)
    # graphics.set_board(board)
    graphics.start()

def cli():
    print("resdgsdfg")
    graphics.set_score(0)

if __name__ == "__main__":
    main()