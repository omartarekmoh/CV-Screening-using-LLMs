#!/bin/bash
# Load conda in the script
source ~/miniconda3/etc/profile.d/conda.sh
conda activate mini-rag-app

echo "✅ Running in conda environment: $CONDA_DEFAULT_ENV"
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 5000
