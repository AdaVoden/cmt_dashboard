from typing import Iterable, Literal, Tuple, Union

import pandas as pd
from attr import define, field
from cmt_website.weather.reader_interface import WeatherReaderInterface


@define
class WeatherData:
    reader: WeatherReaderInterface = field()
    wind_direction: str = field(init=False, default="0")

    def get_temperature(
        self,
        last: float = 0,
        interval: Literal["month", "day", "hour", "minute", None] = None,
    ) -> Iterable[float]:
        pass

    def get_wind_speed(
        self,
        last: float = 0,
        interval: Literal["month", "day", "hour", "minute", None] = None,
    ) -> Iterable[float]:
        pass

    def get_humidity(
        self,
        last: float = 0,
        interval: Literal["month", "day", "hour", "minute", None] = None,
    ) -> Iterable[float]:
        pass

    def get_pressure(
        self,
        last: float = 0,
        interval: Literal["month", "day", "hour", "minute", None] = None,
    ) -> Iterable[float]:
        pass

    def get_current_temperature(self) -> Tuple[float, float, float]:
        pass
