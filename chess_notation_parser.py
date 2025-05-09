import re

def parse_chess_notation(text):
    # Define a regex pattern for standard algebraic notation
    pattern = r'([KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?|O-O(?:-O)?)'
    
    # Find all matches in the text
    moves = re.findall(pattern, text)
    
    # Filter out any invalid moves (e.g., empty strings)
    valid_moves = [move for move in moves if move.strip()]

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
