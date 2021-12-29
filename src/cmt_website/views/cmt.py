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
    status_reader = request.registry.settings["status"]
    weather_data = request.register.settings["weather_data"]
    telescope_status = status_reader.read_telescope()
    dome_status = status_reader.read_dome()
    utc = datetime.now(timezone.utc).strftime("%H:%M:%S")
    local = datetime.now().strftime("%H:%M:%S")
    date = datetime.today().strftime("%d/%m/%y")
    return {
        "temperature": weather_data.temperature.current,
        "humidity": weather_data.humidity.current,
        "wind_speed": weather_data.wind_speed.current,
        "date": date,
        "utc": utc,
        "lst": local,
        "telescope_status": telescope_status.status.name,
        "dome_status": dome_status.status.name,
        "telescope_altitude": telescope_status.altitude.dms,
        "telescope_azimuth": telescope_status.azimuth.dms,
        "telescope_ra": telescope_status.ra.hms,
        "telescope_ha": telescope_status.ha.hms,
        "telescope_dec": telescope_status.dec.hms,
        "dome_azimuth": dome_status.azimuth.dms,
        "dome_shutter": dome_status.shutterstatus.name,
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
