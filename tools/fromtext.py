from obj.fsa import FSA, EPSILON

META_KEYWORDS = ("format", "action", "#")


def _error(line, msg: str):
    if line:
        msg += f'\nError at: "{line}"'
    raise Exception(msg)


# ========================parse with informal========================
def informal_to_fsa(lines: list[str]) -> FSA:
    graph = FSA()
    has_start = False
    has_end = False
    for line in lines:
        line = line.strip()
        if line == "":
            continue

        words = line.split()
        if words[0] in META_KEYWORDS:
            continue

        if words[0] == "start":
            if len(words) != 2:
                _error(line, "Expected exactly 1 word representing start state!")
            graph.start = words[1]
            has_start = True
        elif words[0] == "end":
            if len(words) < 2:
                _error(line, "Expected >= 1 words representing end states!")
            graph.ends = set(words[1:])
            has_end = True
        else:
            if len(words) < 3:
                _error(line, "Expected >= 3 words representing start, *letter, end!")
            start = words[0]
            letters = words[1:-1]
            end = words[-1]
            for letter in letters:
                letter = EPSILON if letter == "e" else letter
                graph.add_transition(start, letter, end)
    if not (has_start or has_end):
        raise Exception("No start/end state in input text!")
    return graph


# ========================parse with formal========================
def formal_to_fsa(lines: list[str]) -> FSA:
    import re
    from pprint import pprint

    lines = " ".join(lines)
    match = re.search(r"{(.+?)}.*?{(.+?)}.*?{(.+?)},(.+?),.*{(.+?)}", lines)
    # parsing text
    # alphabet = list(x.strip() for x in match.group(1).split(","))
    # all_states = list(x.strip() for x in match.group(2).split(","))
    transitions = re.findall(r"\((.+?)\)", match.group(3))
    transitions = [[t.strip() for t in tran.split(",")] for tran in transitions]
    initial_state = match.group(4).strip()
    final_states = list(x.strip() for x in match.group(5).split(","))
    graph = FSA()
    graph.start = initial_state
    graph.ends = final_states
    for tran in transitions:
        graph.add_transition(*tran)
    return graph
