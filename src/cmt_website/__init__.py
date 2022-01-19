from datetime import datetime, timezone
from multiprocessing import Process
from pathlib import Path
from typing import Callable
from astropy.coordinates.earth import EarthLocation

from pyramid.config import Configurator
from pyramid.router import Router

import cmt_website.plotting as plots
import cmt_website.status as status
import cmt_website.data as data


def main(global_config, **settings) -> Router:

    """This function returns a Pyramid WSGI application."""

    with Configurator(settings=settings) as config:
        config.include("pyramid_mako")
        config.include(".routes")
        config.scan()

        settings = config.get_settings()
        sqm_reader = data.make_sqm_reader(
            ip_address=settings["sqm.ip_address"], port=settings["sqm.port"]
        )
        log_path = Path(settings["weather.log_path"])
        weather_data = data.make_weatherdata(reader_path=log_path)
        telescope_reader = status.make_status_reader()
        plotter = plots.make_plotter(weather_data)
        lat = float(settings["site.latitude"])
        long = float(settings["site.longitude"])
        height = float(settings["site.height"])
        observatory_time = data.make_time(longitude=long, latitude=lat, height=height)

        config.add_settings(status=telescope_reader)
        config.add_settings(sqm=sqm_reader)
        config.add_settings(weather_data=weather_data)
        config.add_settings(plotter=plotter)
        config.add_settings(time=observatory_time)
    return config.make_wsgi_app()


def launch_as_daemon(func: Callable):
    """Launches target function as a process, assumes function has no arguments to pass in

    Parameters
    ----------
    func : Callable
        Callable function with no arguments

    """

    daemon = Process(group=None, target=func, daemon=True)
    daemon.start()
