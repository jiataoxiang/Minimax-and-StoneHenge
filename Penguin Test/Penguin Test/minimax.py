"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
# Stack and Tree Class are lecture materials. Credit to CSC148 lecture.
from typing import Any
from copy import deepcopy

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.


def minimax_recursive_strategy(game: Any) -> Any:
    """
    Return a move for game that is much better than randomly choosed moves.
    """
    s_copy = deepcopy(game.current_state)
    moves = s_copy.get_possible_moves()
    game_score = []
    for move in moves:
        game_score.append(max_score(game, s_copy, move)*-1)
    return moves[game_score.index(max(game_score))]


def max_score(game: Any, state: Any, move: str) -> Any:
    """
    find the depth of the game
    """
    old_state = game.current_state
    s_copy = deepcopy(state)
    new_state = s_copy.make_move(move)
    if new_state.get_possible_moves() == []:
        game.current_state = new_state
        if (game.is_winner("p1") and not game.current_state.p1_turn) \
                or (game.is_winner("p2") and game.current_state.p1_turn):
            game.current_state = old_state
            return -1
        elif (game.is_winner("p1") and game.current_state.p1_turn) \
                or (game.is_winner("p2") and not game.current_state.p1_turn):
            game.current_state = old_state
            return 1
        game.current_state = old_state
        return 0

    return max([max_score(game, new_state, i) * -1
                for i in new_state.get_possible_moves()])

# TODO: Implement an iterative version of the minimax strategy.


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.

    Tree class is copied from lecture notes.
    """

    def __init__(self, value=None, children=None, score=None) -> None:
        """
        Create Tree self with content value and 0 or more children
        """
        self.value = value
        # copy children if not None
        self.children = children[:] if children is not None else []
        self.score = score


class Stack:
    """
    Last-in, first-out (LIFO) stack.

    Stack class is copied from lecture notes
    """

    def __init__(self) -> None:
        """
        Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contents = []

    def add(self, obj: object) -> None:
        """
        Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(7)
        """
        self._contents.append(obj)

    def remove(self) -> Tree:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not empty.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contents.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(7)
        >>> s.is_empty()
        False
        """
        return len(self._contents) == 0


def minimax_iterative_strategy(game: Any) -> Any:
    """
    iterative minimax
    """
    s_copy = deepcopy(game.current_state)
    tree_state = Tree(s_copy)
    s = Stack()
    s.add(tree_state)
    while not s.is_empty():
        state = s.remove()
        # if state still have move, we can't set score
        if not game.is_over(state.value):
            # if children is not None, set the score as maxmum of child score
            check_children(state, s)
        # if state is over, set the score -1
        else:
            old_state = game.current_state
            game.current_state = state.value
            if (game.is_winner("p1") and not game.current_state.p1_turn) \
                    or (game.is_winner("p2") and game.current_state.p1_turn):
                game.current_state = old_state
                state.score = -1
            elif (game.is_winner("p1") and game.current_state.p1_turn) \
                    or(game.is_winner("p2") and not game.current_state.p1_turn):
                game.current_state = old_state
                state.score = 1
            else:
                game.current_state = old_state
                state.score = 0
    final_score = []
    final_moves = game.current_state.get_possible_moves()
    for child in tree_state.children:
        final_score.append(child.score*-1)
    index = final_score.index(max(final_score))
    return final_moves[index]


def check_children(state: Tree, s: Stack) -> None:
    """
    check whether is empty
    """
    if state.children != []:
        score = []
        # get the maximum score * -1
        for child in state.children:
            score.append(child.score * -1)
        state.score = max(score)
    # if children is None, we need set their childen
    else:
        moves = state.value.get_possible_moves()
        for move in moves:
            copy_state = deepcopy(state)
            state.children.append(Tree(copy_state.value.make_move(move)))
        s.add(state)
        for i in state.children:
            s.add(i)


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
