def get_possible_moves(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                if is_valid_move(board, i, j, 0, 1, player):
                    moves.append((i, j))
                elif is_valid_move(board, i, j, 0, -1, player):
                    moves.append((i, j))
                elif is_valid_move(board, i, j, 1, 0, player):
                    moves.append((i, j))
                elif is_valid_move(board, i, j, -1, 0, player):
                    moves.append((i, j))
    return moves


# make a function to check if the move is valid
def is_valid_move(board, i, j, x, y, player):
    if i + x < 0 or i + x >= 8 or j + y < 0 or j + y >= 8 or board[i + x][j + y] == player:
        return False
    if board[i + x][j + y] == 0:
        return False
    while True:
        i += x
        j += y
        if i < 0 or i >= 8 or j < 0 or j >= 8:
            return False
        if board[i][j] == 0:
            return False
        if board[i][j] == player:
            return True


# handle the flip of the pieces when a move is made
# the pieces are flipped when the move is valid, all the pieces between the new piece and the old piece are flipped
def flip_pieces(board, i, j, player):
    # Directions to check for opponent's pieces
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # For each direction
    for dx, dy in directions:
        x, y = i + dx, j + dy

        # Initialize a list to store the pieces to be flipped
        pieces_to_flip = []

        # While the cell is within the board and contains an opponent's piece
        while 0 <= x < 8 and 0 <= y < 8 and board[x][y] == -player:
            # Add the piece to the list of pieces to be flipped
            pieces_to_flip.append((x, y))
            x, y = x + dx, y + dy

        # If the cell is within the board and contains the player's piece
        if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == player:
            # Flip all the pieces in the list
            for x, y in pieces_to_flip:
                board[x][y] = player

def utility(board):
    # the utility function will return the difference between the number of pieces of the computer and the user
    return sum([item for sublist in board for item in sublist])

# create the alpha beta pruning algorithm
def alpha_beta_pruning(board, depth, alpha, beta, player):
    
    if depth == 0 or len(get_possible_moves(board, player)) == 0:
        return utility(board)
    if player == 1:
        v = float('-inf')
        for move in get_possible_moves(board, player):
            new_board = [row[:] for row in board]
            flip_pieces(new_board, move[0], move[1], player)
            v = max(v, alpha_beta_pruning(new_board, depth - 1, alpha, beta, -player))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = float('inf')
        for move in get_possible_moves(board, player):
            new_board = [row[:] for row in board]
            flip_pieces(new_board, move[0], move[1], player)
            v = min(v, alpha_beta_pruning(new_board, depth - 1, alpha, beta, -player))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    
# create the function to get the best move for the computer
def get_best_move(board, depth, player):
    best_move = None
    if player == 1:
        v = float('-inf')
        for move in get_possible_moves(board, player):
            new_board = [row[:] for row in board]
            flip_pieces(new_board, move[0], move[1], player)
            new_v = alpha_beta_pruning(new_board, depth - 1, float('-inf'), float('inf'), -player)
            if new_v > v:
                v = new_v
                best_move = move
    else:
        v = float('inf')
        for move in get_possible_moves(board, player):
            new_board = [row[:] for row in board]
            flip_pieces(new_board, move[0], move[1], player)
            new_v = alpha_beta_pruning(new_board, depth - 1, float('-inf'), float('inf'), -player)
            if new_v < v:
                v = new_v
                best_move = move
    return best_move

# create the function to check if the game is over
def is_game_over(board):
    return len(get_possible_moves(board, 1)) == 0 and len(get_possible_moves(board, -1)) == 0

# create the function to check who won the game
def get_winner(board):
    flat_board = [item for sublist in board for item in sublist]
    white_score = flat_board.count(1)
    black_score = flat_board.count(-1)
    if white_score > black_score:
        return 1
    elif black_score > white_score:
        return -1
    else:
        return 0
    
# create the function that we will call to make the computer move
def computer_move(difficulty ,board):

    move = get_best_move(board, difficulty, 1)
    if move is not None:
        board[move[0]][move[1]] = 1
        flip_pieces(board, move[0], move[1], 1)
        return True
    return False
