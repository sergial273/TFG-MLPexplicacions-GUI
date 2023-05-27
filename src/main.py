import pygame
import sys
import chess
from pygame.locals import *
import pygame.scrap

from const import *
from game import Game
from explanations import Explanations

from stockfish import Stockfish

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
        explanations = Explanations("./stockfish/stockfish-windows-2022-x86-64-avx2")
        stockfish = Stockfish(path="./stockfish/stockfish-windows-2022-x86-64-avx2")
        dragger = self.game.dragger
        prev_board = None
        exp = ""
        vs_ia = False
        eval_board = None
        eval = None
        while True:
            if eval_board != board.fen():
                eval_board = board.fen()
                stockfish.set_fen_position(eval_board)
                eval = stockfish.get_evaluation()


            game.show_bg(screen,vs_ia,eval,explication=exp)
            game.show_last_move(screen)
            game.show_moves(screen,board)
            game.show_pieces(screen,board)
            game.show_hover(screen)

            if vs_ia:
                outcome = board.outcome()
                if outcome != None:
                    game.show_end(screen,outcome)
                    board.reset()
                    game.hover_square = None
                    game.last_move = None
                    prev_board = None
                    exp = ""
                    
            if vs_ia and not board.turn:
                prev_board = board.fen()
                stockfish.set_fen_position(board.fen())
                move = stockfish.get_best_move()
                ini = move[0:2]
                fin = move[2:4]
                move = chess.Move.from_uci(ini + fin)
                
                game.last_move = move
                stockfish.make_moves_from_current_position([move])
                board = chess.Board(stockfish.get_fen_position())
                

            if dragger.dragging:
                dragger.update_blit(screen,game)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if event.pos[0] <= BOARD_WIDTH and event.pos[1] <= BOARD_HEIGHT:
                        
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        if board.piece_at(56+clicked_col-8*clicked_row) != None:
                            piece = board.piece_at(56+clicked_col-8*clicked_row)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece.symbol())
                    elif self.game.button_ia_x <= mouse_x <= self.game.button_ia_x + self.game.button_ia_width and self.game.button_ia_y <= mouse_y <= self.game.button_ia_y + self.game.button_ia_height:
                        vs_ia = not vs_ia
                        board.reset()
                        game.hover_square = None
                        game.last_move = None
                        prev_board = None
                        exp = ""
                        eval_board = None
                
                elif event.type == pygame.MOUSEMOTION:
                    if event.pos[0] <= BOARD_WIDTH or event.pos[1] <= BOARD_HEIGHT:
                        motion_row = event.pos[1]// SQSIZE
                        motion_col = event.pos[0] // SQSIZE
                        motion_pos = 56+motion_col-8*motion_row
                        game.hover_square = motion_pos

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            game.show_bg(screen,vs_ia,eval,explication=exp)
                            game.show_last_move(screen)
                            game.show_moves(screen,board)
                            game.show_pieces(screen,board)
                            game.show_hover(screen)
                            dragger.update_blit(screen, game)
                    

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.pos[0] <= BOARD_WIDTH or event.pos[1] <= BOARD_HEIGHT:
                        if dragger.dragging:

                            ini_pos = 56+dragger.initial_col-8*dragger.initial_row

                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            fin_pos = 56+released_col-8*released_row

                            move = chess.Move(ini_pos, fin_pos)       
                            moves = board.legal_moves
                            for a in moves:
                                if move == a:
                                    prev_board = board.fen()
                                    board.push(move)
                                    game.last_move = move
                                    exp = ""
                                    outcome = board.outcome()
                                    if outcome != None:
                                        game.show_end(screen,outcome)
                                        board.reset()
                                        game.hover_square = None
                                        game.last_move = None
                                        prev_board = None
                                        exp = ""
                                        
                        dragger.undrag_piece()
                    
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board.reset()
                        game.hover_square = None
                        game.last_move = None
                        prev_board = None
                        exp = ""
                        eval_board = None

                    if event.key == pygame.K_l:
                        print("Paste FEN position:")
                        fen = input()
                        try:
                            testb = chess.Board(fen)
                            
                        except ValueError:
                            print("Incorrect FEN position")
                            testb = board
                        
                        board = testb
                    
                    if event.key == pygame.K_a:
                        if prev_board != None:
                            exp = explanations.explanations(prev_board,board.fen())

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()