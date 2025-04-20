function getWeather() {
    const city = document.getElementById('cityInput').value;
    fetch(`/weather?city=${city}`)
        .then(response => response.json())
        .then(data => {
            const weatherDiv = document.getElementById('weatherResult');
            if (data.error) {
                weatherDiv.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                // Current weather
                let html = `
                    <h2>Weather in ${data.current.name}</h2>
                    <p>Temperature: ${data.current.main.temp}°C</p>
                    <p>Weather: ${data.current.weather[0].description}</p>
                    <p>Humidity: ${data.current.main.humidity}%</p>
                    
                    <h3>5-Day Forecast</h3>
                    <div class="forecast-container">
                `;
                
                // Process forecast data - OpenWeatherMap returns data in 3-hour intervals
                // Group by day to show daily forecast
                const forecastByDay = {};
                data.forecast.list.forEach(item => {
                    // Get date without time
                    const date = item.dt_txt.split(' ')[0];
                    if (!forecastByDay[date]) {
                        forecastByDay[date] = item;
                    }
                });
                
                // Add forecast items
                Object.keys(forecastByDay).forEach(date => {
                    const forecast = forecastByDay[date];
                    const formattedDate = new Date(date).toLocaleDateString('en-US', { 
                        weekday: 'short', 
                        month: 'short', 
                        day: 'numeric' 
                    });
                    
                    html += `
                        <div class="forecast-item">
                            <p class="forecast-date">${formattedDate}</p>
                            <p>Temp: ${forecast.main.temp}°C</p>
                            <p>${forecast.weather[0].description}</p>
                        </div>
                    `;
                });
                
                html += `</div>`;
                weatherDiv.innerHTML = html;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('weatherResult').innerHTML = 
                '<p class="error">Error fetching weather data</p>';
        });
}
