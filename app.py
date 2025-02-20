from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# You would get this from environment variables in production
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your-api-key')
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'London')
    try:
        # Get current weather
        current_weather = requests.get(
            f"{WEATHER_API_URL}/weather",
            params={
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }
        ).json()
        
        # Get 5-day forecast
        forecast = requests.get(
            f"{WEATHER_API_URL}/forecast",
            params={
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }
        ).json()
        
        return jsonify({
            'current': current_weather,
            'forecast': forecast
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
