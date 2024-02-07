from tic_tac_toe import Minimax_alg, Game, Player


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


AIvsHuman(3, "X", 9, False)
# AIvsAI(5, 2, 4, True)
