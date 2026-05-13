#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade packaging tools to avoid wheel/build errors
python3 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
python3 -m pip install -r requirements.txt

python3 -m spacy download en_core_web_sm