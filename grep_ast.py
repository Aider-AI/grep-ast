#!/usr/bin/env python

import argparse
import re
import os

from tree_sitter_languages import get_parser
from dump import dump

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions")
    parser.add_argument("--no-pretty", action="store_true", help="disable pretty printing")
    parser.add_argument("--encoding", default="utf8", help="file encoding")
    parser.add_argument("pat", help="the pattern to search for")
    parser.add_argument("filenames", nargs='+', help="the files to display")
    args = parser.parse_args()

    # Build the AST
    for filename in args.filenames:
        with open(filename, "r", encoding=args.encoding) as file:
            code = file.read()

        tg = TreeContext(filename, code, pretty=not args.no_pretty)
        loi = tg.grep(args.pat, args.ignore_case)
        if not loi:
            continue

        tg.add_lines_of_interest(loi)
        tg.add_context()

        print()
        if len(args.filenames) > 1:
            print(f"{filename}:")

        tg.display()


class TreeContext:
    def __init__(
            self,
            filename,
            code,
            pretty=False,
    ):
        self.filename = filename
        self.pretty = pretty

        # Mapping of file extensions to parsers
        parsers = {
            ".py": "python",
            ".js": "javascript",
            ".go": "go",
            ".md": "markdown",
            ".erl": "erlang",
            ".lua": "lua",
            ".el": "elisp",
            ".mk": "make",
            ".make": "make",
            ".dockerfile": "dockerfile",
            ".mod": "go-mod",
            ".ex": "elixir",
            ".exs": "elixir",
            ".elm": "elm",
            ".kt": "kotlin",
            ".pl": "perl",
            ".pm": "perl",
            ".m": "objc",
            ".h": "objc",
            ".sql": "sql",
            ".r": "r",
            ".dot": "dot",
            ".hh": "hack",
            ".hck": "hack",
            ".lisp": "commonlisp",
            ".cl": "commonlisp",
            ".sh": "bash",
            ".bash": "bash",
            ".c": "c",
            ".cs": "c-sharp",
            ".cpp": "cpp",
            ".css": "css",
            ".hs": "haskell",
            ".html": "html",
            ".htm": "html",
            ".java": "java",
            ".jsdoc": "jsdoc",
            ".json": "json",
            ".jl": "julia",
            ".ml": "ocaml",
            ".mli": "ocaml",
            ".php": "php",
            ".ql": "ql",
            ".regex": "regex",
            ".rb": "ruby",
            ".rs": "rust",
            ".scala": "scala",
            ".sqlite": "sqlite",
            ".db": "sqlite",
            ".toml": "toml",
            ".tsq": "tsq",
            ".ts": "typescript",
            ".rst": "rst",
            ".hcl": "hcl",
        }

        # Extract file extension
        file_extension = os.path.splitext(self.filename)[1]

        # Get parser based on file extension
        parser = get_parser(parsers.get(file_extension, "python"))
        tree = parser.parse(bytes(code, "utf8"))

        self.lines = code.splitlines()
        self.num_lines = len(self.lines) + 1

        # pretty lines, with highlighted matches
        self.output_lines = dict()

        # Which scopes is each line part of?
        # A scope is the line number on which the scope started
        self.scopes = [set() for _ in range(self.num_lines)]

        # Which lines serve as a short "header" for the scope starting on that line
        self.header = [list() for _ in range(self.num_lines)]

        self.nodes = [list() for _ in range(self.num_lines)]

        root_node = tree.root_node
        self.walk_tree(root_node)

        for i in range(self.num_lines):
            header = sorted(self.header[i])
            if False and i < self.num_lines-1:
                print(header, sorted(set(self.scopes[i])))
                print(i, self.lines[i])

            if len(header) > 1:
                size, head_start, head_end = header[0]
                if size>10:
                    head_end = head_start + 10
            else:
                head_start = i
                head_end = i

            self.header[i] = head_start, head_end

        self.show_lines = set()
        self.lines_of_interest = set()

        return

    def grep(self, pat, ignore_case):

        found = set()
        for i, line in enumerate(self.lines):
            if re.search(pat, line, re.IGNORECASE if ignore_case else 0):
                if self.pretty:
                    highlighted_line = re.sub(pat, lambda match: f'\033[1;31m{match.group()}\033[0m', line, flags=re.IGNORECASE if ignore_case else 0)
                    self.output_lines[i] = highlighted_line
                found.add(i)
        return found

    def add_lines_of_interest(self, line_nums):
        self.lines_of_interest.update(line_nums)

    def add_context(self):
        if not self.lines_of_interest:
            return

        margin=5

        self.show_lines = set(self.lines_of_interest)
        self.show_lines.update(range(self.num_lines - margin - 1, self.num_lines))

        for i in set(self.show_lines):
            self.add_parent_scopes(i)

            if self.nodes[i]:
                last_line = self.get_last_line_of_scope(i)
                size = last_line - i
                if size < 5:
                    self.show_lines.update(range(i, last_line+1))
                else:
                    add = self.sample_lines(i, last_line)
                    for new_line in add:
                        self.show_lines.add(new_line)
                        self.add_parent_scopes(new_line)

        # add the top margin lines of the file
        self.show_lines.update(range(margin))
        self.close_small_gaps()

    def sample_lines(self, i, last_line):
        filled_lines = sorted(i for i in range(i, last_line+1) if self.lines[i].strip())
        size = len(filled_lines)
        if size < 30:
            middle_line = filled_lines[size // 2]
            add = [middle_line]
        else:
            step = size // 30
            add = [filled_lines[i] for i in range(0, size, step)]

        add.append(filled_lines[0])
        add.append(filled_lines[-1])  # Ensure the last line is always included

        return set(add)

    def close_small_gaps(self):
        # a "closing" operation on the integers in set. if i and i+2 are in there but i+1 is not, I want to add i+1
        # Create a new set for the "closed" lines
        closed_show = set(self.show_lines)
        sorted_show = sorted(self.show_lines)
        for i in range(len(sorted_show) - 1):
            if sorted_show[i+1] - sorted_show[i] == 2:
                closed_show.add(sorted_show[i] + 1)

        # pick up adjacent blank lines
        for i, line in enumerate(self.lines):
            if i not in closed_show:
                continue
            if self.lines[i].strip() and i < self.num_lines-2 and not self.lines[i+1].strip():
                closed_show.add(i+1)

        self.show_lines = closed_show


    def display(self):
        if not self.show_lines:
            return

        dots = False
        for i, line in enumerate(self.lines):
            if i not in self.show_lines:
                if dots:
                    print('...░...')
                    dots = False
                continue

            if i in self.lines_of_interest:
                spacer = '█'
                if self.pretty:
                    spacer = f'\033[31m{spacer}\033[0m'
            else:
                spacer = ' '

            print(f"{i+1:3}{spacer}{self.output_lines.get(i, line)}")
            dots = True

    def get_last_line_of_scope(self, i):
        last_line = max(
            node.end_point[0]
            for node in self.nodes[i]
        )
        return last_line

    def add_parent_scopes(self, i):
        for line_num in self.scopes[i]:
            head_start, head_end = self.header[line_num]
            self.show_lines.update(range(head_start, head_end+1))

    def walk_tree(self, node):
        start = node.start_point
        end = node.end_point

        start_line = start[0]
        end_line = end[0]
        size = end_line - start_line

        self.nodes[start_line].append(node)

        #dump(start_line, end_line, node.text)

        if size:
            self.header[start_line].append((size, start_line, end_line))

        for i in range(start_line, end_line+1):
            self.scopes[i].add(start_line)

        for child in node.children:
            self.walk_tree(child)

        return start_line, end_line




if __name__ == "__main__":
    main()
