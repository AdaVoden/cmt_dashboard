import logging

import pandas as pd
from attr import define, field
from cmt_website.weather.feature import WeatherFeature, WindDirection
from cmt_website.weather.reader_interface import WeatherReaderInterface


@define(slots=True, eq=False)
class WeatherData:
    reader: WeatherReaderInterface = field()
    temperature: WeatherFeature = field(init=False)
    wind_speed: WeatherFeature = field(init=False)
    wind_direction: WindDirection = field(init=False)
    humidity: WeatherFeature = field(init=False)
    pressure: WeatherFeature = field(init=False)

    def _create_features(self, df: pd.DataFrame):
        """Creates all weatherfeatures from read data

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe of weather data from source

        """

        self.temperature = WeatherFeature(df["Temperature"])
        self.wind_speed = WeatherFeature(df["Wind Speed"])
        self.wind_direction = WindDirection(df["Wind Direction"])
        self.humidity = WeatherFeature(df["Humidity"])
        self.pressure = WeatherFeature(df["Pressure"])

    def __attrs_pre_init__(self):
        """Calls super init for FileSystemEventHandler"""
        super().__init__()

    def __attrs_post_init__(self):
        """Post-initialization feature creation"""
        self._create_features(self.reader.read())
        logging.info("Created WeatherData class and features")
