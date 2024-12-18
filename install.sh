#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "${SCRIPT_DIR}/config.env"

# Initialize conda
source ~/miniconda3/bin/activate

# Create conda environment and install dependencies
conda create -n env python=3.8 -y
conda activate env
conda install pillow flask -y
pip install exifread

# Set up desktop entry
cp media-organizer.desktop ~/.local/share/applications/
chmod +x launch_media_organizer.sh
update-desktop-database ~/.local/share/applications/
