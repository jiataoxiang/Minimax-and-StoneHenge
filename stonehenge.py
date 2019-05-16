"""
module for stonehenge game
"""
from game import Game
from game_state import GameState


class Stonehenge(Game):
    """
    Abstract class for Stonehenge game to be played with two players.
    """
    def __init__(self, p1_starts: bool):
        """
        Initiate game stonehenge
        """
        self.p1_starts = p1_starts
        self.sidelength = int(input("Enter a side length of the game: "))
        self.current_state = StonehengeState(p1_starts)
        n = 0
        while n != self.sidelength * (self.sidelength + 5)/2:
            self.current_state.cell.append(chr(65 + n))
            n += 1
        i = 0
        while i < ((self.sidelength + 1) * 3):
            self.current_state.leyline.append("@")
            i += 1

    def get_instructions(self) -> str:
        """
        Return the instructions for game StoneHenge.
        """
        instruction = """When a player captures at least half of the cells in
         a ley-line, then the player get the ley-lines. The first player get 
         at least half of the ley-lines is the winner"""
        return instruction

    def is_over(self, state: GameState) -> bool:
        """
        Return whether or not this game is over at state.
        """
        if (state.leyline.count("1") >= (len(state.leyline) / 2)
                or state.leyline.count("2") >= (len(state.leyline) / 2)):
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        num1 = 0
        num2 = 0
        for i in self.current_state.leyline:
            if i == "1":
                num1 += 1
            elif i == "2":
                num2 += 1
        if num1 >= (len(self.current_state.leyline) * 0.5) and player == "p1":
            return True
        elif num2 >= (len(self.current_state.leyline) * 0.5) and player == "p2":
            return True
        return False

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        return string.strip()


