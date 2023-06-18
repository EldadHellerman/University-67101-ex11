#################################################################
# FILE : BoggleLogic.py
# WRITERS : Eldad Hellerman , hellerman , 322898552
#           Omri Baum, omribaum, 315216853
# EXERCISE : intro2cs2 ex10 2023
# DESCRIPTION: A class used for the advanced logic functions of a boggle game.
# STUDENTS WE DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES WE USED: none.
# NOTES: none.
#################################################################

Board = list[list[str]] # board is of the form [['e','ou'], ['a','d']]
Cell = tuple[int, int] #cell is (x, y)
Path = list[Cell]

class BoggleLogic:
    """
    Boggle game logic.
    The logic stores the current board, and the valid words list, and it's in charge of checking
    is a word is valid and to calculate all avaiable paths in a boggle board.
    """
    
    def create_dictionary_lookup(self):
        """
        Creates a lookup dictionary of the upper and lower index bounds of a word, according to it's first two characters.
        For example, lookup['dc'] = (234, 607) if all words starting with 'dc' are between words[234] and  words[607] including.
        This is a micro-optimixation to reduce the binary search time by a bit.
        It reduces the ammount of bisections needed by 9, and for a 300,000 words set that's reducing 19 to 10 - half the time.
        
        Assuming all words in dictionary are at two letters long.
        """        
        lookup = {}
        key = None
        for index, word in enumerate(self.words):
            key = word[:2]
            if key in lookup:
                lookup[key] = (lookup[key][0], index)
            else:
                lookup[key] = (index, index)
        if key is not None: lookup[key] = (lookup[key][0], index)
        self.words_limits_by_first_two_letters = lookup
    
    def read_words_from_iterable(self, words) -> None:
        """
        Creating own words object from a words iterable.

        Args:
            words (iterable): Iterable of words.
        """
        self.words = list(words)
        self.words.sort()
        self.create_dictionary_lookup()

    def read_words_from_file(self, file: str) -> None:
        """
        Creating own words object from a words file.
        A words file has each word on a line ending with a linefeed ('\\n').

        Args:
            file (str): Path to word file.
        """             
        with open(file, "r") as f:
            self.words = f.read().strip().split('\n')
            self.words.sort()
        self.create_dictionary_lookup()
    
    def set_board(self, board: Board) -> None:
        """
        Sets the board.

        Args:
            board (Board): A boggle board.
        """
        self.board = board
    
    def path_to_word(self, path: Path) -> str:
        """
        Computes the word represented by a given path.

        Args:
            path (Path): A path.

        Returns:
            str: The word that path represents.
        """        
        return "".join([self.board[y][x] for (x, y) in path])
    
    def path_to_score(self, path: Path) -> int:
        """
        Computes the score a given path is worth.
        Currently this is just the path length square, though this can use more elaborate schemes like
        scoring harder letters higher.

        Args:
            path (Path): A path.

        Returns:
            int: The score this path is worth.
        """
        return len(path) ** 2
    
    def cell_inside_board(self, cell: Cell) -> bool:
        """
        Checks if a given cell is inside a board.

        Args:
            cell (Cell): Cell to check.

        Returns:
            bool: True if cell is inside board.
        """        
        return(0 <= cell[0] < len(self.board[0])) and (0 <= cell[1] < len(self.board))

    def get_unvisited_neighbors(self, path: Path) -> list[Cell]:
        """
        Finds all unvisited neighbors of the last cell in the path.

        Args:
            board (Board): Board, used to check if cells are out of the board.
            path (Path): Current Path. Cells that are in that path are not returned.

        Returns:
            list[Cell]: A list of all valid neighbors.
        """
        cells_y = range(path[-1][1] - 1, path[-1][1] + 2)
        cells_x = range(path[-1][0] - 1, path[-1][0] + 2)
        # return [(x, y) for y in cells_y for x in cells_x if self.cell_inside_board((x,y)) and ((x,y) not in path)]
        #inline cell inside board is a bit faster!
        return [(x, y) for y in cells_y for x in cells_x if 
                (0 <= x < len(self.board[0])) and (0 <= y < len(self.board)) and ((x,y) not in path)]

    # results returned by a search of word in words:
    RESULT_NO = 0
    RESULT_MAYBE = 1
    RESULT_YES = 2

    def word_in_words(self, word: str) -> int:
        """
        Checks if a given word is inside words.

        Args:
            word (str): Word to check.

        Returns:
            int: RESULT_NO, RESULT_MAYBE, or RESULT_YES.
        """        
        result_maybe = self.RESULT_NO
        lower, upper = 0, len(self.words) - 1
        if(len(word) >= 2): #accelerate search using the lookup:
            key = word[:2]
            if(key not in self.words_limits_by_first_two_letters): return self.RESULT_NO
            lower, upper = self.words_limits_by_first_two_letters[key]
        while lower <= upper:
            mid = (lower + upper) // 2
            pivot = self.words[mid]
            if(word == pivot): return self.RESULT_YES
            if pivot.startswith(word): result_maybe = self.RESULT_MAYBE
            lower, upper = (lower, mid-1) if(word < pivot) else (mid+1, upper)
        return result_maybe
    
    def find_all_paths(self) -> dict[str, list[Path]]:
        """
        Finds all valid paths on the board.
        The result is returned as a dictionary where the key is the word the paths create,
        and the value is a list of all paths that create that word.

        Returns:
            dict[str, list[Path]]: All valid paths in the board.
        """
        results: dict[str: list[Path]] = {}
        def recursive(path: Path) -> list[Path]:
            nonlocal results
            word = self.path_to_word(path)
            r = self.word_in_words(word) 
            if r == self.RESULT_YES: results.setdefault(word, []).append(path)
            elif r == self.RESULT_NO: return
            # if here then (r != self.RESULT_NO)
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results
    
    #faster algorithm for bigger boards, but much more memory use:
    #for small board, the regular algoithm is faster.

    def create_lookup_sets(self):
        """
        Faster algorithm for larger boards if memory consumption if less of an issue.
        Creates lookup sets for all words, as well as all valid start of words.
        Fro example, 'banana' is a valid word, and:
        'b', 'ba', 'ban', 'bana', 'banan' are all valid begginings of a word.
        """
        self.words_set = set()
        self.words_set_possible = set()
        for word in self.words:
            self.words_set.add(word)
            for i in range(1, len(word) + 1):
                self.words_set_possible.add(word[:i])
    
    def find_all_paths_faster(self) -> dict[str, list[Path]]:
        """
        Same as find_all_paths(), but uses the lookup set created with create_lookup_sets().
        
        Finds all valid paths on the board.
        The result is returned as a dictionary where the key is the word the paths create,
        and the value is a list of all paths that create that word.
        Returns:
            dict[str, list[Path]]: All valid paths in the board.
        """        
        results: dict[str: list[Path]] = {}
        def recursive(path: Path) -> list[Path]:
            nonlocal results
            word = self.path_to_word(path)
            r = self.RESULT_MAYBE
            if(word not in self.words_set_possible): return
            elif(word in self.words_set): results.setdefault(word, []).append(path)
            # if here then (r != self.RESULT_NO)
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results
    
    #functions used for their logic:

    def find_paths_of_length(self, n: int, length_path_or_word: bool) -> list[Path]:
        """
        Finds all valid paths on the board, that are of a given path length or word length.
        The result is returned as a list of all paths the meet the requirements.

        Args:
            n (int): Length of path,
            length_path_or_word (bool): True if path length is desired, False if word length.

        Returns:
            list[Path]: All valid paths.
        """
        results: list[Path] = []
        def recursive(path: Path) -> list[Path]:
            """finds all valid paths of length n"""
            nonlocal results, n
            word = self.path_to_word(path)
            length = len(path if length_path_or_word else word)
            r = self.word_in_words(word)
            if length == n and r == self.RESULT_YES: results.append(path)
            if r == self.RESULT_NO or length >= n: return
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results

    def find_paths_heighest_scoring(self) -> list[Path]:
        """
        Finds all valid paths in the board.
        The result is returned as a list paths.
        If there are two paths that represent the same word, the higher scoring
        one is chosen, and the secnod one is dicarded.
        
        Returns:
            list[Path]: All valid paths.
        """        
        results: dict[str: Path] = {}
        def recursive(path: Path) -> list[Path]:
            """finds all valid paths"""
            nonlocal results
            word = self.path_to_word(path)
            score = self.path_to_score(path)
            r = self.word_in_words(word)
            if r == self.RESULT_YES:
                if word in results:
                    if self.path_to_score(path) > self.path_to_score(results[word]):
                        results[word] = path
                else:
                    results[word] = path
            if r == self.RESULT_NO: return
            for neighbor in self.get_unvisited_neighbors(path): # get the valid neighbors
                recursive(path + [neighbor])
        
        for cell in [(x, y) for x in range(len(self.board[0])) for y in range(len(self.board))]:
            recursive([cell])
        return results.values()
