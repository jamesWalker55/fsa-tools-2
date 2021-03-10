import typing
from collections import namedtuple
from collections import defaultdict
from functools import reduce


class FSA:
    """A FSA representation"""

    def __init__(self, transitions=None, alphabet=None, start=None, ends=None):
        self.transitions = transitions or list()
        self._alphabet = alphabet or set()
        self.start = start
        self.ends = ends or list()

    def __str__(self):
        return f"<FSA: {len(self.transitions)} transitions>"

    @staticmethod
    def clone(graph):
        return FSA(
            graph.transitions.copy(),
            graph.alphabet.copy() if graph._alphabet else None,
            graph.start,
            graph.ends.copy())

    # ==================alphabet getter, setter==================
    @property
    def alphabet(self):
        if self._alphabet:
            return self._alphabet
        return frozenset(map(lambda t: t.letter, self.transitions))

    @alphabet.setter
    def alphabet(self, value):
        self._alphabet = value

    # ==================start getter, setter==================
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if value is not None:
            self._start = str(value)
        else:
            self._start = None

    # ==================ends getter, setter==================
    @property
    def ends(self):
        return self._ends

    @ends.setter
    def ends(self, value):
        if value is not None:
            self._ends = frozenset(map(lambda x: str(x), value))
        else:
            self._ends = None

    # ==================transitions==================
    # transition doesn't need a special getter, regular is fine

    def add_transition(self, start, letter, end) -> None:
        transition = Transition(str(start), str(letter), str(end))
        self.transitions.append(transition)

    def remove_duplicate_transitions(self) -> None:
        self.transitions = list(set(self.transitions))

    def combined_transitions(self):
        """Combines `a 1 b`, `a 2 b` to `a (1,2) b`"""
        def tuple_to_transitions(pair, letters):
            start, end = pair
            return Transition(start, ", ".join(letters), end)

        pairs_to_Letters = defaultdict(list)
        for transition in self.transitions:
            pair = (transition.start, transition.end)
            pairs_to_Letters[pair].append(transition.letter)

        return (tuple_to_transitions(k, v) for k, v in pairs_to_Letters.items())

    # ==================other properties==================
    def states(self) -> frozenset:
        # return list of states
        # from getting all transitions
        states = reduce(
            lambda acc, tr: acc | {tr.start, tr.end},
            self.transitions,
            set()
        )
        return frozenset(states)

    def is_deterministic(self) -> bool:
        for _, paths in self.transition_dmap().items():
            for _, destinations in paths.items():
                if len(destinations) > 1:
                    return False
        return True

    def formalize(self) -> str:
        def iterable_to_string(ss):
            if isinstance(ss, set) or isinstance(ss, frozenset):
                ss = sorted(ss)
            return "{" + ",".join(ss) + "}"

        alphabet = iterable_to_string(self.alphabet)
        all_states = set(x for tr in self.transitions for x in [
                         tr.start, tr.end])
        all_states = iterable_to_string(all_states)
        transitions = sorted(
            f"({tr.start},{tr.letter},{tr.end})" for tr in self.transitions)
        transitions = iterable_to_string(transitions)
        initial_state = self.start
        final_states = iterable_to_string(self.ends)
        output = (alphabet, all_states, transitions,
                  initial_state, final_states)
        return iterable_to_string(output)

    def transition_dmap(self):
        tmap = defaultdict(lambda: defaultdict(set))
        # create sets
        for tr in self.transitions:
            tmap[tr.start][tr.letter].add(tr.end)
        # convert to frozenset
        for start in tmap:
            for letter in tmap[start]:
                tmap[start][letter] = frozenset(tmap[start][letter])
        # create dicts for states without outgoing transitions
        for state in self.states():
            tmap[state]
        return tmap


Transition = namedtuple("Transition", ["start", "letter", "end"])


EPSILON = "ε"


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

