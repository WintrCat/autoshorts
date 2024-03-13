from util import MEDIA
from trivia import produce_trivia_short

produce_trivia_short(
    trivia_category="games",
    question_count=3,
    background=f"{MEDIA}/starrynight.jpg",
    music=f"{MEDIA}/shootingstars.mp3",
    font=f"{MEDIA}/Madimi.ttf",
    output="out/result.mp4"
)