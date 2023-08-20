#!/usr/bin/env python

import argparse
import os
import re
import sys

from tree_sitter_languages import get_parser

from .dump import dump  # noqa: F401
from .parsers import PARSERS, filename_to_lang


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", nargs="?", help="the pattern to search for")
    parser.add_argument("filenames", nargs="*", help="the files to display", default=".")
    parser.add_argument("--encoding", default="utf8", help="file encoding")
    parser.add_argument("--languages", action="store_true", help="show supported languages")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions")
    parser.add_argument("--color", action="store_true", help="force color printing", default=None)
    parser.add_argument(
        "--no-color", action="store_false", help="disable color printing", dest="color"
    )
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("-n", "--line-number", action="store_true", help="display line numbers")
    args = parser.parse_args()

    # If stdout is not a terminal, set color to False
    if args.color is None:
        args.color = os.isatty(1)

    # If --languages is provided, print the parsers table and exit
    if args.languages:
        for ext, lang in sorted(PARSERS.items()):
            print(f"{ext}: {lang}")
        return
    elif not args.pattern:
        print("Please provide a pattern to search for")
        return 1

    # Replace the loop in the main function with a call to process_files
    process_files(args.filenames, args)


def process_files(filenames, args):
    for filename in filenames:
        if os.path.isdir(filename):
            # If filename is a directory, recursively process the files in it
            for root, dirs, files in os.walk(filename):
                process_files([os.path.join(root, file) for file in files], args)
            continue

        try:
            with open(filename, "r", encoding=args.encoding) as file:
                code = file.read()
        except UnicodeDecodeError:
            continue

        try:
            tc = TreeContext(
                filename, code, color=args.color, verbose=args.verbose, line_number=args.line_number
            )
        except ValueError:
            continue

        loi = tc.grep(args.pattern, args.ignore_case)
        if not loi:
            continue

        tc.add_lines_of_interest(loi)
        tc.add_context()

        print()
        if len(filenames) > 1:
            print(f"{filename}:")

        tc.display()

        print()


