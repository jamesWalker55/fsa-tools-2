from obj.fsa import FSA
from pathlib import Path


def process(graph: FSA, original_path: Path):
    unnamed_graph = unname(graph)
    output_path = original_path.with_stem(f"{original_path.stem}_unname")
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(unnamed_graph.to_informal())

def unname(graph: FSA) -> FSA:
    state_rename_map = {}
    state_num = 0
    for state in graph.states():
        if state == graph.start:
            state_rename_map[state] = f"q0"
        else:
            state_num = state_num + 1
            state_rename_map[state] = f"q{state_num}"
    print(state_rename_map)
    unnamed_graph = FSA()
    unnamed_graph.start = state_rename_map[graph.start]
    unnamed_graph.ends = set(map(lambda s: state_rename_map[s], graph.ends))
    for tr in graph.transitions:
        unnamed_graph.add_transition(
            state_rename_map[tr.start], tr.letter, state_rename_map[tr.end]
        )
    return unnamed_graph



