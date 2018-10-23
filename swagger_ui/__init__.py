import sys

if sys.version_info >= (3, 0):
    from .sanic_swagger_ui import api_doc as sanic_api_doc

from .flask_swagger_ui import api_doc as flask_api_doc
from .tornado_swagger_ui import api_doc as tornado_api_doc
