#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system build dependencies required for packages like blis, thinc, and spacy
apt-get update && apt-get install -y build-essential python3-dev libblas-dev liblapack-dev

# Upgrade packaging tools to avoid wheel/build errors
python3 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
python3 -m pip install -r requirements.txt

python3 -m spacy download en_core_web_sm