from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    created_word = ""
    for _tuple in path:
        row = _tuple[0]
        col = _tuple[1]
        created_word += str(board[row][col])
    if created_word in words:
        return created_word
    return

def get_neighbors(board, i, j):
    """returns a list of all valid neighbors, given x coord and y coord"""
    width = len(board[0])
    length = len(board)
    neighbors_lst = []
    init_i = i - 1
    init_j = j - 1
    for r in range(3):
        for c in range(3):
            if (0 <= init_i + r < length) and (0 <= init_j + c < width):
                neighbors_lst.append((init_i + r, init_j + c))
    self_location = (i, j)
    self_location = [_tuple for _tuple in neighbors_lst if _tuple != self_location] #self_loc out
    return neighbors_lst


def helper_1(n: int, board: Board, words: Iterable[str], row, col, current_word=""):
    """finds all paths of n length valid words"""
    if len(current_word) > n:   # stop if it's an illegal word
        return
    
    coordinate_list = []

    if len(current_word) == n and current_word in words:
        print(coordinate_list) 
    
    neighbors_list = get_neighbors(board, row, col) # get the valid neighbors
    for neighbor in neighbors_list:
        coordinate_list.append(neighbor)
        helper_1(n: int, board: Board, words: Iterable[str], neighbor[0], neighbor[1], current_word += str(board[neighbor[0]][neighbor[1]])) # run on all neighbors
                

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass
 

if __name__ == "__main__":
    print(get_neighbors([[1,2,3,4], [5,4,3,2], [6,7,8,9], [4,3,2,1]], 0,1))