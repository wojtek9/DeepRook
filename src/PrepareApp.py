from src.core.ConfigManager import ConfigManager
from src.core.dataclasses.BotParams import BotParams
from src.core.enums.Hotkeys import Hotkey
from src.session.SessionData import SessionData
from src.utils import utils


def prepare_app():
    session = SessionData()
    config_manager = ConfigManager()
    config = config_manager.config_data

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

    session.hotkeys = {}
    config_hotkeys = config.get("hotkeys", {})

    for hotkey_name, keybind in config_hotkeys.items():
        try:
            hotkey_enum = Hotkey[hotkey_name]
            session.hotkeys[hotkey_enum] = keybind
        except KeyError:
            pass

    print("config loaded")
    return session, config_manager
