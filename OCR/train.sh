#!/bin/bash

source settings.sh

#FIRST=1
#LAST=1

python getcodec.py

LINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
	I=$(printf '%04d\n' $i)
	MORELINES=($DATA/bin/$I/0001/*.png)
	LINES=("${LINES[@]}" "${MORELINES[@]}")
done
# ocropus-rtrain -load oldmodel -c $CODEC -o $NEW_MODEL $DATA/bin/1/0001/*.png
# ocropus-rtrain -d 1 -c $DATA/codec.txt -N $N -o mymodel $DATA/bin/1/0001/*.png
ocropus-rtrain -c $DATA/codecs/all.txt -N $NTRAIN -F $FTRAIN -o $DATA/models/model "${LINES[@]}"
