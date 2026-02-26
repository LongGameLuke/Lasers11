from enum import Enum

class Color(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    LIGHT_BLUE = "\033[96m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

def log_process_start(message):
    print(f"[{Color.MAGENTA.value}-{Color.RESET.value}] {message}...")

def log_process_error(message, error=None):
    print(f"[{Color.RED.value}!{Color.RESET.value}] {Color.RED.value}ERROR{Color.RESET.value}: {message}")
    if error is not None:
        print(error)

def log_process_complete(message):
    print(f"[{Color.GREEN.value}+{Color.RESET.value}] {message}!")

def log_process(message):
    print(f"[{Color.LIGHT_BLUE.value}***{Color.RESET.value}] {message}")