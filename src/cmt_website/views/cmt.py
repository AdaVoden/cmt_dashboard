from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="home", renderer="cmt_website:templates/cmt.mako")
@view_config(route_name="cmt", renderer="cmt_website:templates/cmt.mako")
def cmt_page(request: Request):
    status_reader = request.registry.settings["status"]
    weather_data = request.registry.settings["weather_data"]
    weather_data.update()
    time = request.registry.settings["time"]
    return {
        "weather_features": weather_data.features,
        "observatory_time": time,
        "status": status_reader,
        "plots": ["temperature", "humidity", "pressure"],
    }


@view_config(route_name="plot", renderer="json")
def plot_json(request: Request):
    plotter = request.registry.settings["plotter"]
    plotter.weather.update()
    plot_type = request.matchdict["plot_name"]
    if plot_type == "temperature":
        return plotter.temperature
    if plot_type == "wind_rose":
        return plotter.wind_rose
    if plot_type == "humidity":
        return plotter.humidity
    if plot_type == "pressure":
        return plotter.pressure
    if plot_type == "sqm":
        return plotter.sqm
    return {}
