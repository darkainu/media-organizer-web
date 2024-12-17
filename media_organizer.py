import os
import shutil
from calendar import month_name
from datetime import datetime
from PIL import Image
import exifread
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

class MediaOrganizerApp:
    def __init__(self, root):
        self.root = root
        # Enable DPI awareness
        self.root.tk.call('tk', 'scaling', 2.0)  # Increase default scaling
        self.root.title("Media File Organizer")
        self.root.geometry("1024x768")  # Larger default size

        # Configure main container with weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create scrollable frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.moved_files = []  # Track moved files for undo
        self.create_widgets()

    def create_widgets(self):
        # Configure styles for ttk widgets
        style = ttk.Style()
        style.configure('Large.TButton', padding=(20, 10))
        style.configure('Large.TLabel', padding=(10, 5))

        # Select folder button
        self.select_btn = ttk.Button(
            self.main_frame,
            text="Select Folder",
            command=self.select_folder,
            style='Large.TButton'
        )
        self.select_btn.grid(row=0, column=0, pady=20, sticky="ew")

        # Path label with wrapping
        self.path_label = ttk.Label(
            self.main_frame,
            text="No folder selected",
            wraplength=800,
            style='Large.TLabel'
        )
        self.path_label.grid(row=1, column=0, pady=20, sticky="ew")

        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            mode='determinate'
        )
        self.progress.grid(row=2, column=0, pady=20, sticky="ew")

        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="",
            style='Large.TLabel'
        )
        self.status_label.grid(row=3, column=0, pady=20, sticky="ew")

        # Organize button
        self.organize_btn = ttk.Button(
            self.main_frame,
            text="Organize Files",
            command=self.organize_files,
            style='Large.TButton'
        )
        self.organize_btn.grid(row=4, column=0, pady=20, sticky="ew")

        # Undo button
        self.undo_btn = ttk.Button(
            self.main_frame,
            text="Undo Last Organization",
            command=self.undo_organization,
            style='Large.TButton'
        )
        self.undo_btn.grid(row=5, column=0, pady=20, sticky="ew")

    def select_folder(self):
        folder_path = filedialog.askdirectory(
            title='Select Folder to Organize',
            initialdir=os.path.expanduser('~')  # Starts in home directory
        )
        if folder_path:
            self.folder_path = folder_path
            self.path_label.configure(text=f"Selected: {folder_path}")

    def get_date_taken(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                if 'EXIF DateTimeOriginal' in tags:
                    date_str = str(tags['EXIF DateTimeOriginal'])
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

            img = Image.open(file_path)
            if hasattr(img, '_getexif') and img._getexif() is not None:
                exif = img._getexif()
                if 36867 in exif:
                    date_str = exif[36867]
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                print(f"No EXIF data found in: {os.path.basename(file_path)}")
            else:
                print(f"File format not recognized for: {os.path.basename(file_path)}")

            return datetime.fromtimestamp(os.path.getmtime(file_path))

        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
            return datetime.fromtimestamp(os.path.getmtime(file_path))

    def organize_files(self):
        self.moved_files.clear()  # Clear previous moves
        if not hasattr(self, 'folder_path'):
            self.status_label.config(text="Please select a folder first!")
            return

        files = [f for f in os.listdir(self.folder_path)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mov', '.avi', '.heic', '.webp'))]

        self.progress['maximum'] = len(files)
        self.progress['value'] = 0

        for i, file in enumerate(files):
            file_path = os.path.join(self.folder_path, file)
            date_taken = self.get_date_taken(file_path)

            year_folder = os.path.join(self.folder_path, str(date_taken.year))
            month_folder = os.path.join(year_folder, month_name[date_taken.month])

            os.makedirs(month_folder, exist_ok=True)

            destination = os.path.join(month_folder, file)
            original_path = file_path
            shutil.move(file_path, destination)

            # Track the move operation
            self.moved_files.append((destination, original_path))

            self.progress['value'] = i + 1
            self.root.update()

        self.status_label.config(text="Organization complete!")

    def undo_organization(self):
        if not self.moved_files:
            self.status_label.config(text="Nothing to undo!")
            return

        self.progress['maximum'] = len(self.moved_files)
        self.progress['value'] = 0

        for i, (current_path, original_path) in enumerate(reversed(self.moved_files)):
            try:
                shutil.move(current_path, original_path)
                self.progress['value'] = i + 1
                self.root.update()
            except Exception as e:
                self.status_label.config(text=f"Error during undo: {str(e)}")
                return

        self.moved_files.clear()
        self.status_label.config(text="Undo complete!")
if __name__ == "__main__":
    root = tk.Tk()
    app = MediaOrganizerApp(root)
    root.mainloop()
