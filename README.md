# grep-ast

Grep soure code files and see matching lines with
useful context that show how they fit into the code.
See the loops, functions, methods, classes, etc
that contain all the matching lines.
Get a sense of what's inside a matched class.
You see relevant code from every layer of the
abstract syntax tree, above and below the matches.


## Usage

```bash
python grep_ast.py [pattern] [filenames...]
```

- `pattern`: The pattern to search for.
- `filenames`: The files to search in.
- `-i, --ignore-case`: Ignore case distinctions.
- `--no-pretty`: Do not colorize matches.
- `--languages`: Print out the supported file types.

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
 13     parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions")
 14     parser.add_argument("--no-pretty", action="store_true", help="disable pretty printing")
 15█    parser.add_argument("--encoding", default="utf8", help="file encoding")
 16     parser.add_argument("--languages", action="store_true", help="print the parsers table")
...░...
 28     for filename in args.filenames:
 29█        with open(filename, "r", encoding=args.encoding) as file:
 30             code = file.read()
 31 
...░...
 34         if not loi:
 35             continue
 36 
 37         tg.add_lines_of_interest(loi)
...░...
 44         tg.display()
 45 
...░...
298 
299 
300 
301 if __name__ == "__main__":
302     main()
```