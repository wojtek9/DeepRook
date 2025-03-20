import pyautogui
import time
import ctypes
from src.bot import Board
from src.bot.Board import detect_board

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_MOVE = 0x0001


def move_to_center():
    pyautogui.moveTo(960, 540)  # Center of a 1920x1080 screen


def mouse_down_win():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def mouse_up_win():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def move_mouse_win(x, y):
    ctypes.windll.user32.SetCursorPos(int(x), int(y))


def move_piece_human(move, board_coords, delay_ms=0.2):
    start_square, end_square = move[:2], move[2:]

    start_x, start_y = Board.get_square_position(start_square, board_coords)
    end_x, end_y = Board.get_square_position(end_square, board_coords)

    pyautogui.moveTo(start_x, start_y, duration=delay_ms)
    pyautogui.mouseDown()
    time.sleep(0.1)  # Small delay for realism
    pyautogui.moveTo(end_x, end_y, duration=delay_ms)
    pyautogui.mouseUp()


def move_piece_hyper(move, board_coords):
    start_square, end_square = move[:2], move[2:]

    start_x, start_y = Board.get_square_position(start_square, board_coords)
    end_x, end_y = Board.get_square_position(end_square, board_coords)

    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y)
    pyautogui.mouseUp()


def move_piece_hypersonic(move, board_coords):
    start_square, end_square = move[:2], move[2:]

    start_x, start_y = Board.get_square_position(start_square, board_coords)
    end_x, end_y = Board.get_square_position(end_square, board_coords)

    move_mouse_win(start_x, start_y)
    mouse_down_win()
    move_mouse_win(end_x, end_y)
    mouse_up_win()


if __name__ == "__main__":
    time.sleep(1)
    # board_coords = detect_board()
    board_coords = (392, 187, 792, 791)
    move_piece_hyper("e2e4", board_coords)
