import json
import sys
import time
import keyboard
import cv2
import numpy as np

from src.bot import Board, Mouse
from src.logger.AppLogger import AppLogger


class ChessBot:
    def __init__(self, play_as_white=True, auto_detection=True, in_analysis=False, move_delay_ms=0.2):
        self.auto_detection = auto_detection
        self.in_analysis = in_analysis
        self.move_delay_ms = move_delay_ms
        self.turn = "w" if play_as_white else "b"
        self.board_coords = None
        self.running = True

    def shutdown(self):
        AppLogger.info("Kill switch - Stopping bot...")
        self.running = False
        sys.exit(0)

    def play_game(self):
        """Starts the bot and plays the game until completion."""

        start_delay = 1  # seconds
        AppLogger.info(f"Starting ChessBot in {start_delay} seconds...")
        AppLogger.info("Press 'esc' to shutdown")
        time.sleep(start_delay)

        if not self.setup_board():
            return

        keyboard.add_hotkey("esc", self.shutdown)
        if not self.auto_detection:
            AppLogger.info("Press 'n' to play next move")
            keyboard.add_hotkey("n", self.play_move)
        # Mouse.move_to_center()

        if self.auto_detection:
            time.sleep(1)
            self.play_move()
            while self.running:
                self.wait_for_opponent()
                if not self.play_move():
                    break
                time.sleep(2)
        else:
            # **KEEP THE BOT LISTENING IN A LOOP**
            while self.running:
                time.sleep(0.1)  # Prevent CPU overuse, keep the loop alive

    def setup_board(self):
        # self.board_coords = Board.detect_board()
        if not self.in_analysis:
            self.board_coords = (236, 187, 792, 792)
        else:
            self.board_coords = (389, 187, 792, 792)
        if not self.board_coords:
            AppLogger.error("Error: Chessboard not detected.")
            return False
        return True

    def wait_for_opponent(self):
        """Waits for the opponent to make a move by detecting changes in the board image."""
        AppLogger.info("Waiting for opponent's move...")
        initial_board = cv2.imread(Board.IMAGE_PATH, cv2.IMREAD_GRAYSCALE)  # Load initial board image
        time.sleep(3)  # Short delay before checking

        while self.running:
            Board.capture_board(self.in_analysis)  # Capture a new board image
            new_board = cv2.imread(Board.IMAGE_PATH, cv2.IMREAD_GRAYSCALE)  # Load new image

            if new_board is None or initial_board is None:
                AppLogger.error("Failed to read board images.")
                return

            # Compute absolute difference between the images
            difference = cv2.absdiff(initial_board, new_board)
            diff_value = np.sum(difference)  # Sum of pixel differences

            if diff_value > 1000:  # Threshold to detect significant changes
                AppLogger.debug("Opponent has moved.")
                break

            if keyboard.is_pressed("esc"):  # Kill switch
                self.shutdown()

            time.sleep(1)  # Prevent excessive CPU usage

    def play_move(self):
        """Captures the board, sends it to the API, and moves the best piece."""
        if not self.running:
            return False

        image_path = Board.capture_board(self.in_analysis)
        if not image_path:
            AppLogger.error("Could not capture board.")
            return False

        response = send_image(image_path, self.turn)  # Get response from API
        if not response:
            AppLogger.error("No valid response received from API.")
            return False

        try:
            # Parse JSON
            if isinstance(response, str):
                response = json.loads(response)  # Convert string to dict

            # Extract best move
            best_move = response.get("best_move")
            if not best_move:
                AppLogger.warn("No valid move found in API response.")
                error = response.get("error")
                if error:
                    AppLogger.error(f"API error - {error}")
                return False

            if not self.running:
                return

            # Execute move with updated board coordinates
            if self.move_delay_ms > 0:
                Mouse.move_piece_human(best_move.strip(), self.board_coords, self.move_delay_ms)
            else:
                Mouse.move_piece_hyper(best_move.strip(), self.board_coords)
            AppLogger.verbose(f"Bot moved: {best_move}")
            return True

        except json.JSONDecodeError:
            AppLogger.error("Failed to parse API response as JSON.")
            return False
