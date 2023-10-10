#!/usr/bin/env fish
fish -C "
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
source venv/bin/activate.fish
"

# this script runs venv on linux in fish shell
# relax

