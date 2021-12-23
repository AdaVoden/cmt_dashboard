from pathlib import Path

import pandas as pd
from attr import define, field
from cmt_website.weather.reader_interface import WeatherReaderInterface
from numpy import float32, float64, int32


@define
class WXReader(WeatherReaderInterface):
    """Reads the wx.log from Talon system using provided path and returns weather
    data from station"""

    log_path: str = field(default="/usr/local/telescope/archive/logs/wx.log")
    _column_names_types = field(
        init=False,
        default=[
            "Julian Date",
            "Wind Speed",
            "Wind Direction",
            "Temperature",
            "Humidity",
            "Pressure",
            "Rain",
            "Alert Codes",
            "AuxTemp1",
            "AuxTemp2",
            "AuxTemp3",
        ],
    )
    _used_column_types = field(
        init=False,
        default={
            "Julian Date": float64,
            "Wind Speed": float32,
            "Wind Direction": int32,
            "Temperature": float32,
            "Humidity": int32,
            "Pressure": float32,
        },
    )
    _used_columns = field(
        init=False,
        default=[
            "Julian Date",
            "Wind Speed",
            "Wind Direction",
            "Temperature",
            "Humidity",
            "Pressure",
        ],
    )
    # _last_row_read = field(init=False, default=0)

    @log_path.validator  # type: ignore
    def _is_file(self, attribute, value):
        """Ensures that target log path is actually a file"""
        try:
            as_path = Path(value)
            assert as_path.is_file
        except AssertionError:
            raise ValueError("Unable to read {value} as it is not a valid file")

    def _read_to_dataframe(self, first_row: int = 0) -> pd.DataFrame:
        """Reads in file from log_path and returns data from specified row onward

        Parameters
        ----------
        first_row : int
            Row to start reading data at

        Returns
        -------
        pd.DataFrame
            Properly formatted weather data in proper types

        """

        df = pd.read_csv(
            filepath_or_buffer=self.log_path,
            delim_whitespace=True,
            names=self._column_names_types,
            index_col=0,  # use JD as index
            usecols=self._used_columns,
            dtype=self._used_column_types,
            engine="c",
            skiprows=first_row,
        )
        # Directly converting with a converter in read_csv failed.
        df["Time"] = pd.to_datetime(df.index.tolist(), unit="D", origin="julian")
        df = df.set_index(df["Time"], drop=True)
        return df  # type: ignore

    def read(self) -> pd.DataFrame:
        """Reads weather data and returns Dataframe with proper formatting

        Returns
        -------
        pd.DataFrame
            Properly formatted weather data in proper types

        """
        return self._read_to_dataframe()

    # def read_from_last(self) -> pd.DataFrame:
    #     return self._read_to_dataframe(first_row=self._last_row_read)

    def read_from_row(self, row: int = 0) -> pd.DataFrame:
        """Reads weather data starting from specified row

        Parameters
        ----------
        row : int
            Row to start reading data at

        Returns
        -------
        pd.DataFrame
            Properly formatted weather data in proper types

        """

        return self._read_to_dataframe(first_row=row)
