import itertools
import json

import init_phase
import utility
from qanda import Answer, Question, QuestionCard, QuestionCardId, QuestionType
from utility import Hand

"""
`State` class represents the state of the game.
Note that `State` objects should be considered immutable.
"""


def all_question_cards():
    with open("questions.json") as f:
        raw_question_data = json.load(f)
    return [QuestionCard(QuestionCardId(data["id"]), data["ja"], data["en"]) for data in raw_question_data]


class State:
    def __init__(
        self,
        hand: Hand | None = None,
        candidates: list[Hand] | None = None,
        question_cards_in_deck: list[QuestionCard] | None = None,
        question_cards_in_field: list[QuestionCard] | None = None,
        question_cards_in_trash: list[QuestionCard] | None = None,
    ):
        self.hand = hand if hand else init_phase.input_hand_with_retry()
        self.candidates = init_phase.calculate_initial_candidates(self.hand) if candidates is None else candidates
        self.question_cards_in_deck = all_question_cards() if question_cards_in_deck is None else question_cards_in_deck
        self.question_cards_in_field: list[QuestionCard] = [] if question_cards_in_field is None else question_cards_in_field
        self.question_cards_in_trash: list[QuestionCard] = [] if question_cards_in_trash is None else question_cards_in_trash
        self.last_action = ""

    def copy(self):
        return State(
            self.hand,
            self.candidates,
            self.question_cards_in_deck,
            self.question_cards_in_field,
            self.question_cards_in_trash,
        )

    def calc_case(self, candidate: Hand) -> int:
        self_fives = list(filter(lambda tile: tile.num == 5, self.hand.tiles))
        cand_fives = list(filter(lambda tile: tile.num == 5, candidate.tiles))
        if len(self_fives) == 0 and len(cand_fives) == 1:
            return 2
        return 1

    def groupby(self, question: Question) -> dict[tuple[int, ...] | int, list[Hand]]:
        sorted_candidates = sorted(self.candidates, key=question.ask)
        groups = dict()
        for k, g in itertools.groupby(sorted_candidates, key=question.ask):
            groups[k] = list(g)
        return groups

    def calc_entropy(self, question: Question) -> float:
        groups = self.groupby(question)
        cases = [sum(map(self.calc_case, group)) for group in groups.values()]
        return utility.calc_entropy(cases)

    def possible_questions(self):
        questions = itertools.chain.from_iterable(map(lambda qc: qc.to_questions(), self.question_cards_in_field))
        return list(questions)

    def narrow_by_qa(self, question: Question, answer: Answer):
        groups = self.groupby(question)
        next_state = self.copy()
        next_state.candidates = groups[answer.value]
        for i, qc in enumerate(self.question_cards_in_field):
            if question.question_card.id == qc.id:
                next_state.question_cards_in_field.pop(i)
                next_state.question_cards_in_trash.append(qc)
        next_state.last_action = f"narrowed by question {question} and answer {answer}"
        return next_state

    def opposite_ask(self, question: Question, answer: Answer | None):
        next_state = self.copy()
        if question.type == QuestionType.SHARED:
            assert answer is not None
            groups = self.groupby(question)
            next_state.candidates = groups[answer.value]
        for i, qc in enumerate(self.question_cards_in_field):
            if question.question_card.id == qc.id:
                next_state.question_cards_in_field.pop(i)
                next_state.question_cards_in_trash.append(qc)
        next_state.last_action = f"opposite asked question {question}{f' and answer {answer} narrows' if answer else ''}"
        return next_state

    def add_question_card(self, idx: int):
        assert 0 <= idx < len(self.question_cards_in_deck)
        next_state = self.copy()
        qc = next_state.question_cards_in_deck.pop(idx)
        next_state.question_cards_in_field.append(qc)
        next_state.last_action = f"added question card `{qc.id}`"
        return next_state

    def delete_question_card(self, idx: int):
        assert 0 <= idx < len(self.question_cards_in_field)
        next_state = self.copy()
        qc = next_state.question_cards_in_field.pop(idx)
        next_state.question_cards_in_trash.append(qc)
        next_state.last_action = f"deleted question card `{qc.id}`"
        return next_state
