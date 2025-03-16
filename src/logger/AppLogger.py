from colorama import Fore, Style, init

init(autoreset=True)


class LogLevel:
    VERBOSE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class AppLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        super().__init__()
        self._initialized = True

    @classmethod
    def verbose(cls, msg: str):
        print(f"{Fore.WHITE}[VERBOSE] -- {msg}{Style.RESET_ALL}")

    @classmethod
    def debug(cls, msg: str):
        print(f"{Fore.BLUE}[DEBUG] -- {msg}{Style.RESET_ALL}")

    @classmethod
    def info(cls, msg: str):
        print(f"{Fore.GREEN}[INFO] -- {msg}{Style.RESET_ALL}")

    @classmethod
    def warn(cls, msg: str):
        print(f"{Fore.YELLOW}[WARN] -- {msg}{Style.RESET_ALL}")

    @classmethod
    def error(cls, msg: str):
        print(f"{Fore.RED}[ERROR] -- {msg}{Style.RESET_ALL}")
