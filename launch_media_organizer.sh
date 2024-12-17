#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "${SCRIPT_DIR}/config.env"

export PATH="/home/${USER_NAME}/miniconda3/bin:$PATH"
source /home/${USER_NAME}/miniconda3/bin/activate
conda activate env
python /home/${USER_NAME}/code/media-organizer/media_organizer.py

