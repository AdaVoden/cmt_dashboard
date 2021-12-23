import pandas as pd
from attr import define, field


@define
class WeatherFeature:

    name: str = field()
    data: pd.Series = field()
    current: float = field(init=False)
    minimum: float = field(init=False)
    maximum: float = field(init=False)


@define
class Wind(WeatherFeature):
    name: str = field(init=False, default="Wind")
    direction: str = field(init=False)
    direction_numeric: float = field(init=False)
