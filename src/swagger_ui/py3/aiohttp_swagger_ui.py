from .. import utils


def api_doc(app, config_path, url_prefix='/api/doc', title='API doc'):
    from aiohttp import web

    async def swagger_index_handler(request):
        return web.Response(text=utils.render_html(url_prefix=url_prefix, title=title),
                            content_type='text/html')

    async def swagger_config_handler(request):
        return web.Response(
            text=utils.load_swagger_config(config_path=config_path, host=request.host),
            content_type='application/json'
        )

    app.router.add_get('{}'.format(url_prefix), swagger_index_handler)
    app.router.add_get('{}/swagger.json'.format(url_prefix), swagger_config_handler)
    app.router.add_static('{}/'.format(url_prefix), path='{}/'.format(utils.get_static_dir()))
