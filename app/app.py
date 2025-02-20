from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

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
            },
            timeout=5
        ).json()
        
        # Get 5-day forecast
        forecast = requests.get(
            f"{WEATHER_API_URL}/forecast",
            params={
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            },
            timeout=5
        ).json()
        
        return jsonify({
            'current': current_weather,
            'forecast': forecast,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error fetching weather data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    try:
        # Test API connectivity
        requests.get(f"{WEATHER_API_URL}/weather", 
                    params={'q': 'London', 'appid': WEATHER_API_KEY},
                    timeout=5)
        return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
