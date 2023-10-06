#!/usr/bin/env fish
fish -C "
python3 -m venv venv
source venv/bin/activate.fish
"

# this script runs venv on linux in fish shell
# relax

# later add file:
# requirements.txt 
# and line:
# pip install -r requirements.txt
# if we will depend on more libraries
