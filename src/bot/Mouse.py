import pyautogui
import time

from src.bot import Board
from src.bot.Board import detect_board

def move_to_center():
    pyautogui.moveTo(960, 540)  # Center of a 1920x1080 screen

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

if __name__ == "__main__":
    time.sleep(3)
    board_coords = detect_board()
    move_piece_human("e2e4", board_coords)