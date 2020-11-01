"""
Tic Tac Toe Player
"""
from sys import exit
import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x,o=0,0
    for k in board:
        for i in range(3):
            if k[i]=='X':
                x=x+1
            elif k[i]=='O':
                o=o+1
    if x>o:
        return(O)
    else:
        return(X)



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    L=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]=='EMPTY' or board[i][j] is None:
                L.update([(i,j)])
    return L



def result(board, a):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board=copy.deepcopy(board)
    if new_board[a[0]][a[1]] is not None:
        raise NameError('Case deja remplie')
    if player(new_board)=='X':
        new_board[a[0]][a[1]]='X'
    else:
        new_board[a[0]][a[1]]='O'

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    s=-5

    for i in range(3):
        k = board[i]
        if (k[0] == k[1] == k[2] and k[0] == 'X'):
            s=1
        if (k[0] == k[1] == k[2] and k[0] == 'O'):
            s=-1

    for j in range(3):
        if (board[0][j] == board[1][j] == board[2][j] and board[0][j] == "X"):
            s=1
        if (board[0][j] == board[1][j] == board[2][j] and board[0][j] == "O"):
            s=-1
    if (board[0][0] == board[1][1] == board[2][2] and board[0][0] == "X"):
        s=1
    if (board[0][0] == board[1][1] == board[2][2] and board[0][0] == "O"):
        s=-1
    if (board[0][2] == board[1][1] == board[2][0] and board[0][2] == "X"):
        s=1
    if (board[0][2] == board[1][1] == board[2][0] and board[0][2] == "O"):
        s=-1
    if s==1:
        return X
    if s==-1:
        return O
    else:
        return None

def Full(board):
    b = 1
    for k in board:
        for j in range(3):
            if k[j] is None:
                b = 0
    if b == 1:
        return True
    else:
        return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)!= None:
        return True
    elif Full(board):
        return True
    else:
        return False




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return(1)
    elif winner(board)==O:
        return(-1)
    else:
        return(0)



def Max_Value(board):
    if terminal(board):
        return(utility(board))
    else:
        v=-2
        for a in actions(board):
            n=Min_Value(result(board,a))
            v=max(v,n)
    return v

def Min_Value(board):
    if terminal(board):
        return(utility(board))
    else:
        v=2
        for a in actions(board):
            m=Max_Value(result(board,a))
            v=min(v,m)
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    q=None
    if player(board) == X:
        p=-2
        for a in actions(board):
            k=Min_Value(result(board,a))
            if p <= k:
                p = k
                q = a
    else:
        p = 2
        for a in actions(board):
            k = Max_Value(result(board, a))
            if p >= k:
                p = k
                q = a
    return (q)


