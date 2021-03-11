import tools.fromtext
import tools.render

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Processes a *.txt file containing graph information.")
parser.add_argument("path", metavar="txt_path", type=str, help="Path to the *.txt file to process")
cmd_args = parser.parse_args()
print()

path = Path(cmd_args.path)

# =========================parse text to graph=========================
def _error(msg: str, line=None):
    if line:
        msg += f'\nError at: "{line}"'
    raise Exception(msg)


def _find_text_args(lines: list[str]):
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


with open(path, "r") as f:
    lines = f.readlines()

args = _find_text_args(lines)
text_format = args["format"]

if text_format.lower() == "informal":
    g = tools.fromtext._informal_to_fsa(lines)
else:
    _error(f"Unknown text format '{text_format}'!")


# =========================process graph=========================
actions: list[str]
actions = args["action"]

if "render" in actions:
    actions.remove("render")
    output_path = path.with_name(f"{path.stem}_render.gv")
    tools.render.render(g, filename=str(output_path))

if len(actions) != 0:
    print(f"Skipping unrecognised actions: {', '.join(actions)}")

