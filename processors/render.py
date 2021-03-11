from graphviz import Digraph
from obj.fsa import FSA, Transition
from pathlib import Path


def process(graph: FSA, original_path: Path, combined=False):
    output_path = original_path.with_name(f"{original_path.stem}_render.gv")
    render(graph, filename=str(output_path))


def process_combined(graph: FSA, original_path: Path):
    process(graph, original_path, combined=True)


def render(graph: FSA, combined: bool=False, filename: str="fsa.gv") -> None:
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
    iter_transitions = combine_transitions(graph.transitions) if combined else graph.transitions
    for transition in sorted(iter_transitions):
        dg.edge(transition.start, transition.end, label=transition.letter)

    # dg.view()
    # dg.save()
    dg.render()


def combine_transitions(transitions: set[Transition]):
    from collections import defaultdict

    def dict_to_transitions(pair, letters):
        start, end = pair
        return Transition(start, ", ".join(letters), end)

    pairs_to_letters = defaultdict(list)
    for transition in transitions:
        pair = (transition.start, transition.end)
        pairs_to_letters[pair].append(transition.letter)

    return (dict_to_transitions(k, v) for k, v in pairs_to_letters.items())