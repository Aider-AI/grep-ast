import re

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    long_description = re.sub(r"\n!\[.*\]\(.*\)", "", long_description)

setup(
    name="grep-ast",
    version="0.3.1",
    description="A tool to grep through the AST of a source file",
    url="https://github.com/paul-gauthier/grep-ast",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "grep-ast=grep_ast.main:main",
            "gast=grep_ast.main:main",
        ],
    },
)
