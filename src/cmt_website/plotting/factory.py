from cmt_website.plotting.bokeh_plotter import BokehPlotter
from cmt_website.plotting.plot_interface import PlottingInterface
from cmt_website.data.weather.data import WeatherData

# basic factory, since it's just two lines should probably remove
def make_plotter(weather_data: WeatherData) -> PlottingInterface:
    plotter = BokehPlotter(weather=weather_data)
    return plotter