class TreeContext:
    def __init__(
        self,
        filename,
        code,
        color=False,
        verbose=False,
        line_number=False,
        parent_context=True,
        child_context=True,
    ):
        self.filename = filename
        self.color = color
        self.verbose = verbose
        self.line_number = line_number

        self.parent_context = parent_context
        self.child_context = child_context

        lang = filename_to_lang(filename)
        if not lang:
            raise ValueError(f"Unknown language for {filename}")

        # Get parser based on file extension
        parser = get_parser(lang)
        tree = parser.parse(bytes(code, "utf8"))

        self.lines = code.splitlines()
        self.num_lines = len(self.lines) + 1

        # color lines, with highlighted matches
        self.output_lines = dict()

        # Which scopes is each line part of?
        # A scope is the line number on which the scope started
        self.scopes = [set() for _ in range(self.num_lines)]

        # Which lines serve as a short "header" for the scope starting on that line
        self.header = [list() for _ in range(self.num_lines)]

        self.nodes = [list() for _ in range(self.num_lines)]

        root_node = tree.root_node
        self.walk_tree(root_node)

        if self.verbose:
            scope_width = max(len(str(set(self.scopes[i]))) for i in range(self.num_lines - 1))
        for i in range(self.num_lines):
            header = sorted(self.header[i])
            if self.verbose and i < self.num_lines - 1:
                scopes = str(sorted(set(self.scopes[i])))
                print(f"{scopes.ljust(scope_width)}", i, self.lines[i])

            if len(header) > 1:
                size, head_start, head_end = header[0]
                if size > 10:
                    head_end = head_start + 10
            else:
                head_start = i
                head_end = i + 1

            self.header[i] = head_start, head_end

        self.show_lines = set()
        self.lines_of_interest = set()

        return

    def grep(self, pat, ignore_case):
        found = set()
        for i, line in enumerate(self.lines):
            if re.search(pat, line, re.IGNORECASE if ignore_case else 0):
                if self.color:
                    highlighted_line = re.sub(
                        pat,
                        lambda match: f"\033[1;31m{match.group()}\033[0m",
                        line,
                        flags=re.IGNORECASE if ignore_case else 0,
                    )
                    self.output_lines[i] = highlighted_line
                found.add(i)
        return found

    def add_lines_of_interest(self, line_nums):
        self.lines_of_interest.update(line_nums)

    def add_context(self):
        if not self.lines_of_interest:
            return

        self.done_parent_scopes = set()

        self.show_lines = set(self.lines_of_interest)
        for line in list(self.show_lines):
            for new_line in [line - 1, line + 1]:
                if self.scopes[line].intersection(self.scopes[new_line]):
                    self.show_lines.add(new_line)

        # add the bottom line (plus parent context)
        bottom_line = self.num_lines - 2
        self.show_lines.add(bottom_line)
        self.add_parent_scopes(bottom_line)

        if self.parent_context:
            for i in set(self.lines_of_interest):
                self.add_parent_scopes(i)

        if self.child_context:
            for i in set(self.lines_of_interest):
                self.add_child_context(i)

        # add the top margin lines of the file
        margin = 3
        self.show_lines.update(range(margin))
        self.close_small_gaps()

    def add_child_context(self, i):
        if not self.nodes[i]:
            return

        last_line = self.get_last_line_of_scope(i)
        size = last_line - i
        if size < 5:
            self.show_lines.update(range(i, last_line + 1))
            return

        children = []
        for node in self.nodes[i]:
            children += self.find_all_children(node)

        children = sorted(
            children,
            key=lambda node: node.end_point[0] - node.start_point[0],
            reverse=True,
        )

        currently_showing = len(self.show_lines)
        max_to_show = 25
        min_to_show = 5
        percent_to_show = 0.10
        max_to_show = max(min(size * percent_to_show, max_to_show), min_to_show)

        for child in children:
            if len(self.show_lines) > currently_showing + max_to_show:
                break
            child_start_line = child.start_point[0]
            self.add_parent_scopes(child_start_line)

    def find_all_children(self, node):
        children = [node]
        for child in node.children:
            children += self.find_all_children(child)
        return children

    def get_last_line_of_scope(self, i):
        last_line = max(node.end_point[0] for node in self.nodes[i])
        return last_line

    def close_small_gaps(self):
        # a "closing" operation on the integers in set.
        # if i and i+2 are in there but i+1 is not, I want to add i+1
        # Create a new set for the "closed" lines
        closed_show = set(self.show_lines)
        sorted_show = sorted(self.show_lines)
        for i in range(len(sorted_show) - 1):
            if sorted_show[i + 1] - sorted_show[i] == 2:
                closed_show.add(sorted_show[i] + 1)

        # pick up adjacent blank lines
        for i, line in enumerate(self.lines):
            if i not in closed_show:
                continue
            if self.lines[i].strip() and i < self.num_lines - 2 and not self.lines[i + 1].strip():
                closed_show.add(i + 1)

        self.show_lines = closed_show

    def display(self):
        if not self.show_lines:
            return ""

        output = ""
        if self.color:
            # reset
            output += "\033[0m\n"

        dots = False
        for i, line in enumerate(self.lines):
            if i not in self.show_lines:
                if dots:
                    if self.line_number:
                        output += "...⋮...\n"
                    else:
                        output += "⋮...\n"
                    dots = False
                continue

            if i in self.lines_of_interest:
                spacer = "█"
                if self.color:
                    spacer = f"\033[31m{spacer}\033[0m"
            else:
                spacer = "│"

            line_output = f"{spacer}{self.output_lines.get(i, line)}"
            if self.line_number:
                line_output = f"{i+1:3}" + line_output
            output += line_output + "\n"

            dots = True

        return output

    def add_parent_scopes(self, i):
        if i in self.done_parent_scopes:
            return
        self.done_parent_scopes.add(i)

        for line_num in self.scopes[i]:
            head_start, head_end = self.header[line_num]
            self.show_lines.update(range(head_start, head_end))

            last_line = self.get_last_line_of_scope(line_num)
            self.add_parent_scopes(last_line)

    def walk_tree(self, node, depth=0):
        start = node.start_point
        end = node.end_point

        start_line = start[0]
        end_line = end[0]
        size = end_line - start_line

        self.nodes[start_line].append(node)

        # dump(start_line, end_line, node.text)
        if self.verbose and node.is_named:
            """
            for k in dir(node):
                print(k, getattr(node, k))
            """
            print(
                "   " * depth,
                node.type,
                f"{start_line}-{end_line}={size+1}",
                node.text.splitlines()[0],
                self.lines[start_line],
            )

        if size:
            self.header[start_line].append((size, start_line, end_line))

        for i in range(start_line, end_line + 1):
            self.scopes[i].add(start_line)

        for child in node.children:
            self.walk_tree(child, depth + 1)

        return start_line, end_line


if __name__ == "__main__":
    res = main()
    sys.exit(res)
