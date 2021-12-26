import os

from qanda import Answer, Question, QuestionType
from state import State


def clear_view():
    os.system("clear")


def print_border():
    print("=" * 80)


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


def show_question_cards_in_deck(state: State):
    print("Awaiting question cards:")
    for idx, qc in enumerate(state.question_cards_in_deck):
        print(f"[{idx}] {qc}")
    print_border()


def show_question_cards_in_field(state: State):
    print("Current question cards:")
    for idx, qc in enumerate(state.question_cards_in_field):
        print(f"[{idx}] {qc}")
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


def show_dashboard(state: State, message=""):
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
    if len(state.candidates) <= 10:
        print("Candidates:")
        print(state.candidates)
    print_border()


def input_command(state: State, message=""):
    clear_view()
    show_dashboard(state, message)
    print("`q[uestion]` / `a[dd]` / `o[pponent]` / `submit` / `undo`")
    return input("$ ")
