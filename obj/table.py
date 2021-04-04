# Allowing running this file directly
if __name__ == "__main__":
    import sys
    sys.path.append("../")

from obj.fsa import Transition
from typing import Union
from obj.fsa import FSA

def _is_frozenset_or_set(obj):
    return isinstance(obj, frozenset) or isinstance(obj, set)


class Table:
    def __init__(self, headers: list[str]):
        self.labels = headers
        self.num_columns = len(headers)
        self.rows: list[list]
        self.rows = []
        self._labels_to_index()

    def __getitem__(self, arg):
        """table[label, value] -> list of rows"""
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

    def __str__(self) -> str:
        widths = self.column_widths()
        pretty_rows = []
        header = True
        for row in ([list(self.labels)] + self.rows):
            pretty_items = []
            for i, content in enumerate(row):
                pretty = str(content).rjust(widths[i])
                pretty_items.append(" " + pretty + " ")
            pretty_rows.append("|".join(pretty_items))
            if header:
                line = "=" * len(pretty_rows[0])
                pretty_rows.append(line)
                header = False
        return "\n".join(pretty_rows)
        

    def add_row(self, row):
        if len(row) != self.num_columns:
            raise Exception("Given row doesn't have same number of columns as table!")
        self.rows.append(list(row))

    def _labels_to_index(self):
        self.label_index = {}
        for i, label in enumerate(self.labels):
            self.label_index[label] = i

    def index_of(self, label):
        return self.label_index[label]

    def copy_column(self, label=None, index=None):
        """input either column name or column index"""
        def row_get_val(row, index):
            return row[index]
        if label:
            index = self.index_of(label)
        return tuple(map(lambda row, i=index: row_get_val(row, i), self.rows))

    def column_widths(self):
        """return tuple of string width of each column"""
        widths = [0 for i in range(self.num_columns)]
        for row in ([list(self.labels)] + self.rows):
            for i in range(self.num_columns):
                width = len(str(row[i]))
                widths[i] = width if width > widths[i] else widths[i]
        return widths


class TransitionTable(Table):
    def __init__(self, alphabet: list[str]):
        super().__init__(["state"] + alphabet)
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
        raise TypeError(f"TransitionTable is indexed by frozenset/set/str, not {type(state)}!")

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
        if not all(map(_is_frozenset_or_set, states)):
            raise KeyError("Input states must be frozensets/sets!")
        states = map(frozenset, states)
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
            return ",".join(sorted(s))
        md = "|".join(self.labels) + "\n"
        md += "|".join(["-" for i in range(len(self.labels))]) + "\n"
        for row in self.rows:
            md += "|".join(map(set_to_string, row))
            md += "\n"
        return md


class MinimiseTable(Table):
    def __init__(self, graph: FSA):
        self.states = sorted(graph.states())
        super().__init__(["state"] + self.states)

if __name__ == '__main__':

    t = Table("i name color".split())
    t.add_row([1, "james", "blue"])
    t.add_row([2, "john", "red"])
    t.add_row([3, "jan", "pink"])

    t["i",3][0][2] = "blackaaaaa"

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