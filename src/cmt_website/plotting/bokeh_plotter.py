from datetime import datetime, timezone
from typing import Literal, List
from math import ceil, radians
import numpy as np
import numpy.typing as npt
from attr import define, field
from bokeh.embed import json_item
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, HoverTool
from bokeh.plotting import Figure, figure
from bokeh.palettes import RdBu10
from cmt_website.plotting.plot_interface import PlottingInterface
from cmt_website.data.weather.data import WeatherData
from cmt_website.data.weather.feature import WeatherFeature
import pandas as pd


@define
class BokehPlotter(PlottingInterface):
    """Plotting object, has necessary data inserted and creates JSON-readable JSON
    scripts that replaces target divs"""

    weather: WeatherData = field()

    @property
    def temperature(self):
        """Plot of temperature data, replaces div with 'temperature' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.temperature,
            title="Weather Station Temperature over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Temperature [\u00B0 C]"
        return json_item(plot, "temperature")

    @property
    def wind_rose(self):
        """Plot of wind speed data, replaces div with 'wind-speed' ID"""
        plot = self._make_wind_rose(
            self.weather.wind_direction.last(3, "hour"),
            self.weather.wind_speed.last(3, "hour"),
            "Wind Rose",
        )
        return json_item(plot, "wind_rose")

    @property
    def humidity(self):
        """Plot of humidity data, replaces div with 'humidity' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.humidity,
            title="Weather Station Humidity over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Humidity [%]"
        return json_item(plot, "humidity")

    @property
    def pressure(self):
        """Plot of pressure data, replaces div with 'pressure' ID"""
        plot = self._plot_from_weatherfeature(
            feature=self.weather.pressure,
            title="Weather Station Pressure over Time",
            type="line",
        )
        plot.yaxis[0].axis_label = "Pressure [mbar]"
        return json_item(plot, "pressure")

    @property
    def sqm(self):
        """Plot of SQM data, replaces div with 'sqm' ID"""
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

    @staticmethod
    def clamp(value: float, minimum: float, maximum: float):
        return minimum if value < minimum else maximum if value > maximum else value

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

    def _make_wind_rose(
        self,
        wind_direction: pd.Series,
        wind_speed: pd.Series,
        title: str,
        radius: int = 400,
        padding: int = 60,
        inner_radius: int = 30,
        grid_circles: int = 4,
        angle_width: float = 0.05,
        max_wind_speed: float = 100,
    ):

        """Makes a wind rose plot from given wind speed/direction

        :param wind_direction: Direction of the wind as a timeseries
        :param wind_speed: Speed of the wind as a timeseries
        :param title: Title of the plot
        :param radius: Radius the plot will have (in pixels)
        :param padding: Padding from outside of the plot to the edge of window
        :param inner_radius: Inner circle of plot, for aesthetics
        :param grid_circles: How many circles comprise the polar plot's grid
        :param angle_width: Width of the data wedges, in radians
        :param max_wind_speed: Maximum wind speed allowed
        :returns: Wind rose figure plot for display

        """

        # Combine and rename
        df = pd.concat([wind_direction, wind_speed], axis=1, join="inner")
        df = df.rename(
            columns={"Wind Direction": "wind_dir", "Wind Speed": "wind_speed"}
        )
        # Resample and take average so we have fewer datapoints to work with, but theyre
        # more accurate
        df = df.resample("30T").mean().dropna()
        # Set up the wedge display settings
        df["start_angle"] = np.radians(df["wind_dir"]) - angle_width
        df["end_angle"] = np.radians(df["wind_dir"]) + angle_width
        # Hover over text
        df["local_time"] = df.index.strftime("%Y %m %d, %r")
        # Set up colour based on input palette
        df["colour"] = df["wind_speed"].apply(
            self.wind_speed_to_colour,
            maximum_wind_speed=max_wind_speed,
            colours=list(RdBu10),
        )
        # Calculate fraction of wind speed from maximum, so we can have wedges
        # of proper length
        df["length"] = df["wind_speed"].apply(
            lambda x: self.clamp(x / max_wind_speed, 0, 1) * (radius - inner_radius)
            + inner_radius,
        )
        fig = figure(
            max_width=750,
            max_height=750,
            x_range=(-radius - padding, radius + padding),
            y_range=(-radius - padding, radius + padding),
            outline_line_color="black",
            x_axis_type=None,
            y_axis_type=None,
            title=title,
            min_border=0,
            toolbar_location=None,
        )

        # turn off x/y grids
        fig.xgrid.grid_line_color = None
        fig.ygrid.grid_line_color = None

        # Direction labelling/Directional axes
        labels = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]
        dir_rads = np.array(
            [((np.pi / 4) * i) + radians(90) for i in range(0, len(labels) + 1)]
        )
        fig.annular_wedge(
            x=0,
            y=0,
            inner_radius=inner_radius,
            outer_radius=radius,
            start_angle=radians(90),
            end_angle=dir_rads,
            line_color="black",
            fill_alpha=0.0,
            line_alpha=0.6,
        )
        # Only getting until end of list, not final number as there's one extra for visual
        # Purposes (hence the -1)
        label_xs = np.cos(dir_rads[:-1]) * (radius + (padding / 2))
        label_ys = np.sin(dir_rads[:-1]) * (radius + (padding / 2))
        fig.text(
            label_xs,
            label_ys,
            labels,
            text_font_size="12px",
            text_align="center",
            text_baseline="middle",
        )

        # Make a grid from circles
        circle_grid_radii = [
            x
            for x in range(
                inner_radius, radius, ceil((radius - inner_radius) / grid_circles)
            )
        ]
        fig.circle(
            x=0,
            y=0,
            radius=circle_grid_radii,
            fill_color=None,
            line_color="black",
            line_alpha=0.6,
        )

        # Display Data
        data = fig.wedge(
            x=0,
            y=0,
            radius="length",
            color="colour",
            start_angle="start_angle",
            end_angle="end_angle",
            source=df,
            alpha=0.8,
        )

        # Setup for the hover text, based on the dataframes column names
        # and the data renderer
        fig.add_tools(
            HoverTool(tooltips="@local_time: @wind_speed km/h", renderers=[data])
        )

        return fig

    @staticmethod
    def wind_speed_to_colour(
        wind_speed: float, maximum_wind_speed: float, colours: List[str]
    ):

        """Converts the wind speed to a colour based on maximum wind speed

        :param wind_speed: wind speed value
        :param maximum_wind_speed: The maximum allowed wind speed
        :param colours: List of hex value colours to convert to
        :returns: Colour mapping of the wind speed

        """
        fraction_of_max = wind_speed / maximum_wind_speed
        # -1 for the len of colours since we start counting at 0
        # and don't want an off-by-one error
        scaled_to_colour_size = fraction_of_max * (len(colours) - 1)
        clamped = int(
            BokehPlotter.clamp(
                scaled_to_colour_size, minimum=0, maximum=len(colours) - 1
            )
        )
        return colours[clamped]
