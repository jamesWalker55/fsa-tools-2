from obj.fsa import FSA
from pathlib import Path
from tools.common import transition_table
from obj.table import Table

# class fs(frozenset):
#     def __str__(self) -> str:
#         original = super().__str__()
#         return original.replace("frozenset", "fs")

def process(graph: FSA, original_path: Path):
    tr_table = transition_table(graph)
    det_table = init_deterministic_table(tr_table, graph)
    loop_process_table(det_table, tr_table)
    
    print(det_table)

def create_starting_row(tr_table: Table, graph: FSA):
    """create the first row for the new deterministic table

    `tr_table` is the original transition table
    
    `graph` us the original graph"""
    original_first_row = tr_table["state", graph.start][0]
    det_first_row = []
    for i, cell in enumerate(original_first_row):
        if i == 0:
            det_first_row.append(frozenset([cell]))
        else:
            det_first_row.append(frozenset(cell))
    return det_first_row

def init_deterministic_table(tr_table: Table, graph: FSA):
    det_table = Table(tr_table.labels)
    det_table.add_row(create_starting_row(tr_table, graph))
    return det_table

def loop_process_table(deterministic: Table, tr_table: Table):
    added_states = set(deterministic.copy_column("state"))
    for row in deterministic.rows:
        used_destinations = frozenset(map(frozenset, row[1:]))
        for final_dest in used_destinations:
            if len(final_dest) != 0 and final_dest not in added_states:
                added_states.add(final_dest)
                dest_row = create_dest_row(tr_table, final_dest)
                deterministic.add_row(dest_row)


def create_dest_row(tr_table: Table, final_dest: frozenset[str]) -> list:
    sub_rows = []
    for subdest in final_dest:
        # find row matching subdestination and append it
        sub_row = tr_table["state", subdest][0]
        sub_rows.append(sub_row)
    combined_row = list(zip(*sub_rows))
    for i, dests in enumerate(combined_row):
        if i == 0:
            # replace start state
            combined_row[0] = final_dest
        else:
            # combine states
            combined_row[i] = frozenset().union(*combined_row[i])
    return combined_row
