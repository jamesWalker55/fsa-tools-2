from obj.fsa import FSA
from obj.table import TransitionTable
from pathlib import Path

def process(graph: FSA, original_path: Path):
    output_path = original_path.with_name(f"{original_path.stem}_tran_table.md")
    table = transition_table(graph)
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(table.to_markdown())

def transition_table(graph: FSA):
    table = TransitionTable(sorted(graph.used_alphabet()))
    for tr in graph.transitions:
        table.add_transition(tr)
    table.freeze()
    return table
