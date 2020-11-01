def main():
    assignement = [[None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None]
                     ]

    L = []
    for i in range(9):
        for j in range(9):
            for k in range(3):
                    if j - 1 + k > 0 and j-1+k < 9 and i - 1 > 0:
                        L.append(i-1,j-1+k)

                    if j - 1 + k > 0 and j-1+k < 9  and i + 1 < 9:
                        L.append(i + 1,j - 1 + k)

            if j - 1 >= 0:
                    L.append(i,j-1)
            if j + 1 < 9:
                    if assignement[i][j + 1] == 1:
                        return False
