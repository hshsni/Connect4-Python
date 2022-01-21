import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255) # rgb values
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT=6
COLUMN_COUNT=7

def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT)) #Board has 6 rows and 7 columns
    return board

def drop_piece(board,row,column,piece):
    board[row][column]=piece
    
def is_valid_loc(board,column):
    return board[ROW_COUNT-1][column] == 0 #To check if the column is filled while trying to drop a piece

def get_next_open_row(board,column):
    for r in range(ROW_COUNT):
        if board[r][column]==0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board,piece):
    # Horizontal
    for c in range(COLUMN_COUNT-3): #No possible winning move that begin in the last three columns
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
             if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Positive Diagonal/
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
             if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Negative diagonal\
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
             if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT): 
            if board[r][c]==1:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    pygame.display.update()

board=create_board()
game_over=False
turn=0
pygame.init()
# Setting screen size for the game
SQUARESIZE=100
width=COLUMN_COUNT*SQUARESIZE
height=(ROW_COUNT+1)*SQUARESIZE # Adding an exra row to show where the piece will drop from top
RADIUS=(SQUARESIZE/2-4) 
size=(width,height)
#print(pygame.font.get_fonts())
font=pygame.font.SysFont('monospace',75)

screen=pygame.display.set_mode(size)
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            xpos=event.pos[0]
            if turn==0:
                pygame.draw.circle(screen,RED,(xpos,int(SQUARESIZE/2)),RADIUS)
            else:
                pygame.draw.circle(screen,YELLOW,(xpos,int(SQUARESIZE/2)),RADIUS)

        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            if turn==0:
                xpos=event.pos[0]
                column=int(math.floor(xpos/SQUARESIZE))
            
                if is_valid_loc(board,column):
                    row=get_next_open_row(board,column)
                    drop_piece(board,row,column,1)
            
                if winning_move(board,1):
                    label=font.render('Player 1 wins!',1,RED)
                    screen.blit(label,(40,10)) #x,y values, position pair for text to appear
                    #print('Player 1 wins')
                    game_over=True
            else:
                xpos=event.pos[0]
                column=int(math.floor(xpos/SQUARESIZE))
            
                if is_valid_loc(board,column):
                    row=get_next_open_row(board,column)
                    drop_piece(board,row,column,2)
            
                if winning_move(board,2):
                    label=font.render('Player 2 wins!',1,YELLOW)
                    #print('Player 2 wins')
                    game_over=True
            draw_board(board)
            
            turn=(turn+1)%2

            if game_over:
                pygame.time.wait(2000)
