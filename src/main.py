import pygame
import sys
import chess

from const import *
from game import Game
from dragger import Dragger

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('ChessMLP-GUI')
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        board = chess.Board()
        dragger = self.game.dragger

        while True:

            game.show_bg(screen)
            game.show_pieces(screen,board)

            if dragger.dragging:
                dragger.update_blit(screen,game)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.piece_at(56+clicked_col-8*clicked_row) != None:
                        piece = board.piece_at(56+clicked_col-8*clicked_row)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece.symbol())
                
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        dragger.update_blit(screen, game)
        

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()


main = Main()
main.mainloop()