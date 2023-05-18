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
            game.show_last_move(screen)
            game.show_moves(screen,board)
            game.show_pieces(screen,board)
            game.show_hover(screen)

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

                    motion_row = event.pos[1]// SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    motion_pos = 56+motion_col-8*motion_row
                    game.hover_square = motion_pos

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen,board)
                        game.show_pieces(screen,board)
                        game.show_hover(screen)
                        dragger.update_blit(screen, game)
        

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:

                        ini_pos = 56+dragger.initial_col-8*dragger.initial_row

                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        fin_pos = 56+released_col-8*released_row

                        move = chess.Move(ini_pos, fin_pos)
                        game.last_move = move
                        moves = board.legal_moves
                        for a in moves:
                            if move == a:
                                board.push(move)






                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()


main = Main()
main.mainloop()