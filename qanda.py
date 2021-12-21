import collections
import re
from enum import Enum

from utility import Color, Hand


class QuestionCardId(Enum):
    WHERE_0 = "where_0"
    WHERE_12 = "where_12"
    WHERE_34 = "where_34"
    WHERE_5 = "where_5"
    WHERE_67 = "where_67"
    WHERE_89 = "where_89"
    WHERE_SEQUENTIAL = "where_sequential"
    WHERE_NEIGHBORING_SAME_COLOR = "where_neighboring_same_color"

    COUNT_EVEN = "count_even"
    COUNT_ODD = "count_odd"
    COUNT_RED = "count_red"
    COUNT_BLUE = "count_blue"
    COUNT_PAIRS = "count_pairs"

    SUM_3_LEFT = "sum_3_left"
    SUM_3_MIDDLE = "sum_3_middle"
    SUM_3_RIGHT = "sum_3_right"
    SUM_RED = "sum_red"
    SUM_BLUE = "sum_blue"

    SHARED_SUM_ALL = "shared_sum_all"
    SHARED_CENTER_45 = "shared_center_45"
    SHARED_DIFF_MIN_MAX = "shared_diff_min_max"


class QuestionType(Enum):
    WHERE = "where"
    COUNT = "count"
    SUM = "sum"
    SHARED = "shared"


class Answer:
    def __init__(self, type: QuestionType, value: int | tuple[int, ...]):
        self.type = type
        self.value = value
        if self.type == QuestionType.WHERE:
            assert isinstance(self.value, tuple)
        elif self.type in (QuestionType.COUNT, QuestionType.SUM):
            assert isinstance(self.value, int)
        elif self.type == QuestionType.SHARED:
            raise NotImplementedError
        else:
            assert False

    def __repr__(self):
        return f"Answer<{self.value}>"


# ca: calculate answer
def ca_where_x(hand: Hand, x: int) -> tuple[int, ...]:
    ans = []
    for idx, tile in enumerate(hand.tiles):
        if tile.num == x:
            ans.append(idx)
    return tuple(ans)


def ca_where_sequential(hand: Hand) -> tuple[int, ...]:
    ans = []
    for idx in range(4):
        if hand.tiles[idx].num + 1 == hand.tiles[idx + 1].num:
            ans.append(idx)
    return tuple(ans)


def ca_where_neighboring_same_color(hand: Hand) -> tuple[int, ...]:
    ans = []
    for idx in range(4):
        if hand.tiles[idx].color == hand.tiles[idx + 1].color:
            ans.append(idx)
    return tuple(ans)


def ca_count_even_odd(hand: Hand, odd: bool = False) -> int:
    rest = 0
    if odd:
        rest = 1
    return sum(1 for tile in hand.tiles if tile.num % 2 == rest)


def ca_count_red_blue(hand: Hand, blue: bool = False) -> int:
    color = Color.RED
    if blue:
        color = Color.BLUE
    return sum(1 for tile in hand.tiles if tile.color == color)


def ca_count_pairs(hand: Hand) -> int:
    nums = [tile.num for tile in hand.tiles]
    counts = collections.Counter(nums).values()
    return sum(1 for cnt in counts if cnt == 2)


def ca_sum_3_x(hand: Hand, start: int = 0, count: int = 3) -> int:
    nums = [tile.num for tile in hand.tiles]
    return sum(nums[start : start + count])  # noqa: E203


def ca_sum_red_blue(hand: Hand, blue: bool = False) -> int:
    color = Color.RED
    if blue:
        color = Color.BLUE
    nums = [tile.num for tile in hand.tiles if tile.color == color]
    return sum(nums)


