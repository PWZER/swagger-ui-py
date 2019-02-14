import sys

if sys.version_info >= (3, 0):
    from .py3.sanic_swagger_ui import api_doc as sanic_api_doc
    from .py3.quart_swagger_ui import api_doc as quart_api_doc
    from .py3.aiohttp_swagger_ui import api_doc as aiohttp_api_doc

from .flask_swagger_ui import api_doc as flask_api_doc
from .tornado_swagger_ui import api_doc as tornado_api_doc
