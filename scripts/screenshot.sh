#!/bin/bash

# exit when any command fails
set -e

PAT=$1
SVG=assets/screenshot-$PAT.svg

CMD="grep-ast $PAT grep_ast/grep_ast.py"

echo > tmp.txt
echo "\$ $CMD" >> tmp.txt

$CMD --color >> tmp.txt

cat tmp.txt | ~/go/bin/ansisvg > $SVG

open $SVG
