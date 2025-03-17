import numpy as np
from PIL import Image
import time

from src.utils import utils


class Rookception:
    def __init__(self, model_path: str):
        from tensorflow.keras.models import load_model  # Lazy import
        self.model = load_model(model_path)
        self.class_labels = ["bB", "bK", "bN", "bP", "bQ", "bR", "empty", "wB", "wK", "wN", "wP", "wQ", "wR"]
        self.img_size = (64, 64)

    def extract_squares(self, image_path):
        """Extracts 64 squares from a chessboard image and saves them."""
        image = Image.open(image_path)
        square_size = 720 // 8  # 90 pixels per square
        squares = []

        for row in range(8):
            row_squares = []
            for col in range(8):
                left = col * square_size
                top = row * square_size
                right = (col + 1) * square_size
                bottom = (row + 1) * square_size

                square_img = image.crop((left, top, right, bottom)).convert("RGB")
                square_img = square_img.resize(self.img_size)  # Resize for CNN
                square_array = np.array(square_img) / 255.0  # Normalize

                row_squares.append(square_array)

            squares.append(row_squares)

        return np.array(squares)  # Shape (8, 8, 64, 64, 3)

    def predict_board(self, image_path):
        # Recognizes all pieces on the chessboard using batch prediction
        squares = self.extract_squares(image_path)  # (8, 8, 64, 64, 3)
        print("\nRecognizing Pieces...")
        # **Flatten the board for batch prediction**
        all_squares = squares.reshape(-1, 64, 64, 3)  # Shape: (64, 64, 64, 3)

        # **Perform batch prediction**
        predictions = self.model.predict(all_squares)  # Predict all 64 squares at once

        # **Process results**
        predicted_classes = np.argmax(predictions, axis=1).reshape(8, 8)
        confidences = np.max(predictions, axis=1).reshape(8, 8) * 100  # Get confidence %
        board_state = np.vectorize(lambda x: self.class_labels[x])(predicted_classes)
        board_with_accuracy = np.vectorize(lambda x, y: f"{self.class_labels[x]} ({y:.2f}%)")(
            predicted_classes, confidences
        )

        utils.print_board(board=board_with_accuracy, title="Predicted board with accuracy")
        utils.print_board(board=board_state, title="Predicted board")

        return board_state


if __name__ == "__main__":
    model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\DeepRook\resources\models\CNN\RookceptionCNN_V1.h5"
    test_img_path = (
        r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\images\chessboard\board.png"
    )
    test_img_path2 = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionBOT\resources\images\board.png"

    # Load image and convert to NumPy array
    # img = Image.open(test_img_path).convert("RGB")  # Ensure 3-channel RGB
    # img_array = np.array(img) / 255.0  # Normalize pixel values

    # Initialize recognizer and predict board
    recognizer = Rookception(model_path)
    start_time = time.time()
    board = recognizer.predict_board(test_img_path2)
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    print(f"Prediction took: {execution_time:.4f} seconds")

    print(utils.board_to_fen(board))
