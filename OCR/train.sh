#!/usr/bin/env bash

./getcodec.py

source settings.sh

LINES=()
for ((i=$FIRST; i<=$LAST; i++))
do
	I=$(printf '%04d\n' $i)

  # get all files
	PAGE_LINES=($DATA/bin/$I/0001/*.png)

  # get files to exclude
  EXCL_LINES=()
  for EXCL in $(cat $DATA/scans/excl_$I.txt);
  do
    L=$DATA/bin/$I/0001/$EXCL.bin.png
  	EXCL_LINES=("${EXCL_LINES[@]}" "${L}")
  done

  # remove excluded files
  FINAL=()
  for L in ${PAGE_LINES[@]};
  do
    if [ "$L" = "$EXCL_LINES" ];
    then
      EXCL_LINES=("${EXCL_LINES[@]:1}")
    else
      FINAL=("${FINAL[@]}" $L)
    fi
  done

	LINES=("${LINES[@]}" "${FINAL[@]}")
done


# python 2 mode
source ./ocropy/ocropus_venv/bin/activate
ocropus-rtrain -c $DATA/codecs/all.txt -N $NTRAIN -F $FTRAIN -o $DATA/models/model "${LINES[@]}"
deactivate 
