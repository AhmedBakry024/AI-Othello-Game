import pygame as game
import pygame.gfxdraw
import controller
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


font = pygame.font.Font(None, 36)
# Initialize the current player (1 for white, -1 for black)
current_player = -1

def select_difficulty_screen():
    win.fill(BACKGROUND)
    # Define the button rectangles
    easy_button_rect = pygame.Rect(150, 100, 110, 50)
    medium_button_rect = pygame.Rect(150, 200, 110, 50)
    hard_button_rect = pygame.Rect(150, 300, 110, 50)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the user clicked on the "Easy" button
                if easy_button_rect.collidepoint(mouse_pos):
                    return 1
                # Check if the user clicked on the "Medium" button
                elif medium_button_rect.collidepoint(mouse_pos):
                    return 3
                # Check if the user clicked on the "Hard" button
                elif hard_button_rect.collidepoint(mouse_pos):
                    return 5

        # Draw the buttons
        pygame.draw.rect(win, WHITE, easy_button_rect)
        pygame.draw.rect(win, WHITE, medium_button_rect)
        pygame.draw.rect(win, WHITE, hard_button_rect)

        # Draw the button labels
        easy_label = font.render("Easy", True, BLACK)
        medium_label = font.render("Medium", True, BLACK)
        hard_label = font.render("Hard", True, BLACK)
        win.blit(easy_label, (easy_button_rect.x + 25, easy_button_rect.y + 15))
        win.blit(medium_label, (medium_button_rect.x + 10, medium_button_rect.y + 15))
        win.blit(hard_label, (hard_button_rect.x + 25, hard_button_rect.y + 15))

        pygame.display.update()

# Call the select_difficulty_screen function at the start of your script
difficulty = select_difficulty_screen()

# Then, in your main loop, use the difficulty variable to adjust the game difficulty

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
        
    for move in controller.get_possible_moves(board, current_player):
        pygame.gfxdraw.aacircle(win, 50*move[0]+25, 50*move[1]+25+100, 10, (0, 255, 0))
        pygame.gfxdraw.filled_circle(win, 50*move[0]+25, 50*move[1]+25+100, 10, (0, 255, 0))
    game.display.update()
    
draw_board()

# Main loop
run = True
while run:
    if len(controller.get_possible_moves(board, current_player)) == 0:
        current_player *= -1
        
    if controller.is_game_over(board):
        pygame.time.wait(500)
        scores = controller.get_winner(board)
        if scores == 1:
            text = "White wins!"
        elif scores == -1:
            text = "Black wins!"
        else:
            text = "It's a draw!"
        text = font.render(text, True, WHITE)
        text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() // 2+20))
        box = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)
        pygame.draw.rect(win, BLACK, box)
        
        win.blit(text, text_rect)
        game.display.update()
        game.time.wait(3000)
        pygame.quit()
    else:
        if current_player == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Calculate the column and row indices.
                    i = mouse_pos[0] // 50  # Calculate the column index
                    j = (mouse_pos[1] - 100) // 50  # Calculate the row index
                    # Check if the click was within the board
                    if 0 <= i < 8 and 0 <= j < 8 and mouse_pos[1] >= 100 :
                        # check if the cell is in the possible moves list
                        if (i, j) in controller.get_possible_moves(board, current_player):
                            if board[i][j] == 0:  # Check if the cell is empty
                                board[i][j] = current_player  # Place a piece
                                controller.flip_pieces(board, i, j, current_player)
                                current_player *= -1  # Switch the current player..
        # If the current player is the computer, make a move
        elif current_player == 1:
            if len(controller.get_possible_moves(board, 1)) > 0:
                controller.computer_move(difficulty,board)
            current_player *= -1  # Switch the current player

    

    draw_board()

game.quit()