from obj.fsa import FSA
from pathlib import Path


def process(graph: FSA, original_path: Path):
    output_path = original_path.with_stem(f"{original_path.stem}_clone")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(graph.to_informal())
