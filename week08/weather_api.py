"""WeatherAPI client and display helpers."""

import requests


class WeatherAPI:
    def __init__(self, api_key, base_url="https://api.weatherapi.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def _get(self, endpoint, params):
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}", params=params, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError):
            return None

    def get_current_weather(self, location):
        return self._get('current.json', {'key': self.api_key, 'q': location})

    def get_forecast(self, location, days=3):
        if not isinstance(days, int) or isinstance(days, bool) or not 1 <= days <= 3:
            raise ValueError('Forecast days must be between 1 and 3.')
        return self._get('forecast.json', {
            'key': self.api_key, 'q': location, 'days': days
        })


def format_current_weather(data):
    location = data['location']
    current = data['current']
    return (f"{location['name']}, {location['country']}: "
            f"{current['temp_f']}°F, {current['condition']['text']}")


def format_forecast(data):
    lines = []
    for item in data['forecast']['forecastday']:
        day = item['day']
        lines.append(
            f"{item['date']}: high {day['maxtemp_f']}°F, "
            f"low {day['mintemp_f']}°F, {day['condition']['text']}"
        )
    return '\n'.join(lines)
