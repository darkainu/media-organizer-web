document.addEventListener('DOMContentLoaded', () => {
    const selectFolderBtn = document.getElementById('selectFolderBtn');
    const organizeBtn = document.getElementById('organizeBtn');
    const status = document.getElementById('status');
    let selectedPath = null;

    selectFolderBtn.addEventListener('click', async () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.webkitdirectory = true;
        input.directory = true;
        input.addEventListener('change', (e) => {
            const files = e.target.files;
            if (files.length > 0) {
                // Set the correct full path including Downloads directory
                const paths = Array.from(files).map(file => file.webkitRelativePath);
                const parentPath = paths[0].split('/')[0];
                selectedPath = `/home/darkainu/Downloads/${parentPath}`;
                status.textContent = `Selected folder: ${selectedPath}`;
            }
        });
        input.click();
    });

    organizeBtn.addEventListener('click', async () => {
        if (!selectedPath) {
            status.textContent = 'Please select a folder first';
            return;
        }

        try {
            const response = await fetch('/organize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ folderPath: selectedPath })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            status.textContent = result.message;
        } catch (error) {
            status.textContent = `Error: ${error.message}`;
        }
    });
});