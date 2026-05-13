#!/bin/bash
set -e

# Install system dependencies required for building packages like blis, thinc, spacy
apt-get update && apt-get install -y build-essential python3-dev libblas-dev liblapack-dev

# Upgrade packaging tools to avoid wheel/build errors
python3 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
python3 -m pip install -r requirements.txt