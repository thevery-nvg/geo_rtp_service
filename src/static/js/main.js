async function sendData() {
    const input = document.getElementById('input').value;
    if (input.trim() === '') {
    alert('Поле не должно быть пустым!');
    return; // Выходим из функции, если поле пустое
}
    const hiddenField = document.getElementById('hiddenField');
    const coordinatesList = document.getElementById('coordinatesList');

    const inputFormatElement = document.getElementById('input_select');
    const inputFormatText = inputFormatElement.options[inputFormatElement.selectedIndex].text;

    const outputFormatElement = document.getElementById('output_select');
    const outputFormatText = outputFormatElement.options[outputFormatElement.selectedIndex].text;


    try {
        const response = await fetch('/api/geocode_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input ,fi:inputFormatText,fo:outputFormatText}),
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
            body: JSON.stringify({ address: input ,fi:inputFormatText,fo:outputFormatText}),
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



//из файла navbar


async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Важно для работы с куками
        });
        if (response.ok) {
            // Успешный выход
            // Очищаем куки вручную
            document.cookie = "fastapi_session=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
            // Очищаем localStorage (если используется JWT)
            localStorage.removeItem('access_token');
            // Перенаправляем пользователя на главную страницу
            //window.location.href = '/';
        } else {
            // Обработка ошибки, если выход не удался
            console.error('Logout failed:', response.statusText);
            alert('Logout failed: ' + response.statusText);
        }
    }
    catch (error) {
       // console.error('Error during logout:', error);
        //alert('Error during logout: ' + error.message);}
        }}

//document.getElementById('logout-button').addEventListener('click', logout);
//из файла navbar


