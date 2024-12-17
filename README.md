# Media Organizer

A Python desktop application that organizes media files (images and videos) by date into year/month folders.

## Features

- Organizes media files based on EXIF data or file modification date
- Supports multiple image formats (PNG, JPG, JPEG, GIF, HEIC, WEBP)
- Supports video formats (MP4, MOV, AVI)
- User-friendly GUI interface
- Undo functionality for file organization

## Installation

1. Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
2. Clone the repository:
   ```bash
   git clone https://github.com/darkainu/media-organizer.git
3. Edit config.env with your username
4. Run the install:
    chmod +x install.sh
    ./install.sh

## Usage

Launch the application either:

From your applications menu
Using the command: ./launch_media_organizer.sh

Then:

Click "Select Folder" to choose the directory containing media files
Click "Organize Files" to start organizing
Use "Undo Last Organization" if needed
