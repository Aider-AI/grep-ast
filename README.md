# grep-ast

Grep soure code files and see matching lines with
useful context that show how they fit into the code.
See which loops, functions, methods, classes, etc
contain all the matching lines.
Get a sense of what's inside a matched class.
You see relevant code from every layer of the
abstract syntax tree, above and below the matches.


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
$ python3 ./grep_ast.py enoding grep_ast.py

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
 15█    parser.add_argument("--encoding", default="utf8", help="file encoding")
...░...
 21     for filename in args.filenames:
 22█        with open(filename, "r", encoding=args.encoding) as file:
 23             code = file.read()
 24 
...░...
 30         tg.add_lines_of_interest(loi)
...░...
 37         tg.display()
 38 
...░...
237 
238 
239 
240 if __name__ == "__main__":
241     main()
```