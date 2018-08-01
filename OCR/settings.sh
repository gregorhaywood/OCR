#!/usr/bin/env bash

# python 3 venv for normal scripts
source venv/bin/activate


# Directory of data.
# Exported to make availible in python scripts
DATA=$(./config.py DATA)

# Configuarble parameters
# pages to process
FIRST=$(./config.py FIRST)
LAST=$(./config.py LAST)
FIRST_T=$(./config.py FIRST)
LAST_T=$(./config.py LAST)


### Parameters of training.

# How many total iterations.
NTRAIN=$(./config.py NTRAIN)
# Saving intermediate model after how many iterations.
FTRAIN=$(./config.py FTRAIN)

MODEL=$(./config.py MODEL)
