from obj.fsa import FSA
from pathlib import Path
from obj.table import EpsilonTable, TransitionTable
from processors.transitiontable import transition_table


def process(graph: FSA, original_path: Path):
    output_table1 = original_path.with_stem(f"{original_path.stem}_epsilon_table1")
    output_table1 = output_table1.with_suffix(".md")
    output_table2 = original_path.with_stem(f"{original_path.stem}_epsilon_table2")
    output_table2 = output_table2.with_suffix(".md")
    output_graph = original_path.with_stem(f"{original_path.stem}_epsilon")
    etable, end_states = epsilon_table(graph)
    new_ttable = no_epsilon_transition_table(graph, etable)
    # new_ttable.labels[0] = "d'"
    final_graph = transition_table_to_graph(new_ttable, graph, end_states)
    with open(output_table1, "w", encoding="utf-8") as f:
        f.write(etable.to_markdown())
    with open(output_table2, "w", encoding="utf-8") as f:
        f.write(new_ttable.to_markdown())
    with open(output_graph, "w", encoding="utf-8") as f:
        f.write(final_graph.to_informal())


def epsilon_table(graph: FSA):
    ttable = transition_table(graph)
    etable = EpsilonTable(ttable)
    index_d = etable.index_of("d")
    index_e = etable.index_of("e")
    index_es = etable.index_of("e*")

    end_states = set(graph.ends)
    print(etable)

    for row in etable.rows:
        print(f"For row: {row}")
        reachable_states = set(row[index_d] | row[index_e])
        to_check = list(row[index_e])
        for dest in to_check:
            dest_row = etable["d", frozenset({dest})]
            new_dests = [x for x in dest_row[index_e] if x not in reachable_states]
            to_check += new_dests
            reachable_states |= set(new_dests)
        row[index_es] = frozenset(reachable_states)
        if len(end_states & row[index_es]) != 0:
            end_states |= row[index_d]
        print(f"    Reachable states: {reachable_states}")
        print(f"    To check: {to_check}")
        print(f"    Final row: {row}")
    print(etable)
    print(f"{end_states=}")
    return etable, end_states


def no_epsilon_transition_table(graph: FSA, etable: EpsilonTable):
    alphabet = graph.used_alphabet()
    alphabet.discard("e")
    alphabet.discard("ε")

    index_d = etable.index_of("d")
    index_es = etable.index_of("e*")

    new_ttable = TransitionTable(alphabet)
    for row in etable.rows:
        from_state = row[index_d]
        new_ttable.add_row([from_state] + [frozenset()] * len(alphabet))
        to_combine = [frozenset({x}) for x in row[index_es]]
        combined_row = etable.combined_state_rows(*to_combine)
        print(combined_row)
        for letter in alphabet:
            eindex = etable.index_of(letter)
            tindex = new_ttable.index_of(letter)
            new_ttable[from_state][tindex] = combined_row[eindex]

    return new_ttable


def transition_table_to_graph(
    ttable: TransitionTable, original_graph: FSA, end_states: set[str]
):
    new_graph = FSA()
    new_graph.start = original_graph.start
    new_graph.ends = end_states.copy()
    for row in ttable.rows:
        start_state = list(row[0])[0]  # get string from set
        label_and_value = zip(ttable.labels, row)
        for letter, states in label_and_value:
            if letter == "state":
                continue
            if len(states) == 0:
                continue
            for state in states:
                new_graph.add_transition(start_state, letter, state)

    return new_graph
