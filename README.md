# grep-ast

Grep soure code files and see matching lines with
useful context that show how they fit into the code.
See the loops, functions, methods, classes, etc
that contain all the matching lines.
Get a sense of what's inside a matched class.
You see relevant code from every layer of the
abstract syntax tree, above and below the matches.

Grep-AST is built with [tree-sitter](https://tree-sitter.github.io/tree-sitter/) and
[tree-sitter-languages](https://github.com/grantjenks/py-tree-sitter-languages).
So it supports a lot of popular [code languages](https://github.com/grantjenks/py-tree-sitter-languages#license).

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

Here we search for **"encoding"** in the source to this tool:

```
$ python3 grep_ast.py encoding grep_ast.py

  1│#!/usr/bin/env python
  2│
  3│import argparse
...⋮...
 10│def main():
 11│    # Parse command line arguments
 12│    parser = argparse.ArgumentParser()
 13│    parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions")
 14│    parser.add_argument("--no-pretty", action="store_true", help="disable pretty printing")
 15█    parser.add_argument("--encoding", default="utf8", help="file encoding")
 16│    parser.add_argument("--languages", action="store_true", help="print the parsers table")
...⋮...
 33│    for filename in args.filenames:
 34█        with open(filename, "r", encoding=args.encoding) as file:
 35│            code = file.read()
 36│
 37│        tc = TreeContext(filename, code, pretty=not args.no_pretty, verbose=args.verbose)
 38│        loi = tc.grep(args.pat, args.ignore_case)
 39│        if not loi:
 40│            continue
 41│
 42│        tc.add_lines_of_interest(loi)
...⋮...
 46│        if len(args.filenames) > 1:
...⋮...
339│if __name__ == "__main__":
340│    main()
```