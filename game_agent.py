"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))

    return float(abs(my_location[0] - opponent_location[0]) + abs(my_location[1] - opponent_location[1]))

def custom_score_not_submitted(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))

    center = (2, 2)

    score = 0
    my_distance_from_center = (my_location[0] - center[0]) ** 2 - (my_location[1] - center[1]) ** 2
    opponent_distance_from_center = (opponent_location[0] - center[0]) ** 2 - (opponent_location[1] - center[1]) ** 2

    if opponent_distance_from_center > my_distance_from_center:
        score += 1
    else:
        score -= 1

    return score


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    move_count = game.move_count

    w = 10 / (move_count + 1)

    # count number of moves available
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - (w * opp_moves))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    score = .0
    total_spaces = game.width * game.height
    remaining_spaces = len(game.get_blank_spaces())
    coefficient = float(total_spaces - remaining_spaces) / float(total_spaces)

    my_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    for move in my_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or
                           move[1] == 0 or move[1] == game.height - 1) else 0
        score += 1 - coefficient * isNearWall

    for move in opponent_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or
                           move[1] == 0 or move[1] == game.height - 1) else 0
        score -= 1 - coefficient * isNearWall

    return score


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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
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

    def _min_value(self, game, depth):
        """
        Get the min value
        :param game:
        :param depth:
        :return: min_value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        min_value = float("inf")

        if self._test_terminal_condition(game, depth):
            return self.score(game, self)

        all_legal_moves = game.get_legal_moves()

        for move in all_legal_moves:
            next_move = game.forecast_move(move)
            min_value = min(min_value, self._max_value(next_move, depth - 1))

        return min_value

    def _max_value(self, game, depth):
        """
        Get the Max value
        :param game:
        :param depth:
        :return: max_value
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        max_value = float("-inf")

        if self._test_terminal_condition(game, depth):
            return self.score(game, self)

        all_legal_moves = game.get_legal_moves()

        for move in all_legal_moves:
            next_move = game.forecast_move(move)
            max_value = max(max_value, self._min_value(next_move, depth - 1))

        return max_value

    def _test_terminal_condition(self, game, depth):
        """
        Check if the game is in terminal state
        :param game:
        :param depth:
        :return:bool
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth > 0 and len(game.get_legal_moves()) > 0:
            return False
        else:
            return True

    def minimax(self, game, depth):
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

        best_move = (-1, -1)

        all_legal_moves = game.get_legal_moves()

        if not all_legal_moves:
            return best_move

        all_values = [(self._min_value(game.forecast_move(move), depth - 1), move) for move in all_legal_moves]

        return max(all_values)[1]


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def _min_value(self, game, depth, alpha, beta):
        """
        :param game:
        :param depth:
        :param alpha:
        :param beta:
        :return: min_value
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)

        if self._test_terminal_condition(game, depth):
            return self.score(game, self), best_move

        min_value = float("inf")

        all_legal_moves = game.get_legal_moves()

        for move in all_legal_moves:
            current_value = self._max_value(game.forecast_move(move), depth - 1, alpha, beta)

            if current_value[0] < min_value :
                min_value = current_value[0]
                best_move = move

            if min_value <= alpha:
                return min_value, best_move

            beta = min(beta, min_value)

        return min_value, best_move

    def _max_value(self, game, depth, alpha, beta):
        """
        :param game:
        :param depth:
        :param alpha:
        :param beta:
        :return: max_value
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)

        if self._test_terminal_condition(game, depth):
            return self.score(game, self), best_move

        max_value = float("-inf")

        all_legal_moves = game.get_legal_moves()

        for move in all_legal_moves:
            current_value = self._min_value(game.forecast_move(move), depth - 1, alpha, beta)

            if current_value[0] > max_value:
                max_value = current_value[0]
                best_move = move

            if max_value >= beta:
                return max_value, best_move

            alpha = max(alpha, max_value)

        return max_value, best_move

    def _test_terminal_condition(self, game, depth):
        """
        Check if the game is in terminal state
        :param game:
        :param depth:
        :return:bool
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth > 0 and len(game.get_legal_moves()) > 0:
            return False
        else:
            return True

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

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = first_best_move = (-1, -1)

        all_legal_moves = game.get_legal_moves()

        if len(all_legal_moves) > 0:
            best_move = all_legal_moves[random.randint(0, len(all_legal_moves) - 1)]

        try:

            depth = 1

            while True:

                move = self.alphabeta(game, depth)

                if move == first_best_move:
                    return best_move
                else:
                    best_move = move

                depth = depth + 1

        except SearchTimeout:

            return best_move

        return best_move

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

        if depth == 0:
            return self.score(game, self), (-1, -1)

        return self._max_value(game, depth, alpha, beta)[1]