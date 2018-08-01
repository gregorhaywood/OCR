#!/usr/bin/env bash

source settings.sh

# select lines to transcribe
LINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
    I=$(printf '%04d\n' $i)
    MORELINES=($DATA/bin/$I/0001/*.png)
    LINES=("${LINES[@]}" "${MORELINES[@]}")
done

# transcribe lines
# python 2 mode
source ./ocropy/ocropus_venv/bin/activate
ocropus-rpred -m $DATA/models/$MODEL "${LINES[@]}"
deactivate