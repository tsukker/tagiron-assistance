from game import Game
from state import State


def main():
    initial_state = State()
    print(f"count: {len(initial_state.candidates)}")
    game = Game(initial_state)
    game.start()


if __name__ == "__main__":
    main()
