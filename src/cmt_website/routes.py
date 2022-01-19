from pyramid.config import Configurator


def includeme(config: Configurator):
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("cmt", "/cmt")
    config.add_route("plot", "/plot/{plot_name}")
    config.add_route("time", "/data/time")
    config.add_route("date", "/data/date")
