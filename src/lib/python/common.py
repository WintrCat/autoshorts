def slide_to_position(
    start: tuple[int, int],
    end: tuple[int, int],
    duration: int
):
    return lambda t : (
        start[0] + (min(t, duration) / duration) * (end[0] - start[0]),
        start[1] + (min(t, duration) / duration) * (end[1] - start[1])
    )