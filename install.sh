#!/bin/bash

# Photon Laser Tag

# Update packages and install pip
command sudo apt update && sudo apt install pip -y

# Install python dependencies
command pip install -r requirements.txt

# Run program
command python3 run.py