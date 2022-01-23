from obj.fsa import Transition
from typing import Union
from obj.fsa import FSA
from itertools import combinations


def _is_frozenset_or_set(obj):
    return isinstance(obj, frozenset) or isinstance(obj, set)


class Table:
    def __init__(self, headers: list[str]):
        self.labels = headers
        self.num_columns = len(headers)
        self.rows: list[list]
        self.rows = []
        self.label_index = None  # initialized later
        self._labels_to_index()

    def _labels_to_index(self):
        self.label_index = {}
        for i, label in enumerate(self.labels):
            self.label_index[label] = i

    def __getitem__(self, arg):
        """table lookup, return all matching rows

        table[column name, value] -> list of rows"""
        assert len(arg) == 2
        label, value = arg
        index = self.index_of(label)
        matches = []
        for row in self.rows:
            if row[index] == value:
                matches.append(row)
        if matches:
            return tuple(matches)
        else:
            raise KeyError(f"Can't find value {value} in column {label}.")

    def __repr__(self) -> str:
        return self.__str__()

    def _column_widths(self):
        """return tuple of string width of each column"""
        widths = [0] * self.num_columns
        for row in [list(self.labels)] + self.rows:
            for i in range(self.num_columns):
                width = len(str(row[i]))
                widths[i] = max(width, widths[i])
        return widths

    def __str__(self) -> str:
        CELL_PADDING = " "
        widths = self._column_widths()
        pretty_rows = []

        def generate_pretty(row):
            cells = []
            for width, content in zip(widths, row):
                pretty = str(content).rjust(width)
                cells.append(CELL_PADDING + pretty + CELL_PADDING)
            return "|".join(cells)

        pretty_rows.append(generate_pretty(self.labels))
        pretty_rows.append("=" * len(pretty_rows[0]))
        for row in self.rows:
            pretty_rows.append(generate_pretty(row))
        return "\n".join(pretty_rows)

    def add_row(self, row):
        if len(row) != self.num_columns:
            raise Exception("Given row doesn't have same number of columns as table!")
        self.rows.append(list(row))

    def index_of(self, label):
        """return index of given label"""
        return self.label_index[label]

    def copy_column(self, label=None, index=None):
        """input either column name or column index"""

        def row_get_val(row, index):
            return row[index]

        if label:
            index = self.index_of(label)
        return tuple(map(lambda row, i=index: row_get_val(row, i), self.rows))


class TransitionTable(Table):
    def __init__(self, alphabet: list[str]):
        super().__init__(["state"] + sorted(alphabet))
        self.num_letters = len(alphabet)
        # record all added states
        self.states = set()

    def __getitem__(self, state: frozenset[str]):
        if isinstance(state, frozenset):
            return super().__getitem__(("state", state))[0]
        elif isinstance(state, set):
            return super().__getitem__(("state", set(state)))[0]
        elif isinstance(state, str):
            return super().__getitem__(("state", frozenset([state])))[0]
        raise TypeError(
            f"TransitionTable is indexed by frozenset/set/str, not {type(state)}!"
        )

    def add_empty_state_row(self, state: frozenset[str]):
        """add a row with `state` as first column, rest as empty sets"""
        # add to record
        self.states.add(state)
        # create then add row
        empty_row = [state] + [set() for i in range(self.num_letters)]
        self.add_row(empty_row)

    def add_transition(self, transition: Transition):
        start = frozenset([transition.start])
        self.add_destination(start, transition.letter, transition.end)

    def add_destination(self, start: frozenset[str], letter: str, end: str):
        if start not in self.states:
            self.add_empty_state_row(start)
        index = self.index_of(letter)
        self[start][index].add(end)

    def add_row(self, row):
        if not all(map(_is_frozenset_or_set, row)):
            raise KeyError("Input cells must all be frozensets/sets!")
        self.states.add(row[0])
        return super().add_row(row)

    def set_destination(self, start: frozenset[str], letter: str, end: frozenset[str]):
        if start not in self.states:
            self.add_empty_state_row(start)
        index = self.index_of(letter)
        self[start][index] = end

    def freeze(self):
        """freezes all sets in the table"""
        for row in self.rows:
            for i, cell in enumerate(row):
                if isinstance(cell, set):
                    row[i] = frozenset(cell)

    def combined_state_rows(self, *states: tuple[frozenset[str]]):
        """return combined rows given the states"""
        if not all(_is_frozenset_or_set(x) for x in states):
            raise KeyError("Input states must be frozensets/sets!")
        states = [frozenset(x) for x in states]
        to_combine = []
        for state in states:
            to_combine.append(self[state])
        combined = list(zip(*to_combine))
        for i, sets in enumerate(combined):
            combined[i] = frozenset().union(*combined[i])
        return combined

    def state_recorded(self, state):
        """return whether state is recorded in `state` column"""
        try:
            self[state]
            return True
        except KeyError:
            return False

    def to_markdown(self):
        def set_to_string(s):
            if len(s) == 0:
                return "$\emptyset$"
            return ",".join(sorted(s))

        md = "|".join(self.labels) + "\n"
        md += "|".join(["-" for i in range(len(self.labels))]) + "\n"
        for row in self.rows:
            md += "|".join(map(set_to_string, row))
            md += "\n"
        return md


