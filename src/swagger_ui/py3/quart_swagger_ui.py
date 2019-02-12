from .. import utils


def api_doc(app, config_path, url_prefix='/api/doc', title='API doc'):
    from quart import Blueprint, request

    swagger_blueprint = Blueprint('swagger_blueprint', __name__, url_prefix=url_prefix,
                                  static_url_path='', static_folder='',
                                  root_path=utils.get_static_dir())

    @swagger_blueprint.route('/', methods=['GET'])
    async def swagger_blueprint_index_handler():
        return utils.render_html(url_prefix=url_prefix, title=title)

    @swagger_blueprint.route('/swagger.json', methods=['GET'])
    async def swagger_blueprint_config_handler():
        return utils.load_swagger_config(config_path=config_path, host=request.host)

    app.register_blueprint(blueprint=swagger_blueprint, url_prefix=url_prefix)
