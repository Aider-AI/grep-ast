# grep-ast

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

## Example


```
$ python3 ./grep_ast.py read grep_ast.py

  1 #!/usr/bin/env python
  2 
  3 import argparse
  4 import re
  5 import os
  6 
...░...
 10 def main():
 11     # Parse command line arguments
 12     parser = argparse.ArgumentParser()
...░...
 20     for filename in args.filenames:
 21         with open(filename, "r") as file:
 22█            code = file.read()
 23 
...░...
224 
225 
226 
227 if __name__ == "__main__":
228     main()
```