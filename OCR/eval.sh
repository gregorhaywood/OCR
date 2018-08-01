#!/usr/bin/env bash

source settings.sh


GTLINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
    I=$(printf '%04d\n' $i)
    MORELINES=($DATA/bin/$I/0001/[0-9][0-9][0-9][0-9][0-9][0-9].gt.txt)
    GTLINES=("${GTLINES[@]}" "${MORELINES[@]}")
done

# python 2 mode
source ./ocropy/ocropus_venv/bin/activate
ocropus-errs "${GTLINES[@]}"
# ocropus-econf -C2 "${GTLINES[@]}"
# ocropus-econf "${GTLINES[@]}"
deactivate
