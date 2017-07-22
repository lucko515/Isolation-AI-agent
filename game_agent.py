"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass



def custom_score(game, player):
    """The idea is to reward agent by giving it rewards on position of the legal moves on the board
    If position is the center agent will recieve the biggest reward, for every circle further from center
    agent is recieving less and less points.

    If number of possible moves are all close to the center agent will have big reward.

    In this Heuristic we are doing that for both us and opponent player, the idea is to maximize our score over opponents
    by having more positions close to center.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    #checking if we have a winner
    if game.is_loser(player):
        return -1e500

    if game.is_winner(player):
        return 1e500

    #Getting legal moves for our opponent and for our player
    player_legal_moves = game.get_legal_moves(player)
    opponent_legal_moves = game.get_legal_moves(game.get_opponent(player))
    #setting scores for our opponent and for us to 0
    score = 0
    score_opp = 0

    #going through all legal moves for our player and collecting score per move
    for move in player_legal_moves:
        #Check if move is in center:
        if move == (3, 3):
            score += 10
        #firs circle around center
        elif move in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]:
            score += 6
        #second circle around center
        elif move in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 5), (3, 1), (3, 5), (4, 1), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]:
            score += 4
        #edges
        else:
            score += 2

    #Going through all legal moves for our opponent and collecting score per move
    for move in opponent_legal_moves:
        #Check if move is in center:
        if move == (3, 3):
            score_opp += 10
        elif move in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]:
            score_opp += 6
        elif move in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 5), (3, 1), (3, 5), (4, 1), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]:
            score_opp += 4
        else:
            score_opp += 2

    return float(score - score_opp)




def custom_score_2(game, player):
    """ The goal of this heuristic is to check how many moves our opponent will have after we play cirtain move
    by the rule of Isolation we want to minimize this number.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    #Checking if we have the winner yet
    if game.is_loser(player):
        return -1e500

    if game.is_winner(player):
        return 1e500

    #getting list of all legal moves for OUR plyer
    legal_moves = game.get_legal_moves(player)

    #setting some value to be default value
    #We need to minimize this number so any big number which is not realistic will work
    best_value = 100

    #Going through list of legal moves for our player
    for move in legal_moves:
        #getting state of the board if we perform that move
        one_move_to_futre = game.forecast_move(move)
        #getting legal moves for a opponent according to the new state
        one_move_to_futre_legal_moves = one_move_to_futre.get_legal_moves(game.get_opponent(player))
        #checking if number of those moves are less then current best value, if yes we change best_value to number of those moves
        if len(one_move_to_futre_legal_moves) < best_value:
            best_value = len(one_move_to_futre_legal_moves)

    return float(best_value)


