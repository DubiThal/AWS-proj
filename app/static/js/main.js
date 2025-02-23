function getWeather() {
    const city = document.getElementById('cityInput').value;
    fetch(`/weather?city=${city}`)
        .then(response => response.json())
        .then(data => {
            const weatherDiv = document.getElementById('weatherResult');
            if (data.error) {
                weatherDiv.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                weatherDiv.innerHTML = `
                    <h2>Weather in ${data.current.name}</h2>
                    <p>Temperature: ${data.current.main.temp}°C</p>
                    <p>Weather: ${data.current.weather[0].description}</p>
                    <p>Humidity: ${data.current.main.humidity}%</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('weatherResult').innerHTML = 
                '<p class="error">Error fetching weather data</p>';
        });
}
