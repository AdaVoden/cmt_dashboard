import logging

from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="home", renderer="cmt_website:templates/cmt.mako")
@view_config(route_name="cmt", renderer="cmt_website:templates/cmt.mako")
def cmt_page(request: Request):
    status_reader = request.registry.settings["status"]
    weather_data = request.registry.settings["weather_data"]
    weather_data.update()
    time = request.registry.settings["time"]
    telescope_status = status_reader.telescope
    dome_status = status_reader.dome

    return {
        "weather_features": weather_data.features,
        "date": time.date,
        "utc": time.utc,
        "lst": time.lst,
        "telescope": telescope_status,
        "dome": dome_status,
        "plots": ["temperature", "windspeed", "winddirection", "humidity", "pressure"],
    }


@view_config(route_name="plot", renderer="json")
def plot_json(request: Request):
    plotter = request.registry.settings["plotter"]
    plotter.weather.update()
    plot_type = request.matchdict["plot_name"]
    if plot_type == "temperature":
        return plotter.temperature
    if plot_type == "windspeed":
        return plotter.wind_speed
    if plot_type == "winddirection":
        return plotter.wind_direction
    if plot_type == "humidity":
        return plotter.humidity
    if plot_type == "pressure":
        return plotter.pressure
    if plot_type == "sqm":
        return plotter.sqm
    return {}


# @view_config(route_name="weather", renderer="cmt_website:templates/weather.mako")
# def weather_page(request):
#     weather_data = request.registry.settings["weather_data"]
#     return {"weather_data": weather_data}


# @view_config(route_name="sqm", renderer="cmt_website:templates/sqm.mako")
# def sqm_page(request: Request):
#     sqm = request.registry.settings["sqm"]
#     try:
#         _, _, _, _, _, sky_brightness = sqm.read_photometer()
#     except OSError as e:
#         logging.error(f"Unable to communicate with SQM device, received error {e}")
#         return {"sky_brightness": "ERROR"}
#     return {"sky_brightness": sky_brightness}
