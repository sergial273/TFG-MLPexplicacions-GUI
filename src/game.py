import os
import sys
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
       self.font = pygame.font.SysFont('monospace',18,bold=True)
       self.button_ia_x = 0
       self.button_ia_y = 0
       self.button_ia_width = 0
       self.button_ia_height = 0
  
    def show_bg(self, surface, ia, explication = ""):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)
        #marge dret
        color = (0,0,0) # negre
        rect = (BOARD_WIDTH, 0, WIDTH-BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(surface, color, rect)
        offset = 150
    
        #text de restart
        color = (255,255,255)
        label = self.font.render("Press 'r' --> Reset Game",1,color)
        label_pos = (BOARD_WIDTH + ((WIDTH-BOARD_WIDTH)-label.get_width())//2, BOARD_HEIGHT//2 + offset)
        surface.blit(label, label_pos)

        #text de analitzar posició
        color = (255,255,255)
        label1 = self.font.render("Press 'a' --> Analyze move",1,color)
        label_pos = (BOARD_WIDTH + ((WIDTH-BOARD_WIDTH)-label1.get_width())//2, BOARD_HEIGHT//2 + label.get_height() + offset)
        surface.blit(label1, label_pos)

        #text de carregar posicio
        color = (255,255,255)
        label2 = self.font.render("Press 'l' --> Load FEN position",1,color)
        label_pos = (BOARD_WIDTH + ((WIDTH-BOARD_WIDTH)-label2.get_width())//2, BOARD_HEIGHT//2 + label.get_height() + label1.get_height() + offset)
        surface.blit(label2, label_pos)

        # Botó de vs ia
        if ia:
            button_text = "Playing Vs. IA"
            button_font = pygame.font.SysFont("Arial", 20)
            button_surface = button_font.render(button_text, True, (0, 0, 0))
            self.button_ia_width = button_surface.get_width() + 10
            self.button_ia_height = button_surface.get_height() + 10
            self.button_ia_x = WIDTH - (self.button_ia_width + 50) 
            self.button_ia_y = 10+self.button_ia_height
            pygame.draw.rect(surface, (0, 0, 255), (self.button_ia_x, self.button_ia_y, self.button_ia_width, self.button_ia_height), border_radius=3)
        else:
            button_text = "Playing Vs. Human"
            button_font = pygame.font.SysFont("Arial", 20)
            button_surface = button_font.render(button_text, True, (0, 0, 0))
            self.button_ia_width = button_surface.get_width() + 10
            self.button_ia_height = button_surface.get_height() + 10
            self.button_ia_x = WIDTH - (self.button_ia_width + 50) 
            self.button_ia_y = 10+self.button_ia_height
            pygame.draw.rect(surface, (255, 0, 0), (self.button_ia_x, self.button_ia_y, self.button_ia_width, self.button_ia_height), border_radius=3)
            
        surface.blit(button_surface, (self.button_ia_x + 5, self.button_ia_y + 5))

        #text de explicar posició posició
        color = (255,255,255)
        if explication != "":
            frase = explication[2] + "\n\n" + explication[0] +"\n"+explication[1]
            
        else:
            frase = ""

        label_pos = (BOARD_WIDTH + 50, BOARD_HEIGHT//2 - 100)
        
        blit_text(surface, frase, label_pos, self.font, color)
        

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

    def show_end(self, screen, outcome):
        message = ""

        if outcome.termination.value == 1:
            player = "white" if outcome.winner else "black"
            message = f"CHECKMATE! {player} won!"

        elif outcome.termination.value == 2:
            message = f"STALEMATE! It's a draw!"

        elif outcome.termination.value == 3:
            message = f"Draw by insufficient material"
        
        elif outcome.termination.value == 4:
            message = f"It's a draw! 75 moves without a pawn move"
        
        elif outcome.termination.value == 5:
            message = f"Draw by fivefold repetition"
        
        else:
            message = f"It's a draw"
     

        message2 = "Click RESTART to continue."

        # Set up the font
        font = pygame.font.SysFont("Arial", 30)

        # Render the message as a surface
        message_surface = font.render(message, True, (255, 255, 255))
        message2_surface = font.render(message2, True, (255, 255, 255))

        # Calculate the position of the message
        message_x = (BOARD_WIDTH - message_surface.get_width()) // 2
        message_y = (BOARD_HEIGHT - message_surface.get_height()) // 2

        message2_x = (BOARD_WIDTH - message2_surface.get_width()) // 2
        message2_y = (BOARD_HEIGHT - message2_surface.get_height()) // 2 + message_surface.get_height()

        # Set up the button
        button_text = "RESTART"
        button_font = pygame.font.SysFont("Arial", 20)
        button_surface = button_font.render(button_text, True, (0, 0, 0))
        button_width = button_surface.get_width() + 10
        button_height = button_surface.get_height() + 10
        button_x = (BOARD_WIDTH - button_width) // 2
        button_y = message_y + message_surface.get_height() + message2_surface.get_height() + 10

        #Set up the backgound
        length = message_surface.get_width() if message_surface.get_width() > message2_surface.get_width() else message2_surface.get_width()
        backgorund_width = length + 20
        background_height = message_surface.get_height() + message2_surface.get_height() + button_height + 50
        background_x = (BOARD_WIDTH - backgorund_width) // 2
        background_y = (BOARD_HEIGHT - background_height) // 2 + 25

        # Draw the message and the button onto the screen
        pygame.draw.rect(screen, (0, 0, 0), (background_x,background_y,backgorund_width,background_height),border_radius=3)
        screen.blit(message_surface, (message_x, message_y))
        screen.blit(message2_surface, (message2_x, message2_y))
        pygame.draw.rect(screen, (208, 67, 67), (button_x, button_y, button_width, button_height), border_radius=3)
        screen.blit(button_surface, (button_x + 5, button_y + 5))

        # Update the display
        pygame.display.flip()

        while True:
            
            for event in pygame.event.get():
        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        # The player clicked the button, so continue the game
                        break
            else:
                continue
            break

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.