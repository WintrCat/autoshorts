from chess import pgn

from board import draw_board

game = list(
    pgn.read_game(
        open("./src/resources/chess/sample.pgn")
    )
    .mainline()
)
flipped = None

for move_index, move_node in enumerate(game):
    if 3 in move_node.nags:
        flipped = move_node.board().turn
        game = game[move_index - 1:]
        break
else:
    print("brilliant move not found in provided PGN.")
    exit()

board_clips = []

board_clips.append(draw_board(
    move_node.board().fen(),
    flipped=flipped,
    duration=10
))