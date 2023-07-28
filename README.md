# Grep AST

Grep soure code files, and surround any lines that match with
useful context that shows how they fit into the code.
It's clear which loops, functions, methods, classes, etc
contain all the matching lines.
You see relevant code from every layer of the
abstract syntax tree above and below the matching lines.


## Usage

```bash
python grep_ast.py [pattern] [filenames] [-i]
```

- `pattern`: The pattern to search for.
- `filenames`: The files to search in.
- `-i, --ignore-case`: Ignore case distinctions.
- `--no-pretty`: Do not colorize matches.

