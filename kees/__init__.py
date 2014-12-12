from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('pplevels', 'pplevels', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('store_mp3_view', '/store_mp3_view')
    config.add_route('uploadLevel', '/uploadLevel')
    config.add_route('query_levels', '/query_levels')
    config.add_route('login', '/login')
    config.add_route('new_user', '/new_user')
    config.scan()
    return config.make_wsgi_app()
