from graphviz import Digraph
from obj.fsa import FSA
from pathlib import Path


def process(graph: FSA, original_path: Path):
    output_path = original_path.with_name(f"{original_path.stem}_render.gv")
    render(graph, str(output_path))


def render(graph: FSA, combined=False, filename: str="fsa.gv") -> None:
    dg = Digraph('FSA', filename=filename, format="png")
    # settings
    dg.attr(rankdir='LR', dpi="150", ordering="out")
    dg.attr('node', shape='circle')
    # start arrow
    dg.node("_start_", label="", shape="point")
    dg.edge('_start_', graph.start)
    # set shape for end states
    for state in graph.ends:
        dg.node(state, shape='doublecircle')
    # create edges
    iter_transitions = graph.combined_transitions() if combined else graph.transitions
    for transition in sorted(iter_transitions):
        dg.edge(transition.start, transition.end, label=transition.letter)

    dg.view()
