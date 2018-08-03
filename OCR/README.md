# OCR Framework
The scripts provided here provide a framework for OCR using Ocropus.

## Installation
Ocropus is written in Python 2, so must be installed with its virtual environment. 
Clone it from [Github] (https://github.com/tmbdev/ocropy), then follow the installation 
instructions for a virtual environment:

    $ git pull git@github.com:tmbdev/ocropy.git
    $ cd ocropy
    $ virtualenv ocropus_venv/
    $ source ocropus_venv/bin/activate
    $ pip install -r requirements.txt
    $ wget -nd http://www.tmbdev.net/en-default.pyrnn.gz
    $ mv en-default.pyrnn.gz models/
    $ python setup.py install

This directory should contain the ocropy directory or a link to it.

The automation scripts in OCR use a different virtual environment, as they are python
3. This is set up as follows:
    $ virtualenv venv
    $ source venv/bin/activate 
    $ pip install -r requirements.txt

NOTE:
*Two virtual environments are used because the internal ocropus one has constraints
that I struggled to incorporate into a single environment. This approach maintains
the modular organisation, although it is rather obtuse.*

## Use
### Setup 
config.yaml must be correctly configured. **DATA** should be a path to the structure above. **FIRST** and **LAST** are the page numbers of the first and last pages to process (they do not need to be padded to 4 digits). **FIRST_T** and **LAST_T** are like **FIRST** and **LAST**, except for training. They are different so that some data can be set aside for validation. *A second reason for this is that a bug in ocropus-rtrain causes it to crash if given too large a training set. If Training crashes, try decreasing the size of the training set.* **NTRAIN** is the total number of data items to iterate through while training. **FTRAIN** is the number of iterations between Ocropus saving checkpoints. **MODEL** is the name of the model to use for transcriptions (of those available in $DATA/models).

## Pipeline
    $ ./prep.sh
This binarizes and segments the scans, and splits the transcriptions into gt.txt files for each line.

    $ ./sellines.py
Opens a GUI for selecting which image segments contain meaningful text. 

    $ ./edittrans.py
Correct gt.txt files through a GUI. This is necessary, as prep.sh does not necessarily label gt.txts correctly. This can also be used as an alternative way to supply the transcriptions.

    $ ./train.sh
Train models according to config.yaml.

    $ ./test.sh, after adjusting FIRST and LAST, and MODEL
Use a model to transcribe data.

    $ ./eval.sh, after adjusting FIRST and LAST
Evaluate a model for accuracy based on the results of a transcription.

    $ ./postproc.py
Created boxed.xml files showing positions of image segments. Currently this overwrites the transcription, which should be avoided.

### Also availible

    $ ./getcodec.py
And manual inspection of $DATA/codecs/names.txt
Maintenance of characters in transcriptions.

    $ ./subtrans.py firstpage lastpage oldgrapheme newgrapheme
    $ ./subtrans.py firstpage lastpage oldgrapheme newgrapheme confirm

which requires manually inspecting files in $DATA/trans/ .
The changed files are of the form trans_1234_new.txt , which can
be compare to files of the form trans_1234.txt . When this is approved,
the change is made permanent by the second command.


