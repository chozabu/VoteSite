from pyramid.config import Configurator

from pyramid.request import Request
from pyramid.request import Response

'''def request_factory(environ):
    request = Request(environ)
    if request.is_xhr:
        request.response = Response()
        request.response.headerlist = []
        request.response.headerlist.extend(
            (
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'application/json')
            )
        )
    return request'''

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)

from pyramid.events import NewRequest

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('pplevels', 'pplevels', cache_max_age=3600)
    config.add_static_view('thumbs', 'thumbs', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('store_mp3_view', '/store_mp3_view')
    config.add_route('get_points', '/get_points')
    config.add_route('join_points', '/join_points')
    config.add_route('get_connections', '/get_connections')
    config.add_route('get_all_connections', '/get_all_connections')
    config.add_route('complex_query_levels', '/complex_query_levels')
    config.add_route('add_point', '/add_point')
    config.add_route('add_vote', '/add_vote')
    config.add_route('query_points', '/query_points')
    config.add_route('get_point', '/get_point')
    config.add_route('get_level', '/get_level')
    config.add_route('get_tags', '/get_tags')
    config.add_route('login', '/login')
    config.add_route('new_user', '/new_user')
    config.add_route('uploadCrash', '/uploadCrash')
    config.add_route('crashLogs', '/crashLogs')
    config.scan()
    #config.set_request_factory(request_factory)
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    return config.make_wsgi_app()
