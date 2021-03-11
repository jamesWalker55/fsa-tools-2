from obj.fsa import FSA
from pathlib import Path
from processors.transitiontable import transition_table
from obj.table import TransitionTable

def process(graph: FSA, original_path: Path):
    det_table = deterministic_table(graph)
    print(det_table)
    
    graph = deterministic_table_to_graph(det_table, graph)
    output_path = original_path.with_name(f"{original_path.stem}_det.txt")
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(graph.to_informal())

def deterministic_table(graph: FSA):
    tr_table = transition_table(graph)
    det_table = TransitionTable(tr_table.labels[1:])
    det_table.add_row(tr_table[graph.start])
    for row in det_table.rows:
        letter_dests = row[1:]
        for dest in letter_dests:
            if len(dest) == 0 or det_table.state_recorded(dest):
                continue
            if len(dest) > 1:
                sub_dests = tuple(map(lambda s: frozenset([s]), dest))
                combined_row = tr_table.combined_state_rows(*sub_dests)
                det_table.add_row(combined_row)
            else:
                det_table.add_row(tr_table[dest])
    return det_table


def deterministic_table_to_graph(tr_table: TransitionTable, original_graph: FSA) -> FSA:
    graph = FSA()
    # graph start
    graph.start = original_graph.start
    # graph ends
    for state in tr_table.states:
        if len(state & original_graph.ends) != 0:
            graph.ends.add(set_to_string(state))
    # transitions
    letters = tr_table.labels[1:]
    for row in tr_table.rows:
        start = set_to_string(row[0])
        for i, letter in enumerate(letters):
            end = row[i+1]
            if len(end) == 0:
                continue
            end = set_to_string(end)
            graph.add_transition(start, letter, end)
    return graph


def set_to_string(s):
    return ",".join(sorted(s))