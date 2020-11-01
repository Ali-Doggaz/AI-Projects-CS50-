from minesweeper import Minesweeper,MinesweeperAI,Sentence

HEIGHT = 8
WIDTH = 8
MINES = 10
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=8)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
game.print()
ai.add_knowledge((0,0),1)
ai.add_knowledge((0,1),1)



print("****")
for sentence in ai.knowledge:
    print(sentence.cells,"=",sentence.count)
print("****\n safes:",ai.safes,"\n","mines: ",ai.mines)




'''
revealed = set()
flags = set()
lost = False
move = None
while(lost==False):
    move = ai.make_safe_move()
    if move is None:
        move = ai.make_random_move()
        if move is None:
            flags = ai.mines.copy()
            print("No moves left to make.")
        else:
            print("No known safe moves, AI making random move.")
    else:
        print("AI making safe move.")

#Make the move
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
'''