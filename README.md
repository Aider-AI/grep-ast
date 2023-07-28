# Grep AST

This repository contains a Python script for searching patterns in files using Abstract Syntax Trees (AST).

## Usage

```bash
python grep_ast.py [pattern] [filenames] [-i]
```

### Arguments

- `pattern`: The pattern to search for.
- `filenames`: The files to search in.
- `-i, --ignore-case`: Ignore case distinctions.

## Dependencies

This script uses the following Python libraries:

- argparse
- re
- os
- tree_sitter_languages
- dump

## License

This project is licensed under the MIT License.
