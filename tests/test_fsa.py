import pytest
import obj.fsa


def easy_graph(start: str, ends: set[str], transitions: set[str]) -> obj.fsa.FSA:
    graph = obj.fsa.FSA()
    for tr in transitions:
        graph.add_transition(*tr.split())
    graph.ends = ends
    graph.start = start
    return graph


@pytest.fixture
def graph_a() -> obj.fsa.FSA:
    # Non-deterministic
    start = "q0"
    ends = {"q3"}
    transitions = {
        "q0 0 q1",
        "q0 0 q3",
        "q0 1 q3",
        "q1 1 q2",
        "q1 1 q3",
        "q2 0 q3",
        "q3 0 q3",
    }
    return easy_graph(start, ends, transitions)


@pytest.fixture
def graph_b() -> obj.fsa.FSA:
    # Non-deterministic
    start = "q0"
    ends = {"q5"}
    transitions = {
        "q0 a q1",
        "q0 a q2",
        "q1 b q3",
        "q2 b q4",
        "q3 c q5",
        "q4 d q5",
    }
    return easy_graph(start, ends, transitions)


@pytest.fixture
def graph_c() -> obj.fsa.FSA:
    # Deterministic
    start = "q0"
    ends = {"q0", "q1", "q2"}
    transitions = {
        "q0 a q0",
        "q0 b q1",
        "q0 c q2",
        "q1 b q1",
        "q1 c q2",
        "q2 c q2",
    }
    return easy_graph(start, ends, transitions)


def test_fsa_states(graph_a: obj.fsa.FSA, graph_b: obj.fsa.FSA, graph_c: obj.fsa.FSA):
    assert graph_a.states() == {"q0", "q1", "q2", "q3"}
    assert graph_b.states() == {"q0", "q1", "q2", "q3", "q4", "q5"}
    assert graph_c.states() == {"q0", "q1", "q2"}


# def test_fsa_deterministic(graph_a: obj.fsa.FSA, graph_b: obj.fsa.FSA, graph_c: obj.fsa.FSA):
#     assert graph_a.is_deterministic() == False
#     assert graph_b.is_deterministic() == False
#     assert graph_c.is_deterministic() == True


# def test_fsa_alphabet(graph_a: obj.fsa.FSA, graph_b: obj.fsa.FSA, graph_c: obj.fsa.FSA):
#     assert graph_a.alphabet == set("0 1".split())
#     assert graph_b.alphabet == set("a b c d".split())
#     assert graph_c.alphabet == set("a b c".split())
