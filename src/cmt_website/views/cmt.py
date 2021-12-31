import logging
from datetime import datetime, timezone

from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="home")
def home_page(request):
    raise HTTPMovedPermanently("/cmt")


@view_config(route_name="cmt", renderer="cmt_website:templates/cmt.mako")
def cmt_page(request):
    status_reader = request.registry.settings["status"]
    weather_data = request.registry.settings["weather_data"]
    telescope_status = status_reader.telescope
    dome_status = status_reader.dome
    utc = datetime.now(timezone.utc).strftime("%H:%M:%S")
    local = datetime.now().strftime("%H:%M:%S")
    date = datetime.today().strftime("%d/%m/%y")
    return {
        "weather_features": weather_data.features,
        "date": date,
        "utc": utc,
        "lst": local,
        "telescope": telescope_status,
        "dome": dome_status,
        "plots": ["temperature", "windspeed", "winddirection", "humidity", "pressure"],
    }


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
