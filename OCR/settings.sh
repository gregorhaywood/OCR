#!/usr/bin/env bash

# python 3 venv for normal scripts
source venv/bin/activate


# Directory of data.
# Exported to make availible in python scripts
export DATA="../French"

# Configuarble parameters
# pages to process
export FIRST=1
export LAST=2


### Parameters of training.

# How many total iterations.
NTRAIN=1000
# Saving intermediate model after how many iterations.
FTRAIN=1000

MODEL=model-00001000.pyrnn.gz
