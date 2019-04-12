import os
import sys
import json
import yaml
import urllib.request

from jinja2 import Environment, FileSystemLoader, select_autoescape

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class Interface(object):

    def __init__(self, app, app_type=None, config_path=None, config_url=None,
                 url_prefix='/api/doc', title='API doc', editor=False):

        self._app = app
        self._title = title
        self._url_prefix = url_prefix
        self._config_url = config_url
        self._config_path = config_path
        self._editor = editor

        assert self._config_url or self._config_path, 'config_url or config_path is required!'

        self._env = Environment(
            loader=FileSystemLoader(os.path.join(CURRENT_DIR, 'templates')),
            autoescape=select_autoescape(['html'])
        )

        if app_type and hasattr(self, '_{}_handler'.format(app_type)):
            getattr(self, '_{}_handler'.format(app_type))()
        else:
            self._auto_match_handler()

    @property
    def static_dir(self):
        return os.path.join(CURRENT_DIR, 'static')

    @property
    def doc_html(self):
        return self._env.get_template('doc.html').render(
            url_prefix=self._url_prefix, title=self._title, config_url=self._uri('/swagger.json')
        )

    @property
    def editor_html(self):
        print('here')
        return self._env.get_template('editor.html').render(
            url_prefix=self._url_prefix, title=self._title, config_url=self._uri('/swagger.json')
        )

    def _load_config(self, config_str):
        try:
            return json.loads(config_str)
        except ValueError:
            pass

        try:
            return yaml.load(config_str)
        except yaml.YAMLError:
            pass

        raise Exception('Invalid swagger config file format!')

    def get_config(self, host):
        if self._config_path:
            assert os.path.isfile(self._config_path)

            with open(self._config_path, 'r') as config_file:
                config = self._load_config(config_file.read())

        elif self._config_url:
            with urllib.request.urlopen(self._config_url) as config_file:
                config = self._load_config(config_file.read())

        config['host'] = host
        return config

    def _uri(self, suffix=''):
        return r'{}{}'.format(self._url_prefix, suffix)

    def _tornado_handler(self):
        from tornado.web import RequestHandler, StaticFileHandler

        interface = self

        class DocHandler(RequestHandler):
            def get(self, *args, **kwargs):
                return self.write(interface.doc_html)

        class EditorHandler(RequestHandler):
            def get(self, *args, **kwargs):
                return self.write(interface.editor_html)

        class ConfigHandler(RequestHandler):
            def get(self, *args, **kwargs):
                return self.write(interface.get_config(self.request.host))

        handlers = [
            (self._uri(), DocHandler),
            (self._uri('/swagger.json'), ConfigHandler),
            (self._uri('/(.+)'), StaticFileHandler, {'path': self.static_dir}),
        ]

        if self._editor:
            handlers.insert(1, (self._uri('/editor'), EditorHandler))

        print(handlers)
        self._app.add_handlers('.*', handlers)

    def _flask_handler(self):
        from flask import request, jsonify
        from flask.blueprints import Blueprint

        swagger_blueprint = Blueprint(
            'swagger_blueprint', __name__, url_prefix=self._url_prefix,
            static_folder=self.static_dir, static_url_path='/'
        )

        @swagger_blueprint.route(r'/')
        def swagger_blueprint_index_handler():
            return self.index_html

        @swagger_blueprint.route(r'/swagger.json')
        def swagger_blueprint_config_handler():
            return jsonify(self.get_config(request.host))

        self._app.register_blueprint(swagger_blueprint)

    def _aiohttp_handler(self):
        from aiohttp import web

        async def swagger_index_handler(request):
            return web.Response(text=self.index_html, content_type='text/html')

        async def swagger_config_handler(request):
            return web.json_response(self.get_config(request.host))

        self._app.router.add_get(self._uri(), swagger_index_handler)
        self._app.router.add_get(self._uri('/swagger.json'), swagger_config_handler)
        self._app.router.add_static(self._uri('/'), path='{}/'.format(self.static_dir))

    def _sanic_handler(self):
        from sanic import response
        from sanic.blueprints import Blueprint

        swagger_blueprint = Blueprint('swagger_blueprint', url_prefix=self._url_prefix)

        @swagger_blueprint.get('/')
        async def swagger_blueprint_index_handler(request):
            return response.html(self.index_html)

        @swagger_blueprint.get('/swagger.json')
        async def swagger_blueprint_config_handler(request):
            return response.json(self.get_config(request.host))

        swagger_blueprint.static('/', self.static_dir)
        self._app.blueprint(swagger_blueprint)

    def _quart_handler(self):
        from quart import Blueprint, request
        from quart.json import jsonify

        swagger_blueprint = Blueprint(
            'swagger_blueprint', __name__, url_prefix=self._url_prefix,
            static_url_path='', static_folder='', root_path=self.static_dir
        )

        @swagger_blueprint.route('/', methods=['GET'])
        async def swagger_blueprint_index_handler():
            return self.index_html

        @swagger_blueprint.route('/swagger.json', methods=['GET'])
        async def swagger_blueprint_config_handler():
            return jsonify(self.get_config(request.host))

        self._app.register_blueprint(blueprint=swagger_blueprint, url_prefix=self._url_prefix)

    def _auto_match_handler(self):
        try:
            import tornado.web
            if isinstance(self._app, tornado.web.Application):
                return self._tornado_handler()
        except ImportError:
            pass

        try:
            import flask
            if isinstance(self._app, flask.Flask):
                return self._flask_handler()
        except ImportError:
            pass

        if sys.version_info >= (3, 0):
            try:
                import sanic
                if isinstance(self._app, sanic.Sanic):
                    return self._sanic_handler()
            except ImportError:
                pass

            try:
                import aiohttp.web
                if isinstance(self._app, aiohttp.web.Application):
                    return self._aiohttp_handler()
            except ImportError:
                pass

            try:
                import quart
                if isinstance(self._app, quart.Quart):
                    return self._quart_handler()
            except ImportError:
                pass

        raise Exception('No match application isinstance type!')
