import pytest
from grep_ast.parsers import PARSERS, get_parser

def test_get_parser_for_all_parsers():
    for lang in PARSERS.values():
        assert get_parser(lang) is not None
