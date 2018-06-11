#!/bin/bash

source ./ocropy/ocropus_venv/bin/activate
# Directory of data.
DATA=../Data/FrenchBible

# Configuarble parameters
FIRST=1
LAST=1

### Parameters of training.

# How many iterations.
NTRAIN=1000
# Saving intermediate model after how many iterations.
FTRAIN=1000

MODEL=model-00001000.pyrnn.gz
