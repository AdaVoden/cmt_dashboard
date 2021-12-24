import pandas as pd
from attr import define, field
from cmt_website.weather.feature import WeatherFeature, WindDirection
from cmt_website.weather.reader_interface import WeatherReaderInterface


@define
class WeatherData:
    reader: WeatherReaderInterface = field()
    temperature: WeatherFeature = field(init=False)
    wind_speed: WeatherFeature = field(init=False)
    wind_direction: WindDirection = field(init=False)
    humidity: WeatherFeature = field(init=False)
    pressure: WeatherFeature = field(init=False)
