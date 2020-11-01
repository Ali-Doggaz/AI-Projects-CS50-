import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count==len(self.cells):
            return self.cells
        return None


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        return None


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count=self.count-1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)




class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    def add_sentence(self,cell,count):# 3) add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        S = set()
        for i in range(-1, 2):
            if ((cell[0] + 1, cell[1] + i) not in self.moves_made and 0 <= cell[0] + 1 < self.height and 0 <= cell[
                1] + i < self.width):
                if (cell[0] + 1, cell[1] + i) in self.mines:
                    count = count - 1
                elif (cell[0] + 1, cell[1] + i) in self.safes:
                    count = count
                else:
                    S.add((cell[0] + 1, cell[1] + i))
        for i in range(-1, 2):
            if (cell[0] - 1, cell[1] + i) not in self.moves_made and 0 <= cell[0] - 1 < self.height and 0 <= cell[
                1] + i < self.width:
                if (cell[0] - 1, cell[1] + i) in self.mines:
                    count = count - 1
                elif (cell[0] - 1, cell[1] + i) in self.safes:
                    count = count
                else:
                    S.add((cell[0] - 1, cell[1] + i))
        for i in range(-1, 2, 2):
            if (cell[0], cell[1] + i) not in self.moves_made and 0 <= cell[0] < self.height and 0 <= cell[
                1] + i < self.width:
                if (cell[0], cell[1] + i) in self.mines:
                    count = count - 1
                elif (cell[0], cell[1] + i) in self.safes:
                    count = count
                else:
                    S.add((cell[0], cell[1] + i))
        sentence = Sentence(S, count)
        self.knowledge.append(sentence)
        print("Sentence = ",sentence.cells,"=",sentence.count)


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
        """
        # 1) mark the cell as a move that has been made

        self.moves_made.add(cell)
        # 2) mark the cell as safe
        # B- update any sentences that contain the cell as well.
        self.mark_safe(cell)
        #3) add sentence
        self.add_sentence(cell,count)


        mine = set()
        safe = set()
        for sentence in self.knowledge:
            if sentence.known_mines() is not None:
                for a in sentence.known_mines():
                    mine.add(a)
            if sentence.known_safes() is not None:
                for b in sentence.known_safes():
                    safe.add(b)
        for a in mine:
            self.mark_mine(a)
        for b in safe:
            self.mark_safe(b)
        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        '''
        k = 1
        while (k):
            k = 0
            liste=[]
            for sentence in self.knowledge:
                for second in self.knowledge:
                    if len(second.cells)==0:
                        continue
                    if not (second.cells == sentence.cells) and second.cells is not None and sentence.cells is not None:
                        if ((second.cells & sentence.cells) == second.cells):
                            k = 1
                            I = set()
                            I = sentence.cells - second.cells
                            nbr = len(sentence.cells)-len(second.cells)
                            m = Sentence(I, nbr)
                            liste.append(m)
        for o in liste:
            self.knowledge.append(o)
        '''
        liste = []
        for sentence in self.knowledge:
            for second in self.knowledge:
                if len(second.cells) == 0:
                    continue
                if not (second.cells == sentence.cells) and second.cells is not None and sentence.cells is not None:
                    if ((second.cells & sentence.cells) == second.cells):
                        I = set()
                        I = sentence.cells - second.cells
                        nbr = sentence.count - second.count
                        m = Sentence(I, nbr)
                        liste.append(m)

        for o in liste:
            self.knowledge.append(o)



        for sentence in self.knowledge:
            if len(sentence.cells)==0:
                self.knowledge.remove(sentence)

        liste1=[]
        liste2=[]

        for sentence in self.knowledge:
            if sentence.known_mines() is not None:
                for a in sentence.known_mines():
                    liste1.append(a)
            if sentence.known_safes() is not None:
                for b in sentence.known_safes():
                    liste2.append(b)
            for a in liste1:
                self.mark_mine(a)
            for b in liste2:
                self.mark_safe(b)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for x, y in self.safes:
            if (x, y) not in self.moves_made:
                return ((x, y))
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        for i in range(self.width):
            for j in range(self.height):
                if ((i,j) not in self.mines) and ((i,j) not in self.moves_made):
                    return ((i,j))
        return None

