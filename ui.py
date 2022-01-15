import os

from qanda import Answer, Question, QuestionCard, QuestionType
from state import State
from utility import Hand, colorize, entire_east_asian_width, ljust_east_asian


def clear_view():
    os.system("clear")


def print_border():
    print("=" * 90)


def input_int(message="") -> int | None:
    while True:
        idx_opt = input(message + " ")
        if idx_opt == "exit":
            return None
        try:
            num = int(idx_opt)
        except ValueError:
            continue
        return num


def input_where(message="") -> tuple[int, ...] | None:
    while True:
        lis_opt = input(message + " ")
        if lis_opt == "exit":
            return None
        if lis_opt == "none":
            return tuple()
        if lis_opt == "":
            continue
        try:
            lis = list(map(lambda x: int(x) - 1, lis_opt.split()))
        except ValueError:
            continue
        return tuple(lis)


def aligned_question_cards(cards: list[QuestionCard]):
    qc_id_max = 0
    qc_desc_max = 0
    for card in cards:
        qc_id_max = max(qc_id_max, entire_east_asian_width(card.id_str()))
        qc_desc_max = max(qc_desc_max, entire_east_asian_width(card.description()))
    qc_id_max += len("Card<>")
    return [
        [ljust_east_asian(f"Card<{card.id_str()}>", qc_id_max), ljust_east_asian(card.description(), qc_desc_max)]
        for card in cards
    ]


def show_question_cards(cards: list[QuestionCard]):
    aligned = aligned_question_cards(cards)
    for idx, (qc_id, qc_desc) in enumerate(aligned):
        idx_str = f"[{idx}]".ljust(4, " ")
        print(f"{qc_id} {idx_str} {colorize(qc_desc)}")


def show_question_cards_in_deck(state: State):
    print("Awaiting question cards:")
    show_question_cards(state.question_cards_in_deck)
    print_border()


def show_question_cards_in_field(state: State):
    print("Current question cards:")
    show_question_cards(state.question_cards_in_field)
    print_border()


def show_possible_questions(state: State) -> list[Question]:
    questions = state.possible_questions()
    for idx, q in enumerate(questions):
        entropy = state.calc_entropy(q)
        groups = state.groupby(q)
        print(f"[{idx}] {q} : entropy {entropy}, max {max(map(len, groups.values()))}")
    print_border()
    return questions


def qa_list(state: State, question: Question) -> Answer | None:
    while True:
        clear_view()
        print(f"Asked {question}")
        lis = input_where("Answer:")
        if lis is None:
            return None
        return Answer(question.type, tuple(lis))


def qa_int(state: State, question: Question) -> Answer | None:
    while True:
        clear_view()
        print(f"Asked {question}")
        num = input_int("Answer:")
        if num is None:
            return None
        return Answer(question.type, num)


def qa(state: State) -> tuple[int, Question, Answer] | None:
    while True:
        clear_view()
        questions = show_possible_questions(state)
        idx = input_int("Which question do you ask?")
        if idx is None:
            return None
        if 0 <= idx < len(questions):
            pass
        else:
            continue
        question = questions[idx]
        if question.type == QuestionType.WHERE:
            answer = qa_list(state, question)
        elif question.type in (QuestionType.COUNT, QuestionType.SUM):
            answer = qa_int(state, question)
        elif question.type == QuestionType.SHARED:
            answer = qa_int(state, question)
        else:
            answer = None
        if answer is None:
            return None
        return (idx, question, answer)


def add(state: State) -> int | None:
    while True:
        clear_view()
        show_question_cards_in_deck(state)
        idx = input_int("which card has been added?")
        if idx is None:
            return None
        if 0 <= idx < len(state.question_cards_in_deck):
            return idx
        else:
            continue


def opponent(state: State) -> tuple[int, Question, Answer | None] | None:
    while True:
        clear_view()
        questions = show_possible_questions(state)
        idx = input_int("Which question did the opponent ask?")
        if idx is None:
            return None
        if 0 <= idx < len(questions):
            pass
        else:
            continue
        question = questions[idx]
        if question.type == QuestionType.SHARED:
            answer_opt = qa_int(state, question)
            if answer_opt is None:
                return None
            answer = answer_opt
        else:
            answer = None
        return (idx, question, answer)


def comma_separated_hands(hands: list[Hand]) -> str:
    return ", ".join(map(repr, hands))


def show_all_candidates(state: State):
    hands_per_line = 5
    separated_hands = [state.candidates[i : i + hands_per_line] for i in range(0, len(state.candidates), hands_per_line)]
    print("Candidates: [")
    for hands in separated_hands[:-1]:
        print(" " * 4 + comma_separated_hands(hands) + ",")
    print(" " * 4 + comma_separated_hands(separated_hands[-1]))
    print("]")


def show_dashboard(state: State, message="", show_all=False):
    # Your hand section
    print(f"Your hand: {state.hand}")
    print_border()
    # Question cards section
    show_question_cards_in_field(state)
    # Message section (if exists)
    if message:
        print(f"!! {message}")
        print_border()
    # Candidates of opponent's hand section
    print(f"Current candidates: {len(state.candidates)}")
    if len(state.candidates) <= 10 or show_all:
        show_all_candidates(state)
    print_border()


def input_command(state: State, message="", show_all=False):
    clear_view()
    show_dashboard(state, message, show_all)
    print("`q[uestion]` / `a[dd]` / `o[pponent]` / `s[ubmit]` / `show_all` / `undo`")
    return input("$ ")
