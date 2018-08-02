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

The script directory,'OCR,' should contain the ocropy directory or a link to it.

The automation scripts in OCR use a different virtual environment, as they are python
3. This is set up as follows:
In OCR/:
    $ virtualenv venv
    $ source venv/bin/activate 
    $ pip install -r requirements.txt

NOTE:
*Two virtual environments are used because the internal ocropus one has constraints
that I struggled to incorporate into a single environment. This approach maintains
the modular organisation, although it is rather obtuse.*

## Use
### Setup 
A directory tree must be created to store works in progress. It should have the 
following structure:
<pre>
$DATA/
|__scans/
|   |__
|   |__
|__trans/
|   |__
|   |__
|__codecs/
|   |__
|   |__
|__bin/
|   |__
|   |__
|__models/
|   |__model-{%08d}.pyrnn.gz - the outputs of training ocropus
</pre>
$DATA/scans

contains:
* [files of form:] scan_123.tif
* [files of form:] exclude_123.txt

Files of form exclude_123.txt contain lines of form 010003.bin.png,
corresponding to lines automatically extracted from the scan that need
to be ignored.

$DATA/trans

contains:
* [files of form:] trans_123.txt

$DATA/codecs

contains:
* ordinaries.txt
* all.txt
* names.txt

The file ordinaries.txt is maintained by hand. It contains ordinary
characters, which correspond to a single key on a normal keyboard.
The file all.txt may be overwritten automatically, as extracted
from the transcriptions. The file named.txt is a human readable
version, with names of glyphs.

$DATA/bin

contains reproducible files. Must be initialised to contain the directory structure.

$DATA/models

contains models resulting from training.

$DATA/backup

may be used for storing backups.
