import os
import pygame

from const import *
from dragger import Dragger

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
       self.dragger = Dragger()

       self.last_move = None
       self.hover_square = None
  
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
            if self.dragger.dragging:
                if not elem.isdigit() and elem != "/":
                    if row!=self.dragger.initial_row or col != self.dragger.initial_col:
                        img= pygame.image.load(self.get_texture(elem,size=68))
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        surface.blit(img,img.get_rect(center=img_center))
                elif elem == "/":
                    row += 1
                    col = -1
                col+=1

            else:
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
    
    def show_moves(self, surface, board):

        if self.dragger.dragging:
            piece = self.dragger.piece
            moves = board.legal_moves
            piece_position = 56+self.dragger.initial_col-8*self.dragger.initial_row
            # loop all valid moves
            for move in moves:
                if move.from_square == piece_position:
                    col = move.to_square % 8
                    row = 7-((move.to_square - col)//8)

                    # color
                    color = '#C86464' if (row + col) % 2 == 0 else '#C84646'
                    # rect
                    rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                    # blit
                    pygame.draw.rect(surface, color, rect)


    def show_last_move(self, surface):
        if self.last_move != None:
            for move in [self.last_move.from_square,self.last_move.to_square]:
                col = move % 8
                row = 7-((move - col)//8)

                # color
                color = (244, 247, 116) if (row + col) % 2 == 0 else (172, 195, 51)
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hover_square != None:
            col = self.hover_square % 8
            row = 7-((self.hover_square - col)//8)
            # color
            color = (180, 180, 180)
            # rect
            rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=5)
