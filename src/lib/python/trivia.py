from random import choice
import moviepy.editor as editor
from moviepy.video.fx.resize import resize

from args import parse_args

class Question:
    title: str
    answers: list[str]
    correct_answer: int

    def __init__(self):
        self.answers = []

# Parse trivia files into object
trivia: dict[str, list[Question]] = {}

categories = [
    "animals", 
    "games"
]

for category in categories:
    questions: list[Question] = []

    f = (
        open(f"src/resources/trivia/{category}.txt", "r", encoding="utf-8")
        .read()
        .split("\n")
    )
    for line in f:
        data = " ".join(line.split(" ")[1:])

        if line.startswith("#Q"):
            questions.append(Question())
            questions[-1].title = data
        elif line.startswith("^"):
            questions[-1].correct_answer = data
        elif len(line) > 0 and line[0] in list("ABCD"):
            questions[-1].answers.append(data)

    trivia.update({ category: questions })

# Filter out trivia questions with long answers or titles
def every(arr: list, predicate):
    for item in arr:
        if not predicate(item):
            return False
    return True

for category in trivia:
    trivia[category] = [
        question for question in trivia[category]
        if len(question.title) <= 64
        and len(question.answers) == 4
        and every(question.answers, lambda ans : len(ans) <= 40)
    ]

# Get a random question from a category
def get_question(category: str = None):
    return choice(
        trivia[choice(categories) if category == None else category]
    )

# Produce trivia video
def produce_trivia_short(
    trivia_category: str,
    question_count: int,
    background: str,
    music: str,
    font: str,
    output: str
):
    # Show question for 10 seconds, answer for 3.5 secs

    background = resize(
        (
            editor.ImageClip(background)
            .set_duration(13.5 * question_count)
        ),
        height=1280
    )

    music = editor.CompositeAudioClip([
        editor.AudioFileClip(music)
        .cutout(0, 25)
        .set_end(13.5 * question_count)
    ])

    clips = []

    for question_index in range(min(10, question_count)):
        question = get_question(
            choice(categories) if trivia_category == None else trivia_category
        )
        trivia[trivia_category].remove(question)

        question_text = (
            editor.TextClip(
                question.title,
                fontsize=60, 
                color="white", 
                stroke_color="black", 
                stroke_width=2,
                method="caption",
                size=(720, None),
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
                    f"{list('ABCD')[i]} - {question.answers[i]}", 
                    fontsize=60, 
                    color="white", 
                    stroke_color="black", 
                    stroke_width=2,
                    method="caption",
                    size=(720, None),
                    font=font
                )
                .set_position(("center", 0.3 + (i / 7)), relative=True)
                .set_start(question_index * 13.5)
                .set_duration(10)
            ) for i in range(4)
        ]
        clips += answer_texts

        countdown_texts = [
            (
                editor.TextClip(
                    str(10 - i), 
                    fontsize=80, 
                    color="white", 
                    stroke_color="black", 
                    stroke_width=2,
                    method="caption",
                    size=(720, None),
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
                question.correct_answer, 
                fontsize=80, 
                color="#00ff00", 
                stroke_color="black", 
                stroke_width=2,
                method="caption",
                size=(720, None),
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
            size=(720, 1280)
        )
        .set_audio(music)
    )

    result.write_videofile(
        output, 
        fps=30, 
        audio_codec="aac"
    )

if __name__ == "__main__":
    arguments = parse_args()
    print(arguments)
    print(arguments["category"])
    produce_trivia_short(
        trivia_category=arguments["category"],
        question_count=arguments["count"],
        background=arguments["background"],
        music=arguments["music"],
        font=arguments["font"],
        output=arguments["output"]
    )