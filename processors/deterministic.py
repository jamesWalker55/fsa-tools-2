from obj.fsa import FSA
from pathlib import Path
from tools.common import transition_table
from obj.table import TransitionTable

def process(graph: FSA, original_path: Path):
    tr_table = transition_table(graph)
    det_table = TransitionTable(tr_table.labels[1:])
    det_table.add_row(tr_table[graph.start])
    for row in det_table.rows:
        letter_dests = row[1:]
        for dest in letter_dests:
            if len(dest) == 0:
                continue
            if det_table.state_recorded(dest):
                continue
            sub_dests = tuple(map(frozenset, dest))
            combined_row = tr_table.combined_state_rows(*sub_dests)
            det_table.add_row(combined_row)
    
    print(det_table)
