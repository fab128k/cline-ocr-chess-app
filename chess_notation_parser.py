import re

def clean_text(text):
    """Clean up the text for better parsing."""
    # Replace common OCR errors
    replacements = {
        '0': 'O',  # Replace zero with capital O for castling
        'l': '1',  # Common OCR error: lowercase l as 1
        'I': '1',  # Common OCR error: capital I as 1
        '|': '1',  # Common OCR error: pipe as 1
        'o': 'o',  # Ensure lowercase o for castling in Italian notation
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def identify_notation_system(text):
    """Try to identify whether the text uses English or Italian notation."""
    # Count frequency of piece characters in both systems
    english_pieces = ['K', 'Q', 'R', 'B', 'N']
    italian_pieces = ['R', 'D', 'T', 'A', 'C']
    
    # Initialize counters
    english_count = 0
    italian_count = 0
    
    # Count occurrences of piece symbols
    for piece in english_pieces:
        if piece in text:
            english_count += text.count(piece)
    
    # Check for Italian pieces, excluding those that overlap with English
    if 'D' in text:  # D for Donna (Queen) is uniquely Italian
        italian_count += text.count('D')
    if 'T' in text:  # T for Torre (Rook) is uniquely Italian
        italian_count += text.count('T')
    if 'A' in text:  # A for Alfiere (Bishop) is uniquely Italian
        italian_count += text.count('A')
    if 'C' in text:  # C for Cavallo (Knight) is uniquely Italian
        italian_count += text.count('C')
    
    # Determine the likely notation system
    if italian_count > english_count:
        return 'italian'
    else:
        return 'english'

def parse_chess_notation(text):
    """Parse chess notation from the extracted text, supporting both English and Italian notation."""
    # Clean the text
    cleaned_text = clean_text(text)
    
    # Identify notation system
    notation_system = identify_notation_system(cleaned_text)
    
    # Define regex patterns for both notation systems
    if notation_system == 'english':
        # English notation pattern (K, Q, R, B, N)
        piece_chars = 'KQRBN'
        castling_pattern = r'O-O(?:-O)?'
    else:
        # Italian notation pattern (R, D, T, A, C)
        piece_chars = 'RDTAC'
        castling_pattern = r'[Oo]-[Oo](?:-[Oo])?|0-0(?:-0)?'
    
    # Combined pattern for moves
    move_pattern = fr'([{piece_chars}]?[a-h]?[1-8]?x?[a-h][1-8](?:=[{piece_chars}])?|{castling_pattern})'
    
    # Find all matches in the text
    moves = re.findall(move_pattern, cleaned_text)
    
    # Filter out any invalid moves (e.g., empty strings)
    valid_moves = [move for move in moves if move.strip()]
    
    # Handle numbered moves (e.g., "1. e4 e5")
    numbered_pattern = r'(\d+)\.\s*([a-zA-Z0-9-=+#]+)(?:\s+([a-zA-Z0-9-=+#]+))?'
    numbered_matches = re.findall(numbered_pattern, cleaned_text)
    
    for match in numbered_matches:
        move_number, white_move, black_move = match
        if white_move and white_move not in valid_moves:
            valid_moves.append(white_move)
        if black_move and black_move not in valid_moves:
            valid_moves.append(black_move)
    
    return valid_moves

if __name__ == "__main__":
    # Example usage
    sample_text = """
    1. e4 e5
    2. Nf3 Nc6
    3. Bb5 a6
    """
    parsed_moves = parse_chess_notation(sample_text)
    print("Parsed Moves:")
    print(parsed_moves)
