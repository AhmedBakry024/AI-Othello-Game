# I'm making a game of Othello using Pygame 
# I'm going to start by creating the board and the pieces
# THere will be two players, one black and one white
# the user should play against the computer
# I will start by creating the board and the pieces

import pygame as game
import pygame.gfxdraw
game.init()

win = game.display.set_mode((400, 500))

game.display.set_caption("Othello")

# Colors
WHITE = (244, 253, 250)
BLACK = (19, 26, 24)
BACKGROUND = (0, 144, 103)

# Board
board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, -1, 0, 0, 0],
    [0, 0, 0, -1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


# Create a font object
font = pygame.font.Font(None, 36)

# Draw board
def draw_board():
    win.fill(BACKGROUND)
    
     # Draw the scoreboard
    pygame.draw.rect(win, BLACK, (5, 5, 390, 90),45,10)
    # Flatten the board
    flat_board = [item for sublist in board for item in sublist]

# Render the scores
    white_score_text = font.render(f"White: {flat_board.count(1)}", True, WHITE)
    black_score_text = font.render(f"Black: {flat_board.count(-1)}", True, WHITE)
# Blit the scores
    win.blit(white_score_text, (30, 40))  # Blit the white score at the left
    win.blit(black_score_text, (win.get_width() - black_score_text.get_width() - 30, 40))  # Blit the black score at the right
    
    # Draw lines
    for i in range(8):
        game.draw.line(win, BLACK, (50*i, 100), (50*i, 500), 2)
        game.draw.line(win, BLACK, (0, 50*i+ 100), (400, 50*i+100), 2)
    # Draw pieces
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                pygame.gfxdraw.aacircle(win, 50*i+25, 50*j+25+100, 20, WHITE)
                pygame.gfxdraw.filled_circle(win, 50*i+25, 50*j+25+100, 20, WHITE)
            elif board[i][j] == -1:
                pygame.gfxdraw.aacircle(win, 50*i+25, 50*j+25+100, 20, BLACK)
                pygame.gfxdraw.filled_circle(win, 50*i+25, 50*j+25+100, 20, BLACK)
        
    game.display.update()
    # make the board clickable for the user to place their pieces
    
    
draw_board()

# Initialize the current player (1 for white, -1 for black)
current_player = -1

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Calculate the column and row indices
            i = mouse_pos[0] // 50  # Calculate the column index
            j = (mouse_pos[1] - 100) // 50  # Calculate the row index

            # Check if the click was within the board
            if 0 <= i < 8 and 0 <= j < 8 and mouse_pos[1] >= 100:  
                if board[i][j] == 0:  # Check if the cell is empty
                    board[i][j] = current_player  # Place a piece
                    current_player *= -1  # Switch the current player
    draw_board()

game.quit()