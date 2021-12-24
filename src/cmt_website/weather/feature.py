from typing import Literal

import pandas as pd
from attr import define, field


@define
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
        self.current = new_data.tail(1).item()
        self._data = new_data
        last_day = self.last(amount=1, interval="day")
        self.minimum = last_day.min()
        self.maximum = last_day.max()

    def __attrs_post_init__(self):
        self.update(self._data)

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
        current = self._data.tail(1).index
        offset = pd.Timedelta(value=amount, unit=interval)
        delta_time = current - offset
        return self._data[delta_time:]


@define
class WindDirection(WeatherFeature):
    """Container and accessor for the data of wind direction, with distinct
    accessor for the cardinal direction of the wind direction"""

    @property
    def cardinal(self):
        """Matches the direction East from North to the cardinal directions"""
        current = self.current
        # I don't really like doing this, but cannot think of a better way yet
        if current >= 337.5 or current < 22.5:
            return "N"
        if current >= 22.5 and current < 67.5:
            return "NE"
        if current >= 67.5 and current < 112.5:
            return "E"
        if current >= 112.5 and current < 157.5:
            return "SE"
        if current >= 157.5 and current < 202.5:
            return "S"
        if current >= 202.5 and current < 247.5:
            return "SW"
        if current >= 247.5 and current < 292.5:
            return "W"
        if current >= 292.5 and current < 337.5:
            return "NW"
