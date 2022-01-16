from pathlib import Path

from cmt_website.data.weather.data import WeatherData
from cmt_website.data.weather.wx_reader import WXReader


def make_watched_weatherdata(reader_path: Path) -> WeatherData:
    reader = WXReader(log_path=reader_path)
    weather_data = WeatherData(reader)
    return weather_data
