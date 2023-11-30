import copy


class Player:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def set_pos(self, state):
        new_board = state.board
        not_set = True
        while not_set:
            yval = int(input("Give row:")) - 1
            xval = int(input("Give col:")) - 1
            if (
                xval > state.game.size - 1
                or yval > state.game.size - 1
                or xval * yval < 0
            ):
                print("Index out of the board size")
            elif new_board[yval][xval] == 0:
                break
            else:
                print("Space is already taken")

        new_board[yval][xval] = self.symbol
        return new_board


class State:
    def __init__(self, game, board):
        self.board = board
        self.game = game

        self.p1_weak_1 = 0
        self.p1_strong_1 = 0

        self.p1_weak_2 = 0
        self.p1_strong_2 = 0

        self.p2_weak_1 = 0
        self.p2_strong_1 = 0

        self.p2_weak_2 = 0
        self.p2_strong_2 = 0

        self.winner = None
        self.check_state()

    def draw(self):
        for num1, row in enumerate(self.board):
            row1 = []
            for num2, el in enumerate(row):
                if el != 0:
                    row1.append(el)
                else:
                    row1.append(" ")
                if num2 != self.game.size - 1:
                    row1.append("|")
            print(*row1)
            if num1 != self.game.size - 1:
                print(*["-" for x in range(2 * self.game.size - 1)])

        if self.winner is not None:
            if self.winner == "Draw":
                print("There is a draw")
            else:
                print(f"The winner is: {self.winner.symbol}")
        print("\n")

    def check_row(self, row):
        first = None
        counter = 1
        freeze = 0
        size = len(self.board)
        was_freezed = False
        for num in range(len(row[:-1])):
            if freeze != 0:
                freeze -= 1
            elif row[num] == row[num + 1] and row[num] != 0:
                counter += 1
                if (counter == size) or (size > 3 and counter == 4):
                    if row[num] == self.game.p1_s:
                        self.winner = self.game.players[0]
                    else:
                        self.winner = self.game.players[1]
                    return 1
                continue
            elif (
                row[num] != 0
                and row[num + 1] == 0
                and num + 2 < len(row[:-1])
                and row[num] == row[num + 2]
            ):
                counter += 1
                freeze = 2
                was_freezed = True
            elif row[num] != row[num + 1]:
                if (counter == size - 1) or (size > 3 and counter == 3):  # 1 brakuje
                    if first == 0 and row[num + 1] == 0:
                        if row[num] == self.game.p1_s and not was_freezed:
                            self.p1_strong_1 += 1
                        else:
                            self.p2_strong_1 += 1
                    elif first == 0 or row[num + 1] == 0:
                        if row[num] == self.game.p1_s:
                            self.p1_weak_1 += 1
                        else:
                            self.p2_weak_1 += 1

                elif size > 3 and counter == 2:  # 2 brakuje
                    if first == 0 and row[num + 1] == 0 and not was_freezed:
                        if row[num] == self.game.p1_s:
                            self.p1_strong_2 += 1
                        else:
                            self.p2_strong_2 += 1
                    elif first == 0 or row[num + 1] == 0:
                        if row[num] == self.game.p1_s:
                            self.p1_weak_2 += 1
                        else:
                            self.p2_weak_2 += 1

                elif counter == 1:
                    first = row[num]
                if freeze == 0:
                    counter = 1

    def check_column(self, col):
        size = len(self.board)
        first = None
        counter = 1
        freeze = 0
        was_freezed = False
        for row in range(size - 1):
            if freeze != 0:
                freeze -= 1
            elif (
                self.board[row][col] == self.board[row + 1][col]
                and self.board[row][col] != 0
            ):
                counter += 1
                if (counter == size) or (size > 3 and counter == 4):
                    if self.board[row][col] == self.game.p1_s:
                        self.winner = self.game.players[0]
                    else:
                        self.winner = self.game.players[1]
                    return 1
                continue
            elif (
                self.board[row][col] != 0
                and self.board[row + 1][col] == 0
                and row + 2 < size - 1
                and self.board[row][col] == self.board[row + 2][col]
            ):
                counter += 1
                freeze = 2
                was_freezed = True
            elif self.board[row][col] != self.board[row + 1][col]:
                if (counter == size - 1) or (size > 3 and counter == 3):  # 1 brakuje
                    if first == 0 and self.board[row + 1][col] == 0 and not was_freezed:
                        if self.board[row][col] == self.game.p1_s:
                            self.p1_strong_1 += 1
                        else:
                            self.p2_strong_1 += 1
                    elif first == 0 or self.board[row + 1][col] == 0:
                        if self.board[row][col] == self.game.p1_s:
                            self.p1_weak_1 += 1
                        else:
                            self.p2_weak_1 += 1

                elif size > 3 and counter == 2:  # 2 brakuje
                    if first == 0 and self.board[row + 1][col] == 0 and not was_freezed:
                        if self.board[row][col] == self.game.p1_s:
                            self.p1_strong_2 += 1
                        else:
                            self.p2_strong_2 += 1
                    elif first == 0 or self.board[row + 1][col] == 0:
                        if self.board[row][col] == self.game.p1_s:
                            self.p1_weak_2 += 1
                        else:
                            self.p2_weak_2 += 1

                elif counter == 1:
                    first = self.board[row][col]
                counter = 1

    def check_first_diag(self):
        size = len(self.board)
        for j in range(size - 2):
            first = None
            counter = 1
            freeze = 0
            was_freezed = False
            for i in range(size - 1 - j):
                fir = i + j
                sec = i
                if freeze != 0:
                    freeze -= 1
                elif (
                    self.board[fir][sec] == self.board[fir + 1][sec + 1]
                    and self.board[fir][sec] != 0
                ):
                    counter += 1
                    if (counter == size) or (size > 3 and counter == 4):
                        if self.board[fir][sec] == self.game.p1_s:
                            self.winner = self.game.players[0]
                        else:
                            self.winner = self.game.players[1]
                        return 1
                    continue
                elif (
                    self.board[fir][sec] != 0
                    and self.board[fir + 1][sec + 1] == 0
                    and sec + 2 < size - 1 - j
                    and fir + 2 < size - 1
                    and self.board[fir][sec] == self.board[fir + 2][sec + 2]
                ):
                    counter += 1
                    freeze = 2
                    was_freezed = True
                elif self.board[fir][sec] != self.board[fir + 1][sec + 1]:
                    if (counter == size - 1) or (
                        size > 3 and counter == 3
                    ):  # 1 brakuje
                        if (
                            first == 0
                            and self.board[fir + 1][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_strong_1 += 1
                            else:
                                self.p2_strong_1 += 1
                        elif first == 0 or self.board[fir + 1][sec + 1] == 0:
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_weak_1 += 1
                            else:
                                self.p2_weak_1 += 1

                    elif size > 3 and counter == 2:  # 2 brakuje
                        if (
                            first == 0
                            and self.board[fir + 1][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_strong_2 += 1
                            else:
                                self.p2_strong_2 += 1
                        elif first == 0 or self.board[fir + 1][sec + 1] == 0:
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_weak_2 += 1
                            else:
                                self.p2_weak_2 += 1

                    elif counter == 1:
                        first = self.board[fir][sec]
                    counter = 1

        counter = 1
        for j in range(1, size - 2):
            counter = 1
            first = None
            freeze = 0
            was_freezed = False
            for i in range(size - 1 - j):
                fir = i
                sec = i + j
                if freeze != 0:
                    freeze -= 1
                elif (
                    self.board[fir][sec] == self.board[fir + 1][sec + 1]
                    and self.board[fir][sec] != 0
                ):
                    counter += 1
                    if (counter == size) or (size > 3 and counter == 4):
                        if self.board[fir][sec] == self.game.p1_s:
                            self.winner = self.game.players[0]
                        else:
                            self.winner = self.game.players[1]
                        return 1
                    continue
                elif (
                    self.board[fir][sec] != 0
                    and self.board[fir + 1][sec + 1] == 0
                    and fir + 2 < size - 1 - j
                    and sec + 2 < size - 1
                    and self.board[fir][sec] == self.board[fir + 2][sec + 2]
                ):
                    counter += 1
                    freeze = 2
                    was_freezed = True
                elif self.board[fir][sec] != self.board[fir + 1][sec + 1]:
                    if (counter == size - 1) or (
                        size > 3 and counter == 3
                    ):  # 1 brakuje
                        if (
                            first == 0
                            and self.board[fir + 1][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_strong_1 += 1
                            else:
                                self.p2_strong_1 += 1
                        elif first == 0 or self.board[fir + 1][sec + 1] == 0:
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_weak_1 += 1
                            else:
                                self.p2_weak_1 += 1

                    elif size > 3 and counter == 2:  # 2 brakuje
                        if (
                            first == 0
                            and self.board[fir + 1][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_strong_2 += 1
                            else:
                                self.p2_strong_2 += 1
                        elif first == 0 or self.board[fir + 1][sec + 1] == 0:
                            if self.board[fir][sec] == self.game.p1_s:
                                self.p1_weak_2 += 1
                            else:
                                self.p2_weak_2 += 1

                    elif counter == 1:
                        first = self.board[fir][sec]
                    counter = 1

    def check_second_diag(self):
        size = len(self.board)
        for j in range(size - 2):
            counter = 1
            freeze = 0
            first = None
            was_freezed = False
            for i in range(size - 1 - j):
                fir = i + j
                sec = i
                if freeze != 0:
                    freeze -= 1
                elif (
                    self.board[size - 1 - fir][sec]
                    == self.board[size - 2 - fir][sec + 1]
                    and self.board[size - 1 - fir][sec] != 0
                ):
                    counter += 1
                    if (counter == size) or (size > 3 and counter == 4):
                        if self.board[size - 1 - fir][sec] == self.game.p1_s:
                            self.winner = self.game.players[0]
                        else:
                            self.winner = self.game.players[1]
                        return 1
                    continue
                elif (
                    self.board[size - 1 - fir][sec] != 0
                    and self.board[size - 2 - fir][sec + 1] == 0
                    and size - 3 - fir > 0
                    and sec + 2 < size
                    and self.board[size - 1 - fir][sec]
                    == self.board[size - 3 - fir][sec + 2]
                ):
                    counter += 1
                    freeze = 2
                    was_freezed = True
                elif (
                    self.board[size - 1 - fir][sec]
                    != self.board[size - 2 - fir][sec + 1]
                ):
                    if (counter == size - 1) or (
                        size > 3 and counter == 3
                    ):  # 1 brakuje
                        if (
                            first == 0
                            and self.board[size - 2 - fir][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_strong_1 += 1
                            else:
                                self.p2_strong_1 += 1
                        elif first == 0 or self.board[size - 2 - fir][sec + 1] == 0:
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_weak_1 += 1
                            else:
                                self.p2_weak_1 += 1

                    elif size > 3 and counter == 2:  # 2 brakuje
                        if (
                            first == 0
                            and self.board[size - 2 - fir][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_strong_2 += 1
                            else:
                                self.p2_strong_2 += 1
                        elif first == 0 or self.board[size - 2 - fir][sec + 1] == 0:
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_weak_2 += 1
                            else:
                                self.p2_weak_2 += 1
                    if counter == 1:
                        first = self.board[size - 1 - fir][sec]
                    counter = 1

        counter = 1
        first = None
        for j in range(1, size - 2):
            counter = 1
            first = None
            freeze = 0
            was_freezed = False
            for i in range(size - 1 - j):
                fir = i
                sec = i + j
                if freeze != 0:
                    freeze -= 1
                elif (
                    self.board[size - 1 - fir][sec]
                    == self.board[size - 2 - fir][sec + 1]
                    and self.board[size - 1 - fir][sec] != 0
                ):
                    counter += 1
                    if (counter == size) or (size > 3 and counter == 4):
                        if self.board[size - 1 - fir][sec] == self.game.p1_s:
                            self.winner = self.game.players[0]
                        else:
                            self.winner = self.game.players[1]
                        return 1
                    continue
                elif (
                    self.board[size - 1 - fir][sec] != 0
                    and self.board[size - 2 - fir][sec + 1] == 0
                    and size - 3 - fir > 0
                    and sec + 2 < size
                    and self.board[size - 1 - fir][sec]
                    == self.board[size - 3 - fir][sec + 2]
                ):
                    counter += 1
                    freeze = 2
                    was_freezed = True
                elif (
                    self.board[size - 1 - fir][sec]
                    != self.board[size - 2 - fir][sec + 1]
                ):
                    if (counter == size - 1) or (
                        size > 3 and counter == 3
                    ):  # 1 brakuje
                        if (
                            first == 0
                            and self.board[size - 2 - fir][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_strong_1 += 1
                            else:
                                self.p2_strong_1 += 1
                        elif first == 0 or self.board[size - 2 - fir][sec + 1] == 0:
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_weak_1 += 1
                            else:
                                self.p2_weak_1 += 1

                    elif size > 3 and counter == 2:  # 2 brakuje
                        if (
                            first == 0
                            and self.board[size - 2 - fir][sec + 1] == 0
                            and not was_freezed
                        ):
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_strong_2 += 1
                            else:
                                self.p2_strong_2 += 1
                        elif first == 0 or self.board[size - 2 - fir][sec + 1] == 0:
                            if self.board[size - 1 - fir][sec] == self.game.p1_s:
                                self.p1_weak_2 += 1
                            else:
                                self.p2_weak_2 += 1

                    elif counter == 1:
                        first = self.board[size - 1 - fir][sec]
                    counter = 1

    def check_draw(self):
        for rowInd, row in enumerate(self.board):
            for colInd, i in enumerate(row):
                if i == 0:
                    return False
        self.winner = "Draw"
        return True

    def check_state(self):
        size = len(self.board)
        # rows
        for row in self.board:
            if self.check_row(row):
                return 1
        # columns
        for col in range(size):
            if self.check_column(col):
                return 1
        # diagonals
        if self.check_first_diag():
            return 1

        elif self.check_second_diag():
            return 1
        # draw
        elif self.check_draw():
            return 1


class Game:
    def __init__(self, size: int, players: list):
        board = [[0 for col in range(size)] for row in range(size)]
        self.size = size
        self.players = players
        self.p1_s = players[0].symbol
        self.p2_s = players[1].symbol
        self.state = State(self, board)

    def move(self, player):
        board = player.set_pos(self.state)
        self.set_board(board)

    def set_board(self, board):
        self.state = State(self, board)
        self.state.draw()


class Minimax_alg:
    def __init__(self, game: Game, player1: Player, d0: int):
        self.player = player1
        self.game = game
        for player in game.players:
            if player != player1:
                self.oponent = player
        self.depth = d0
        self.heur_step = 0.4 / self.depth

    def heuristic(self, state, movemax):
        if (self.player == state.game.players[0] and not movemax) or (
            self.player != state.game.players[0] and movemax
        ):
            if state.p2_weak_1 > 0 or state.p2_strong_1 > 0:
                return -0.8
            if state.p1_strong_1:
                return 0.8
            elif state.p1_weak_1 >= 2:
                return 0.8
            elif state.p1_weak_1 == 1:
                return 0.5
            elif state.p1_strong_2 >= 2:
                return 0.5
        else:
            if state.p1_weak_1 > 0 or state.p1_strong_1 > 0:
                return -0.8
            if state.p2_strong_1:
                return 0.8
            elif state.p2_weak_1 >= 2:
                return 0.8
            elif state.p2_weak_1 == 1:
                return 0.5
            elif state.p2_strong_2 >= 2:
                return 0.5
        return 0

    def possible(self, state, move_max):
        board = copy.deepcopy(state.board)
        pos_states = []
        for rowInd, row in enumerate(board):
            for colInd, i in enumerate(row):
                if i == 0:
                    new_board = copy.deepcopy(board)
                    if move_max:
                        symbol = self.player.symbol
                    else:
                        symbol = self.oponent.symbol
                    new_board[rowInd][colInd] = symbol
                    pos_states.append(State(self.game, new_board))
        return pos_states

    def run_alg(self, state: State):
        self.best_choice = {}
        self.alpha = {}
        self.beta = {}
        res = self.Minimax(state, self.depth, True, -1, 1)
        print(res)
        return self.best_choice[self.depth].board

    def Minimax(self, state: State, d: int, move_max: bool, alpha: float, beta: float):
        self.beta[d] = beta
        self.alpha[d] = alpha

        if state.winner is not None:
            if state.winner == self.player:
                return 0.5 + (0.5 / self.depth) * d
            elif state.winner == "Draw":
                return 0
            else:
                return -1
        elif d == 0:
            return self.heuristic(state, move_max)

        possible = self.possible(state, move_max)
        if move_max:
            self.best_choice[d] = possible[0]
            self.alpha[d - 1] = -1
            for u in possible:
                old_alpha = copy.deepcopy(self.alpha[d - 1])
                self.alpha[d - 1] = max(
                    [
                        float(self.alpha[d - 1]),
                        self.Minimax(
                            u, d - 1, not move_max, self.alpha[d - 1], self.beta[d]
                        ),
                    ]
                )
                if old_alpha != self.alpha[d - 1]:
                    self.best_choice[d] = u

                if self.alpha[d - 1] >= self.beta[d]:
                    return float(self.alpha[d - 1])
            return float(self.alpha[d - 1])
        else:
            self.beta[d - 1] = 1
            for u in possible:
                self.beta[d - 1] = min(
                    [
                        float(self.beta[d - 1]),
                        self.Minimax(
                            u, d - 1, not move_max, self.alpha[d], self.beta[d - 1]
                        ),
                    ]
                )
                if self.alpha[d] >= self.beta[d - 1]:
                    return float(self.beta[d - 1])
            return float(self.beta[d - 1])


def AIvsHuman(size: int, symbol: str, depth: int, i_start=True):
    p1 = Player(symbol)
    p2 = Player("A")
    game1 = Game(size, [p1, p2])
    dep = depth
    min1 = Minimax_alg(game1, p2, dep)
    if i_start:
        alg_turn = False
    else:
        alg_turn = True
    while game1.state.winner is None:
        if alg_turn:
            game1.set_board(min1.run_alg(game1.state))
        else:
            game1.move(p1)
        alg_turn = not alg_turn


def AIvsAI(size: int, d1: int, d2: int, fir_start=True):
    A1 = Player("X")
    A2 = Player("O")
    game1 = Game(size, [A1, A2])
    min1 = Minimax_alg(game1, A1, d1)
    min2 = Minimax_alg(game1, A2, d2)
    print(f"X - depth = {d1}")
    print(f"O - depth = {d2}")
    if fir_start:
        alg1_turn = True
        print("X starts")
    else:
        alg1_turn = False
        print("O starts")
    print("\n")
    while game1.state.winner is None:
        if alg1_turn:
            game1.set_board(min1.run_alg(game1.state))
        else:
            game1.set_board(min2.run_alg(game1.state))
        alg1_turn = not alg1_turn


# AIvsHuman(3, "X", 9, False)
AIvsAI(5, 2, 4, True)
