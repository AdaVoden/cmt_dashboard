import logging
from typing import Dict

import pandas as pd
from attr import define, field
from cmt_website.data.interfaces import DataReader
from cmt_website.data.weather.feature import WeatherFeature, WindDirection


@define(slots=True)
class WeatherData:
    reader: DataReader = field()
    temperature: WeatherFeature = field(init=False)
    wind_speed: WeatherFeature = field(init=False)
    wind_direction: WindDirection = field(init=False)
    humidity: WeatherFeature = field(init=False)
    pressure: WeatherFeature = field(init=False)

    @property
    def features(self) -> Dict[str, WeatherFeature]:
        return {
            "Temperature": self.temperature,
            "Humidity": self.humidity,
            "Pressure": self.pressure,
            "Wind speed": self.wind_speed,
            "Wind direction": self.wind_direction,
        }

    def _create_features(self, df: pd.DataFrame):
        """Creates all weatherfeatures from read data

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe of weather data from source

        """

        self.temperature = WeatherFeature(df["Temperature"], unit="\u00B0 C")
        self.wind_speed = WeatherFeature(df["Wind Speed"], unit="km/h")
        self.wind_direction = WindDirection(df["Wind Direction"], unit="\u00B0 E of N")
        self.humidity = WeatherFeature(df["Humidity"], unit="%")
        self.pressure = WeatherFeature(df["Pressure"], unit="mbar")

    def __attrs_post_init__(self):
        """Post-initialization feature creation from weather data"""
        self._create_features(self.reader.read())
        logging.info("Created WeatherData class and features")

    def update(self):
        logging.info("Updating Weather data")
        self._create_features(self.reader.read())
