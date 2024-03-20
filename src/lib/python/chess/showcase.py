from sys import argv
from json import loads
from io import StringIO
from chess import pgn
import moviepy.editor as editor

from board import draw_board

def produce_short(
    output: str,
    game_pgn: str
):
    game_moves = list(
        pgn.read_game(StringIO(game_pgn))
        .mainline()
    )
    flipped = False

    for move_index, move_node in enumerate(game_moves):
        if pgn.NAG_BRILLIANT_MOVE in move_node.nags:
            game_moves = game_moves[move_index - 1:]
            flipped = move_node.turn()
            
            break
    else:
        raise ValueError("brilliant move not found in provided PGN.")
    
    board_clips = [
        draw_board(
            fen=game_moves[0].board().fen(),
            flipped=flipped,
            duration=5
        ),
        
        draw_board(
            fen=game_moves[0].board().fen(),
            flipped=flipped,
            highlighted_move=game_moves[1].uci(),
            animated=True,
            brilliancy=True,
            duration=0.2
        ).set_start(5),

        draw_board(
            fen=game_moves[1].board().fen(),
            flipped=flipped,
            highlighted_move=game_moves[1].uci(),
            brilliancy=True,
            duration=5
        ).set_start(5.2)
    ]

    result = editor.CompositeVideoClip(board_clips)

    result.write_videofile(
        filename=output,
        fps=24,
        audio_codec="aac",
        threads=14
    )


if __name__ == "__main__":
    args = loads(argv[1])

    produce_short(
        output=args["output"],
        game_pgn=args["pgn"]
    )