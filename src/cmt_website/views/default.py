from pyramid.view import view_config


@view_config(route_name="home", renderer="cmt_website:templates/default.mako")
def home_page(request):
    return {"project": "cmt_website"}
