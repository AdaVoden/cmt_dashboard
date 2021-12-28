from pathlib import Path

from cmt_website.weather.data import WeatherData
from cmt_website.weather.wx_reader import WXReader
from watchdog.observers import Observer


def make_watched_weatherdata(reader_path: Path) -> WeatherData:
    reader = WXReader(log_path=reader_path)
    weather_data = WeatherData(reader)
    observer = Observer(timeout=1)
    observer.schedule(event_handler=weather_data, path=reader_path)
    observer.start()
    return weather_data
