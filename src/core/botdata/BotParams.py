from dataclasses import dataclass


@dataclass
class BotParams:
    start_delay: int = 0
    human_mouse_movements: bool = False
    random_move_delay: bool = False
    min_move_delay: float = 0.0
    max_move_delay: float = 0.0
    auto_detection: bool = False
    auto_move: bool = False
