let selectedFolderPath = null;
let isOrganizing = false;

document.addEventListener('DOMContentLoaded', () => {
    const selectFolderBtn = document.getElementById('selectFolderBtn');
    const organizeBtn = document.getElementById('organizeBtn');
    const undoBtn = document.getElementById('undoBtn');
    const progressBar = document.getElementById('progressBar').querySelector('.progress-fill');
    const progressText = document.getElementById('progressText');
    const folderPath = document.getElementById('folderPath');
    const organizationStatus = document.getElementById('organizationStatus');

    selectFolderBtn.addEventListener('click', async () => {
        try {
            const dirHandle = await window.showDirectoryPicker({
                mode: 'readwrite',
                startIn: 'downloads',
                types: [{
                    description: 'Media Files',
                    accept: {
                        'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.heic'],
                        'video/*': ['.mp4', '.mov', '.avi']
                    }
                }],
                excludeAcceptAllOption: false
            });

            // Verify we have permission
            const permissionStatus = await dirHandle.queryPermission({ mode: 'readwrite' });
            if (permissionStatus !== 'granted') {
                await dirHandle.requestPermission({ mode: 'readwrite' });
            }

            selectedFolderPath = dirHandle.name;
            folderPath.textContent = selectedFolderPath;
            organizeBtn.disabled = false;
            organizationStatus.textContent = '';
        } catch (err) {
            console.error('Error selecting folder:', err);
        }
    });

    organizeBtn.addEventListener('click', async () => {
        if (!selectedFolderPath || isOrganizing) return;

        isOrganizing = true;
        organizeBtn.disabled = true;
        progressBar.style.width = '0%';
        organizationStatus.textContent = 'Organizing files...';

        try {
            const response = await fetch('/organize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ folderPath: selectedFolderPath })
            });

            const data = await response.json();

            if (response.ok) {
                progressBar.style.width = '100%';
                progressText.textContent = '100%';
                organizationStatus.textContent = `Success! Organized ${data.organized_files} files.`;
                undoBtn.disabled = false;
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            organizationStatus.textContent = `Error: ${error.message}`;
        } finally {
            isOrganizing = false;
            organizeBtn.disabled = false;
        }
    });

    undoBtn.addEventListener('click', async () => {
        if (isOrganizing) return;

        try {
            undoBtn.disabled = true;
            organizationStatus.textContent = 'Undoing changes...';

            const response = await fetch('/undo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ folderPath: selectedFolderPath })
            });

            const data = await response.json();

            if (response.ok) {
                organizationStatus.textContent = 'Changes reverted successfully!';
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            organizationStatus.textContent = `Error: ${error.message}`;
        } finally {
            undoBtn.disabled = false;
        }
    });
});