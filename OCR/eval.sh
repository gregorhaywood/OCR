#!/bin/bash

source settings.sh

#FIRST=1
#LAST=6

GTLINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
    I=$(printf '%04d\n' $i)
    MORELINES=($DATA/bin/$I/0001/[0-9][0-9][0-9][0-9][0-9][0-9].gt.txt)
    GTLINES=("${GTLINES[@]}" "${MORELINES[@]}")
done

LINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
    I=$(printf '%04d\n' $i)
    MORELINES=($DATA/bin/$I/0001/[0-9][0-9][0-9][0-9][0-9][0-9].txt)
    LINES=("${LINES[@]}" "${MORELINES[@]}")
done

TOTALDIFF=0
for i in ${!GTLINES[@]}; do
	DIFF=$(lev.py "${GTLINES[i]}" "${LINES[i]}")
	TOTALDIFF=$(($TOTALDIFF+$DIFF))
done

TOTALSIZE=0
for i in ${!GTLINES[@]}; do
	FILESIZE=$(wc -c -m "${GTLINES[i]}" | awk '{print $1;}')
	TOTALSIZE=$(($TOTALSIZE+$FILESIZE-1))
done

# echo $((10000 * $TOTALDIFF / $TOTALSIZE))

ocropus-errs "${GTLINES[@]}"

# ocropus-econf -C2 "${GTLINES[@]}"

# ocropus-econf "${GTLINES[@]}"
