from collections import namedtuple
from collections import defaultdict
from functools import reduce
from typing import Union


Transition = namedtuple("Transition", ["start", "letter", "end"])


EPSILON = "ε"


class FSA:
    """A FSA representation
    
    ```
    transitions: set[Transition]
    alphabet: set[str]
    start: str
    ends: set[str]
    ```
    """

    def __init__(self, transitions=None, alphabet=None, start=None, ends=None):
        self.transitions: set[Transition] = transitions or set()
        self.alphabet: set[str] = alphabet or set()
        self.start: str = start or ""
        self.ends: set[str] = ends or set()

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

    def to_informal(self):
        """return string with informal representation of self"""
        informal = "format informal\n\n"
        informal += f"start {self.start}\n"
        informal += f"end {' '.join(sorted(self.ends))}\n"
        for tr in self.transitions:
            informal += f"{tr.start} {tr.letter} {tr.end}\n"
        return informal
