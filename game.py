import sys

import ui
from qanda import Answer, Question
from state import State


class Game:
    def __init__(self, initial_state: State):
        self.history = [initial_state]
        self.future: list[State] = []
        self.message = ""

    def current_state(self):
        return self.history[-1]

    def set_message(self, new_message=""):
        self.message = new_message

    def narrow_by_qa(self, question: Question, answer: Answer):
        next_state = self.current_state().narrow_by_qa(question, answer)
        self.history.append(next_state)
        self.future = []

    def add_question_card(self, idx: int) -> None:
        next_state = self.current_state().add_question_card(idx)
        self.history.append(next_state)
        self.future = []

    def opposite_ask(self, question: Question, answer: Answer | None):
        next_state = self.current_state().opposite_ask(question, answer)
        self.history.append(next_state)
        self.future = []

    def delete_question_card(self, idx: int) -> None:
        next_state = self.current_state().delete_question_card(idx)
        self.history.append(next_state)
        self.future = []

    """
    You can execute specific commands interactively through the shell-like interface.
    Basically, each commands represent actual actions in the game.
    In another words, you need to convey what happened in the game to this system.

    There are two types of commands: basic commands and advanced commands.
    Basic commands represent real, concrete actions.
    Advanced commands are more like meta-actions, i.e. :
    - undo previous actions to go back to the past state,
    - save the state to file so that you can review how the game proceeded.
    Currently, below commands are available:
    - Basic commands
    -- question : Ask a question and obtain information
    -- add : Add the specified card in the deck to the field
    -- opposite : Opposite player asks a question (Obtain info if shared-type one is choosen)
    -- delete : Remove the specified card from the field to the trash
    - Advanced commands
    -- (none)
    """

    def start(self):
        while True:
            state = self.current_state()
            command = ui.input_command(state, self.message)
            if command == "finish":
                sys.exit()
            self.set_message()
            if command == "":
                continue
            elif "question".startswith(command):
                result = ui.qa(state)
                if result is None:
                    self.set_message("Cancelled `question`")
                    continue
                idx, question, answer = result
                self.narrow_by_qa(question, answer)
            elif "add".startswith(command):
                idx: int | None = ui.add(state)
                if idx is None:
                    self.set_message("Cancelled `add`")
                    continue
                self.add_question_card(idx)
            elif "opposite".startswith(command):
                result = ui.opposite(state)
                if result is None:
                    self.set_message("Cancelled `opposite`")
                    continue
                idx, question, answer = result
                self.opposite_ask(question, answer)
            elif "delete".startswith(command):
                idx: int | None = ui.delete(state)
                if idx is None:
                    self.set_message("Cancelled `delete`")
                    continue
                self.delete_question_card(idx)
            elif "submit".startswith(command):
                print("`submit` is not implemented now")
                pass
            elif "undo".startswith(command):
                print("`undo` is not implemented now")
                pass
            else:
                pass
