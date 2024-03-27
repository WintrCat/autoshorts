from random import randint, choice
from sys import argv
from json import loads

import moviepy.editor as editor
from moviepy.video.fx.resize import resize
from moviepy.audio.fx.volumex import volumex


class Question:
    title: str
    answers: list[str]
    correct_answer: int

    def __init__(self):
        self.answers = []


def produce_short(
    questions: list[Question],
    background: str,
    music: str,
    font: str,
    output: str
):
    question_count = len(questions)

    background_video_length = editor.VideoFileClip(background).duration
    background = resize(
        (
            editor.VideoFileClip(background)
            .cutout(0, randint(1, round(background_video_length) - 65))
            .set_duration(13.5 * question_count)
            .set_position(("center", "center"))
        ),
        height=1920
    )

    music = editor.CompositeAudioClip([
        editor.AudioFileClip(music)
        .set_end(13.5 * question_count)
    ])

    clips = []

    for question_index, question in enumerate(questions):
        question_text = (
            editor.TextClip(
                question["title"],
                fontsize=90, 
                color="white", 
                stroke_color="black", 
                stroke_width=2,
                method="caption",
                size=(1080, None),
                font=font
            )
            .set_position(("center", 0.1), relative=True)
            .set_start(question_index * 13.5)
            .set_duration(10)
        )
        clips.append(question_text)

        answer_texts = [
            (
                editor.TextClip(
                    f"{list('ABCD')[i]} - {question["answers"][i]}", 
                    fontsize=90, 
                    color="white", 
                    stroke_color="black", 
                    stroke_width=2,
                    method="caption",
                    size=(1080, None),
                    font=font
                )
                .set_position(("center", 0.3 + (i / 7)), relative=True)
                .set_start(question_index * 13.5)
                .set_duration(10)
            ) for i in range(len(question["answers"]))
        ]
        clips += answer_texts

        countdown_texts = [
            (
                editor.TextClip(
                    str(10 - i), 
                    fontsize=120, 
                    color="white", 
                    stroke_color="black", 
                    stroke_width=2,
                    method="caption",
                    size=(1080, None),
                    font=font
                )
                .set_start(question_index * 13.5 + i)
                .set_duration(1)
                .set_position(("center", 0.87), relative=True)
            ) for i in range(10)
        ]
        clips += countdown_texts

        correct_answer_text = (
            editor.TextClip(
                question["answers"][question["correct"]], 
                fontsize=120, 
                color="#00ff00", 
                stroke_color="black", 
                stroke_width=2,
                method="caption",
                size=(1080, None),
                font=font
            )
            .set_start(question_index * 13.5 + 10)
            .set_duration(3.5)
            .set_position("center")
        )
        clips.append(correct_answer_text)

    result = (
        editor.CompositeVideoClip(
            [
                background,
                *clips
            ], 
            size=(1080, 1920)
        )
        .set_audio(music)
    )

    result.write_videofile(
        output, 
        fps=24, 
        audio_codec="aac",
        threads=4
    )

if __name__ == "__main__":
    args = loads(argv[1])
    
    produce_short(
        questions=args["questions"],

        background=args["assets"]["background"],
        music=args["assets"]["music"],
        font=args["assets"]["font"],

        output=args["output"]
    )