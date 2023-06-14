from typing import List, Tuple, Iterable, Optional

# board is of the form [['e','ou'], ['a','d']]
# path is of the form (x, y): [(1,1), (1,2), (2,2)]
Board = List[List[str]]
Cell = Tuple[int, int]
Path = List[Cell]

def path_to_word(board: Board, path: Path) -> str:
    return "".join([board[y][x] for (x, y) in path])

def is_word_in_words(word: str, words: Iterable[str]) -> bool:
    return (word in words)
    
def get_unvisited_neighbors(board: Board, path: Path) -> list[Cell]:
    """
    Finds all unvisited neighbors of the last cell in the path.

    Args:
        board (Board): Board, used to check if cells are out of the board.
        path (Path): Current Path. Cells that are in that path are not returned.

    Returns:
        list[Cell]: Returns a list of all valid neighbors, given x coord and y coord
    """
    width = len(board[0])
    height = len(board)
    x, y = path[-1][0], path[-1][1]
    cells_y = range(y - 1, y + 2)
    cells_x = range(x - 1, x + 2)
    return [(x, y) for y in cells_y for x in cells_x if (0<=y<height) and (0<=x<width) and ((x,y) not in path)]

def find_length_n_paths_recursive(board: Board, words: Iterable[str], path: Path, n: int) -> list[Path]:
    """finds all paths of n length valid words"""

    if len(path) == n:
        return [path] if is_word_in_words(path_to_word(board, path), words) else []
    
    results: list[Path]= []
    for neighbor in get_unvisited_neighbors(board, path): # get the valid neighbors
        results += find_length_n_paths_recursive(board, words, path + [neighbor],  n)
    return results

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]: #################################
    word = path_to_word(path)
    return word if is_word_in_words(word, words) else None

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:#################################
    results: list[Path] = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            results += find_length_n_paths_recursive(board, words, [(x,y)], n)
    return results

def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:#################################
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:#################################
    pass
 

if __name__ == "__main__":
    with open("src/boggle_dict.txt", "r") as f:
        words = f.readlines()
    
    board = [['a','s','d','b'], ['z','e','r','y'], ['t','t','b','j'], ['i','o','p','s']]
    # words = ["sdb", 'aeb']
    r = find_length_n_paths(3, board, words)
    print(r)
    # helper_1(2,[['a','s','d','b'], ['a','e','r','y'], ['t','t','h','j'], ['i','o','p','s']], ["asd", 'aeb'], 0, 0, unvalid_coordinates=[])
    # print(get_neighbors([[a,s,d,d], [a,e,r,y], [t,t,h,j], [i,o,p,s]], 0,1))