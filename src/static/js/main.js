async function sendData() {
    const input = document.getElementById('input').value;
    if (input.trim() === '') {
    alert('Поле не должно быть пустым!');
    return; // Выходим из функции, если поле пустое
}
    const hiddenField = document.getElementById('hiddenField');
    const coordinatesList = document.getElementById('coordinatesList');

    try {
        const response = await fetch('/api/geocode_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        displayCoordinates(data)
    } catch (error) {
        coordinatesList.textContent = 'Произошла ошибка: ' + error.message;
    }

    try {
        const response = await fetch('/api/geocode_gpx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        hiddenField.value = JSON.stringify(data, null, 2);

    } catch (error) {
        hiddenField.textContent = 'Произошла ошибка: ' + error.message;
    }

}
async function sendData_google() {
    const input = document.getElementById('input').value;
    if (input.trim() === '') {
        alert('Поле не должно быть пустым!');
        return; // Выходим из функции, если поле пустое
    }
    const hiddenField = document.getElementById('hiddenField');
    const coordinatesList = document.getElementById('coordinatesList');
    const button = document.getElementById('downloadButton');
    try {
        const response = await fetch('/api/google_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        displayCoordinates(data)
    } catch (error) {
        coordinatesList.textContent = 'Произошла ошибка: ' + error.message;
    }

    try {
        const response = await fetch('/api/google_gpx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        hiddenField.value = JSON.stringify(data, null, 2);
        console.log(hiddenField.value);
    } catch (error) {
        hiddenField.textContent = 'Произошла ошибка: ' + error.message;
    }

}

function displayCoordinates(coordinates) {
    const coordinatesList = document.getElementById('coordinatesList');
    coordinatesList.innerHTML = '';
    coordinates.forEach(coord => {
        const li = document.createElement('li');
        li.textContent = coord;
        coordinatesList.appendChild(li);
    });
}

function downloadData() {
    const button = document.getElementById('downloadButton');

    const output = document.getElementById('hiddenField').value;

    if (!output) {
        alert('Нет данных для скачивания');
        return;
    }

    const jsonData = JSON.parse(output);
    const blob = new Blob([jsonData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'geocoding_result.gpx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}







async function sendData_ready() {
    const input = document.getElementById('input').value;
    if (input.trim() === '') {
    alert('Поле не должно быть пустым!');
    return; // Выходим из функции, если поле пустое
}
    const hiddenField = document.getElementById('hiddenField');
    const coordinatesList = document.getElementById('coordinatesList');

    try {
        const response = await fetch('/api/geocode_list_ready', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        displayCoordinates(data)
    } catch (error) {
        coordinatesList.textContent = 'Произошла ошибка: ' + error.message;
    }

    try {
        const response = await fetch('/api/geocode_gpx_ready', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        hiddenField.value = JSON.stringify(data, null, 2);

    } catch (error) {
        hiddenField.textContent = 'Произошла ошибка: ' + error.message;
    }

}




document.addEventListener('DOMContentLoaded', () => {
  const uploadButton = document.getElementById('uploadButton');
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');
  const uploadFilesButton = document.getElementById('uploadFilesButton');
  const progressBar = document.getElementById('progressBar');
  const progressBarFill = document.getElementById('progressBarFill');
  const uploadText = document.getElementById('uploadText');
  const uploadIcon = document.getElementById('uploadIcon');

  let filesArray = [];
  let expanded = false;

  uploadButton.addEventListener('click', () => {
    if (!expanded) {
      fileInput.click();
    } else {
      uploadFiles(filesArray);
    }
  });

  fileInput.addEventListener('change', () => {
    filesArray = Array.from(fileInput.files);
    fileList.innerHTML = '';

    filesArray.forEach(file => {
      const listItem = document.createElement('li');
      listItem.textContent = `${file.name} (${formatBytes(file.size)})`;
      fileList.appendChild(listItem);
    });

    expandButton();
  });

  function expandButton() {
    expanded = true;
    uploadButton.classList.add('expanded');
    fileList.style.display = 'block';
    uploadFilesButton.style.display = 'block';
    uploadText.style.display = 'none';
    uploadIcon.style.display = 'none';
  }

  function collapseButton() {
    expanded = false;
    uploadButton.classList.remove('expanded');
    fileList.style.display = 'none';
    uploadFilesButton.style.display = 'none';
    uploadText.style.display = 'block';
    uploadIcon.style.display = 'block';
  }

  uploadFilesButton.addEventListener('click', () => {
    if (filesArray.length > 0) {
      uploadFiles(filesArray);
    } else {
      alert('Please select files to upload.');
    }
  });

  async function uploadFiles(files) {
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }

        try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();

        console.log('Upload successful:', result);




    } catch (error) {
        console.error('Upload failed:', error);
        alert('Failed to upload files.');
    }

//Фейковый прогресс бар
    progressBar.style.display = 'block';
    let uploadedFiles = 0;

    files.forEach(file => {
      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        progressBarFill.style.width = `${progress}%`;

        if (progress >= 100) {
          clearInterval(interval);
          uploadedFiles++;

          if (uploadedFiles === files.length) {
            alert('All files uploaded!');
            progressBar.style.display = 'none';
            progressBarFill.style.width = '0%';
            collapseButton();
          }
        }
      }, 300);
    });
//Фейковый прогресс бар
    }



  function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }
});