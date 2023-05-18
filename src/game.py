import os
import pygame
import chess

from const import *

class Game:

    def __init__(self):
       self.PiecesTonNum = {
        "p": "pawn",
        "n": "knight",
        "b": "bishop",
        "r": "rook",
        "q": "queen",
        "k": "king"
        }
  
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)

    def show_pieces(self,surface, board):
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
        
        row = col = 0
        for elem in codifsencera1:

            if not elem.isdigit() and elem != "/":
                
                img= pygame.image.load(self.get_texture(elem,size=68))
                img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                surface.blit(img,img.get_rect(center=img_center))
            elif elem == "/":
                row += 1
                col = -1
            col+=1


    def get_texture(self, piece,size=68):
        
        if piece.isupper(): #white
            return os.path.join(f'piece_img/{size}px/white_{self.PiecesTonNum[piece.lower()]}.png')
        else:
            return os.path.join(f'piece_img/{size}px/black_{self.PiecesTonNum[piece.lower()]}.png')
            
            
