#!/bin/bash

source settings.sh
#FIRST=1
#LAST=1

# binarize
for ((i=$FIRST; i<=$LAST; i++))
do
	I=$(printf '%04d\n' $i)
	:
	rm -r ${DATA}/bin/$I
	ocropus-nlbin -n ${DATA}/scans/scan_$I.tif -o ${DATA}/bin/$I
done

# split images
for ((i=$FIRST; i<=$LAST; i++))
do
	I=$(printf '%04d\n' $i)
	:
	rm -r ${DATA}/bin/$I/0001
	ocropus-gpageseg --maxcolseps 0 ${DATA}/bin/$I/0001.bin.png
done

# split transcriptions
for ((i=$FIRST; i<=$LAST; i++))
do
	./septrans.py $i
done
