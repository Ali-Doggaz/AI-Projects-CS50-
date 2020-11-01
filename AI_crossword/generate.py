import sys
from random import choice
from crossword import *
import copy

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in list(self.crossword.variables):
            for word in list(self.domains[var]):
                if var.length != len(word):
                    self.domains[var].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if x == y:
            return False
        if self.crossword.overlaps[x, y] is None:
            return False
        k=0
        i = self.crossword.overlaps[x, y][0]
        j = self.crossword.overlaps[x, y][1]
        for val_x in list(self.domains[x]):
            s = 0
            k=0
            for val_y in self.domains[y]:
                '''
                if len(val_x)<(i+1):
                    continue
                if len(val_y)<(j+1):
                    continue
                '''
                if val_x[i] == val_y[j]:
                    s = 1
            if s==0:
                self.domains[x].remove(val_x)
                k=1
        if k==1:
            return True
        return False


        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        L=[]
        if arcs!=None:
            for o in arcs:
                L.append[o]
        else:
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x==y or self.crossword.overlaps[x,y]==None:
                        continue
                    L.append((x,y))
        while len(L)!=0:
            (x,y)=L[0]
            L.remove(L[0])
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for Z in self.crossword.variables - {y}:
                    L.append((Z,x))
        return True



        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False
        return True

        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        L=[]
        #checks that there are no repeating words
        for val in assignment.values():
            if val in L:
                return False
            L.append(val)
        #check that all the words' length is correct
        for var,val in assignment.items():
            if var.length != len(val):
                return False
        #checks conflicts between neighbors
        for var,val in assignment.items():
            for var_y,val_y in assignment.items():
                if var == var_y:
                    continue
                if self.crossword.overlaps[var, var_y] == None:
                    continue
                s = 0
                i = self.crossword.overlaps[var, var_y][0]
                j = self.crossword.overlaps[var, var_y][1]
                k = 0
                if val[i] != val_y[j]:
                        return False

        return True




        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        L=dict()
        for word in self.domains[var]:
            L[word] = 0
        for word in L:
            for var_y in self.crossword.variables - set(assignment.keys()):
                if var_y == var:
                    continue
                if self.crossword.overlaps[var, var_y] == None:
                    continue
                i = self.crossword.overlaps[var, var_y][0]
                j = self.crossword.overlaps[var, var_y][1]
                for val_y in self.domains[var_y]:
                    if word[i] != val_y[j]:
                        L[word] = L[word]+1
        C = list(sorted(L, key=L.get))
        return C




        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min = 100000
        for var in set(self.crossword.variables)-set(assignment.keys()):
            s = len(self.domains[var])
            if s<= min:
                min=s
        L=[]
        for var in set(self.crossword.variables)-set(assignment.keys()):
            if len(self.domains[var]) == min:
                L.append(var)
        if len(L) == 1:
            return L[0]

        max=0

        for var in L:
            s= len(self.crossword.neighbors(var))
            if s>=max:
                max=s

        for var in L:
            s = len(self.crossword.neighbors(var))
            if s == max:
                return var
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var,assignment):
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = val
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()




    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
