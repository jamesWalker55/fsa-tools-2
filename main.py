import tools.fromtext
import processors.render
import processors.clone
import processors.deterministic
import processors.transitiontable
import processors.formalise
import processors.unname
import processors.minimise
import processors.epsilon

import argparse
from pathlib import Path
from typing import Union

parser = argparse.ArgumentParser(
    description="Processes a *.txt file containing graph information."
)
parser.add_argument(
    "path", metavar="txt_path", type=Path, help="Path to the *.txt file to process"
)
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
    "minimise": processors.minimise.process,
    "epsilon": processors.epsilon.process,
}


# =========================parse text to graph=========================
def _find_lines_args(lines: list[str]):
    args: dict[str, Union[list[str], str]]
    args = {}
    for line in lines:
        if line.strip().startswith("format "):
            words = line.split()
            if len(words) != 2:
                raise Exception(
                    f"Expected exactly 1 word representing parser!\nError at: {line}"
                )
            args["format"] = words[1]
        elif line.strip().startswith("action "):
            words = line.split()
            if len(words) < 2:
                raise Exception(
                    f"Expected at least 1 word representing actions to perform!\nError at: {line}"
                )
            args["action"] = words[1:]

    if len(args.keys()) != 2:
        raise Exception("Format/Action line is missing!")

    return args


def main():
    cmd_args = parser.parse_args()

    with open(cmd_args.path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    args = _find_lines_args(lines)

    print(f"Parsing with format as '{args['format']}'")
    if args["format"].lower() == "informal":
        graph = tools.fromtext.informal_to_fsa(lines)
    elif args["format"].lower() == "formal":
        graph = tools.fromtext.formal_to_fsa(lines)
    else:
        raise Exception(f"Unknown text format '{args['format']}'!")
    print("Parsing success!")

    actions: list[str]
    actions = args["action"]
    for action in actions:
        func = proc_funcs.get(action.lower())
        if func:
            print(f"{action.capitalize()}: Starting...")
            func(graph, cmd_args.path)
            print(f"{action.capitalize()}: Success!")
            print()
        else:
            print(f"Unknown action '{action}'")


main()