class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    def __init__(self, is_p1_turn: bool, cell=None, line=None) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        self.capital = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        GameState.__init__(self, is_p1_turn)
        self.cell = [] if cell is None else cell
        self.leyline = [] if line is None else line

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        e = int(((2 * (len(self.cell)) + 25 / 4) ** 0.5) - 5 / 2)
        n = e
        b = 2
        times = 0
        leyline = 0
        s = " " * (2 * (e-1) + 6)
        s += "{}   {}\n".format(self.leyline[3 * (e + 1) - 1],
                                self.leyline[3 * (e + 1) - 2])
        s += " " * (2 * (e-1) + 5)
        s += "/   /\n"
        while n != 0:
            s += " " * 2 * (e + 1 - b)
            s += "{}".format(self.leyline[leyline])
            for i in range(b):
                s += " - {}".format(self.cell[times + i])
            s += " " * 3
            s += self.leyline[3 * (e + 1) - 3 - leyline] if b != e + 1 else ""
            s += "\n   "
            s += " " * 2 * (e + 1 - b)
            if b != e + 1:
                for i in range(b):
                    s += "/ \\ "
                s += "/"
                s += "\n"
            else:
                s += " " * 2
                for i in range(b - 1):
                    s += "\\ / "
                s += "\\"
                s += "\n"
            times += b
            b += 1
            n -= 1
            leyline += 1
        s += " " * 2
        s += self.leyline[e]
        for i in range(b - 2):
            s += " - {}".format(self.cell[i + times])
        s += " " * 3
        s += self.leyline[(e+1)*2 - 1]
        s += "\n"
        s += " " * 4
        for i in range(b - 2):
            s += "   \\"
        s += "\n"
        s += " " * 5
        for i in range(b - 2):
            s += "   {}".format(self.leyline[e+i + 1])
        return s

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        moves = []
        if (self.leyline.count("1") >= len(self.leyline)/2
                or self.leyline.count("2") >= len(self.leyline)/2):
            return moves
        for i in range(len(self.cell)):
            if self.cell[i] != "1" and self.cell[i] != "2":
                moves.append(self.cell[i])
        return moves

    def test_horizontal(self, cell, leyline) -> None:
        """
        find who occupied horizontal leylines.
        """
        size = int(((2 * (len(cell)) + 25 / 4) ** 0.5) - 5 / 2)
        ley_line1 = []
        for n in range(size):
            ley_line1.append(cell[size * (size + 5) // 2 - n - 1])
        if ley_line1.count("1") >= len(ley_line1) / 2:
            if leyline[size] != "2":
                leyline[size] = "1"
        elif ley_line1.count("2") >= len(ley_line1) / 2:
            if leyline[size] != "1":
                leyline[size] = "2"
        b = size + 1
        ley_line1 = []
        while b != 1:
            for n in range(b):
                ley_line1.append(cell[(b - 1) * (b + 2) // 2 - n - 1])
            if ley_line1.count("1") >= len(ley_line1) / 2:
                if ley_line1[b - 2] != "2":
                    leyline[b - 2] = "1"
            elif ley_line1.count("2") >= len(ley_line1) / 2:
                if leyline[b - 2] != "1":
                    leyline[b - 2] = "2"
            ley_line1 = []
            b -= 1

    def test_upward(self, cell, leyline) -> None:
        """
        find who occupied upward leylines.
        """
        size = int(((2 * (len(cell)) + 25 / 4) ** 0.5) - 5 / 2)
        ley_line1 = []
        for n in range(size):
            ley_line1.append(cell[(n + 2) * (n + 1) // 2 - 1])
        if ley_line1.count("1") >= len(ley_line1) / 2:
            if leyline[(size + 1) * 3 - 1] != "2":
                leyline[(size + 1) * 3 - 1] = "1"
        elif ley_line1.count("2") >= len(ley_line1) / 2:
            if leyline[(size + 1) * 3 - 1] != "1":
                leyline[(size + 1) * 3 - 1] = "2"
        b = size + 1
        j = 1
        ley_line1 = []
        i = 0
        while b != 1:
            ley_line1.append(cell[(size + 1) * (size + 2) // 2 - 1 + i])
            for n in range(b - 1):
                ley_line1.append(cell[(n + 2 + i) * (n + 1 + i) // 2 - 1 + j])
            if ley_line1.count("1") >= len(ley_line1) / 2:
                if leyline[(size + 1) * 3 - 1 - j] != "2":
                    leyline[(size + 1) * 3 - 1 - j] = "1"
            elif ley_line1.count("2") >= len(ley_line1) / 2:
                if leyline[(size + 1) * 3 - 1 - j] != "1":
                    leyline[(size + 1) * 3 - 1 - j] = "2"
            ley_line1 = []
            b -= 1
            j += 1
            i += 1

    def test_downward(self, cell, leyline) -> None:
        """
        find who occupied downward leylines.
        """
        size = int(((2 * (len(cell)) + 25 / 4) ** 0.5) - 5 / 2)
        ley_line1 = []
        for n in range(size):
            ley_line1.append(cell[(n + 1) * (n + 4) // 2 - 1])
        if ley_line1.count("1") >= len(ley_line1) / 2:
            if leyline[(size + 1) * 2 - 1] != "2":
                leyline[(size + 1) * 2 - 1] = "1"
        elif ley_line1.count("2") >= len(ley_line1) / 2:
            if leyline[(size + 1) * 2 - 1] != "1":
                leyline[(size + 1) * 2 - 1] = "2"
        b = size + 1
        j = 1
        ley_line1 = []
        i = 0
        while b != 1:
            ley_line1.append(cell[size * (size + 5) // 2 - j])
            for n in range(b - 1):
                ley_line1.append(cell[(n + 1 + i) * (n + 4 + i) // 2 - 1 - j])
            if ley_line1.count("1") >= len(ley_line1) / 2:
                if leyline[(size + 1) * 2 - 1 - j] != "2":
                    leyline[(size + 1) * 2 - 1 - j] = "1"
            elif ley_line1.count("2") >= len(ley_line1) / 2:
                if leyline[(size + 1) * 2 - 1 - j] != "1":
                    leyline[(size + 1) * 2 - 1 - j] = "2"
            ley_line1 = []
            i += 1
            b -= 1
            j += 1

    def make_move(self, move: str) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        cell = self.cell.copy()
        leyline = self.leyline.copy()
        for i in range(len(cell)):
            if cell[i] == move:
                cell[i] = "1" if self.p1_turn else "2"
        if self.p1_turn is True:
            p1_turn = False
        else:
            p1_turn = True
        # test horizontal leylines
        self.test_horizontal(cell, leyline)
        # test downward leylines
        self.test_downward(cell, leyline)
        # test upwards leylines
        self.test_upward(cell, leyline)
        return StonehengeState(p1_turn, cell, leyline)

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return self.__str__() + "\n p1's turn: {}".format(self.p1_turn)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        # over state
        if self.leyline.count("1") >= len(self.leyline)/2 and self.p1_turn:
            return self.WIN
        elif self.leyline.count("1") >= len(self.leyline)/2 \
                and not self.p1_turn:
            return self.LOSE
        elif self.leyline.count("2") >= len(self.leyline)/2 and self.p1_turn:
            return self.LOSE
        elif self.leyline.count("2") >= len(self.leyline)/2 \
                and not self.p1_turn:
            return self.WIN
        # not over
        for i in self.get_possible_moves():
            g = self
            k = g.make_move(i)
            if self.p1_turn:
                if k.leyline.count("1") >= len(k.leyline)/2:
                    return self.WIN
            elif not self.p1_turn:
                if k.leyline.count("2") >= len(k.leyline)/2:
                    return self.WIN
        # return LOSE situation
        times = 0
        for i in self.get_possible_moves():
            k = self.make_move(i)
            for b in k.get_possible_moves():
                g = k.make_move(b)
                if g.get_possible_moves() == []:
                    times += 1
        if times == len(self.get_possible_moves()):
            return self.LOSE
        return self.DRAW


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
