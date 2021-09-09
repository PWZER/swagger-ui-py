import json
import re
import urllib.request
from distutils.version import StrictVersion
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

CURRENT_DIR = Path(__file__).resolve().parent


class Interface(object):

    def __init__(self, app, app_type=None, config=None, config_path=None, config_url=None,
                 config_spec=None, url_prefix='/api/doc', title='API doc', editor=False):

        self._app = app
        self._title = title
        self._url_prefix = url_prefix.rstrip('/')
        self._editor = editor

        self._config = config
        self._config_url = config_url
        self._config_path = config_path
        self._config_spec = config_spec
        assert self._config or self._config_url or self._config_path or self._config_spec, \
            'One of arguments "config", "config_path", "config_url" or "config_spec" is required!'

        self._env = Environment(
            loader=FileSystemLoader(str(CURRENT_DIR.joinpath('templates'))),
            autoescape=select_autoescape(['html'])
        )

        if app_type and hasattr(self, '_{}_handler'.format(app_type)):
            getattr(self, '_{}_handler'.format(app_type))()
        else:
            self._auto_match_handler()

    @property
    def static_dir(self):
        return str(CURRENT_DIR.joinpath('static'))

    @property
    def doc_html(self):
        return self._env.get_template('doc.html').render(
            url_prefix=self._url_prefix, title=self._title, config_url=self._uri('/swagger.json')
        )

    @property
    def editor_html(self):
        return self._env.get_template('editor.html').render(
            url_prefix=self._url_prefix, title=self._title, config_url=self._uri('/swagger.json')
        )

    def _load_config(self, config_str):
        try:
            return json.loads(config_str)
        except ValueError:
            pass

        try:
            return yaml.load(config_str, Loader=yaml.FullLoader)
        except yaml.YAMLError:
            pass

        raise Exception('Invalid swagger config file format!')

    def get_config(self, host):
        if self._config:
            config = self._config
        elif self._config_path:
            assert Path(self._config_path).is_file()

            with open(self._config_path, 'rb') as config_file:
                config = self._load_config(config_file.read())
        elif self._config_url:
            with urllib.request.urlopen(self._config_url) as config_file:
                config = self._load_config(config_file.read())
        elif self._config_spec:
            config = self._load_config(self._config_spec)

        if StrictVersion(config.get('openapi', '2.0.0')) >= StrictVersion('3.0.0'):
            for server in config['servers']:
                server['url'] = re.sub(r'//[a-z0-9\-\.:]+/?', '//{}/'.format(host), server['url'])
        elif 'host' not in config:
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
            (self._uri('/'), DocHandler),
            (self._uri('/swagger.json'), ConfigHandler),
            (self._uri('/(.+)'), StaticFileHandler, {'path': self.static_dir}),
        ]

        if self._editor:
            handlers.insert(1, (self._uri('/editor'), EditorHandler))

        self._app.add_handlers('.*', handlers)

    def _flask_handler(self):
        from flask import request, jsonify
        from flask.blueprints import Blueprint

        swagger_blueprint = Blueprint(
            'swagger_blueprint', __name__, url_prefix=self._url_prefix,
            static_folder=self.static_dir, static_url_path='/'
        )

        @swagger_blueprint.route(r'')
        def swagger_blueprint_doc_handler():
            return self.doc_html

        @swagger_blueprint.route(r'/')
        def swagger_blueprint_doc_v2_handler():
            return self.doc_html

        @swagger_blueprint.route(r'/swagger.json')
        def swagger_blueprint_config_handler():
            return jsonify(self.get_config(request.host))

        if self._editor:
            @swagger_blueprint.route(r'/editor')
            def swagger_blueprint_editor_handler():
                return self.editor_html

        self._app.register_blueprint(swagger_blueprint)

    def _aiohttp_handler(self):
        from aiohttp import web

        async def swagger_doc_handler(request):
            return web.Response(text=self.doc_html, content_type='text/html')

        async def swagger_editor_handler(request):
            return web.Response(text=self.editor_html, content_type='text/html')

        async def swagger_config_handler(request):
            return web.json_response(self.get_config(request.host))

        self._app.router.add_get(self._uri(), swagger_doc_handler)
        self._app.router.add_get(self._uri('/'), swagger_doc_handler)

        if self._editor:
            self._app.router.add_get(self._uri('/editor'), swagger_editor_handler)

        self._app.router.add_get(self._uri('/swagger.json'), swagger_config_handler)
        self._app.router.add_static(self._uri('/'), path='{}/'.format(self.static_dir))

    def _bottle_handler(self):
        from bottle import static_file, request

        @self._app.get(self._uri())
        @self._app.get(self._uri(r'/'))
        def index():
            return self.doc_html

        @self._app.get(self._uri(r'/swagger.json'))
        def config_handler():
            return self.get_config(request.urlparts.netloc)

        @self._app.get(self._uri(r'/<filepath>'))
        def java_script_file(filepath):
            return static_file(filepath, root=self.static_dir)

        if self._editor:
            @self._app.get(self._uri('/editor'))
            def editor():
                return self.editor_html

    def _sanic_handler(self):
        from sanic import response
        from sanic.blueprints import Blueprint

        swagger_blueprint = Blueprint('swagger_blueprint', url_prefix=self._url_prefix)

        @swagger_blueprint.get('/')
        async def swagger_blueprint_doc_handler(request):
            return response.html(self.doc_html)

        if self._editor:
            @swagger_blueprint.get('/editor')
            async def swagger_blueprint_editor_handler(request):
                return response.html(self.editor_html)

        @swagger_blueprint.get('/swagger.json')
        async def swagger_blueprint_config_handler(request):
            return response.json(self.get_config(request.host))

        swagger_blueprint.static('/', str(self.static_dir))
        self._app.blueprint(swagger_blueprint)

    def _quart_handler(self):
        from quart import Blueprint, request
        from quart.json import jsonify

        swagger_blueprint = Blueprint(
            'swagger_blueprint', __name__, url_prefix=self._url_prefix,
            static_url_path='', static_folder='', root_path=self.static_dir
        )

        @swagger_blueprint.route('/', methods=['GET'])
        async def swagger_blueprint_doc_handler():
            return self.doc_html

        if self._editor:
            @swagger_blueprint.route('/editor', methods=['GET'])
            async def swagger_blueprint_editor_handler():
                return self.editor_html

        @swagger_blueprint.route('/swagger.json', methods=['GET'])
        async def swagger_blueprint_config_handler():
            return jsonify(self.get_config(request.host))

        self._app.register_blueprint(blueprint=swagger_blueprint, url_prefix=self._url_prefix)

    def _falcon_handler(self, use_async):
        import json
        interface = self

        class Handler(object):
            async def on_get_async(self, req, resp):
                self.on_get(req, resp)

        class SwaggerDocHandler(Handler):
            def on_get(self, req, resp):
                resp.content_type = 'text/html'
                resp.body = interface.doc_html

        class SwaggerEditorHandler(Handler):
            def on_get(self, req, resp):
                resp.content_type = 'text/html'
                resp.body = interface.editor_html

        class SwaggerConfigHandler(Handler):
            def on_get(self, req, resp):
                resp.content_type = 'application/json'
                resp.body = json.dumps(interface.get_config(f'{req.host}:{req.port}'))

        suffix = 'async' if use_async else None
        self._app.add_route(self._uri('/'), SwaggerDocHandler(), suffix=suffix)

        if self._editor:
            self._app.add_route(self._uri('/editor'), SwaggerEditorHandler(), suffix=suffix)

        self._app.add_route(self._uri('/swagger.json'), SwaggerConfigHandler(), suffix=suffix)
        self._app.add_static_route(prefix=self._uri(
            '/'), directory='{}/'.format(self.static_dir), downloadable=True)

    def _starlette_handler(self):
        from starlette.responses import HTMLResponse, JSONResponse
        from starlette.staticfiles import StaticFiles

        async def swagger_doc_handler(request):
            return HTMLResponse(content=self.doc_html, media_type='text/html')

        async def swagger_editor_handler(request):
            return JSONResponse(content=self.editor_html, media_type='text/html')

        async def swagger_config_handler(request):
            host = '{}:{}'.format(request.url.hostname, request.url.port)
            return JSONResponse(self.get_config(host))

        self._app.router.add_route(self._uri(''), swagger_doc_handler, ['get'], 'swagger-ui')
        self._app.router.add_route(self._uri('/'), swagger_doc_handler, ['get'], 'swagger-ui')

        if self._editor:
            self._app.router.add_route(
                self._uri('/editor'), swagger_editor_handler, ['get'], 'swagger-editor')

        self._app.router.add_route(self._uri('/swagger.json'),
                                   swagger_config_handler, ['get'], 'swagger-config')
        self._app.router.mount(self._uri('/'),
                               app=StaticFiles(directory='{}/'.format(self.static_dir)),
                               name='swagger-static-files')

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

        try:
            import starlette.applications
            if isinstance(self._app, starlette.applications.Starlette):
                return self._starlette_handler()
        except ImportError:
            pass

        try:
            import falcon
            from distutils.version import StrictVersion

            if StrictVersion(falcon.__version__) >= StrictVersion('3.0.0'):
                import falcon.asgi
                if isinstance(self._app, falcon.asgi.App):
                    return self._falcon_handler(use_async=True)
                elif isinstance(self._app, falcon.App):
                    return self._falcon_handler(use_async=False)
            else:
                if isinstance(self._app, falcon.API):
                    return self._falcon_handler(use_async=False)
        except ImportError as ex:
            pass

        try:
            from bottle import Bottle
            if isinstance(self._app, Bottle):
                return self._bottle_handler()
        except ImportError:
            pass

        raise Exception('No match application isinstance type!')
