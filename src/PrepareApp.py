from src.core.ConfigManager import ConfigManager
from src.core.botdata.BotParams import BotParams
from src.session.SessionData import SessionData
from src.utils import utils


def prepare_app():
    session = SessionData()
    config_manager = ConfigManager()
    config = config_manager.config_data

    session.selected_region = config.get("selected_region", None)
    session.play_as_white = config.get("play_as_white", True)
    session.game_state = config.get("game_state", "Not Started")
    session.bot_enabled = config.get("bot_enabled", False)
    session.selected_engine = config.get("engine", "Stockfish")
    session.engine_rating = config.get("engine_rating", 3000)
    session.temp_chessboard_image = config.get("temp_chessboard_image", None)
    session.model_path = config.get("model_path", "")

    if not session.model_path:
        model_path = utils.get_model_path()
        session.model_path = model_path

    bot_params_config = config.get("bot_params", {})
    session.bot_params = BotParams(
        start_delay=bot_params_config.get("start_delay", 0),
        human_mouse_movements=bot_params_config.get("human_mouse_movements", False),
        random_move_delay=bot_params_config.get("random_move_delay", False),
        min_move_delay=bot_params_config.get("min_move_delay", 0.0),
        max_move_delay=bot_params_config.get("max_move_delay", 0.0),
        auto_detection=bot_params_config.get("auto_detection", False),
        auto_move=bot_params_config.get("auto_move", False),
    )
    print("config loaded")
    return session, config_manager
