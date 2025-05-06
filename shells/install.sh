#!/bin/bash
# Load conda in the script
source ~/miniconda3/etc/profile.d/conda.sh
conda activate mini-rag-app

pip install -r src/requirements.txt