import json
from datetime import datetime, timezone
from typing import Literal

import numpy as np
import numpy.typing as npt
from attr import define, field
from bokeh.embed import json_item
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
from bokeh.plotting import Figure, figure
from cmt_website.plotting.plot_interface import PlottingInterface
from cmt_website.weather.data import WeatherData
from cmt_website.weather.feature import WeatherFeature


@define
class BokehPlotter(PlottingInterface):
    """Plotting object, has necessary data inserted and creates JSON-readable JSON
    scripts that replaces target divs"""

    weather: WeatherData = field()

    @property
    def temperature(self):
        """Plot of temperature data, replaces div with 'plot-temperature' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.temperature,
            title="Weather Station Temperature over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Temperature [\u00B0 C]"
        return json.dumps(json_item(plot, "plot-temperature"))

    @property
    def wind_speed(self):
        """Plot of wind speed data, replaces div with 'plot-wind-speed' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.wind_speed,
            title="Weather Station Wind Speed over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Wind Speed [km/h]"
        return json.dumps(json_item(plot, "plot-wind-speed"))

    @property
    def wind_direction(self):
        """Plot of wind_direction data, replaces div with 'plot-wind-direction' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.wind_direction,
            title="Weather Station Wind Direction over Time",
            type="scatter",
        )
        plot.yaxis[0].axis_label = "Wind Direction [Degrees East from North]"
        return json.dumps(json_item(plot, "plot-wind-direction"))

    @property
    def humidity(self):
        """Plot of humidity data, replaces div with 'plot-humidity' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.humidity,
            title="Weather Station Humidity over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Humidity [%]"
        return json.dumps(json_item(plot, "plot-humidity"))

    @property
    def pressure(self):
        """Plot of pressure data, replaces div with 'plot-pressure' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.wind_speed,
            title="Weather Station Pressure over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Pressure [mbar]"
        return json.dumps(json_item(plot, "plot-pressure"))

    @property
    def sqm(self):
        """Plot of SQM data, replaces div with 'plot-sqm' ID"""
        pass

    @staticmethod
    def _make_figure(title: str) -> Figure:
        """Makes Bokeh figure object with default settings, including setting the
        x-label as the current timezone's time

        Parameters
        ----------
        title : str
            Title of the plot

        Returns
        -------
        Figure
            Bokeh figure without any graph information

        """

        utc_dt = datetime.now(timezone.utc)
        current_timezone = utc_dt.astimezone().tzname()
        fig = figure(
            title=title,
            sizing_mode="scale_both",
            x_axis_label=f"Time [{current_timezone}]",
            max_width=750,
            max_height=750,
        )
        return fig

    def _plot_from_weatherfeature(
        self, feature: WeatherFeature, title: str, type: Literal["line", "scatter"]
    ) -> Figure:
        """Creates a plot from a given weatherfeature, can create lineplots or
        scatterplots

        Parameters
        ----------
        feature : WeatherFeature
            Target weather feature to retreive data from
        title : str
            Title of plot
        type : Literal["line", "scatter"]
            Targets either a line or scatterplot

        Returns
        -------
        Figure
            Bokeh figure with graph information

        """
        data = feature.last(amount=30, interval="day")
        x_data = data.index.to_numpy()
        y_data = data.to_numpy()
        if type == "line":
            return self._make_lineplot(xs=x_data, ys=y_data, title=title)
        if type == "scatter":
            return self._make_scatterplot(xs=x_data, ys=y_data, title=title)
        raise ValueError("Received incorrect plot type")

    # Next two functions violate DRY principles and should be refactored
    def _make_lineplot(
        self, xs: npt.NDArray[np.datetime64], ys: npt.NDArray[np.float_], title: str
    ) -> Figure:
        """Creates a line plot on given Bokeh figure, with target x and y data. Assumes
        that x data is datetime.

        Parameters
        ----------
        xs : npt.NDArray[np.datetime64]
            Datetime data for x-axis
        ys : npt.NDArray[np.float_]
            Numerical data for y-axis
        title : str
            Title of plot

        Returns
        -------
        Figure
            Figure with line plot

        """
        fig = self._make_figure(title=title)

        fig.line(x=xs, y=ys)
        fig.xaxis[0].formatter = DatetimeTickFormatter()
        fig.yaxis[0].formatter = NumeralTickFormatter(format="0.00")
        return fig

    def _make_scatterplot(
        self, xs: npt.NDArray[np.datetime64], ys: npt.NDArray[np.float_], title: str
    ) -> Figure:
        """Creates a scatter plot on given Bokeh figure, with target x and y data.
        Assumes that x data is datetime.

        Parameters
        ----------
        xs : npt.NDArray[np.datetime64]
            Datetime data for x-axis
        ys : npt.NDArray[np.float_]
            Numerical data for y-axis
        title : str
            Title of plot

        Returns
        -------
        Figure
            Figure with line plot

        """

        fig = self._make_figure(title=title)

        fig.scatter(x=xs, y=ys)
        fig.xaxis[0].formatter = DatetimeTickFormatter()
        fig.yaxis[0].formatter = NumeralTickFormatter(format="0.00")
        return fig
