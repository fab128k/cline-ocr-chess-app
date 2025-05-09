def generate_pgn(moves, event="Unknown Event", date="????.??.??", white="White Player", black="Black Player", result="*"):
    # Create PGN header
    pgn_header = f"""[Event "{event}"]
[Date "{date}"]
[White "{white}"]
[Black "{black}"]
[Result "{result}"]
"""

    # Format moves into PGN format
    pgn_moves = ""
    for i in range(0, len(moves), 2):
        move_number = i // 2 + 1
        white_move = moves[i]
        black_move = moves[i + 1] if i + 1 < len(moves) else ""
        pgn_moves += f"{move_number}. {white_move} {black_move} "

    # Combine header and moves
    pgn_content = pgn_header + "\n" + pgn_moves.strip() + " " + result

    return pgn_content

if __name__ == "__main__":
    # Example usage
    sample_moves = ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"]
    pgn = generate_pgn(sample_moves)
    print("Generated PGN:")
    print(pgn)
