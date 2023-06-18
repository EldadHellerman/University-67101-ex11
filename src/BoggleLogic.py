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

Board = list[list[str]]
Cell = tuple[int, int]
Path = list[Cell]
# board is of the form [['e','ou'], ['a','d']]
# path is of the form (x, y): [(1,1), (1,2), (2,2)]


class BoggleLogic:
    """
    Boggle game logic.
    """
    
    def create_dictionary_lookup(self):
        """creates a dictionary in which two letters:str is a key and the value is a tuple (a,b)
        where a is first appearance of a word starts with the two lettrs. and b is the index of the last word starts with the 2 lettters.
        """        
        #for example, d['dc'] = (234, 607)
        #if all words starting with dc are in the dictionary between 234 and 607 including
        #assuming all words in dictionary are at two letters long
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
        """sorts the words and apply the create_dictionary_lookup function (see line 24)
        Args:
            words (iterable):
        """        
        self.words = list(words)
        self.words.sort()
        self.create_dictionary_lookup()

    def read_words_from_file(self, file: str) -> None:
        """gets words from the self value "words" and apply the create_dictionary_lookup function (see line 24) 
        Args:
            file (str): _description_
        """             
        with open(file, "r") as f:
            self.words = f.read().strip().split('\n')
            self.words.sort()
        self.create_dictionary_lookup()
    
    def set_board(self, board: Board) -> None:
        """sets a variable
        Args:
            board (Board): board
        """
        self.board = board
    
    def path_to_word(self, path: Path) -> str:
        """_summary_

        Args:
            path (Path): chosen path by user

        Returns:
            str: the word matches to path
        """        
        return "".join([self.board[y][x] for (x, y) in path])
    
    def path_to_score(self, path: Path) -> int:
        #path score can be changed to include more complex calculations
        return len(path) ** 2
    
    def cell_inside_board(self, cell: Cell) -> bool:
        return(0 <= cell[0] < len(self.board[0])) and (0 <= cell[1] < len(self.board))

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
        return [(x, y) for y in cells_y for x in cells_x if self.cell_inside_board((x,y)) and ((x,y) not in path)]

    RESULT_NO = 0
    RESULT_MAYBE = 1
    RESULT_YES = 2

    def word_in_words(self, word: str) -> int:
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
        """_summary_

        Returns:
            dict[str, list[Path]]: _description_
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
        """_summary_
        """        
        self.words_set = set()
        self.words_set_possible = set()
        for word in self.words:
            self.words_set.add(word)
            for i in range(1, len(word) + 1):
                self.words_set_possible.add(word[:i])
    
    def find_all_paths_faster(self) -> dict[str, list[Path]]:
        """_summary_

        Returns:
            dict[str, list[Path]]: _description_
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
        """_summary_

        Args:
            n (int): _description_
            length_path_or_word (bool): _description_

        Returns:
            list[Path]: _description_
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
        """_summary_

        Returns:
            list[Path]: _description_
        """        
        results: dict[str: Path] = {}
        def recursive(path: Path) -> list[Path]:
            """finds all valid paths of length n"""
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
        #in my format:
        # results = dict(filter(lambda pair: self.path_to_score(pair[1]) >= max_score , results.items()))
        # for k,v in results.items(): results[k] = [v]
        # return results


