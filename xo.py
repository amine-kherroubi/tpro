from math import inf
from typing import Final, Literal, Optional

HUMAN: Final[Literal["X"]] = "X"
AI: Final[Literal["O"]] = "O"
EMPTY: Final[Literal[" "]] = " "

WIN_PATHS: Final[list[list[int]]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def check_winner(board: list[str]) -> Optional[str]:
    for path in WIN_PATHS:
        if board[path[0]] == board[path[1]] == board[path[2]] != EMPTY:
            return board[path[0]]
    if EMPTY not in board:
        return "Tie"
    return None


def minimax(board: list[str], depth: int, is_maximizing: bool) -> int:
    result: Optional[str] = check_winner(board)

    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "Tie":
        return 0

    if is_maximizing:
        best_val: float = -inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score: int = minimax(board, depth + 1, False)
                board[i] = EMPTY
                best_val = max(best_val, score)
        return int(best_val)

    best_val: float = inf
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = HUMAN
            score: int = minimax(board, depth + 1, True)
            board[i] = EMPTY
            best_val = min(best_val, score)
    return int(best_val)


def get_best_move(board: list[str]) -> int:
    best_score: float = -inf
    move: int = -1
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score: int = minimax(board, 0, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                move = i
    return move


def print_board(board: list[str]) -> None:
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---+---+---")


def main() -> None:
    board: list[str] = [EMPTY] * 9
    print("Tic-Tac-Toe: You (X) vs AI (O)")

    while True:
        print_board(board)
        if check_winner(board):
            break

        try:
            choice: int = int(input("Enter move (0-8): "))
            if not (0 <= choice <= 8) or board[choice] != EMPTY:
                print("Invalid move. Try again.")
                continue
        except ValueError:
            print("Please enter a number between 0 and 8.")
            continue

        board[choice] = HUMAN

        if check_winner(board):
            break

        print("\nAI is calculating...")
        ai_move: int = get_best_move(board)
        board[ai_move] = AI

    result: Optional[str] = check_winner(board)
    print_board(board)
    print(f"\nGame Over! Result: {result}")


if __name__ == "__main__":
    main()
