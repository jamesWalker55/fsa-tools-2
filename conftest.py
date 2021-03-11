import obj.fsa
import tools.fromtext
import tools.render

path = "graph.txt"

with open(path, "r") as f:
    text = f.read()

# g = tools.fromtext.lines_to_fsa(text.split("\n"))
g = tools.fromtext.from_file(path)

# tools.render.render(g)