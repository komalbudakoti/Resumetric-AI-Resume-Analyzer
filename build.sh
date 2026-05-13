#!/bin/bash

# Install system dependencies required for building packages like blis, thinc, spacy
apt-get update && apt-get install -y build-essential python3-dev libblas-dev liblapack-dev

# Install Python dependencies
pip install -r requirements.txt