def custom_score_3(game, player):
    """ 
    The idea is to reward agent by giving it rewards on position of the legal moves on the board
    If position is the center agent will recieve the biggest reward, for every circle further from center
    agent is recieving less and less points.

    If number of possible moves are all close to the center agent will have big reward.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    #Checking if we have a winner
    if game.is_loser(player):
        return -1e500

    if game.is_winner(player):
        return 1e500

    #Getting list of all legal moves for our player
    player_legal_moves = game.get_legal_moves(player)
    opponent_legal_moves = game.get_legal_moves(game.get_opponent(player))
    #The score is set to be 0 as default
    score = 0
    score_opp = 0

    #Going through all possible moves
    for move in player_legal_moves:

        if move in opponent_legal_moves:
            score += 10
        else:
            score -= 1

    for move in opponent_legal_moves:

        if move in player_legal_moves:
            score_opp -=10
        else:
            score_opp += 1
    # for move in player_legal_moves:
    #     #Check if move is in center:
    #     if move == (3, 3):
    #         score += 10
    #     #This check is for the places around the center position
    #     elif move in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]:
    #         score += 6
    #     #Second circle from center 
    #     elif move in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 5), (3, 1), (3, 5), (4, 1), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]:
    #         score += 4
    #     #All to the edges
    #     else:
    #         score += 2

    return float(score - score_opp)


def custom_score_4(game, player):
    """This eval function is mentioned in the classes
    By subtracting number of our moves by 2 times opponent moves we are chasing him by trying to minimize that difference

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    #This logic is used to check if we have winner of looser
    if game.is_loser(player):
        return -1e500
    if game.is_winner(player):
        return 1e500

    #We first get number of possible moves for our player
    player_legal_moves = len(game.get_legal_moves(player))
    #Then we get number of possible moves for opponent player
    opponent_legal_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(player_legal_moves - 2*opponent_legal_moves)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score_3, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def minimax_helper(self, game, depth, max_player=True):
        """Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int - number which represents to what depth should we search our game tree

        max_player: boolean - to represent which player is currently on the move (considering our game tree)

        Returns
        -------
        best_value - float value which represent the best_value which is on the node of the best_move to be performed

        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Checking if we came to depth of zero, in that case we back-proped to the root and we are ready to value our position
        #For valuing we are using our heuristic functions, and we return -1, -1  as NaN value for our move  
        if depth == 0:
            return self.score(game, self), (-1, -1)

        #If lenght of list of legal moves is 0 we return  utility, witch iz -inf for MIN player, MAX player will have +inf in case of winning
        # or we return 0. if non of players won
        if len(game.get_legal_moves()) == 0:
            return game.utility(self), (-1, -1)

        #Setting default values for the best move
        best_move = (-1, -1)
        best_value = 0

        #We are setting WORST cases values for our best_value variable
        #NOTE: I've used 1e500 to represent infinity value in the code
        #       It is kinda hardcoded in another way to represent it, we can use float('-inf') or float('inf')
        if max_player:
            best_value = -1e500
        else:
            best_value = 1e500
        
        #Getting list of all legal moves
        list_of_moves = game.get_legal_moves()

        #The meat of the minimax function
        #We iterate through all legal moves from our list
        for move in list_of_moves:
            #creating 'new state' for our game, which is just look of our board when we perform move
            new_state = game.forecast_move(move)
            #calling recursively minimax_helper function on new_state, decresing our depth by one and using oposite value for our max_player agrument
            current_val, _ = self.minimax_helper(new_state, depth-1, not max_player)

            #This is logic if MAX is currently on the move
            if max_player:
                #getting temp value which will be max of current best_value and calculated value from recursive call
                temp_value = max(best_value, current_val)
                #if temp value choose current_val to be max, temp_value will be differnt to best_value (-inf)
                if temp_value != best_value:
                    #Setting new values for our best_value and new value for best_move
                    best_value, best_move = current_val, move

            #This is logic for MIN player      
            else:
                temp_value = min(best_value, current_val)
                if temp_value != best_value:
                    best_value, best_move = current_val, move

        return best_value, best_move

    def minimax(self, game, depth, max_player=True):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Calling helper function for minimax algo
        best_value, best_move = self.minimax_helper(game, depth, max_player)
        return best_move



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        
        best_move = None

        #First check if we have legal moves to perform
        #This will assure to return some value if  there is no moves to be performed
        if len(game.get_legal_moves()) == 0:
            best_move = (-1, -1)
            return best_move

        try:
            
            #Iterative deepening
            #Setting depth to 0 for start of iterative deepening
            depth = 0
            #using while True to represent infinity loop
            #loop will be stopped when time for the turn runs out
            while True:
                #calling alphabeta function on current game state and depth
                move = self.alphabeta(game, depth)
                #setting new value for best_move to be the best move return by alphabeta algorithm
                best_move = move
                #increasing the depth by one
                depth += 1
               
            print(depth) 

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move



    def alphabeta_helper(self, game, depth, alpha, beta, max_player):
        """Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int - number which represents to what depth should we search our game tree

        alpha - best already explored option along path to the root for maximizer

        beta - best already explored option along path to the root for minimizer

        max_player: boolean - to represent which player is currently on the move (considering our game tree)

        Returns
        -------
        best_value - float value which represent the best_value which is on the node of the best_move to be performed

        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Setting default value to (-1, -1) as our 
        best_move = (-1, -1)
        
        #Checking if we came to depth of zero, in that case we back-proped to the root and we are ready to value our position
        #For valuing we are using our heuristic functions, and we return -1, -1  as NaN value for our move  
        if depth == 0:
            return self.score(game, self), best_move

        #If lenght of list of legal moves is 0 we return  utility, witch iz -inf for MIN player, MAX player will have +inf in case of winning
        # or we return 0. if non of players won
        if len(game.get_legal_moves()) == 0:
            return game.utility(self), best_move

        best_value = 0

        #We are setting WORST cases values for our best_value variable
        #NOTE: I've used 1e500 to represent infinity value in the code
        #       It is kinda hardcoded in another way to represent it, we can use float('-inf') or float('inf')
        if max_player:
            best_value = -1e500
        else:
            best_value = 1e500

        #Getting list of all legal moves
        list_of_moves = game.get_legal_moves()

        #The meat of the minimax function
        #We iterate through all legal moves from our list
        for move in list_of_moves:
            #creating 'new_state' which is look of our gameboard after some move is performed
            new_state = game.forecast_move(move)
            #recursively calling alphabeta_player with new_state created, depth decreased by one and opposite value of the current one for max_player arg
            current_val, _ = self.alphabeta_helper(new_state, depth-1, alpha, beta, not max_player)

            #this logic is for MAX player
            if max_player:
                #getting temp value which will be max of current best_value and calculated value from recursive call
                temp_value = max(best_value, current_val)
                #if temp value choose current_val to be max, temp_value will be differnt to best_value (-inf)               
                if temp_value != best_value:
                    #setting new value for best_value and best_move
                    best_value, best_move = current_val, move
                
                #checking if beta is less or equal to best_value (value on the node)
                #If that is the case we can safely break from the loop and not loop to dipper parts of the tree in that direction
                if beta <= best_value:
                    break
                #setting new values for alpha, max value between -inf (default one) and bet_value
                alpha = max(alpha, best_value)

            #This logic is for MIN player
            else:
                temp_value = min(best_value, current_val)
                if temp_value != best_value:
                    best_value, best_move = current_val, move
                
                #checking if alpha is bigger or equal to best_value (value on the node)
                #If that is the case we can safely break from the loop and not loop to dipper parts of the tree in that direction
                if alpha >= best_value:
                    break

                #setting new values for beta, min value between -inf (default one) and bet_value
                beta = min(beta, best_value)

        return best_value, best_move




    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #calling alphabeta helper function
        best_value, best_move = self.alphabeta_helper(game, depth, alpha, beta, True)
        
        return best_move
