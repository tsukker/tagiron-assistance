import itertools
import os

from utility import Color, Hand, Tile


def input_hand_print_help():
    os.system("clear")
    print(
        """Example:
    - `1r` for red 1
    - `2b` for blue 2
    - `5` for green 5
    """
    )


def input_tile():
    while True:
        tile_opt = input("Input your tile: ")
        if len(tile_opt) < 1:
            print("Input length must be two (or one for tile `5`), please retry.")
            continue
        if tile_opt[0] < "0" or "9" < tile_opt[0]:
            print("First character must be between `0` and `9`, please retry.")
            continue
        num = int(tile_opt[0])
        if num == 5:
            return Tile(num, Color.GREEN)
        if len(tile_opt) < 2:
            print("Input length must be two, please retry.")
            continue
        color_opt = tile_opt[1].lower()
        if color_opt not in ("r", "b"):
            print("Second character must be `r` or `b`, please retry.")
            continue
        color = Color.RED if color_opt == "r" else Color.BLUE
        return Tile(num, color)


def input_hand():
    tiles: list[Tile] = []
    while len(tiles) < 5:
        os.system("clear")
        input_hand_print_help()
        print(f"Current hand: {Hand(tiles)}")
        tile = input_tile()
        if tile.num == 5:
            if sum(1 for tile in tiles if tile.num == 5) == 2:
                print("Both two `5` tiles already in your hand, please retry.")
                continue
            else:
                pass  # valid new tile
        elif tile in tiles:
            print("That tile already in your hand, please retry.")
            continue
        tiles.append(tile)
    return Hand(tiles)


def input_hand_with_retry():
    while True:
        hand = input_hand()
        print(hand)
        while True:
            confirmation = input("Correct? (yes/no) [yes] ")
            if confirmation == "no":
                print("Please retry.")
                break
            elif confirmation == "yes" or confirmation == "":
                return hand
            else:
                continue


def prepare_other_tiles(hand: Hand):
    idx = 0
    other_tiles: list[Tile] = []
    for num in range(10):
        for color in (Color.RED, Color.BLUE):
            tile = Tile(num, color)
            if num == 5:
                tile = Tile(num, Color.GREEN)
            if idx < 5 and tile == hand.tiles[idx]:
                idx += 1
                continue
            else:
                other_tiles.append(tile)
    return other_tiles


def calculate_initial_candidates(hand: Hand):
    other_tiles: list[Tile] = prepare_other_tiles(hand)
    print(f"Other tiles <{' '.join(map(str, other_tiles))}>")
    with_duplicate = sorted(itertools.combinations(other_tiles, 5))
    assert len(with_duplicate) > 0
    candidates = [Hand(list(with_duplicate[0]))]
    for tiles, tiles_prev in zip(with_duplicate[1:], with_duplicate):
        if tiles != tiles_prev:
            candidates.append(Hand(list(tiles)))
    return candidates
