from datetime import datetime, timezone

from cmt_website.pysqm_reader import SQMLE
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

SQM_READER = SQMLE(_device_address="136.159.57.187")


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
    return {
        "current_temp": -18.1,
        "max_temp": -9.1,
        "min_temp": -19.3,
        "current_pressure": 861.8,
        "max_pressure": 863.3,
        "min_pressure": 857.4,
        "current_humidity": 69,
        "max_humidity": 77,
        "min_humidity": 59,
        "current_wind_speed": 14,
        "max_wind_speed": 32,
        "min_wind_speed": 0,
        "wind_direction": "NE",
    }


@view_config(route_name="sqm", renderer="cmt_website:templates/sqm.mako")
def sqm_page(request):
    return {"sky_brightness": 15}


@view_config(
    route_name="current_image", renderer="cmt_website:templates/current_image.mako"
)
def current_image(request):
    return {}
