from sys import argv
from json import loads
from chess import pgn

import moviepy.editor as editor
from moviepy.video.fx.resize import resize

RESOURCES = "./src/resources/chess"
PIECES = {
    "r": "black_rook",
    "n": "black_knight",
    "b": "black_bishop",
    "q": "black_queen",
    "k": "black_king",
    "p": "black_pawn",
    "R": "white_rook",
    "N": "white_knight",
    "B": "white_bishop",
    "Q": "white_queen",
    "K": "white_king",
    "P": "white_pawn"
}

def draw_board(
    fen: str, 
    animated_move: str = None,
    x: int = 0,
    y: int = 0,
    width: int = 1080,
    duration: int = 10
):
    background = (
            editor.ImageClip(f"{RESOURCES}/board.png")
            .set_duration(duration)
            .set_position((x, y))
        )

    pieces = []

    square_x = 0
    square_y = 0
    for char in fen.split(" ")[0]:
        if char.isdigit():
            square_x += int(char)
            if square_x >= 8:
                square_x -= 8
        elif char == "/":
            square_x = 0
            square_y += 1
        else:
            piece = (
                editor.ImageClip(f"{RESOURCES}/next.png", transparent=True)
                .set_duration(duration)
                # .set_position((
                #     round(x + square_x * (width / 8)),
                #     round(y + square_y * (width / 8))
                # ))
            )
            pieces.append(piece)

            x += 1
            if square_x >= 8:
                square_x -= 8

    result = editor.CompositeVideoClip(
        [
            background,
            *pieces,
            (editor.ImageClip(f"{RESOURCES}/next.png", transparent=True)
                .set_duration(duration)
                .set_position((0.5, 0.5), relative=True))
        ]
    )

    return result


game = list(
    pgn.read_game(
        open("./src/resources/chess/sample.pgn")
    )
    .mainline()
)

board = draw_board(
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
    x=0,
    y=0,
    width=1080,
    duration=1
)

board.write_videofile(
    "out/chess.webm",
    fps=30,
    audio_codec="aac",
    threads=4
)