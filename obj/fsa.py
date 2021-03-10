from collections import namedtuple
from collections import defaultdict
from functools import reduce
from typing import Union


Transition = namedtuple("Transition", ["start", "letter", "end"])


EPSILON = "ε"


class FSA:
    """A FSA representation"""

    def __init__(
        self,
        transitions: Union[set[Transition], None] = None,
        alphabet: Union[set[str], None] = None,
        start: Union[str, None] = None,
        ends: Union[set[str], None] = None
    ):
        self.transitions = transitions or set()
        self.alphabet = alphabet
        self.start = start
        self.ends = ends

    def __str__(self):
        return f"<FSA: {len(self.transitions)} transitions>"

    def clone(self):
        return FSA(
            self.transitions.copy(),
            self.alphabet.copy() if self._alphabet else None,
            self.start,
            self.ends.copy())

    # ==================transitions==================
    # transition doesn't need a special getter, regular is fine

    def add_transition(self, start, letter, end) -> None:
        transition = Transition(str(start), str(letter), str(end))
        self.transitions.add(transition)

    # ==================other properties==================

    def valid(self):
        """return whether graph can be rendered / is valid"""
        return self.start != None and self.ends != None

    def used_alphabet(self):
        """return set of all alphabet used in transitions"""
        return set(map(lambda t: t.letter, self.transitions))

    def states(self, transitions=None) -> frozenset[str]:
        """return set of all states used in transitions

        `transitions` argument is for unit testing
        """
        transitions = transitions or self.transitions
        states: set[str] = reduce(
            lambda acc, tr: acc | {tr.start, tr.end},
            transitions,
            set()
        )
        return frozenset(states)


if __name__ == '__main__':

    sigma = "{(q0 , a, q0), (q0 , b, q0 ), (q0 , b, q1 ), (q1, a, q2 ), (q1 , b, q2 )}"
    a_formal = "({a, b}, {q0 , q1 , q2 }, "+sigma+", q0, {q1 , q2 })"

    a_informal = """
    start 0
    end 1 2
    0 a 0
    0 b 0
    0 b 1
    1 a 2
    1 b 2
    """

    b_informal = """
    start 0
    end 0
    0 e 1
    0 b 2
    1 a 0
    2 a 1
    2 b 1
    2 a 2
    """
