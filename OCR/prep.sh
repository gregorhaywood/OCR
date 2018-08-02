#!/usr/bin/env bash

source settings.sh

# python 2 mode
source ./ocropy/ocropus_venv/bin/activate

# binarize
for ((i=$FIRST; i<=$LAST; i++))
do
	I=$(printf '%04d\n' $i)
	:
	rm -r ${DATA}/bin/$I
	if [ -f ${DATA}/scans/scan_$I.tif ];
	then 
		ocropus-nlbin -n ${DATA}/scans/scan_$I.tif -o ${DATA}/bin/$I
	elif [ -f ${DATA}/scans/scan_$I.png ];
	then
		ocropus-nlbin -n ${DATA}/scans/scan_$I.png -o ${DATA}/bin/$I
	fi
done


# split images
for ((i=$FIRST; i<=$LAST; i++))
do
	I=$(printf '%04d\n' $i)
	:
	rm -r ${DATA}/bin/$I/0001
	ocropus-gpageseg -n ${DATA}/bin/$I/0001.bin.png
	for F in ${DATA}/bin/$I/0001/*.bin.png;
	do 
	  echo > $(python3 -c '(print("'$F'".split(".bin.png")[0] + ".gt.txt"))');
	done
done

# back to python 3 mode
deactivate
source venv/bin/activate

# split transcriptions
for ((i=$FIRST; i<=$LAST; i++))
do
	./septrans.py $i
done
