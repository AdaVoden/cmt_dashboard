from cmt_website.plotting.bokeh_plotter import BokehPlotter
from cmt_website.plotting.plot_interface import PlottingInterface
from cmt_website.weather.data import WeatherData


def make_plotter(weather_data: WeatherData) -> PlottingInterface:
    plotter = BokehPlotter(weather=weather_data)
    return plotter
