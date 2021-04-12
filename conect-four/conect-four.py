# This is a version of Connect 4. Made by Danny0.

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
    player_index = 0
    players_symbols = ["X", "O"]

    show_header()
    players = ask_players_names()
    # players = ["Dani", "Gisselle"]
    player = players[player_index].capitalize()
    # players_symbols = [players[0][0].upper(), players[1][0].upper()]

    # Game loop
    while not get_winner(board, players_symbols):

        player = players[player_index].capitalize()
        symbol = players_symbols[player_index]

        announce_player(player, player_index, players_symbols)
        show_board(board)

        if not set_location(board, player, symbol):
            continue

        player_index = (player_index + 1) % 2

    # Game Over

    print(f"\n\nCongratulations {player}! You win!\n")
    show_board(board)
    print("\n\n---------------------")
    print("----- Game over -----")
    print("---------------------")


# Functions


def set_location(board, player, symbol):
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
        col = int(input(f"{player} select a column: "))
    except:
        print("\nInvalid input please input a positive integer...",end="")
        return False
    col -= 1
    # Check if input is out of bounds.
    if col < 0 or col > (len(board[0]) - 1):
        print("\nOut of bounds...", end="")
        return False

    # Check for the cell, and check if it's empty, or occupied, if occupied
    # then sets row and updates the cell to check the cell above.
    cell = board[row][col]
    while cell is not None:
        row -= 1
        cell = board[row][col]
        if row < 0:
            print("\nSorry, This column is full...", end="")
            return False

    board[row][col] = symbol
    return True


def announce_player(player, player_index, players_symbols):
    print()
    print(f"It's {player}'s [{(players_symbols[player_index])}] Turn. Current board: ")
    print()


def get_winner(board, players_symbols):
    sequences = get_sequences(board)
    symbols = []
    for symbol in players_symbols:
        s_list = []
        for i in range(4):
            s_list.append(symbol)
        symbols.append(s_list)

    for sequence in sequences:
        for i in range(len(sequence)):
            if sequence[i:(i+4)] in symbols:
                return True
    return False


def get_sequences(board):
    """
    Receives the LIST board, and it

    RETURNS out all sequences
    Where you can win. rows, columns and diagonals.

    """
    sequences = []
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
        [board[0][0], board[1][1], board[2][2], board[3][3], board[4][4], board[5][5]],
        [board[0][6], board[1][5], board[2][4], board[3][3], board[4][2], board[5][1]],
        [board[5][0], board[4][1], board[3][2], board[2][3], board[1][4], board[5][5]],
        [board[5][6], board[4][5], board[3][4], board[2][3], board[1][2], board[0][1]],
        # 5 long diagonals
        [board[1][0], board[2][1], board[3][2], board[4][3], board[5][4]],
        [board[1][6], board[2][5], board[3][4], board[4][3], board[5][2]],
        # 4 long diagonals
        [board[2][0], board[3][1], board[4][2], board[5][3]],
        [board[5][3], board[4][4], board[3][5], board[2][6]]

    ]
    sequences = rows + columns + diagonals

    return sequences


def show_board(board):
    """
    Receives a list "board" of lists with the board.

    Prints the board to the screen.
    """
    for row in board:
        print("| ", end="")
        for cell in row:
            symbol = cell if cell is not None else "_"
            print(symbol, end=" | ")
        print()


def ask_players_names():
    """
    Asks the user for the names of the players.

    returns list of players
    """
    players = []
    number_of_players = 2

    for i in range(number_of_players):
        index = i + 1
        players.append(input(f"Player {index}: What's your name? "))

    return players


def show_header():
    print("--------------------")
    print("---- Connect 4! ----")
    print("--------------------")
    print("\n\n")


if __name__ == '__main__':
    main()
