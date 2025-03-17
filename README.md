# grep-ast

Grep source code files and see matching lines with
useful context that show how they fit into the code.
See the loops, functions, methods, classes, etc
that contain all the matching lines.
Get a sense of what's inside a matched class or function definition.
You see relevant code from every layer of the
abstract syntax tree, above and below the matches.

By default, grep-AST recurses the current directory to search all source code files.
It respects `.gitignore`, so it will usually "do the right thing" in most repos
if you just do `grep-ast <regex>` without specifying any filenames.

You can also invoke `grep-ast` as `gast` for convenience.

Grep-AST is built with [tree-sitter](https://tree-sitter.github.io/tree-sitter/) and
[tree-sitter-languages](https://github.com/grantjenks/py-tree-sitter-languages).
So it supports a lot of popular [code languages](https://github.com/paul-gauthier/grep-ast/blob/main/grep_ast/parsers.py).

## Install

```bash
python -m pip install git+https://github.com/paul-gauthier/grep-ast.git
```

## Adding Support for New Languages

To add support for a new language, you need to update the `PARSERS` dictionary in `grep_ast/parsers.py` with the appropriate file extensions and language name as recognized by `tree-sitter`. For example, to add support for Clojure, you would add:

```python
".clj": "clojure",
".cljs": "clojure",
".cljc": "clojure",
```

Ensure that the language is supported by `tree-sitter` and `py-tree-sitter-languages`. You may need to install additional language parsers if they are not included by default.

Basic usage:

```bash
grep-ast [pattern] [filenames...]
```

Full options list:

```
usage: grep_ast.py [-h] [-i] [--color] [--no-color] [--encoding ENCODING] [--languages] [--verbose]
                   [pat] [filenames ...]

positional arguments:
  pat                  the pattern to search for
  filenames            the files to display

options:
  -h, --help           show this help message and exit
  -i, --ignore-case    ignore case distinctions
  --color              force color printing
  --no-color           disable color printing
  --encoding ENCODING  file encoding
  --languages          print the parsers table
  --verbose            enable verbose output
```

## Examples

Here we search for **"encoding"** in the source to this tool.
These results mainly highlight how `grep-ast`
shows you how the matches fit into the code base.

<img src="assets/screenshot-encoding.svg" alt="aider screencast">

Here we search for **"TreeContext"** in the source to this tool.
These results mainly highlight how `grep-ast`
helps you understand the *contents* of a matching
named code block (class, function, method, etc).

<img src="assets/screenshot-TreeContext.svg" alt="aider screencast">
