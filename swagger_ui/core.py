import copy
import importlib
import re
import urllib.request
from distutils.version import StrictVersion
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from swagger_ui.utils import SWAGGER_UI_PY_ROOT, _load_config
from swagger_ui.handlers import supported_list


_DefaultSwaggerUIBundleParameters = {
    "dom_id": "\"#swagger-ui\"",
    "deepLinking": "true",
    "displayRequestDuration": "true",
    "layout": "\"StandaloneLayout\"",
    "plugins": "[SwaggerUIBundle.plugins.DownloadUrl]",
    "presets": "[SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset]",
}


class ApplicationDocument(object):

    def __init__(self,
                 app,
                 app_type=None,
                 config=None,
                 config_path=None,
                 config_url=None,
                 config_spec=None,
                 url_prefix=r'/api/doc',
                 title='API doc',
                 editor=False,
                 parameters={},
                 **extra_config):
        self.app = app
        self.app_type = app_type
        self.title = title
        self.url_prefix = url_prefix.rstrip('/')
        self.editor = editor
        self.extra_config = extra_config

        self.config = config
        self.config_url = config_url
        self.config_path = config_path
        self.config_spec = config_spec
        assert self.config or self.config_url or self.config_path or self.config_spec, \
            'One of arguments "config", "config_path", "config_url" or "config_spec" is required!'

        # parameters
        self.parameters = copy.deepcopy(_DefaultSwaggerUIBundleParameters)
        if parameters:
            self.parameters.update(parameters)
        self.parameters["url"] = "\"{}\"".format(self.swagger_json_uri_absolute)

        self.env = Environment(
            loader=FileSystemLoader(
                str(SWAGGER_UI_PY_ROOT.joinpath('templates'))),
            autoescape=select_autoescape(['html']),
        )

    @property
    def static_dir(self):
        return str(SWAGGER_UI_PY_ROOT.joinpath('static'))

    @property
    def doc_html(self):
        return self.env.get_template('doc.html').render(
            url_prefix=self.url_prefix,
            title=self.title,
            config_url=self.swagger_json_uri_absolute,
            parameters=self.parameters,
        )

    @property
    def editor_html(self):
        return self.env.get_template('editor.html').render(
            url_prefix=self.url_prefix,
            title=self.title,
            config_url=self.swagger_json_uri_absolute,
            parameters=self.parameters,
        )

    def uri(self, suffix=''):
        return r'{}{}'.format(self.url_prefix, suffix)

    @property
    def static_uri_relative(self):
        return r'/static'

    @property
    def static_uri_absolute(self):
        return self.uri(self.static_uri_relative)

    @property
    def swagger_json_uri_relative(self):
        return r'/swagger.json'

    @property
    def swagger_json_uri_absolute(self):
        return self.uri(self.swagger_json_uri_relative)

    def root_uri_relative(self, slashes=False):
        return r'/' if slashes else r''

    def root_uri_absolute(self, slashes=False):
        return self.uri(self.root_uri_relative(slashes))

    def editor_uri_relative(self, slashes=False):
        return r'/editor/' if slashes else r'/editor'

    def editor_uri_absolute(self, slashes=False):
        return self.uri(self.editor_uri_relative(slashes))

    def get_config(self, host):
        if self.config:
            config = self.config
        elif self.config_path:
            assert Path(self.config_path).is_file()

            with open(self.config_path, 'rb') as config_file:
                config = _load_config(config_file.read())
        elif self.config_url:
            with urllib.request.urlopen(self.config_url) as config_file:
                config = _load_config(config_file.read())
        elif self.config_spec:
            config = _load_config(self.config_spec)

        version = config.get('openapi', '2.0.0')
        if StrictVersion(version) >= StrictVersion('3.0.0'):
            for server in config['servers']:
                server['url'] = re.sub(r'//[a-z0-9\-\.:]+/?',
                                       '//{}/'.format(host), server['url'])
        elif 'host' not in config:
            config['host'] = host
        return config

    def match_handler(self):

        def match(name):
            mod = importlib.import_module(
                'swagger_ui.handlers.{}'.format(name))
            return hasattr(mod, 'match') and mod.match(self)

        if self.app_type:
            return match(self.app_type)

        for name in supported_list:
            handler = match(name)
            if handler:
                return handler
        return None
