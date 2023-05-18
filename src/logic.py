import chess

class Logic:
    def __init__(self):
       pass

    def get_game(self,board):
        nboard = board.fen().split()[0]
        a = 0
        codifsencera1 = ""
        for elem in nboard:
            if not elem.isdigit() and elem != "/":
                a += 1
                codifsencera1 += elem
            elif elem == "/":
                codifsencera1 += elem
            else:
                codifsencera1 += ("1" * int(elem))
        
        return codifsencera1
    
