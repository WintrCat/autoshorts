from chess import (
    Board, 
    square_name as square_name_of, 
    parse_square, 
    PAWN
)
import moviepy.editor as editor
from moviepy.video.fx.resize import resize
from moviepy.video.compositing.transitions import crossfadeout

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


def get_coordinates(square: str, flipped: bool = False, board_width: int = 1080):
    files = list("abcdefgh")
    return (
        ((7 - files.index(square[0])) if flipped else files.index(square[0])) * (board_width / 8),
        ((int(square[1]) - 1) if flipped else 8 - int(square[1])) * (board_width / 8)
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
    piece_clips = []

    board = Board(fen)

    ep_square = None
    ep_fade_square = None
    
    if not board.ep_square is None:
        ep_square = square_name_of(board.ep_square)
        if ep_square[1] == "3":
            ep_fade_square = ep_square[0] + "4"
        else:
            ep_fade_square = ep_square[0] + "5"

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
                    square_x * (width / 8),
                    square_y * (width / 8)
                )),
                newsize=(
                    width / 8,
                    width / 8
                )
            )

            square_name = get_square(square_x, square_y, flipped)
            if animated:
                if square_name == highlighted_move[0:2]:
                    piece = piece.set_position(slide_to_position(
                        get_coordinates(square_name, flipped),
                        get_coordinates(highlighted_move[2:4], flipped),
                        duration - 0.05
                    ))
                elif (
                    square_name == highlighted_move[2:4]
                    or (
                        square_name == ep_fade_square
                        and highlighted_move[2:4] == ep_square
                        and board.piece_at(parse_square(highlighted_move[0:2])).piece_type == PAWN
                    )
                ):
                    piece = crossfadeout(piece, duration - 0.05)                    

            piece_clips.append(piece)

            square_x += -1 if flipped else 1

    move_highlights = []
    if not highlighted_move is None:
        highlight_type = "brilliant" if brilliancy else "default"

        move_highlights = [
            resize(
                editor.ImageClip(f"{RESOURCES}/{highlight_type}highlight.png") 
                .set_duration(duration)
                .set_position(
                    get_coordinates(highlighted_move[i * 2 : i * 2 + 2], flipped)
                )
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
            get_coordinates(highlighted_move[2:4], flipped)
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
        *piece_clips
    ]

    if brilliancy:
        result_clips.append(classification_icon)

    return editor.CompositeVideoClip(result_clips)