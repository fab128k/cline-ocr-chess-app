import pytesseract
from PIL import Image
import cv2
import numpy as np

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    contrast_enhanced = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # Apply a slight GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(contrast_enhanced, (3, 3), 0)

    # Use Otsu's thresholding after Gaussian filtering
    _, otsu_thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return otsu_thresh

def extract_text_from_image(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(processed_image)

    return text

if __name__ == "__main__":
    # Example usage
    image_path = "path_to_your_image.jpg"
    extracted_text = extract_text_from_image(image_path)
    print("Extracted Text:")
    print(extracted_text)
