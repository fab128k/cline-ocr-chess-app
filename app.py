from flask import Flask, request, jsonify, send_from_directory
import logging
from ocr_component import extract_text_from_image
from chess_notation_parser import parse_chess_notation
from pgn_generator import generate_pgn

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.debug("Received a file upload request.")
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file to a temporary location
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        logging.debug("Saving file to temporary location.")
        
        # Extract text from the image
        logging.debug("Extracting text from the image.")
        extracted_text = extract_text_from_image(file_path)

        logging.debug(f"Extracted text: {extracted_text}")

        # Parse the chess notation
        logging.debug("Parsing chess notation.")
        moves = parse_chess_notation(extracted_text)

        logging.debug(f"Parsed moves: {moves}")

        # Generate PGN
        logging.debug("Generating PGN.")
        pgn = generate_pgn(moves)

        logging.debug(f"Generated PGN: {pgn}")

        return jsonify({'pgn': pgn})
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to a temporary location
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)

    # Extract text from the image
    extracted_text = extract_text_from_image(file_path)

    # Parse the chess notation
    moves = parse_chess_notation(extracted_text)

    # Generate PGN
    pgn = generate_pgn(moves)

    return jsonify({'pgn': pgn})

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

    app.run(debug=True, host='0.0.0.0', port=5001)
