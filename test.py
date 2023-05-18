import chess

board = chess.Board()

print(board)
for elem in board.fen().split()[0]:
    print(elem)