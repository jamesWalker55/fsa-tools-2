import tools.fromtext
import processors.render
import processors.clone
import processors.deterministic

import argparse
from pathlib import Path
from typing import Union

parser = argparse.ArgumentParser(description="Processes a *.txt file containing graph information.")
parser.add_argument("path", metavar="txt_path", type=str, help="Path to the *.txt file to process")
cmd_args = parser.parse_args()
print()


# =========================parse text to graph=========================
def _error(msg: str, line=None):
    if line:
        msg += f'\nError at: "{line}"'
    raise Exception(msg)


def _find_lines_args(lines: list[str]):
    args: dict[str, Union[list[str], str]]
    args = {}
    for line in lines:
        if line.strip().startswith("format "):
            words = line.split()
            if len(words) != 2:
                _error("Expected exactly 1 word representing parser!", line=line)
            args["format"] = words[1]
        elif line.strip().startswith("action "):
            words = line.split()
            if len(words) < 2:
                _error("Expected at least 1 word representing actions to perform!", line=line)
            args["action"] = words[1:]

    if len(args.keys()) != 2:
        _error("Format/Action line is missing!")

    return args


path = Path(cmd_args.path)

with open(path, "r") as f:
    lines = f.readlines()

args = _find_lines_args(lines)

if args["format"].lower() == "informal":
    graph = tools.fromtext._informal_to_fsa(lines)
else:
    _error(f"Unknown text format '{args['format']}'!")


# =========================process graph=========================
actions: list[str]
actions = args["action"]

import tools.common as com

proc_funcs = {
    "render": processors.render.process,
    "render_combined": processors.render.process_combined,
    "clone": processors.clone.process,
    "deterministic": processors.deterministic.process,
    "transition_table": lambda graph, path: print(com.transition_table(graph))
}


for action in actions:
    func = proc_funcs.get(action.lower())
    if func:
        print(f"{action.capitalize()}: Starting...")
        func(graph, path)
        print(f"{action.capitalize()}: Success!")
        print()
    else:
        print(f"Unknown action '{action}'!")
