from flask import Flask, render_template, request, jsonify
import os
from media_organizer import MediaOrganizerApp
import tkinter as tk

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    try:
        data = request.get_json()
        folder_path = data.get('folderPath')
        print(f"Received folder path: {folder_path}")

        if not os.path.exists(folder_path):
            return jsonify({'error': f'Directory not found: {folder_path}'}), 404

        root = tk.Tk()
        root.withdraw()
        organizer = MediaOrganizerApp(root)
        organizer.folder_path = folder_path
        organizer.organize_files()
        root.destroy()

        return jsonify({'message': 'Files organized successfully'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)