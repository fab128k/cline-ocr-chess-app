# OCR Chess App

An application that uses OCR to read chess scoresheet game images and output a .pgn file with the game annotation.

## Features

- Extract text from chess scoresheet images using OCR
- Parse chess notation from the extracted text
- Generate PGN files with the game annotation
- Provide a simple web interface for uploading images and downloading PGN files
- RESTful API for integration with other applications

## Prerequisites

- Python 3.x
- Tesseract OCR
- Flask
- OpenCV

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/fab128k/cline-ocr-chess-app.git
   cd cline-ocr-chess-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install flask pytesseract opencv-python
   ```

4. Ensure Tesseract OCR is installed on your system.

## Usage

1. Start the Flask server:
   ```
   flask run
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload a chess scoresheet image

4. The application will process the image and return a PGN file with the game annotation

## API Endpoints

- `POST /upload`: Upload a chess scoresheet image and receive a PGN file
  - Request: Form data with `file` field containing the image
  - Response: JSON with `pgn` field containing the PGN string

## Project Structure

- `app.py`: Main Flask application
- `ocr_component.py`: OCR component for extracting text from images
- `chess_notation_parser.py`: Parser for chess notation
- `pgn_generator.py`: PGN file generator
- `templates/index.html`: Frontend for the application

## License

MIT
