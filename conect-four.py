# 12th of April, 2020
# Connect 4! by Dani Ocaranza.
import json
import os.path
from colorama import Fore, init

init()


def main():
    # Set the board.
    board = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
    ]

    # Initialize the game variables.
    yellow = Fore.YELLOW
    reset = Fore.RESET
    red = Fore.RED
    player_index = 0
    players_symbols = [red + "O" + reset,
                       yellow + "O" + reset]

    show_header()
    show_leaderboard(load_leaderboard())
    players = ask_players_names()
    # active_player = players[player_index]
    # Use this instead if you want the symbols to be
    # the initial of the player's name.
    # players_symbols = [players[0][0].upper(), players[1][0].upper()]

    # Game loop
    while not get_winner(board, players_symbols):

        active_player = players[player_index]
        symbol = players_symbols[player_index]

        announce_player(active_player, player_index, players_symbols)
        show_board(board)

        if not set_location(board, active_player, symbol, player_index):
            continue

        player_index = (player_index + 1) % 2

    winner = active_player
    print(Fore.RESET)
    # Game Over
    show_board(board)
    print(Fore.RED, end="")
    print("\n\n---------------------")
    print("----- Game over -----")
    print("---------------------")
    if player_index == 1:
        print(Fore.RED, end="")
    else:
        print(Fore.YELLOW, end="")
    print(f"Congratulations {active_player}! You win!\n")

    record_winner(winner)


# Functions


def load_leaderboard():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json').replace('\\', '/')
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def set_location(board, player, symbol, player_index):
    """
    It tries to add the symbol to the board if it can.
    list 'board': The board list.
    list 'player': the name of the player.
    str 'symbol': the symbol of the active player.
    return 'bool': on success, returns True otherwise False.
    """
    row = len(board) - 1
    # input failsafe. Only accept ints.
    try:
        if player_index == 0:
            print(Fore.RED, end="")
        else:
            print(Fore.YELLOW, end="")
        col = int(input(f"{player} select a column: "))
    except ValueError:
        print(Fore.RED + "\nInvalid input please input a positive integer...",
              end="")
        return False
    col -= 1
    # Check if input is out of bounds.
    if col < 0 or col > (len(board[0]) - 1):
        print(Fore.RED + "\nOut of bounds...", end="")
        return False
    # Check for the cell, and check if it's empty, or occupied, if occupied
    # then sets row and updates the cell to check the cell above.
    cell = board[row][col]
    while cell is not None:
        row -= 1
        cell = board[row][col]
        if row < 0:
            print(Fore.RED + "\nSorry, This column is full...", end="")
            return False
    board[row][col] = symbol
    return True


def get_sequences(board):
    """
    Receives the LIST board, and it
    RETURNS a list of lists with all sequences
    Where you can win: rows, columns and diagonals.
    Only works on a 7 by 6 board.
    """
    rows = board
    columns = [
        [board[0][col],
         board[1][col],
         board[2][col],
         board[3][col],
         board[4][col],
         board[5][col], ] for col in range(len(board))
    ]
    diagonals = [
        # Longest diagonals
        [board[0][0], board[1][1], board[2][2], board[3][3], board[4][4], board[5][5]],#
        [board[0][6], board[1][5], board[2][4], board[3][3], board[4][2], board[5][1]],#
        [board[5][0], board[4][1], board[3][2], board[2][3], board[1][4], board[0][5]],#
        [board[5][6], board[4][5], board[3][4], board[2][3], board[1][2], board[0][1]],#
        # 5 long diagonals
        [board[1][0], board[2][1], board[3][2], board[4][3], board[5][4]],
        [board[1][6], board[2][5], board[3][4], board[4][3], board[5][2]],
        [board[4][0], board[3][1], board[2][2], board[1][3], board[0][4]],
        [board[4][6], board[2][5], board[3][4], board[4][3], board[5][2]],
        # 4 long diagonals
        [board[2][0], board[3][1], board[4][2], board[5][3]],
        [board[2][6], board[3][5], board[4][4], board[5][3]],
        [board[3][0], board[2][1], board[1][2], board[0][3]],
        [board[3][6], board[2][5], board[1][4], board[0][3]]
    ]
    sequences = rows + columns + diagonals
    return sequences


def get_winner(board, players_symbols):
    """
    :list of lists board: Receives the board.
    :list players_symbols: Receives the list with symbols.
    :returns: True if winner is found, otherwise False.
    """
    sequences = get_sequences(board)
    symbols = []
    for symbol in players_symbols:
        s_list = []
        for i in range(4):
            s_list.append(symbol)
        symbols.append(s_list)
    for sequence in sequences:
        for i in range(len(sequence)):
            if sequence[i:(i + 4)] in symbols:
                return True
    return False


def record_winner(winner_name):
    leaderboard = load_leaderboard()
    if winner_name in leaderboard:
        leaderboard[winner_name] += 1
    else:
        leaderboard[winner_name] = 1
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json').replace('\\', '/')
    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaderboard, fout)


def ask_players_names():
    """
    Asks the user for the names of the players.
    returns list of players
    """
    players = []
    number_of_players = 2
    for i in range(number_of_players):
        index = i + 1
        if i == 0:
            print(Fore.RED, end="")
        else:
            print(Fore.YELLOW, end="")
        player = (input(f"Player {index}: What's your name? "))
        player = player.capitalize()
        players.append(player)
        print(Fore.WHITE, end="")
    return players


def show_header():
    print(Fore.MAGENTA)
    print("      --------------------")
    print("      ---- Connect 4! ----")
    print("      --------------------\n")
    print(Fore.WHITE, end="")


def show_leaderboard(leaderboard):
    print(Fore.GREEN)
    sorted_wins = list(leaderboard.items())
    sorted_wins.sort(key=lambda i: i[1], reverse=True, )
    max_str_len = 31
    print("*       # LEADERBOARD #       *")
    print("---------    TOP 10   ---------")
    # MAIN LOOP THROUGH LIST OF SCORES
    if leaderboard == {}:
        print("------- No scores yet... ------")
    for name, wins in sorted_wins[0:10]:
        col = f"{name} ------------------------------- {wins}"
        remove = len(col) - max_str_len
        col = col.replace('-', '', remove)
        print(col)
    print("_______________________________")
    print(Fore.WHITE, end="")


def announce_player(player, player_index, players_symbols):
    print(Fore.GREEN)  # This statements only change colour of text.
    print(f"It's {player}'s [{(players_symbols[player_index])}" +
          Fore.GREEN + "] Turn. Current board: ", end="")
    print(Fore.WHITE)


def show_board(board):
    """
    Receives a list (board) of lists [rows] with the board.
    Prints the board to the screen.
    """
    print("_ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _ 7 _")
    for row in board:
        print("| ", end="")
        for cell in row:
            symbol = cell if cell is not None else "_"
            print(symbol, end=" | ")
        print()


if __name__ == '__main__':
    main()
