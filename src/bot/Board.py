import pyautogui
from PIL import Image
import cv2
import numpy as np

BOARD_REGION_LIVE = (235, 185, 790, 790)  # (x, y, width, height)
BOARD_REGION_ANALYSIS = (393, 185, 790, 790)  # (x, y, width, height)
TARGET_SIZE = (720, 720)
TEMPLATE_BOARD_PATH = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionBOT\resources\images\board.png"
DETECTION_DEBUG_PATH = (
    r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionBOT\resources\images\board_detection.png"
)
IMAGE_PATH = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionBOT\resources\images\current_board.png"


def capture_board(in_analysis=False):
    """Captures an image of the chessboard, resizes it, and saves it locally."""
    board_region = BOARD_REGION_ANALYSIS if in_analysis else BOARD_REGION_LIVE
    screenshot = pyautogui.screenshot(region=board_region)

    # Resize to 720x720
    resized = screenshot.resize(TARGET_SIZE, Image.LANCZOS)
    resized.save(IMAGE_PATH)

    # print(f"Board captured, resized to {TARGET_SIZE}, and saved as {IMAGE_PATH}")
    return IMAGE_PATH


def detect_board():
    """Detects the chessboard dynamically on the screen and saves the detection image."""
    screenshot = pyautogui.screenshot()  # Take a full-screen screenshot
    screen_array = np.array(screenshot)  # Convert to NumPy array (RGB format)

    # Convert screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screen_array, cv2.COLOR_RGB2GRAY)

    # Load the chessboard template
    template = cv2.imread(TEMPLATE_BOARD_PATH, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("Error: Template image not found.")
        return None

    # Template matching to find the board on the screen
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Get the board's top-left corner coordinates
    board_x, board_y = max_loc
    board_x, board_y = (236, 187)

    # **Fix width and height calculation**
    board_w = template.shape[1] + 10  # Increase width
    board_h = template.shape[0] + 10  # Increase height
    board_w = 792
    board_h = 792

    # **Debug print to check detection accuracy**
    print(f"Adjusted board detection: x={board_x}, y={board_y}, width={board_w}, height={board_h}")

    # **Draw a rectangle on the detected board**
    detected_image = screen_array.copy()
    cv2.rectangle(
        detected_image, (board_x, board_y), (board_x + board_w, board_y + board_h), (0, 255, 0), 2
    )  # Green rectangle with thickness 5

    # **Save the debug image**
    cv2.imwrite(DETECTION_DEBUG_PATH, cv2.cvtColor(detected_image, cv2.COLOR_RGB2BGR))

    return (board_x, board_y, board_w, board_h)


def get_square_position(square, board_coords):
    """Converts chess square (e.g., 'e2') to pixel coordinates based on detected board."""
    board_x, board_y, board_w, board_h = board_coords
    square_size = board_w // 8  # Assuming a square board

    file_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    rank_map = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    file, rank = square[0], square[1]  # Extract file and rank from notation
    x = board_x + file_map[file] * square_size + square_size // 2  # Center of square
    y = board_y + rank_map[rank] * square_size + square_size // 2

    return x, y


if __name__ == "__main__":
    print(detect_board())
