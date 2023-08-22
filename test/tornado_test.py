from multiprocessing import Process

import pytest
from common import kwargs_list
from common import mode_list
from common import send_requests


def server_process(port, mode, **kwargs):
    import tornado.ioloop
    import tornado.web

    class HelloWorldHandler(tornado.web.RequestHandler):
        def get(self, *args, **kwargs):
            return self.write('Hello World!!!')

    app = tornado.web.Application([
        (r'/hello/world', HelloWorldHandler),
    ])

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import tornado_api_doc
        tornado_api_doc(app, **kwargs)

    app.listen(address='localhost', port=port)
    tornado.ioloop.IOLoop.current().start()


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_tornado(port, mode, kwargs):
    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
