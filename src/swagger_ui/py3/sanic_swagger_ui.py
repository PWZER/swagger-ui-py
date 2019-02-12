from .. import utils


def api_doc(app, config_path, url_prefix='/api/doc', title='API doc'):
    from sanic import response
    from sanic.blueprints import Blueprint

    swagger_blueprint = Blueprint('swagger_blueprint', url_prefix=url_prefix)

    @swagger_blueprint.get('/')
    async def swagger_blueprint_index_handler(request):
        # swagger_url_prefix = request.url[:-1] if request.url.endswith('/') else request.url
        return response.html(utils.render_html(url_prefix=url_prefix, title=title))

    @swagger_blueprint.get('/swagger.json')
    async def swagger_blueprint_config_handler(request):
        return response.text(utils.load_swagger_config(config_path=config_path, host=request.host))

    swagger_blueprint.static('/', utils.get_static_dir())
    app.blueprint(swagger_blueprint)
