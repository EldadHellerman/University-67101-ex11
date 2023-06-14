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


def path_to_word(board, path):
    word = ""
    for _tuple in path:
        row = _tuple[0]
        col = _tuple[1]
        word += board[row][col]
    return word

def helper_1(n:int, board: Board, words: Iterable[str], path: list[tuple], all_paths=[]):
    """finds all paths of n length valid words"""
    if len(path) == n:
        if path_to_word in words:
            all_paths.append(path)
        return
    last_tuple = path[-1]

    neighbors_list = get_neighbors(board, last_tuple[0], last_tuple[1] ) # get the valid neighbors

    for _tuple in neighbors_list:
        if _tuple in path:
            neighbors_list.remove(_tuple)   # valid neighbors with no visited cells!
    
    if neighbors_list != []:
        for neighbor in neighbors_list: # go over all neighbors
            path.append(neighbor)
            helper_1(n, board, words, path, all_paths)

    

# def helper_1(n: int, board: Board, words: Iterable[str], path: list[tuple]):
#     """finds all paths of n length valid words"""
#     print("row is", row, "col is", col)
#     print("the Current is", current_word)
#     unvalid_coordinates.append((row, col))

#     if len(current_word) > n:   # stop if it's an illegal word
#         return
    
#     path_list = []

#     if len() == n and current_word in words:
#         print("THE ASWER IS:", path_list) 
    
#     neighbors_list = get_neighbors(board, row, col) # get the valid neighbors
#     for neighbor in neighbors_list:
#         if neighbor not in unvalid_coordinates:
#             path_list.append(neighbor)
#             print(path_list)
#             added_letters = board[neighbor[0]][neighbor[1]]
#             print(added_letters)
#             helper_1(n, board, words, neighbor[0], neighbor[1], current_word += added_letters, unvalid_coordinates)

                

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    for row in range(len(board)):
        for col in range(len(board[0])):
            helper_1(n, board, words,[(row,col)])
    pass


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass
 

if __name__ == "__main__":
    find_length_n_paths(2,[['a','s','d','b'], ['a','e','r','y'], ['t','t','h','j'], ['i','o','p','s']], ["sdb", 'aeb'])
    # helper_1(2,[['a','s','d','b'], ['a','e','r','y'], ['t','t','h','j'], ['i','o','p','s']], ["asd", 'aeb'], 0, 0, unvalid_coordinates=[])
    # print(get_neighbors([[a,s,d,d], [a,e,r,y], [t,t,h,j], [i,o,p,s]], 0,1))