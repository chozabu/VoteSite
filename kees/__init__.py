from pyramid.config import Configurator


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
    config.add_route('uploadLevel', '/uploadLevel')
    config.add_route('query_levels', '/query_levels')
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
    return config.make_wsgi_app()
