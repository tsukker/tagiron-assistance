import ui
from qanda import Answer, Question
from state import State


class Game:
    def __init__(self, initial_state: State):
        self.history = [initial_state]
        self.now = 0
        self.message = ""
        self.show_all_candidates = False

    def current_state(self):
        return self.history[self.now]

    def travel_to(self, idx):
        self.now = idx
        self.set_message(f"Travel to state <{self.history[self.now].last_action}>")

    def record_state(self, next_state: State):
        self.history = self.history[: self.now + 1] + [next_state]
        self.now += 1

    def set_message(self, new_message=""):
        self.message = new_message

    def narrow_by_qa(self, question: Question, answer: Answer):
        next_state = self.current_state().narrow_by_qa(question, answer)
        self.record_state(next_state)

    def add_question_card(self, idx: int) -> None:
        next_state = self.current_state().add_question_card(idx)
        self.record_state(next_state)

    def opponent_ask(self, question: Question, answer: Answer | None):
        next_state = self.current_state().opponent_ask(question, answer)
        self.record_state(next_state)

    """
    You can execute specific commands interactively through the shell-like interface.
    Basically, each commands represent actual actions in the game.
    In another words, you need to convey what happened in the game to this system.

    There are three types of commands: basic commands, advanced commands, and system commands.
    Basic commands represent real, concrete actions.
    Advanced commands are more like meta-actions, i.e. :
    - undo previous actions to go back to the past state,
    - save the state to file so that you can review how the game proceeded.
    System commands terminate the current game. Any other commands above cannot do that.

    Currently available commands are following:
    - Basic commands
    -- `question` : Ask a question and obtain information
    -- `add` : Add the specified card in the deck to the field
    -- `opponent` : Opponent asks a question (Obtain info if shared-type one is choosen)
    - Advanced commands
    -- `show_all` : Toggle show_all switch;
        if True, the dashboard shows all candidates even if the number of them is greater than 10
    - System commands
    -- `finish` : Finish the current game and quit the system
    -- `restart` : Finish the current game and start a new game
    """

    def start(self):
        while True:
            state = self.current_state()
            command = ui.input_command(state, self.message, self.show_all_candidates)
            if command == "finish":
                return False
            elif command == "restart":
                return True
            self.set_message()
            if command == "":
                continue
            elif "question".startswith(command):
                result = ui.qa(state, self.message, self.show_all_candidates)
                if result is None:
                    self.set_message("Cancelled `question`")
                    continue
                idx, question, answer = result
                self.narrow_by_qa(question, answer)
            elif "add".startswith(command):
                idx: int | None = ui.add(state, self.message, self.show_all_candidates)
                if idx is None:
                    self.set_message("Cancelled `add`")
                    continue
                self.add_question_card(idx)
            elif "opponent".startswith(command):
                result = ui.opponent(state, self.message, self.show_all_candidates)
                if result is None:
                    self.set_message("Cancelled `opponent`")
                    continue
                idx, question, answer = result
                self.opponent_ask(question, answer)
            elif "submit".startswith(command):
                print("`submit` is not implemented now")
                pass
            elif "show_all" == command:
                self.show_all_candidates = not self.show_all_candidates
            elif "history" == command:
                result = ui.maybe_travel(self.history, self.now, state, self.message, self.show_all_candidates)
                if result is None:
                    self.set_message("Cancelled `history`")
                    continue
                if result < 0 or len(self.history) <= result:
                    continue
                self.travel_to(result)
            elif "undo".startswith(command):
                print("`undo` is not implemented now")
                pass
            else:
                pass
