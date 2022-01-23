# FSA Tools 2

A set of tools for rendering, processing, solving finite state automata and pushdown automata.

## How to use

```bash
main.py INPUT_FILE
main.py examples/informal1.txt
```

This tool takes a single text file as input. The text file describes the FSA/PDA and lists actions to perform on the FSA/PDA. An input file looks like this:

```
# this is a comment

# state the input format with "format INPUT_FORMAT"
# we will use the "informal" format to describe our FSA

format informal

# state the actions to perform with "action ACTION1 ACTION2 ..."

# "render" - render the described fsa into an image
# "formalise" - describe the fsa using formal mathematical notation, saved to a file

action render formalise

# begin describing the fsa, we're using the "informal" format

start q1
end q3

q1 a q1
q1 b q1
q1 a q2
q2 a q2
q2 b q2
q2 b q3
q3 a q3
q3 b q3
```

After running the above file, it generates an image (`render`) and a new text file (`formalise`):

> ![](docs/test_render.gv.png)
> 
> ```
> format formal
> action render
> 
> {{a,b},{q1,q2,q3},{(q1,a,q1),(q1,a,q2),(q1,b,q1),(q2,a,q2),(q2,b,q2),(q2,b,q3),(q3,a,q3),(q3,b,q3)},q1,{q3}}
> ```
