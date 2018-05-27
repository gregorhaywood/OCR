#!/bin/bash

source settings.sh

FIRST=1
LAST=6

# MODEL=model-00001000.pyrnn.gz
# MODEL=model-00002000.pyrnn.gz
# MODEL=model-00003000.pyrnn.gz
# MODEL=model-00004000.pyrnn.gz
MODEL=model-00005000.pyrnn.gz

LINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
    I=$(printf '%04d\n' $i)
    MORELINES=($DATA/bin/$I/0001/*.png)
    LINES=("${LINES[@]}" "${MORELINES[@]}")
done

ocropus-rpred -m $DATA/models/$MODEL "${LINES[@]}"
