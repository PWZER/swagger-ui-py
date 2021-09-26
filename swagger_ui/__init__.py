import sys

from swagger_ui import core
from swagger_ui.handlers import supported_list


def api_doc(app, **kwargs):
    doc = core.ApplicationDocument(app, **kwargs)

    handler = doc.match_handler()

    if not handler:
        raise Exception('No match application isinstance type!')

    if not callable(handler):
        raise Exception('handler is callable required!')

    return handler(doc)


def create_api_doc(app_type):
    def _api_doc(app, **kwargs):
        kwargs['app_type'] = app_type
        return api_doc(app, **kwargs)
    return _api_doc


for name in supported_list:
    setattr(sys.modules[__name__], '{}_api_doc'.format(name), create_api_doc(name))
