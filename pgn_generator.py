def generate_pgn(moves, event="Unknown Event", date="????.??.??", white="White Player", black="Black Player", result="*", site="", round="", additional_tags=None):
    # Create PGN header
    # Build the PGN header with required tags
    pgn_header = f"""[Event "{event}"]
[Site "{site}"]
[Date "{date}"]
[Round "{round}"]
[White "{white}"]
[Black "{black}"]
[Result "{result}"]
"""
    
    # Add any additional tags if provided
    if additional_tags:
        for tag, value in additional_tags.items():
            pgn_header += f'[{tag} "{value}"]\n'

    # If no moves were identified, return just the header and result
    if not moves:
        return pgn_header + "\n" + result
    
    # Format moves into PGN format with proper move numbering
    pgn_moves = ""
    for i in range(0, len(moves), 2):
        move_number = i // 2 + 1
        white_move = moves[i]
        
        # Add white's move
        pgn_moves += f"{move_number}. {white_move} "
        
        # Add black's move if available
        if i + 1 < len(moves):
            black_move = moves[i + 1]
            pgn_moves += f"{black_move} "

    # Combine header and moves
    pgn_content = pgn_header + "\n" + pgn_moves.strip() + " " + result

    return pgn_content

if __name__ == "__main__":
    # Example usage
    sample_moves = ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"]
    pgn = generate_pgn(sample_moves)
    print("Generated PGN:")
    print(pgn)