class MinimiseTable(Table):
    class NotAStateError(Exception):
        pass

    class InvalidPosition(Exception):
        pass

    def __init__(self, graph: FSA):
        self.states = sorted(graph.states())
        super().__init__(["state"] + self.states[:-1])
        for i, state in enumerate(self.states[:0:-1]):
            row = [state] + [False] * (self.num_columns - 1 - i) + [None] * i
            self.add_row(row)

    def _states_to_indexes(self, s1, s2):
        """given 2 states, return column and row

        will error if position is outside table"""
        if not (s1 in self.states and s2 in self.states):
            raise self.NotAStateError(f"{s1}, {s2}")
        s1, s2 = sorted((s1, s2))
        col = self.states.index(s1) + 1
        row = len(self.states) - self.states.index(s2) - 1
        if not (
            (0 <= row < self.num_columns)
            and (0 <= col - 1 < self.num_columns)
            and (col + row < self.num_columns)
        ):
            raise self.InvalidPosition(f"{s1}, {s2}")
        return col, row

    def __getitem__(self, key):
        """table[state 1, state 2] -> cell value"""
        assert len(key) == 2
        col, row = self._states_to_indexes(*key)
        return self.rows[row][col]

    def __setitem__(self, key, val):
        """table[state 1, state 2] = some bool value"""
        assert len(key) == 2
        # assert isinstance(val, bool)
        col, row = self._states_to_indexes(*key)
        self.rows[row][col] = val

    def _column_widths(self):
        """return tuple of string width of each column"""
        widths = [0] * self.num_columns
        for row in [list(self.labels)] + self.rows:
            for i in range(self.num_columns):
                element = row[i]

                if isinstance(element, bool) or element is None:
                    width = 1
                else:
                    width = len(str(element))
                widths[i] = max(width, widths[i])
        return widths

    def __str__(self) -> str:
        CELL_PADDING = " "
        widths = self._column_widths()
        pretty_rows = []

        def generate_pretty(row):
            cells = []
            for width, element in zip(widths, row):
                if element == True:
                    content = "X"
                elif element == False or element is None:
                    content = " "
                else:
                    content = str(element)
                cells.append(CELL_PADDING + content.rjust(width) + CELL_PADDING)
            return "|".join(cells)

        for row in self.rows[::-1]:
            pretty_rows.append(generate_pretty(row))
        pretty_rows.append("=" * len(pretty_rows[0]))
        pretty_rows.append(generate_pretty(self.labels))
        return "\n".join(pretty_rows)

    def generator(self):
        """return all valid state combinations for this table"""
        return combinations(self.states, 2)


class EpsilonTable(Table):
    class InvalidTransitionTableError(Exception):
        pass

    def __init__(self, ttable: TransitionTable):
        if not isinstance(ttable, TransitionTable):
            raise TypeError("Input must be the transition table for the graph!")
        old_headers = ttable.labels
        if not ("e" in old_headers or "ε" in old_headers):
            raise self.InvalidTransitionTableError(
                "Graph's alphabet doesn't contain epsilon! Likely doesn't need epsilon removal"
            )
        # convert epsilon to "e" instead of "ε"
        old_headers = ["e" if x == "ε" else x for x in old_headers]
        new_headers = ["d", *old_headers[1:], "e*"]
        super().__init__(new_headers)
        new_rows = [[*row, None] for row in ttable.rows]
        for row in new_rows:
            self.add_row(row)

    def __getitem__(self, arg):
        matches = super().__getitem__(arg)
        return matches[0]

    def combined_state_rows(self, *states: tuple[frozenset[str]]):
        """return combined rows given the states"""
        if not all(map(_is_frozenset_or_set, states)):
            raise KeyError("Input states must be frozensets/sets!")
        states = [frozenset(x) for x in states]
        to_combine = []
        for state in states:
            to_combine.append(self["d", state])
        combined = list(zip(*to_combine))
        for i, sets in enumerate(combined):
            combined[i] = frozenset().union(*combined[i])
        return combined

    def to_markdown(self):
        def set_to_string(s):
            if len(s) == 0:
                return "$\emptyset$"
            return ",".join(sorted(s))

        md = "|".join(self.labels) + "\n"
        md += "|".join(["-" for i in range(len(self.labels))]) + "\n"
        for row in self.rows:
            md += "|".join(set_to_string(x) for x in row)
            md += "\n"
        return md


if __name__ == "__main__":

    t = Table("i name color".split())
    t.add_row([1, "james", "blue"])
    t.add_row([2, "john", "red"])
    t.add_row([3, "jan", "pink"])

    t["i", 3][0][2] = "blackaaaaa"

    c = t.copy_column("color")

    a = TransitionTable("a b c".split())
    a.add_transition(Transition(*"q0 a q1".split()))
    a.add_transition(Transition(*"q0 b q1".split()))
    a.add_transition(Transition(*"q1 b q0".split()))
    a.add_transition(Transition(*"q2 a q1".split()))
    a.freeze()
    print(a)
    fs = lambda s: frozenset([s])
    print(a.to_markdown())
