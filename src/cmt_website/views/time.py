from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="time", renderer="json")
def time_json(request: Request):
    time = request.registry.settings["time"]
    return {"UTC": time.utc, time.timezone: time.local, "LST": time.lst}


@view_config(route_name="date", renderer="json")
def date_json(request: Request):
    time = request.registry.settings["time"]
    return {"date": time.date}
