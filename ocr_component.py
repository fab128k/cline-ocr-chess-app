import pytesseract
from PIL import Image
import cv2
import numpy as np
import math
import os

def deskew(image):
    """Deskew the image to correct any rotation."""
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated

def remove_noise(image):
    """Remove noise from the image."""
    # Apply morphological operations
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Apply median blur
    denoised = cv2.medianBlur(opening, 3)
    
    return denoised

def preprocess_image(image_path):
    """Enhanced preprocessing for chess scoresheets."""
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)
    
    # Apply a slight GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(contrast_enhanced, (3, 3), 0)
    
    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Invert the image (text should be black on white background for OCR)
    binary = cv2.bitwise_not(adaptive_thresh)
    
    # Try to deskew the image if needed
    deskewed = deskew(binary)
    
    # Remove noise
    cleaned = remove_noise(deskewed)
    
    return cleaned

def extract_text_from_image(image_path, lang='eng'):
    """Extract text from chess scoresheet with optimized settings."""
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Save the processed image for debugging if needed
    temp_path = os.path.join('/tmp', 'processed_' + os.path.basename(image_path))
    cv2.imwrite(temp_path, processed_image)
    
    # Configure Tesseract parameters optimized for chess scoresheets
    config = '--psm 6 --oem 3 -c tessedit_char_whitelist="KQRBNADTCabcdefgh12345678xX+#=OoI-. "' 
    
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(processed_image, lang=lang, config=config)
    
    # Try alternative processing if no text was found
    if not text.strip():
        # Try a different preprocessing approach
        gray = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(binary, lang=lang, config=config)
    
    return text

if __name__ == "__main__":
    # Example usage
    image_path = "path_to_your_image.jpg"
    extracted_text = extract_text_from_image(image_path)
    print("Extracted Text:")
    print(extracted_text)
