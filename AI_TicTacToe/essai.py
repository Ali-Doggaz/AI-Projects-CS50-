from TicTac import terminal,winner,utility,actions,minimax,result,Min_Value,initial_state,player
from sys import exit

def game(board):
       if terminal(board):
              print("winner is :",winner(board))
              exit(0)
       board = result(board, minimax(board))
       print(board)
       if terminal(board):
              print("winner is :",winner(board))
              exit(1)
       '''
       f = set()
       i = int(input("veuillez saisir votre action i:"))
       j = int(input("j:"))
       f.update([(i, j)])
       print(f[0])
       print(f[1])
       #board=result(board,f)
       '''
       board=result(board,minimax(board))
       print(board)
       game(board)

def main():
       print("game started!")
       board=initial_state()
       print(board)
       game(board)
       print("game ended!")

main()


'''


board=[['X', 'O', 'X'],
['X', 'O', 'EMPTY'],
['O', 'X', 'X']]

print(minimax(board))
'''