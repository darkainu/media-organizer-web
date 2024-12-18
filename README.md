# Media Organizer Web

A web-based media file organizer that helps you sort photos and videos into Year/Month folders automatically.

## Features
- Organize media files into Year/Month folders
- Smart date detection using EXIF data
- Supports multiple formats (PNG, JPG, JPEG, GIF, HEIC, MP4, MOV, AVI)
- Clean web interface
- Progress tracking
- Undo functionality
- PWA support for offline access

## Installation
1. Clone the repository:
```bash
git clone https://github.com/darkainu/media-organizer-web.git
cd media-organizer-web

2. Install dependencies:
pip install -r requirements.txt

3. Run the application:
python app.py

## Usage
1. Open your browser to http://localhost:5000
2. Select a folder containing your media files
3. Click "Organize Files" to start
4. Use "Undo Changes" if needed

## Requirements
1. Python 3.8+
2. Flask
3. Pillow