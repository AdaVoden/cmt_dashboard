from pyramid.config import Configurator
from pyramid.router import Router

import cmt_website.sqm as sqm


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
        config.add_settings(sqm=sqm_reader)
    return config.make_wsgi_app()
