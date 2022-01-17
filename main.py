import sys

from game import Game
from state import State


def main():
    while True:
        initial_state = State()
        game = Game(initial_state)
        restart = game.start()
        if restart:
            continue
        sys.exit()


if __name__ == "__main__":
    main()
