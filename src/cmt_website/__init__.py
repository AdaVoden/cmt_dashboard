from pathlib import Path

from pyramid.config import Configurator
from pyramid.router import Router

import cmt_website.plotting as plots
import cmt_website.sqm as sqm
import cmt_website.status as status
import cmt_website.weather as weather


def main(global_config, **settings) -> Router:

    """This function returns a Pyramid WSGI application."""

    with Configurator(settings=settings) as config:
        config.include("pyramid_mako")
        config.include(".routes")
        config.scan()
        settings = config.get_settings()
        sqm_reader = sqm.make_sqm_reader(
            ip_address=settings["sqm.ip_address"], port=settings["sqm.port"]
        )
        log_path = Path(settings["weather.log_path"])
        weather_data = weather.make_watched_weatherdata(reader_path=log_path)
        telescope_reader = status.make_status_reader()
        plotter = plots.make_plotter(weather_data)
        config.add_settings(status=telescope_reader)
        config.add_settings(sqm=sqm_reader)
        config.add_settings(weather_data=weather_data)
        config.add_settings(plotter=plotter)
    return config.make_wsgi_app()
