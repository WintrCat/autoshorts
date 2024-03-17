from sys import argv
from json import loads
from chess import pgn

import moviepy.editor as editor
from moviepy.video.fx.resize import resize
from moviepy.video.fx.scroll import scroll

from common import slide_to_position

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

def get_square(x: int, y: int, flipped: bool = False):
    return (
        list("abcdefgh")[(7 - x) if flipped else x]
        + (str(y + 1) if flipped else str(8 - y))
    )

def get_coordinates(square: str, flipped: bool = False):
    files = list("abcdefgh")
    return (
        (7 - files.index(square[0])) if flipped else files.index(square[0]),
        (int(square[1]) - 1) if flipped else 8 - int(square[1])
    )

def scale_coordinates(coords: tuple[int, int], board_width: int):
    return (
        coords[0] * (board_width / 8),
        coords[1] * (board_width / 8)
    )

def draw_board(
    fen: str,
    flipped: bool = False,
    highlighted_move: str = None,
    animated: bool = False,
    brilliancy: bool = False,
    width: int = 1080,
    duration: int = 10
):  
    board_flip_suffix = "flipped" if flipped else ""
    background = resize(
        (
            editor.ImageClip(f"{RESOURCES}/board{board_flip_suffix}.png")
            .set_duration(duration)
        ),
        newsize=(width, width)
    )

    pieces: list[editor.ImageClip] = []
    square_x = 7 if flipped else 0
    square_y = square_x
    for char in fen.split(" ")[0]:
        if char.isdigit():
            square_x += int(char) * (-1 if flipped else 1)
        elif char == "/":
            square_x = 7 if flipped else 0
            square_y += -1 if flipped else 1
        else:
            piece = resize(
                editor.ImageClip(f"{RESOURCES}/{PIECES[char]}.webp")
                .set_duration(duration)
                .set_position((
                    round(square_x * (width / 8)),
                    round(square_y * (width / 8))
                )),
                newsize=(
                    width / 8,
                    width / 8
                )
            )

            if animated:
                square_name = get_square(square_x, square_y, flipped)
                if square_name == highlighted_move[0:2]:
                    piece = piece.set_position(slide_to_position(
                        scale_coordinates(get_coordinates(square_name, flipped), width),
                        scale_coordinates(get_coordinates(highlighted_move[2:4], flipped), width),
                        duration - 0.1
                    ))

            pieces.append(piece)

            square_x += -1 if flipped else 1

    move_highlights = []
    if not highlighted_move is None:
        highlight_type = "brilliant" if brilliancy else "default"

        move_highlights = [
            resize(
                editor.ImageClip(f"{RESOURCES}/{highlight_type}highlight.png") 
                .set_duration(duration)
                .set_position(scale_coordinates(
                    get_coordinates(highlighted_move[i * 2 : i * 2 + 2], flipped),
                    width
                ))
                .set_opacity(0.7),
                newsize=(
                    width / 8,
                    width / 8
                )
            )
            
            for i in range(2)
        ]

        classification_icon_size = width / 18
        classification_icon_position = list(
            scale_coordinates(
                get_coordinates(highlighted_move[2:4], flipped),
                width
            )
        )
        classification_icon_position[0] += (width / 8) - (classification_icon_size / 1.5)
        classification_icon_position[1] -= classification_icon_size / 3

        classification_icon = resize(
            editor.ImageClip(f"{RESOURCES}/brilliant.webp")
            .set_duration(duration)
            .set_position(tuple(classification_icon_position)),
            newsize=(
                classification_icon_size, 
                classification_icon_size
            )
        )

    result_clips = [
        background,
        *move_highlights,
        *pieces
    ]

    if brilliancy:
        result_clips.append(classification_icon)

    return editor.CompositeVideoClip(result_clips)

game = list(
    pgn.read_game(
        open("./src/resources/chess/sample.pgn")
    )
    .mainline()
)

boards = []
for move_index, move_node in enumerate(game[:5]):
    boards.append(
        draw_board(
            move_node.board().fen(),
            duration=0.5,
            highlighted_move=move_node.uci(),
            brilliancy=True
        )
        .set_start(move_index * 0.7)
    )

    if move_index >= len(game) - 1:
        break

    upcoming_move = game[move_index + 1].uci()
    boards.append(
        draw_board(
            move_node.board().fen(),
            duration=0.2,
            highlighted_move=upcoming_move,
            animated=True,
            brilliancy=True
        )
        .set_start(move_index * 0.7 + 0.5)
    )

result = editor.CompositeVideoClip(boards)

result.write_videofile(
    "out/chess.mp4",
    fps=24,
    audio_codec="aac",
    threads=4
)