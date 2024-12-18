from flask import Flask, render_template, request, jsonify, session
import os
from pathlib import Path
from media_organizer import MediaOrganizerApp
import tkinter as tk
import shutil

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Add this for session support

# Track moved files globally
moved_files = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    global moved_files
    try:
        data = request.get_json()
        folder_name = data.get('folderPath')
        home_dir = str(Path.home())
        folder_path = os.path.join(home_dir, 'Downloads', folder_name)
        print(f"Attempting to organize files in: {folder_path}")

        root = tk.Tk()
        root.withdraw()
        organizer = MediaOrganizerApp(root)
        organizer.folder_path = folder_path
        result = organizer.organize_files()
        moved_files = organizer.moved_files  # Store moved files
        root.destroy()

        return jsonify({
            'message': 'Files organized successfully',
            'organized_files': len(result) if result else 0
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/undo', methods=['POST'])
def undo():
    global moved_files
    try:
        data = request.get_json()
        folder_name = data.get('folderPath')
        home_dir = str(Path.home())
        folder_path = os.path.join(home_dir, 'Downloads', folder_name)

        # Revert each file move
        for new_path, original_path in moved_files:
            if os.path.exists(new_path):
                os.makedirs(os.path.dirname(original_path), exist_ok=True)
                shutil.move(new_path, original_path)

        moved_files = []  # Clear the moved files list
        return jsonify({'message': 'Changes reverted successfully'})
    except Exception as e:
        print(f"Error during undo: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
