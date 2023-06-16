
# board is of the form [['e','ou'], ['a','d']]
# path is of the form (x, y): [(1,1), (1,2), (2,2)]
Board = list[list[str]]
Cell = tuple[int, int]
Path = list[Cell]

class BoggleLogic:
    """
    Boggle game logic.
    """
    
    def read_words_from_iterable(self, words):
        self.words = list(words)
        self.words.sort()
    
    def read_words_from_file(self, file):
        with open(file, "r") as f:
            self.words = f.read().strip().split('\n')
            self.words.sort()
    
    def set_board(self, board):
        self.board = board
    
    def path_to_word(self, path: Path) -> str:
        return "".join([self.board[y][x] for (x, y) in path])
    
    def path_to_score(self, path):
        #path score can be changed to include more complex calculations
        return len(path) ** 2
    
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

    def word_in_words(self, word, maybe=False) -> bool:
        def binary_search_rec(lower, upper):
            if(lower > upper): return False
            mid = (lower + upper) // 2
            pivot = self.words[mid]
            if(maybe and pivot.startswith(word)): return True
            if(not maybe and (word == pivot)): return True
            elif(word < pivot): return binary_search_rec(lower, mid-1)
            elif(word > pivot): return binary_search_rec(mid+1, upper)
        return binary_search_rec(0, len(self.words)-1)
    
    def find_all_paths(self) -> dict[str: list[Path]]:
        results: dict[str: list[Path]] = {}
        def recursive(path: Path) -> list[Path]:
            nonlocal results
            word = self.path_to_word(path)
            if self.word_in_words(word): results.setdefault(word, []).append(path)
            if not self.word_in_words(word, maybe=True): return
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results
    

    
    #functions used for their logic:

    def find_paths_of_length(self, n, length_path_or_word) -> list[Path]:
        results: list[Path] = []
        def recursive(path: Path) -> list[Path]:
            """finds all valid paths of length n"""
            nonlocal results, n
            word = self.path_to_word(path)
            length = len(path if length_path_or_word else word)
            if length == n and self.word_in_words(word): results.append(path)
            if not self.word_in_words(word, maybe=True) or length >= n: return
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results

    def find_paths_heighest_scoring(self) -> list[Path]:
        results: dict[str: list[Path]] = {}
        max_score = 0
        def recursive(path: Path) -> list[Path]:
            """finds all valid paths of length n"""
            nonlocal results, max_score
            word = self.path_to_word(path)
            score = self.path_to_score(path)
            if self.word_in_words(word) and score >= max_score:
                max_score = score
                #if word wasnt found before or if it has higher score than the proviously found one:
                if(word not in results or score > self.path_to_score(results[word])):
                    results[word] = path
            if not self.word_in_words(word, maybe=True): return
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        #results still need to be filtered to only the heighest ones
        return filter(lambda path: self.path_to_score(path) >= max_score , results.values())
        #in my format:
        # results = dict(filter(lambda pair: self.path_to_score(pair[1]) >= max_score , results.items()))
        # for k,v in results.items(): results[k] = [v]
        # return results


