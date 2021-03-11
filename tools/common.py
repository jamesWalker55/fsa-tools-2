# common tools

from obj.fsa import FSA
from pathlib import Path
from obj.table import Table

def transition_table(graph: FSA):
    table = Table(["state"] + sorted(graph.used_alphabet()))
    added_states = set()
    for tr in graph.transitions:
        if tr.start not in added_states:
            added_states.add(tr.start)
            new_row = [tr.start] + [set() for i in range(table.num_columns - 1)]
            table.add_row(new_row)
        matching_rows = table["state", tr.start]
        if len(matching_rows) != 1:
            raise Exception("Something went horribly wrong! Multiple/Zero rows have the same state tr.start!")
        index = table.index_of(tr.letter)
        matching_rows[0][index].add(tr.end)
    return table