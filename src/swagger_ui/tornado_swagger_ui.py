from . import utils


def api_doc(app, config_path, url_prefix=r'/api/doc', title='API doc'):
    from tornado.web import RequestHandler, StaticFileHandler

    class SwaggerIndexHandler(RequestHandler):

        def get(self, *args, **kwargs):
            return self.write(utils.render_html(url_prefix=url_prefix, title=title))

    class SwaggerConfigHandler(RequestHandler):

        def get(self, *args, **kwargs):
            return self.write(utils.load_swagger_config(config_path=config_path,
                                                        host=self.request.host))

    handlers = [(url_prefix, SwaggerIndexHandler),
                (r'%s/swagger.json' % url_prefix, SwaggerConfigHandler),
                (r'%s/(.+)' % url_prefix, StaticFileHandler, {'path': utils.get_static_dir()})]
    app.add_handlers('.*', handlers)
