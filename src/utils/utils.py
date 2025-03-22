import os

from PySide6.QtCore import QStandardPaths, QFile, QIODevice
from numpy import ndarray


def get_temp_dir():
    temp_loc = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation)
    temp_dir = os.path.join(temp_loc, "DeepRookCache")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def get_model_path():
    # Extract the .h5 model from Qt Resources and return the path to use with TensorFlow
    resource_path = ":/models/Rookception.h5"
    temp_dir = get_temp_dir()
    temp_model_path = os.path.join(temp_dir, "Rookception.h5")

    if not QFile.exists(resource_path):
        print(f"Resource not found: {resource_path}")
        return None

    file = QFile(resource_path)
    if file.open(QFile.OpenModeFlag.ReadOnly):
        with open(temp_model_path, "wb") as temp_file:
            temp_file.write(file.readAll())  # Extract to temp location
        file.close()
        print(f"Model extracted to: {temp_model_path}")
        return temp_model_path
    else:
        print("Failed to open model resource file.")
        return None


def get_turn_from_play_as_white(play_as_white: bool):
    return "w" if play_as_white else "b"


def convert_to_keyboard_hotkey(hotkey_str: str) -> str:
    if not hotkey_str.strip():
        return ""

    key_map = {
        "CTRL": "ctrl",
        "SHIFT": "shift",
        "ALT": "alt",
        "META": "command",
        "UP": "up",
        "DOWN": "down",
        "LEFT": "left",
        "RIGHT": "right",
        "ENTER": "enter",
        "RETURN": "enter",
        "ESC": "esc",
        "SPACE": "space",
        "TAB": "tab",
        "BACKSPACE": "backspace",
        "DELETE": "delete",
    }

    keys = hotkey_str.upper().split(" + ")
    converted_keys = [key_map.get(key, key.lower()) for key in keys]
    return "+".join(converted_keys)


def convert_to_user_friendly_hotkey(keyboard_str: str) -> str:
    if not keyboard_str.strip():
        return ""

    key_map = {
        "ctrl": "CTRL",
        "shift": "SHIFT",
        "alt": "ALT",
        "command": "META",
        "win": "META",
        "up": "UP",
        "down": "DOWN",
        "left": "LEFT",
        "right": "RIGHT",
        "enter": "ENTER",
        "esc": "ESC",
        "space": "SPACE",
        "tab": "TAB",
        "backspace": "BACKSPACE",
        "delete": "DELETE",
    }

    keys = keyboard_str.lower().split("+")
    converted_keys = [key_map.get(key, key.upper()) for key in keys]
    return " + ".join(converted_keys)


def board_to_fen(board_state: ndarray, turn="w", castling_rights="KQkq", en_passant="-", halfmove="0", fullmove="1"):
    # Convert board state (8x8 numpy array) into FEN string including castling rights and en passant

    # Map CNN labels to chess symbols
    piece_map = {
        "bP": "p",
        "bN": "n",
        "bB": "b",
        "bR": "r",
        "bQ": "q",
        "bK": "k",
        "wP": "P",
        "wN": "N",
        "wB": "B",
        "wR": "R",
        "wQ": "Q",
        "wK": "K",
        "empty": "1",
    }

    fen_rows = []

    for row in board_state:
        fen_row = ""
        empty_count = 0

        for square in row:
            piece = piece_map.get(square, "1")  # Default to empty if not recognized

            if piece == "1":  # Empty square
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece

        if empty_count > 0:
            fen_row += str(empty_count)

        fen_rows.append(fen_row)

    fen_board = "/".join(fen_rows)

    # Construct full FEN string with castling rights & en passant
    fen = f"{fen_board} {turn} {castling_rights} {en_passant} {halfmove} {fullmove}"
    return fen


def infer_castling_rights(board_state):
    rights = ""

    # White king + rooks
    if board_state[7][4] == "wK":
        if board_state[7][0] == "wR":
            rights += "Q"
        if board_state[7][7] == "wR":
            rights += "K"

    # Black king + rooks
    if board_state[0][4] == "bK":
        if board_state[0][0] == "bR":
            rights += "q"
        if board_state[0][7] == "bR":
            rights += "k"

    if not rights.strip():
        return "-"

    return rights


def print_board(board, title=""):
    index_mapping = {i: 8 - i for i in range(8)}

    piece_map = {
        "bP": "♟",
        "bN": "♞",
        "bB": "♝",
        "bR": "♜",
        "bQ": "♛",
        "bK": "♚",
        "wP": "♙",
        "wN": "♘",
        "wB": "♗",
        "wR": "♖",
        "wQ": "♕",
        "wK": "♔",
        "empty": ".",
    }

    board = [[piece_map.get(piece, piece) for piece in row] for row in board]

    if title:
        print(f"\n{title}:")

    print("---------------------------------")
    for idx, row in enumerate(board):
        row_number = index_mapping[idx]
        formatted_row = " | ".join(f"{piece}" for piece in row)
        print(f"{row_number} | {formatted_row} |")
        print("---------------------------------")
    print("    a   b   c   d   e   f   g   h")
