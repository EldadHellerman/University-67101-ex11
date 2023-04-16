#################################################################
# FILE : XXX XXX XXX XXX
# WRITER : Eldad Hellerman , hellerman , 322898552
# EXERCISE : intro2cs2 ex? XXX XXX XXX XXX 2023
# DESCRIPTION: XXX XXX XXX XXX
# STUDENTS I DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES I USED: none.
# NOTES: none.
#################################################################

import time


tictoc_time = 0


def tic():
    global tictoc_time
    tictoc_time = time.time()


def toc(comment=""):
    global tictoc_time
    end = time.time()
    print(comment+" took:", end-tictoc_time, "seconds")
    
if __name__ == "__main__":
    pass

