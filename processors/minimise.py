from collections import defaultdict
from obj.table import MinimiseTable
from obj.fsa import FSA, Transition
from pathlib import Path
from pprint import pprint


def process(graph: FSA, original_path: Path):
    if not is_deterministic(graph):
        raise Exception("Graph is not deterministic! Aborting...")
    min_table = minimise_table(graph)
    min_dfa = minimum_dfa(graph, min_table)
    output_path = original_path.with_stem(f"{original_path.stem}_min")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(min_dfa.to_informal())


def is_deterministic(graph: FSA):
    letter_map = defaultdict(set)
    for tr in graph.transitions:
        if tr.letter in letter_map[tr.start]:
            return False
        letter_map[tr.start].add(tr.letter)
    return True


def minimise_table(graph: FSA):
    table = MinimiseTable(graph)
    used_alphabet = graph.used_alphabet()

    def one_final_state(s1, s2):
        print(f"({s1}, {s2}): One of them is an accepting state")
        return (s1 in graph.ends) ^ (s2 in graph.ends)

    def apply_transition(state, letter):
        possible_routes = [
            tr for tr in graph.transitions if tr.start == state and tr.letter == letter
        ]
        # graph is deterministic (we verified already), so there must be 0-1 routes
        if len(possible_routes) == 0:
            return None
        return possible_routes[0].end

    def attempt_mark_pair(s1, s2):
        """test a pair of states, and mark it if it can be marked

        return True/False indicating whether any marking was done"""
        # input already marked
        if table[s1, s2]:
            return False
        # input not marked
        for letter in used_alphabet:
            f1 = apply_transition(s1, letter)
            f2 = apply_transition(s2, letter)
            try:
                if f1 == None and f2 == None:
                    # skip if BOTH states don't accept letter
                    continue
                # table[f1, f2] :
                #   state is marked / True
                # (None in (f1, f2)) :
                #   one state accepts letter, other state doesn't accept letter
                if (None in (f1, f2)) or table[f1, f2]:
                    if table[f1, f2]:
                        print(
                            f"({s1}, {s2}): They transition to a marked cell ({f1}, {f2}) with letter {letter}"
                        )
                    elif f1 == None:
                        print(
                            f"({s1}, {s2}): State {s2} can transition with letter {letter} while {s1} cannot"
                        )
                    else:
                        print(
                            f"({s1}, {s2}): State {s1} can transition with letter {letter} while {s2} cannot"
                        )
                    table[s1, s2] = True
                    return True
            except MinimiseTable.InvalidPosition:
                pass
        return False

    for s1, s2 in table.generator():
        if one_final_state(s1, s2):
            table[s1, s2] = True
    print("After marking cells with exactly 1 final state:")
    print(table)
    print("Start looping:")
    while True:
        marked_something = False
        for s1, s2 in table.generator():
            marked_something = attempt_mark_pair(s1, s2) or marked_something
        if not marked_something:
            break
        print(table)
    print("After looping and marking all valid cells:")
    print(table)
    return table


def minimum_dfa(old_graph: FSA, min_table: MinimiseTable):
    graph = old_graph.clone()
    for s1, s2 in min_table.generator():
        marked = min_table[s1, s2]
        if marked:
            continue
        new_state = s1 + "/" + s2
        if graph.start in (s1, s2):
            graph.start = new_state
        if s1 in graph.ends:
            graph.ends.remove(s1)
            graph.ends.add(new_state)
        if s2 in graph.ends:
            graph.ends.remove(s2)
            graph.ends.add(new_state)
        transitions_copy = graph.transitions.copy()
        for tr in transitions_copy:
            start, letter, end = tr.start, tr.letter, tr.end
            if start in (s1, s2):
                start = new_state
            if end in (s1, s2):
                end = new_state
            graph.remove_transition(tr)
            graph.add_transition(start, letter, end)
    return graph
