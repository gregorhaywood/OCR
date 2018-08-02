# Viterbi Space Finder
These scripts use the Viterbi algorithm to find spaces in images. Tests have yielded good results against truth transcripts.

## Scripts
All scripts contain their own help menus (via -h). Models are stored as csv files.

    $ ./mm-train.py [-h] -m MODEL -o OUT FILE [FILE ...]
Train an existing MODEL on FILE(s), storing the results in DIR.

    $ ./mm-fit [-h] -m MODEL FILE [FILE ...]
Fit a model to a number of input files.

    $ ./mm-view.py [-h] CODEC
View a codec csv in a human readable form.

## Codec Creation
Codec creation is difficult to automate. A line is needed for each character, and is of the form:
    **CHAR**, [**TRANS**, **MU**]...
**TRANS** is the transition probability in negative logarithm form. Before training, this can be assumed to be 0.5 in normal notation, so 0.6931471805599453 in NegLog form. **MU** for a given state will be *log(n+1)*, where *n* is the number of black pixels in a column matching that state (the +1 is needed to handle empty columns). **MU** should not be lower than 1 for any **CHAR** except space. Each **CHAR** will need a different number of states, which must be estimated. 

NOTE:
*In addition to the expected characters, '~' must be included, as Ocropus can always output this.*

