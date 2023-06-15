# board is of the form [['e','ou'], ['a','d']]
# path is of the form (x, y): [(1,1), (1,2), (2,2)]
Board = list[list[str]]
Cell = tuple[int, int]
Path = list[Cell]

class BoggleLogic:
    """
    Boggle game logic.
    """
    def __init__(self, words_file):
        self.read_words_from_file(words_file)
    
    def read_words_from_file(self, file):
        with open(file, "r") as f:
            self.words = f.read().strip().split('\n')
            self.words.sort()
    
    def set_board(self, board):
        self.board = board
    
    def path_to_word(self, path: Path) -> str:
        return "".join([self.board[y][x] for (x, y) in path])

    def get_unvisited_neighbors(self, path: Path) -> list[Cell]:
        """
        Finds all unvisited neighbors of the last cell in the path.

        Args:
            board (Board): Board, used to check if cells are out of the board.
            path (Path): Current Path. Cells that are in that path are not returned.

        Returns:
            list[Cell]: Returns a list of all valid neighbors, given x coord and y coord
        """
        cells_y = range(path[-1][1] - 1, path[-1][1] + 2)
        cells_x = range(path[-1][0] - 1, path[-1][0] + 2)
        inside_board = lambda x,y: (0 <= x < len(self.board[0])) and (0 <= y < len(self.board))
        return [(x, y) for y in cells_y for x in cells_x if inside_board(x,y) and ((x,y) not in path)]

    def word_in_words(self, word, maybe=False):
        def binary_search_rec(lower, upper):
            if(lower > upper): return False
            mid = (lower + upper) // 2
            pivot = self.words[mid]
            if(maybe and pivot.startswith(word)): return True
            if(not maybe and (word == pivot)): return True
            elif(word < pivot): return binary_search_rec(lower, mid-1)
            elif(word > pivot): return binary_search_rec(mid+1, upper)
        return binary_search_rec(0, len(self.words)-1)
    
    def is_valid_path(self, path: Path) -> str | None: #################################
        word = self.path_to_word(path)
        return word if self.is_word_in_words(word) else None

    def find_length_n_paths_recursive(self, path: Path, n: int) -> list[Path]:
        """finds all paths of n length valid words"""
        word = self.path_to_word(path)
        if not self.word_in_words(word, maybe=True): return []
        if len(path) == n: return [path] if self.word_in_words(word) else []
        
        results: list[Path]= []
        for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
            results += self.find_length_n_paths_recursive(path + [neighbor],  n)
        return results
    
    def find_length_n_paths(self, n: int) -> list[Path]:#################################
        cells = [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]
        return [self.find_length_n_paths_recursive([cell], n) for cell in cells]
    


    def find_all_paths(self) -> dict[str: list[Path]]:
        results: dict[str: list[Path]] = {}
        def recursive(path: Path) -> list[Path]:
            """finds all paths of n length valid words"""
            nonlocal results
            word = self.path_to_word(path)
            if self.word_in_words(word): results.setdefault(word, []).append(path)
            if not self.word_in_words(word, maybe=True): return
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results