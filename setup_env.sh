#!/bin/bash
echo "============================"
echo "Setting up virtual environment"
echo "============================"

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "============================"
echo "Setup complete!"
echo "To activate later, run: source .venv/bin/activate"
echo "============================"