class QuestionCard:
    def __init__(self, qcid: QuestionCardId, ja: str, en: str):
        self.id = qcid
        assert isinstance(self.id.value, str)
        self.ja, self.en = ja, en
        if self.id.value.startswith("where_"):
            self.type = QuestionType.WHERE
        elif self.id.value.startswith("count_"):
            self.type = QuestionType.COUNT
        elif self.id.value.startswith("sum_"):
            self.type = QuestionType.SUM
        elif self.id.value.startswith("shared_"):
            self.type = QuestionType.SHARED
        else:
            assert False

    def __repr__(self):
        ja_shrinked = re.sub(r"\n[\s\S]*$", "...", self.ja_without_lf())
        return f"Card<{self.id.value}> {ja_shrinked}"

    def ja_without_lf(self):
        return self.ja.replace("\n", " ")

    def to_questions(self):
        if self.id == QuestionCardId.WHERE_12:
            return [Question(self, 1), Question(self, 2)]
        if self.id == QuestionCardId.WHERE_34:
            return [Question(self, 3), Question(self, 4)]
        if self.id == QuestionCardId.WHERE_67:
            return [Question(self, 6), Question(self, 7)]
        if self.id == QuestionCardId.WHERE_89:
            return [Question(self, 8), Question(self, 9)]
        if self.type == QuestionType.SHARED:
            return []
        return [Question(self)]


class Question:
    def __init__(self, question_card: QuestionCard, option: int | None = None):
        self.question_card = question_card
        self.option = option
        self.type = self.question_card.type

    # NOTE: too specific implementation
    def __repr__(self):
        description = self.question_card.ja_without_lf()
        opt = "" if self.option is None else f", option({self.option})"
        return f"Question<{description}{opt}>"

    def ask(self, hand: Hand):
        if self.question_card.id == QuestionCardId.WHERE_0:
            return ca_where_x(hand, 0)
        elif self.question_card.id == QuestionCardId.WHERE_12:
            assert self.option in (1, 2)
            return ca_where_x(hand, self.option)
        elif self.question_card.id == QuestionCardId.WHERE_34:
            assert self.option in (3, 4)
            return ca_where_x(hand, self.option)
        elif self.question_card.id == QuestionCardId.WHERE_5:
            return ca_where_x(hand, 5)
        elif self.question_card.id == QuestionCardId.WHERE_67:
            assert self.option in (6, 7)
            return ca_where_x(hand, self.option)
        elif self.question_card.id == QuestionCardId.WHERE_89:
            assert self.option in (8, 9)
            return ca_where_x(hand, self.option)
        elif self.question_card.id == QuestionCardId.WHERE_SEQUENTIAL:
            return ca_where_sequential(hand)
        elif self.question_card.id == QuestionCardId.WHERE_NEIGHBORING_SAME_COLOR:
            return ca_where_neighboring_same_color(hand)
        elif self.question_card.id == QuestionCardId.COUNT_EVEN:
            return ca_count_even_odd(hand)
        elif self.question_card.id == QuestionCardId.COUNT_ODD:
            return ca_count_even_odd(hand, odd=True)
        elif self.question_card.id == QuestionCardId.COUNT_RED:
            return ca_count_red_blue(hand)
        elif self.question_card.id == QuestionCardId.COUNT_BLUE:
            return ca_count_red_blue(hand, blue=True)
        elif self.question_card.id == QuestionCardId.COUNT_PAIRS:
            return ca_count_pairs(hand)
        elif self.question_card.id == QuestionCardId.SUM_3_LEFT:
            return ca_sum_3_x(hand)
        elif self.question_card.id == QuestionCardId.SUM_3_MIDDLE:
            return ca_sum_3_x(hand, start=1)
        elif self.question_card.id == QuestionCardId.SUM_3_RIGHT:
            return ca_sum_3_x(hand, start=2)
        elif self.question_card.id == QuestionCardId.SUM_RED:
            return ca_sum_red_blue(hand)
        elif self.question_card.id == QuestionCardId.SUM_BLUE:
            return ca_sum_red_blue(hand, blue=True)
        else:
            raise NotImplementedError
