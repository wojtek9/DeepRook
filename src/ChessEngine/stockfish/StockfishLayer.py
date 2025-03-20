from stockfish import Stockfish
from src.utils import utils, hardcodedpathsTEMP

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
get_top_moves(3)
"""


class StockfishLayer:
    def __init__(self):
        self.stockfish = self.start_stockfish()
        self.game_fen = None

    @staticmethod
    def start_stockfish():
        try:
            return Stockfish(hardcodedpathsTEMP.STOCKFISH_PATH)
        except Exception as e:
            print(f"[ERROR] Failed to start Stockfish: {e}")
            return None

    def get_next_move(self, board_state, turn):
        # Returns the best move from Stockfish given a board state and updates game state
        if not self.is_alive():
            self.restart_stockfish()
        try:
            # Update game state before getting the best move
            self.update_game_state(board_state, turn)
            best_move = self.stockfish.get_best_move()

            # Apply the move and update the FEN
            self.stockfish.make_moves_from_current_position([best_move])
            self.game_fen = self.stockfish.get_fen_position()

            return best_move
        except Exception as e:
            print(f"Stockfish error - {e}")
            return None

    def is_alive(self):
        # Checks if Stockfish is still responsive
        if self.stockfish is None:
            return False

        try:
            # Try getting a move to see if Stockfish is still alive
            self.stockfish.get_best_move()
            return True  # Stockfish is alive
        except Exception:
            return False  # Stockfish has crashed

    def restart_stockfish(self):
        # Restarts Stockfish if it crashes
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
        # If it's the first move, assume all castling rights are available
        if self.game_fen is None:
            castling_rights = "KQkq"
            en_passant = "-"
            halfmove = "0"
            fullmove = "1"
        else:
            # Extract previous castling rights & en passant info from FEN
            fen_parts = self.game_fen.split(" ")
            castling_rights = fen_parts[2] if len(fen_parts) > 2 else "-"
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
