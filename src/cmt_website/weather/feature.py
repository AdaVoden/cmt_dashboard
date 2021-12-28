import logging
from typing import Literal

import numpy as np
import pandas as pd
from attr import define, field


@define(slots=True)
class WeatherFeature:
    """Container and accessor for the data of a specific weather feature, such as
    temperature"""

    _data: pd.Series = field()
    current: float = field(init=False)
    minimum: float = field(init=False)
    maximum: float = field(init=False)

    def update(self, new_data: pd.Series):
        """Takes in new data to update the current WeatherFeature

        Parameters
        ----------
        new_data : pd.Series
            New data

        """
        self.current = np.around(new_data.tail(1).item(), decimals=2)
        self._data = new_data
        last_day = self.last(amount=1, interval="day")
        self.minimum = np.around(last_day.min(), decimals=2)
        self.maximum = np.around(last_day.max(), decimals=2)
        logging.debug(f"Updated weather feature {self._data.name} with new data")

    def __attrs_post_init__(self):
        self.update(self._data)
        logging.debug(f"Initialized weather feature {self._data.name}")

    def last(
        self, amount: float = 1, interval: Literal["minute", "hour", "day"] = "day"
    ) -> pd.Series:
        """Retrieves all weather features from the specified interval of time

        Parameters
        ----------
        amount : float
            The number of intervals to retrieve from the weather feature
        interval : Literal["minute", "hour", "day"]
            The interval of time to look back, limited to minute hour or day.

        Returns
        -------
        pd.Series
            Timeseries of the weather feature from specified point in history
            onward

        Raises
        ------
        ValueError
            Thrown if interval parameter given anything other than minute, hour
            or day

        """
        time_intervals_allowed = ["minute", "hour", "day"]
        if interval not in time_intervals_allowed:
            raise ValueError(
                f"Not an understandable time interval, expected one of {', '.join(time_intervals_allowed)}, received {interval}"
            )
        current = self._data.tail(1).index.item()
        offset = pd.Timedelta(value=amount, unit=interval)
        delta_time = current - offset
        return self._data[delta_time:]


@define(slots=True)
class WindDirection(WeatherFeature):
    """Container and accessor for the data of wind direction, with distinct
    accessor for the cardinal direction of the wind direction"""

    @property
    def cardinal(self):
        """Matches the direction East from North to the cardinal directions"""
        wind_direction = self.current
        # I don't really like doing this, but cannot think of a better way yet
        if wind_direction >= 337.5 or wind_direction < 22.5:
            return "N"
        if wind_direction >= 22.5 and wind_direction < 67.5:
            return "NE"
        if wind_direction >= 67.5 and wind_direction < 112.5:
            return "E"
        if wind_direction >= 112.5 and wind_direction < 157.5:
            return "SE"
        if wind_direction >= 157.5 and wind_direction < 202.5:
            return "S"
        if wind_direction >= 202.5 and wind_direction < 247.5:
            return "SW"
        if wind_direction >= 247.5 and wind_direction < 292.5:
            return "W"
        if wind_direction >= 292.5 and wind_direction < 337.5:
            return "NW"
