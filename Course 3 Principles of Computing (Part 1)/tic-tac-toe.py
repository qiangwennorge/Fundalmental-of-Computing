"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    The function plays a game starting with the given player by making random moves, 
    alternating between players. 
    Function modifies the board input.
    """
    empty_squares = board.get_empty_squares()
    while not board.check_win():
        random_selection = random.randrange(len(empty_squares))
        board.move(empty_squares[random_selection][0], empty_squares[random_selection][1], player)
        player = provided.switch_player(player)
        

def mc_update_scores(scores, board, player): 
    """
    The function scores the completed board 
    and updates the scores grid. 
    """
    winner = board.check_win()
    for _row in range(board.get_dim()):
        for _col in range(board.get_dim()):
            if winner == provided.PLAYERX:
                if board.square(_row, _col) == provided.PLAYERX:
                    scores[_row][_col] += SCORE_CURRENT
                elif board.square(_row, _col) == provided.PLAYERO:
                    scores[_row][_col] -= SCORE_OTHER
            elif winner == provided.PLAYERO:
                if board.square(_row, _col) == provided.PLAYERX:
                    scores[_row][_col] -= SCORE_CURRENT
                elif board.square(_row, _col) == provided.PLAYERO:
                    scores[_row][_col] += SCORE_OTHER


def get_best_move(board, scores):
    """
    The function finds all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.
    """
    empty_squares = board.get_empty_squares()
    scores_dict = {}
    for square in empty_squares:
        scores_dict[square] = scores[square[0]][square[1]]
    max_score = max(scores_dict.values())
    max_scores_list = [x for x,y in scores_dict.items() 
                       if y == max_score]
    choice = random.randrange(len(max_scores_list))
    return max_scores_list[choice]


def mc_move(board, player, trials): 
    """
    The function uses the Monte Carlo simulation to return
    a move for the machine player in the form of a (row, column) tuple. 
    """
    scores = [[0 * col * row for col in range(board.get_dim())] for row in range(board.get_dim())]
    for dummy_trial in range(trials):
        cloned_board = board.clone()
        mc_trial(cloned_board, player)
        mc_update_scores(scores, cloned_board, player)  
    return get_best_move(board, scores)  



# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
