from flask import Flask, request, jsonify, send_from_directory
import logging
import os
import traceback
from ocr_component import extract_text_from_image
from chess_notation_parser import parse_chess_notation, clean_text, identify_notation_system
from pgn_generator import generate_pgn

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        logger.debug("Received a file upload request.")
        
        # Check if file exists in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Get optional parameters
        lang = request.form.get('lang', 'eng')  # Default to English
        event = request.form.get('event', 'Unknown Event')
        date = request.form.get('date', '????.??.??')
        white = request.form.get('white', 'White Player')
        black = request.form.get('black', 'Black Player')
        result = request.form.get('result', '*')

        # Save the file to a temporary location with original filename
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        logger.debug(f"Saved file to {file_path}")
        
        # Extract text from the image
        logger.debug(f"Extracting text from the image using language: {lang}")
        extracted_text = extract_text_from_image(file_path, lang=lang)
        logger.debug(f"Extracted text: {extracted_text}")
        
        # Clean the text
        cleaned_text = clean_text(extracted_text)
        logger.debug(f"Cleaned text: {cleaned_text}")
        
        # Identify notation system
        notation_system = identify_notation_system(cleaned_text)
        logger.debug(f"Identified notation system: {notation_system}")
        
        # Parse the chess notation
        logger.debug("Parsing chess notation.")
        moves = parse_chess_notation(extracted_text)
        logger.debug(f"Parsed moves: {moves}")
        
        # Generate PGN
        logger.debug("Generating PGN.")
        pgn = generate_pgn(moves, event=event, date=date, white=white, black=black, result=result)
        logger.debug(f"Generated PGN: {pgn}")
        
        # Create response with additional debug info
        response = {
            'pgn': pgn,
            'debug': {
                'extracted_text': extracted_text,
                'cleaned_text': cleaned_text,
                'notation_system': notation_system,
                'moves': moves,
                'processed_image': f"/tmp/processed_{file.filename}"
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
