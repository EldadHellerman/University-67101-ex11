from typing import List, Tuple, Iterable, Optional

from BoggleLogic import BoggleLogic

Board = List[List[str]]
Path = List[Tuple[int, int]]

def convert_path_switch_xy(path):
    return [(y,x) for x,y in path]

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    path = convert_path_switch_xy(path)
    logic = BoggleLogic()
    logic.set_board(board)
    #check path is valid (non repeating cells or jumps between non-neighboring cells):
    #check first cell seperatly:
    if(len(path) > 0 and not logic.cell_inside_board(path[0])): return None
    for subpath, next_cell in [(path[:i], path[i]) for i in range(1, len(path))]:
        if next_cell not in logic.get_unvisited_neighbors(subpath):
            return None
    #the path itself is vaild, let's check it represents a valid word
    logic.read_words_from_iterable(words)
    word = logic.path_to_word(path)
    return word if (logic.word_in_words(word) == logic.RESULT_YES) else None

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    logic = BoggleLogic()
    logic.set_board(board)
    logic.read_words_from_iterable(words)
    paths = logic.find_paths_of_length(n, True)
    return list(map(lambda path: convert_path_switch_xy(path), paths))

def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    logic = BoggleLogic()
    logic.set_board(board)
    logic.read_words_from_iterable(words)
    paths = logic.find_paths_of_length(n, False)
    return list(map(lambda path: convert_path_switch_xy(path), paths))

def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    logic = BoggleLogic()
    logic.set_board(board)
    logic.read_words_from_iterable(words)
    paths = logic.find_paths_heighest_scoring()
    return list(map(lambda path: convert_path_switch_xy(path), paths))

if __name__ == "__main__":
    board = [['A', 'B', 'C', 'D'],
             ['E', 'F', 'G', 'H'],
             ['I', 'G', 'K', 'L'],
             ['M', 'N', 'O', 'P']]
    words = ('ABC', 'CDH') #, 'ABCD')
    print(max_score_paths(board, words))
    # expected: [[(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 1), (0, 2), (0, 3)]]
    # actual:   [[(0, 0), (0, 1), (0, 2), (0, 3)]]
