import logging
from datetime import datetime, timezone

from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="home")
def home_page(request):
    raise HTTPFound("/cmt")


@view_config(route_name="cmt", renderer="cmt_website:templates/cmt.mako")
def cmt_page(request):
    utc = datetime.now(timezone.utc).strftime("%H:%M:%S")
    local = datetime.now().strftime("%H:%M:%S")
    date = datetime.today().strftime("%d/%m/%y")
    return {
        "temperature": -18.1,
        "humidity": 0,
        "wind_speed": 10,
        "date": date,
        "utc": utc,
        "lst": local,
        "telescope_status": "Not Bacon",
        "dome_status": "More bacon",
        "telescope_altitude": "50:12:06",
        "telescope_azimuth": "201:26:55",
        "telescope_ra": "18:59:13.8",
        "telescope_ha": "00:55:32.6",
        "telescope_dec": "12:41:45",
        "dome_azimuth": "180:0",
        "dome_shutter": "ANGRY",
        "camera_filter": "Potato",
        "camera_focus": 0.0,
        "camera_temperature": -10.0,
    }


@view_config(route_name="weather", renderer="cmt_website:templates/weather.mako")
def weather_page(request):
    weather_data = request.registry.settings["weather_data"]
    return {"weather_data": weather_data}


@view_config(route_name="sqm", renderer="cmt_website:templates/sqm.mako")
def sqm_page(request: Request):
    sqm = request.registry.settings["sqm"]
    try:
        _, _, _, _, _, sky_brightness = sqm.read_photometer()
    except OSError as e:
        logging.error(f"Unable to communicate with SQM device, received error {e}")
        return {"sky_brightness": "ERROR"}
    return {"sky_brightness": sky_brightness}


@view_config(
    route_name="current_image", renderer="cmt_website:templates/current_image.mako"
)
def current_image(request):
    return {}
