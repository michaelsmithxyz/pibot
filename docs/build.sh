#!/bin/bash

for f in $(ls src/)
do
    ext="${f##*.}"
    if [ "$ext" != "md" ]
    then
        continue
    fi
    echo "Building file" "src/$f"
    pandoc -f markdown -t html -o "tmpfile" "src/$f"
    cat src/template.head tmpfile src/template.tail > "$(basename -s .md $f).html"
    rm tmpfile
done
