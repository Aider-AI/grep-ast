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
So it supports a lot of popular [code languages](https://github.com/paul-gauthier/grep-ast/blob/main/parsers.py).

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
 13│def main():
 14│    # Parse command line arguments
 15│    parser = argparse.ArgumentParser()
 16│    parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions")
 17│    parser.add_argument("--no-pretty", action="store_true", help="disable pretty printing")
 18<span style="color: #aa0000">█</span>    parser.add_argument("--<span style="font-weight: bold; color: #aa0000">encoding</span>", default="utf8", help="file <span style="font-weight: bold; color: #aa0000">encoding</span>")
 19│    parser.add_argument("--languages", action="store_true", help="print the parsers table")
...⋮...
 36│    for filename in args.filenames:
 37<span style="color: #aa0000">█</span>        with open(filename, "r", <span style="font-weight: bold; color: #aa0000">encoding</span>=args.<span style="font-weight: bold; color: #aa0000">encoding</span>) as file:
 38│            code = file.read()
 39│
 40│        tc = TreeContext(filename, code, pretty=not args.no_pretty, verbose=args.verbose)
 41│        loi = tc.grep(args.pat, args.ignore_case)
 42│        if not loi:
 43│            continue
 44│
...⋮...
 49│        if len(args.filenames) &gt; 1:
 50│            print(f"{filename}:")
 51│
...⋮...
284│if __name__ == "__main__":
285│    main()
```