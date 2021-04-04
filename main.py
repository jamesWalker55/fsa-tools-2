import tools.fromtext
import processors.render
import processors.clone
import processors.deterministic
import processors.transitiontable
import processors.formalise
import processors.unname

import argparse
from pathlib import Path
from typing import Union

parser = argparse.ArgumentParser(description="Processes a *.txt file containing graph information.")
parser.add_argument("path", metavar="txt_path", type=str, help="Path to the *.txt file to process")
parser.add_argument("skip", metavar="skip_processing", type=int, help="Whether to enable debug mode or not")
cmd_args = parser.parse_args()
print()

# =========================define fuctions=========================

proc_funcs = {
    "render": processors.render.process,
    "render_combined": processors.render.process_combined,
    "render_in": processors.render.process_in,
    "render_in_combined": processors.render.process_in_combined,
    "clone": processors.clone.process,
    "deterministic": processors.deterministic.process,
    "transition_table": processors.transitiontable.process,
    "formalise": processors.formalise.process,
    "unname": processors.unname.process,
}


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

with open(path, "r", encoding='utf-8') as f:
    lines = f.read().splitlines()

args = _find_lines_args(lines)

print(f"Parsing with format as '{args['format']}'")

if args["format"].lower() == "informal":
    graph = tools.fromtext.informal_to_fsa(lines)
elif args["format"].lower() == "formal":
    graph = tools.fromtext.formal_to_fsa(lines)
else:
    _error(f"Unknown text format '{args['format']}'!")

print("Parsing success!")

# =========================process graph=========================
actions: list[str]
actions = args["action"]

if cmd_args.skip == 1:
    print("skip is intended for use with python interactive mode")
    print("Skipping all processing")
    print(f"    `graph`: {graph}")
    print(f"    `path`: {path}")
    from obj.fsa import FSA
else:
    for action in actions:
        func = proc_funcs.get(action.lower())
        if func:
            print(f"{action.capitalize()}: Starting...")
            func(graph, path)
            print(f"{action.capitalize()}: Success!")
            print()
        else:
            print(f"Unknown action '{action}'")
