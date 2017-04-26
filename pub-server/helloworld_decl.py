"""
Pyramid Web Framework first application, from http://trypyramid.com

Declarative Configuration version, using configuration decorations for multi-file applications.
Visit http://localhost:8080/hello/world
"""

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name="hello", request_method="GET")
def hello_world(request):
    return Response('Hello %(name)s! (scan)' % request.matchdict)

if __name__ == '__main__':
    config = Configurator()
    config.add_route("hello", "/hello/{name}")
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()