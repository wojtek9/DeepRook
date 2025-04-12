from pprint import pprint

from stockfish import Stockfish
from src.utils import utils, hardcodedpathsTEMP
from collections import Counter, deque

"""
Stockfish levels:
set_skill_level(n)
0	~800 (Beginner)
5	~1200 (Casual Player)
10	~1500 (Club Player)
15	~2000 (Expert)
20	~2500+ (Grandmaster)

Stockfish depth:
set_depth(n)
Lower depth (3-10) → Faster calculations (~0.1s per move).
Higher depth (15-30) → Stronger play but slower.
Very high depth (30-99) → Superhuman play (~Stockfish 15 at max strength).

get top moves:
get_top_moves(n)
"""


class StockfishLayer:
    def __init__(self):
        self.stockfish = self.start_stockfish()
        # self.stockfish.set_skill_level(12)
        pprint(self.stockfish.get_parameters())
        self.game_fen = None
        self.fen_history = deque(maxlen=100)
        self.move_history = deque(maxlen=100)
        self.has_up = False

    @staticmethod
    def start_stockfish():
        try:
            return Stockfish(hardcodedpathsTEMP.STOCKFISH_PATH)
        except Exception as e:
            print(f"[ERROR] Failed to start Stockfish: {e}")
            return None

    def get_next_move(self, board_state, turn):
        if not self.is_alive():
            self.restart_stockfish()

        try:
            self.update_game_state(board_state, turn)

            if not self.stockfish.is_fen_valid(self.game_fen):
                print(f"[ERROR] Invalid FEN passed to Stockfish: {self.game_fen}")
                return None
            self.fen_history.append(self.game_fen)

            top_moves = self.stockfish.get_top_moves(2)

            if not top_moves or "Move" not in top_moves[0]:
                print("[ERROR] Stockfish returned no valid top moves.")
                return None

            best_move = self.stockfish.get_best_move()

            if not best_move:
                print("[ERROR] Stockfish returned None for best move.")
                return None

            print("fen history: ", self.fen_history)

            # Detect if repeating moves
            # if self.is_draw_about_to_happen(best_move):
            #     if len(top_moves) > 1:
            #         best_move = top_moves[1]["Move"]
            #         print("[WARNING] Repetition detected: selecting next best move.")
            #     else:
            #         print("[WARNING] Only one move available; repetition may occur.")

            # Apply the move and update FEN
            self.stockfish.make_moves_from_current_position([best_move])
            # self.game_fen = self.stockfish.get_fen_position()
            self.move_history.append(best_move)

            return best_move

        except Exception as e:
            print(f"[DEBUG] Move History: {self.move_history}")
            print(f"[DEBUG] Last FEN: {self.fen_history[-1:]}")
            print(f"[ERROR] Stockfish crashed at FEN: {self.game_fen}")
            print(f"[ERROR] Exception: {type(e).__name__} - {e}")
            return None

    def is_draw_about_to_happen(self, next_move: str) -> bool:
        """
        Simulate the move and check if it will cause the board position
        (excluding turn, castling, etc.) to appear for the third time.
        """
        if not next_move:
            return False

        try:
            # Simulate the FEN after next_move
            self.stockfish.set_fen_position(self.game_fen)
            self.stockfish.make_moves_from_current_position([next_move])
            simulated_fen = self.stockfish.get_fen_position()
            self.stockfish.set_fen_position(self.game_fen)  # Reset

            # Extract only the board layout part
            stripped_fen = simulated_fen.split(" ")[0]

            # Include the simulated FEN in the count
            all_positions = [fen.split(" ")[0] for fen in self.fen_history]
            all_positions.append(stripped_fen)

            repetition_count = all_positions.count(stripped_fen)
            print(repetition_count)

            if repetition_count >= 2:
                print("[WARNING] Draw about to happen due to threefold repetition.")
                return True

            return False

        except Exception as e:
            print(f"[ERROR] Failed to simulate repetition: {e}")
            return False

    def is_alive(self):
        if self.stockfish is None:
            return False

        try:
            self.stockfish.get_best_move()
            return True
        except Exception:
            return False

    def restart_stockfish(self):
        print("[ERROR] -- Stockfish crashed. Restarting...")
        self.stockfish = self.start_stockfish()

    def get_game_state(self):
        if self.game_fen is None:
            return None

        fen_parts = self.game_fen.split(" ")
        return {
            "fen": self.game_fen,
            "castling_rights": fen_parts[2],  # Castling rights (KQkq or -)
            "en_passant": fen_parts[3],  # En passant target square (e.g., "e3" or "-")
        }

    def update_game_state(self, board_state, turn):
        if self.game_fen is None:
            castling_rights = "KQkq"
            en_passant = "-"
            halfmove = "0"
            fullmove = "1"
        else:
            fen_parts = self.game_fen.split(" ")
            # castling_rights = fen_parts[2] if len(fen_parts) > 2 else "-"
            castling_rights = utils.infer_castling_rights(board_state)
            en_passant = fen_parts[3] if len(fen_parts) > 3 else "-"
            halfmove = fen_parts[4] if len(fen_parts) > 4 else "0"
            fullmove = fen_parts[5] if len(fen_parts) > 5 else "1"

        # Generate updated FEN
        self.game_fen = utils.board_to_fen(
            board_state=board_state,
            turn=turn,
            castling_rights=castling_rights,
            en_passant=en_passant,
            halfmove=halfmove,
            fullmove=fullmove,
        )

        # Set the updated FEN position in Stockfish
        self.stockfish.set_fen_position(self.game_fen)
