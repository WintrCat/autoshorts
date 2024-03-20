from sys import argv
from json import loads
from io import StringIO
from chess import pgn

import moviepy.editor as editor
from moviepy.video.fx.resize import resize

from board import draw_board

clip_durations = {
    "puzzle": 10,
    "move": 0.2,
    "solution": 5
}
full_duration = sum(clip_durations.values())

def produce_short(
    output: str,
    game_pgn: str,
    background: str,
    font: str,
    music: str
):
    background = resize(
        (
            editor.ImageClip(background)
            .set_duration(full_duration)
            .set_position((0, 0))
        ),
        height=1920
    )

    question_text = (
        editor.TextClip(
            "Can you find the brilliant move?",
            font=font,
            fontsize=120,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(1080, None)
        )
        .set_duration(clip_durations["puzzle"])
        .set_position((0, 0.6), relative=True)
    )

    countdown_texts = [
        (
            editor.TextClip(
                str(clip_durations["puzzle"] - i),
                font=font,
                fontsize=120,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(1080, None)
            )
            .set_start(i)
            .set_duration(1)
            .set_position((0, 0.8), relative=True)
        ) for i in range(clip_durations["puzzle"])
    ]

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
            duration=clip_durations["puzzle"]
        ),
        
        draw_board(
            fen=game_moves[0].board().fen(),
            flipped=flipped,
            highlighted_move=game_moves[1].uci(),
            animated=True,
            brilliancy=True,
            duration=clip_durations["move"]
        ).set_start(clip_durations["puzzle"]),

        draw_board(
            fen=game_moves[1].board().fen(),
            flipped=flipped,
            highlighted_move=game_moves[1].uci(),
            brilliancy=True,
            duration=clip_durations["solution"]
        ).set_start(clip_durations["puzzle"] + clip_durations["move"])
    ]

    move_audio_clip = None
    brilliancy_san = game_moves[1].san()

    move_audio_clip_name = "move"
    if brilliancy_san.endswith("+"):
        move_audio_clip_name = "check"
    elif "x" in brilliancy_san:
        move_audio_clip_name = "capture"

    move_audio_clip = (
        editor.AudioFileClip(f"./src/resources/chess/{move_audio_clip_name}.mp3")
        .set_start(clip_durations["puzzle"])
    )

    music_clip = (
        editor.AudioFileClip(music)
        .cutout(0, 25)
        .set_duration(full_duration)
    )

    solution_text = (
        editor.TextClip(
            brilliancy_san,
            font=font,
            fontsize=160,
            color="#00ff00",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(1080, None)
        )
        .set_start(clip_durations["puzzle"])
        .set_duration(clip_durations["move"] + clip_durations["solution"])
        .set_position((0, 0.75), relative=True)
    )

    result = editor.CompositeVideoClip([
        background,
        question_text,
        *countdown_texts,
        solution_text,
        *board_clips
    ]).set_audio(
        editor.CompositeAudioClip([
            move_audio_clip,
            music_clip
        ])
    )

    result.write_videofile(
        filename=output,
        fps=24,
        audio_codec="aac",
        threads=4
    )


if __name__ == "__main__":
    args = loads(argv[1])

    produce_short(
        output=args["output"],
        game_pgn=args["pgn"],
        background=args["assets"]["background"],
        font=args["assets"]["font"],
        music=args["assets"]["music"]
    )