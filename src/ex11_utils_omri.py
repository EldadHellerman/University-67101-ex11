from typing import List, Tuple, Iterable, Optional

# board is of the form [['e','ou'], ['a','d']]
# path is of the form (x, y): [(1,1), (1,2), (2,2)]
Board = List[List[str]]
Cell = Tuple[int, int]
Path = List[Cell]

def path_to_word(board: Board, path: Path) -> str:
    return "".join([board[y][x] for (x, y) in path])

def is_word_in_words(word: str, words: Iterable[str]) -> bool:
    # return (word in words)
    return binary_search_word(words, word)
    
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
    word = path_to_word(board, path)
    if not binary_search_word_valid_start(words, word):
        return []
    if len(path) == n:
        return [path] if is_word_in_words(word, words) else []
    
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




def get_words_from_file():
    with open("src/boggle_dict.txt", "r") as f:
        return f.read().strip().split('\n')

def binary_search_word_valid_start(words, word):
    def binary_search_rec(lower, upper):
        if(lower > upper): return False
        mid = (lower + upper) // 2
        pivot = words[mid]
        if(pivot.startswith(word)): return True
        elif(word < pivot): return binary_search_rec(lower, mid-1)
        elif(word > pivot): return binary_search_rec(mid+1, upper)
    return binary_search_rec(0, len(words)-1)

def binary_search_word(words, word):
    def binary_search_rec(lower, upper):
        if(lower > upper): return False
        mid = (lower + upper) // 2
        pivot = words[mid]
        if(word == pivot): return True
        elif(word < pivot): return binary_search_rec(lower, mid-1)
        elif(word > pivot): return binary_search_rec(mid+1, upper)
    return binary_search_rec(0, len(words)-1)

if __name__ == "__main__":
    board = [['a','s','d','b'], ['z','e','r','y'], ['t','t','b','j'], ['i','o','p','s']]
    # words = ["sdb", 'aeb']
    import time
    print("reading dict:", end="    ")
    t = time.time()
    words = get_words_from_file()
    print(f"took {time.time()-t}")
    import random
    random.shuffle(words)
    print("sorting dict:", end="    ")
    t = time.time()
    words.sort()
    # words = sorted(words)
    print(f"took {time.time()-t}")
    
    # r = find_length_n_paths(3, board, words)
    # print(r)
    
    print("check word in dict:", end="    ")
    t = time.time()
    for i in range(50):
        r = "qnvidod" in words
    print(f"took {time.time()-t}")
    
    print("check word in dict:", end="    ")
    t = time.time()
    results = []
    for w in words:
        r = binary_search_word(words, w)
        results.append(r)
    print(f"took {time.time()-t}")
    print(f"result is {sum(results)}")

    # helper_1(2,[['a','s','d','b'], ['a','e','r','y'], ['t','t','h','j'], ['i','o','p','s']], ["asd", 'aeb'], 0, 0, unvalid_coordinates=[])
    # print(get_neighbors([[a,s,d,d], [a,e,r,y], [t,t,h,j], [i,o,p,s]], 0,1))