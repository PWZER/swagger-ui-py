from . import utils


def api_doc(app, config_path, url_prefix='/api/doc', title='API doc'):
    from flask import request
    from flask.blueprints import Blueprint

    swagger_blueprint = Blueprint('swagger_blueprint', __name__, url_prefix=url_prefix,
                                  static_folder=utils.get_static_dir(), static_url_path='/')

    @swagger_blueprint.route(r'/')
    def swagger_blueprint_index_handler():
        # swagger_url_prefix = request.url[:-1] if request.url.endswith('/') else request.url
        return utils.render_html(url_prefix=url_prefix, title=title)

    @swagger_blueprint.route(r'/swagger.json')
    def swagger_blueprint_config_handler():
        return utils.load_swagger_config(config_path=config_path, host=request.host)

    app.register_blueprint(swagger_blueprint)
